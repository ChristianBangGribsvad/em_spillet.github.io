"""
WC 2026 Pipeline Integration Test
==================================
Tests:
  1. check_group_winners  - unit-tests for find_group_winners() tiebreaker logic
  2. check_scoring        - match-prediction + group-winner scoring with known results
  3. Full pipeline run    - 3 simulated match days (Groups A & B), file assertions

Output is written to  test/test-results/  and kept after the run so you can
inspect the generated SVGs, markdown pages and pickled DataFrames.

Usage
-----
    cd <repo root>
    python test/test_pipeline.py
"""

import sys
import os
import shutil
import pandas as pd

# ── Path setup (must happen before chdir) ────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.dirname(SCRIPT_DIR)
TEST_DIR   = os.path.join(SCRIPT_DIR, "test-results")

sys.path.insert(0, os.path.join(ROOT, 'scripts'))

from eval_funcs   import eval_match_predictions, eval_groups, find_group_winners
from plot_funcs   import plot_user, plot_group_progress, plot_best_round, plot_standings
from create_pages import create_pages
from insert_pages import update_pages

# ── Simulated match IDs (must match process_match() output exactly) ──────────
GROUP_A_IDS = [
    "Group A Predictions [Mexico - South Africa]",
    "Group A Predictions [South Korea - Czechia]",
    "Group A Predictions [Czechia - South Africa]",
    "Group A Predictions [Mexico - South Korea]",
    "Group A Predictions [Czechia - Mexico]",
    "Group A Predictions [South Africa - South Korea]",
]
GROUP_B_IDS = [
    "Group B Predictions [Canada - Bosnia-Herzegovina]",
    "Group B Predictions [Qatar - Switzerland]",
    "Group B Predictions [Switzerland - Bosnia-Herzegovina]",
    "Group B Predictions [Canada - Qatar]",
    "Group B Predictions [Switzerland - Canada]",
    "Group B Predictions [Bosnia-Herzegovina - Qatar]",
]

def build_results(scored: dict) -> list:
    """
    Return a results list in the same format as get_results().
    Unscored matches get 'None - None' to signal 'not yet played'.
    """
    return [(mid, scored.get(mid, "None - None"))
            for mid in GROUP_A_IDS + GROUP_B_IDS]


# ── Three days of incremental results ────────────────────────────────────────
# Final standings:
#   Group A: 1st Mexico (7 pts, GD +4), 2nd South Korea (5 pts)
#   Group B: 1st Canada (7 pts, GD +4), 2nd Switzerland (7 pts, GD +3)

DAY1_SCORED = {
    "Group A Predictions [Mexico - South Africa]":       "2 - 1",
    "Group A Predictions [South Korea - Czechia]":       "1 - 1",
    "Group B Predictions [Canada - Bosnia-Herzegovina]": "3 - 0",
    "Group B Predictions [Qatar - Switzerland]":         "0 - 2",
}

DAY2_SCORED = {
    **DAY1_SCORED,
    "Group A Predictions [Czechia - South Africa]":           "2 - 0",
    "Group A Predictions [Mexico - South Korea]":             "1 - 1",
    "Group B Predictions [Switzerland - Bosnia-Herzegovina]": "2 - 1",
    "Group B Predictions [Canada - Qatar]":                   "1 - 0",
}

DAY3_SCORED = {
    **DAY2_SCORED,
    "Group A Predictions [Czechia - Mexico]":           "0 - 1",
    "Group A Predictions [South Africa - South Korea]": "1 - 2",
    "Group B Predictions [Switzerland - Canada]":       "1 - 1",
    "Group B Predictions [Bosnia-Herzegovina - Qatar]": "1 - 2",
}

SIMULATED_DAYS = [
    ("2026-06-12", DAY1_SCORED,  4),
    ("2026-06-16", DAY2_SCORED,  8),
    ("2026-06-20", DAY3_SCORED, 12),
]


# ── Directory setup / teardown ───────────────────────────────────────────────
def setup():
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    for sub in ["data/user_dfs", "data/group_dfs",
                "pages/user_plots", "pages/group_plots"]:
        os.makedirs(os.path.join(TEST_DIR, sub), exist_ok=True)

    shutil.copy(os.path.join(ROOT, "index_template.md"),
                os.path.join(TEST_DIR, "index_template.md"))

    os.chdir(TEST_DIR)
    print(f"[setup] Output dir: {TEST_DIR}")


def teardown():
    os.chdir(ROOT)
    print(f"\n[teardown] Results kept at: {TEST_DIR}")
    print("  data/user_dfs/     - per-participant pickles (3 rows: predictions, results, points)")
    print("  data/group_dfs/    - per-team-group pickles (date-indexed cumulative scores)")
    print("  pages/user_plots/  - per-participant SVGs")
    print("  pages/group_plots/ - group line/bar/standings SVGs")
    print("  pages/*.md         - participant markdown pages")
    print("  index.md           - homepage")


# ── 1. Group-winner unit tests ────────────────────────────────────────────────
def check_group_winners() -> bool:
    """
    Unit-tests for find_group_winners() covering the main tiebreaker paths.

    Case 1 (Group M) - Clear winner, clear 2nd: no ties at all.
      Alpha 9 pts > Beta 6 > Gamma 3 > Delta 0
      Expected: 1st=Alpha, 2nd=Beta

    Case 2 (Group N) - 2-way tie for 1st, resolved by head-to-head result.
      Alpha 6 pts = Beta 6 pts; Alpha beat Beta 1-0
      Expected: 1st=Alpha, 2nd=Beta

    Case 3 (Group O) - 2-way tie for 1st, h2h was a draw, resolved by goal difference.
      Alpha 7 pts = Beta 7 pts; drew 2-2; Alpha GD +5 < Beta GD +7
      Expected: 1st=Beta, 2nd=Alpha

    Case 4 (Group P) - 3-way tie, resolved by goal difference.
      Alpha 6 = Beta 6 = Gamma 6 (circular wins); Delta 0
      GD: Gamma +3 > Alpha +2 > Beta +1
      Expected: 1st=Gamma, 2nd=Alpha
    """
    cases = [
        # (description, results_list, group_key, exp_1st, exp_2nd)
        (
            "Case 1: clear winner",
            [
                ("Group M Predictions [Alpha - Beta]",  "3 - 0"),
                ("Group M Predictions [Gamma - Delta]", "2 - 0"),
                ("Group M Predictions [Alpha - Gamma]", "2 - 0"),
                ("Group M Predictions [Beta - Delta]",  "2 - 0"),
                ("Group M Predictions [Alpha - Delta]", "1 - 0"),
                ("Group M Predictions [Beta - Gamma]",  "2 - 1"),
            ],
            "Group M", "Alpha", "Beta",
        ),
        (
            "Case 2: 2-way tie, head-to-head decides (Alpha beat Beta 1-0)",
            [
                ("Group N Predictions [Alpha - Beta]",  "1 - 0"),
                ("Group N Predictions [Gamma - Delta]", "1 - 1"),
                ("Group N Predictions [Alpha - Gamma]", "0 - 1"),
                ("Group N Predictions [Beta - Delta]",  "2 - 1"),
                ("Group N Predictions [Alpha - Delta]", "2 - 0"),
                ("Group N Predictions [Beta - Gamma]",  "2 - 1"),
            ],
            # Points: Alpha=6, Beta=6, Gamma=4, Delta=1
            "Group N", "Alpha", "Beta",
        ),
        (
            "Case 3: 2-way tie, drew h2h 2-2, goal difference decides (Beta GD+7 > Alpha GD+5)",
            [
                ("Group O Predictions [Alpha - Beta]",  "2 - 2"),
                ("Group O Predictions [Gamma - Delta]", "1 - 1"),
                ("Group O Predictions [Alpha - Gamma]", "3 - 0"),
                ("Group O Predictions [Beta - Delta]",  "4 - 0"),
                ("Group O Predictions [Alpha - Delta]", "2 - 0"),
                ("Group O Predictions [Beta - Gamma]",  "3 - 0"),
            ],
            # Points: Alpha=7, Beta=7, Gamma=1, Delta=1
            # GD: Alpha=(2+3+2)-(2+0+0)=+5, Beta=(2+4+3)-(2+0+0)=+7
            "Group O", "Beta", "Alpha",
        ),
        (
            "Case 4: 3-way tie (circular wins), goal difference decides (Gamma GD+3 > Alpha GD+2 > Beta GD+1)",
            [
                ("Group P Predictions [Alpha - Beta]",  "2 - 1"),
                ("Group P Predictions [Gamma - Delta]", "3 - 0"),
                ("Group P Predictions [Beta - Gamma]",  "2 - 1"),
                ("Group P Predictions [Alpha - Delta]", "2 - 0"),
                ("Group P Predictions [Gamma - Alpha]", "2 - 1"),
                ("Group P Predictions [Beta - Delta]",  "1 - 0"),
            ],
            # Points: Alpha=6, Beta=6, Gamma=6, Delta=0
            # GD: Alpha=(2+2+1)-(1+0+2)=+2, Beta=(1+2+1)-(2+1+0)=+1, Gamma=(3+1+2)-(0+2+1)=+3
            "Group P", "Gamma", "Alpha",
        ),
    ]

    all_ok = True
    print(f"\n{'='*60}")
    print("GROUP WINNER UNIT TESTS")
    print(f"{'='*60}")
    for desc, results, group_key, exp_1st, exp_2nd in cases:
        res = find_group_winners(results)
        got_1st = res.get(group_key, {}).get("1st", "??")
        got_2nd = res.get(group_key, {}).get("2nd", "??")
        ok = (got_1st == exp_1st) and (got_2nd == exp_2nd)
        all_ok &= ok
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}]  {desc}")
        if not ok:
            print(f"         Expected 1st={exp_1st}, 2nd={exp_2nd}")
            print(f"         Got      1st={got_1st}, 2nd={got_2nd}")
    print("=" * 60)
    return all_ok


# ── 2. Scoring checks (match + group winners) ─────────────────────────────────
def check_scoring(predictions_df: pd.DataFrame) -> bool:
    """
    Sanity checks against the Day-3 (fully resolved) results.

    Match scoring for Mexico vs South Africa (actual 2-1):
      Alice pred 2-1  -> exact score   -> 15 pts
      Bob   pred 1-0  -> correct win only -> 5 pts
      Carol pred 2-0  -> correct win + correct home score -> 10 pts

    Group A result: Mexico 1st, South Korea 2nd
      Alice: Mexico 1st + SK 2nd (both correct)  ->  7.5 + 7.5 = 15 pts
      Bob:   Czechia 1st (wrong) + SK 2nd (right) ->  0   + 5   =  5 pts
      Carol: Mexico 1st (right) + Czechia 2nd (wrong) -> 5 + 0  =  5 pts

    Group B result: Canada 1st, Switzerland 2nd
      Alice: Canada 1st + Switzerland 2nd (both correct) -> 7.5 + 7.5 = 15 pts
      Bob:   Switzerland 1st + Canada 2nd (swapped)      ->  5  +  5  = 10 pts
      Carol: Canada 1st (right) + Qatar 2nd (wrong)      ->  5  +  0  =  5 pts
    """
    results_day3 = build_results(DAY3_SCORED)
    all_ok = True

    # (name, exp_match_pts, exp_grp_a_pts, exp_grp_b_pts)
    # Carol predicted 2-0 vs actual 2-1: correct outcome AND correct home score = 10 pts
    expectations = [
        ("Alice Sm", 15, 15.0, 15.0),
        ("Bob Jo",    5,  5.0, 10.0),
        ("Carol Da", 10,  5.0,  5.0),
    ]

    rows = []
    for name, exp_match, exp_a, exp_b in expectations:
        df = (predictions_df[predictions_df["d_name"] == name]
              .reset_index(drop=True))
        df = eval_match_predictions(df, results_day3)
        df = eval_groups(df, results_day3)

        col_match = "Group A Predictions [Mexico - South Africa]"
        match_pts = df.at[2, col_match]
        a_pts = df.at[2, "Group A 1st place"] + df.at[2, "Group A 2nd place"]
        b_pts = df.at[2, "Group B 1st place"] + df.at[2, "Group B 2nd place"]

        ok = (match_pts == exp_match) and (a_pts == exp_a) and (b_pts == exp_b)
        all_ok &= ok
        rows.append((name, match_pts, exp_match, a_pts, exp_a, b_pts, exp_b, ok))

    print(f"\n{'='*60}")
    print("SCORING CHECKS  (Day-3 results)")
    print(f"{'='*60}")
    print(f"  {'Name':<12}  {'MexSA':>8}  {'GrpA':>10}  {'GrpB':>10}  Status")
    print(f"  {'-'*12}  {'-'*8}  {'-'*10}  {'-'*10}  ------")
    for name, mp, emp, ap, eap, bp, ebp, ok in rows:
        status = "PASS" if ok else "FAIL"
        m_str = f"{mp:>3}{'+' if mp==emp else f'!={emp}'}"
        a_str = f"{ap:>5}{'+' if ap==eap else f'!={eap}'}"
        b_str = f"{bp:>5}{'+' if bp==ebp else f'!={ebp}'}"
        print(f"  {name:<12}  {m_str:>8}  {a_str:>10}  {b_str:>10}  [{status}]")
    print("=" * 60)
    return all_ok


# ── 3. Full pipeline run ──────────────────────────────────────────────────────
def run_day(predictions_df: pd.DataFrame, date_str: str, scored: dict):
    results = build_results(scored)

    max_val = 0
    todays_schmeichel = {"Nobody": {"value": 0, "group": "Nobody", "fname": ""}}

    for user in predictions_df["d_name"]:
        user_df = (predictions_df[predictions_df["d_name"] == user]
                   .reset_index(drop=True))

        user_df = eval_match_predictions(user_df, results)
        user_df = eval_groups(user_df, results)

        user_df.to_pickle(f"data/user_dfs/{user_df.at[0, 'f_name']}")

        for group in user_df.at[0, "Which team(s) do you belong to?"].split(";"):
            gfile = f"data/group_dfs/{group}"
            df_grp = pd.read_pickle(gfile) if os.path.isfile(gfile) else pd.DataFrame()

            plot_user(user_df)

            total_score = user_df.loc[2].sum()
            df_grp.loc[date_str, user] = total_score
            df_grp.to_pickle(gfile)

            if df_grp.shape[0] > 1:
                user_val = df_grp.loc[date_str, user] - df_grp.iloc[-2][user]
            else:
                user_val = total_score

            if user_val > max_val:
                todays_schmeichel = {
                    user: {
                        "value": user_val,
                        "group": user_df.at[0, "Which team(s) do you belong to?"]
                                        .replace(";", " and "),
                        "fname": user_df.at[0, "f_name"],
                    }
                }
                max_val = user_val
            elif user_val == max_val:
                todays_schmeichel[user] = {
                    "value": user_val,
                    "group": user_df.at[0, "Which team(s) do you belong to?"]
                                    .replace(";", " and "),
                    "fname": user_df.at[0, "f_name"],
                }

    for group in os.listdir("data/group_dfs"):
        df_grp = pd.read_pickle(f"data/group_dfs/{group}")
        plot_group_progress(df_grp, group)
        plot_best_round(df_grp, group)
        plot_standings(df_grp, group)

    create_pages(predictions_df)
    update_pages(predictions_df, todays_schmeichel)

    print(f"  Schmeichel: {list(todays_schmeichel.keys())} "
          f"({list(todays_schmeichel.values())[0]['value']} pts)")


# ── File-existence assertions ─────────────────────────────────────────────────
def assert_files(predictions_df: pd.DataFrame) -> bool:
    expected = []

    for _, row in predictions_df.iterrows():
        fname = row["f_name"]
        expected += [
            f"pages/user_plots/{fname}.svg",
            f"pages/{fname}.md",
        ]

    groups = (predictions_df["Which team(s) do you belong to?"]
              .str.split(";").explode().unique())
    for group in groups:
        g = group.replace(" ", "_")
        expected += [
            f"pages/group_plots/lines_{g}.svg",
            f"pages/group_plots/bars_{g}.svg",
            f"pages/group_plots/standing_{g}.svg",
        ]

    expected.append("index.md")

    passes, failures = [], []
    for path in expected:
        if os.path.isfile(path):
            passes.append(path)
        else:
            failures.append(path)

    print(f"\n{'='*60}")
    print(f"FILE ASSERTIONS  - {len(passes)} passed / {len(failures)} failed")
    for p in passes:
        print(f"  PASS  {p}")
    for f in failures:
        print(f"  FAIL  {f}  <- missing")
    print("=" * 60)

    return len(failures) == 0


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("\n" + "=" * 60)
    print("WC 2026 Pipeline Integration Test")
    print("=" * 60)

    # Group-winner unit tests run before filesystem setup (no side effects)
    all_ok = check_group_winners()

    setup()
    try:
        predictions_df = pd.read_csv(os.path.join(SCRIPT_DIR, "test_data.csv"))
        predictions_df["f_name"] = [
            f"{r['First name']}_{str(r['Last name'])[:2]}".replace(" ", "_").replace('"', "_")
            for _, r in predictions_df.iterrows()
        ]
        predictions_df["d_name"] = [
            f"{r['First name']} {str(r['Last name'])[:2]}"
            for _, r in predictions_df.iterrows()
        ]

        all_ok &= check_scoring(predictions_df)

        for date_str, scored, n_played in SIMULATED_DAYS:
            print(f"\n--- Day {date_str}  ({n_played}/12 Group A+B matches resolved) ---")
            run_day(predictions_df.copy(), date_str, scored)

        all_ok &= assert_files(predictions_df)

        if all_ok:
            print("\n[PASS]  All checks passed.\n")
        else:
            print("\n[FAIL]  One or more checks failed - see output above.\n")
            raise SystemExit(1)

    finally:
        teardown()


if __name__ == "__main__":
    main()
