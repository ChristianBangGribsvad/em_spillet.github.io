"""
WC 2026 Pipeline Integration Test
==================================
Tests the full pipeline end-to-end with dummy WC 2026 data:
  - Match-prediction scoring  (eval_match_predictions)
  - SVG visualisation          (plot_user, plot_group_progress,
                                plot_best_round, plot_standings)
  - Markdown page generation   (create_pages, update_pages)

Three simulated match days are processed in sequence so that
incremental score accumulation is exercised.

All output is written to  test/test-results/  which is deleted
automatically once the test finishes (pass or fail).

Usage
-----
    cd <repo root>
    python test/test_pipeline.py

Known issues printed at startup
--------------------------------
  1. eval_groups() is hardcoded for exactly 6 groups (EURO 2024 logic)
     and contains a hard-wired Denmark override.  Both must be fixed
     before the WC 2026 launch.  The function is intentionally SKIPPED
     in this test to avoid a guaranteed IndexError.

  2. main.py scores special predictions (final winner/loser, top scorer,
     home-country progression) by hardcoded column indices 52-55.  These
     will point to wrong columns with the new WC CSV layout and must be
     replaced with column-name lookups.
"""

import sys
import os
import shutil
import pandas as pd

# ── Path setup (must happen before chdir) ────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.dirname(SCRIPT_DIR)
TEST_DIR   = os.path.join(SCRIPT_DIR, "test-results")

sys.path.insert(0, ROOT)

from eval_funcs   import eval_match_predictions, dk_finish
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
# Actual final standings (for reference):
#   Group A: 1st Mexico (7 pts), 2nd South Korea (5 pts)
#   Group B: 1st Canada (7 pts), 2nd Switzerland (7 pts, lower GD)

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
    ("2026-06-12", DAY1_SCORED, 4),
    ("2026-06-16", DAY2_SCORED, 8),
    ("2026-06-20", DAY3_SCORED, 12),
]


# ── Directory setup / teardown ───────────────────────────────────────────────
def setup():
    for sub in ["data/user_dfs", "data/group_dfs",
                "pages/user_plots", "pages/group_plots"]:
        os.makedirs(os.path.join(TEST_DIR, sub), exist_ok=True)

    shutil.copy(os.path.join(ROOT, "index_template.md"),
                os.path.join(TEST_DIR, "index_template.md"))

    os.chdir(TEST_DIR)
    print(f"[setup] Temp dir: {TEST_DIR}")


def teardown():
    os.chdir(ROOT)
    shutil.rmtree(TEST_DIR)
    print(f"[teardown] Removed {TEST_DIR}")


# ── One-day pipeline run ──────────────────────────────────────────────────────
def run_day(predictions_df: pd.DataFrame, date_str: str, scored: dict):
    results = build_results(scored)

    max_val = 0
    todays_schmeichel = {"Nobody": {"value": 0, "group": "Nobody", "fname": ""}}

    for user in predictions_df["d_name"]:
        user_df = (predictions_df[predictions_df["d_name"] == user]
                   .reset_index(drop=True))

        # Score group-stage match predictions
        user_df = eval_match_predictions(user_df, results)

        # eval_groups is intentionally skipped — see module docstring for why.

        # dk_finish / dk_goals_scored are no-ops: Denmark is not in Groups A/B
        user_df, dk_end = dk_finish(results, user_df)

        # Persist latest user evaluation
        user_df.to_pickle(f"data/user_dfs/{user_df.at[0, 'f_name']}")

        # Update each team-group the participant belongs to
        for group in user_df.at[0, "Which team(s) do you belong to?"].split(";"):
            gfile = f"data/group_dfs/{group}"
            df_grp = pd.read_pickle(gfile) if os.path.isfile(gfile) else pd.DataFrame()

            plot_user(user_df)

            total_score = user_df.loc[2].sum()
            df_grp.loc[date_str, user] = total_score
            df_grp.to_pickle(gfile)

            # Today's Schmeichel: points gained since previous day
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

    # Group-level plots
    for group in os.listdir("data/group_dfs"):
        df_grp = pd.read_pickle(f"data/group_dfs/{group}")
        plot_group_progress(df_grp, group)
        plot_best_round(df_grp, group)   # skipped silently when only 1 row
        plot_standings(df_grp, group)

    create_pages(predictions_df)
    update_pages(predictions_df, todays_schmeichel)

    print(f"  Schmeichel: {list(todays_schmeichel.keys())} "
          f"({list(todays_schmeichel.values())[0]['value']} pts)")


# ── File-existence assertions ─────────────────────────────────────────────────
def assert_files(predictions_df: pd.DataFrame) -> bool:
    expected = []

    # Per-participant: SVG table + markdown page
    for _, row in predictions_df.iterrows():
        fname = row["f_name"]
        expected += [
            f"pages/user_plots/{fname}.svg",
            f"pages/{fname}.md",
        ]

    # Per-team-group: line chart, bar chart, standings table
    groups = (predictions_df["Which team(s) do you belong to?"]
              .str.split(";").explode().unique())
    for group in groups:
        g = group.replace(" ", "_")
        expected += [
            f"pages/group_plots/lines_{g}.svg",
            f"pages/group_plots/bars_{g}.svg",    # created from day 2 onward
            f"pages/group_plots/standing_{g}.svg",
        ]

    # Homepage
    expected.append("index.md")

    passes, failures = [], []
    for path in expected:
        if os.path.isfile(path):
            passes.append(path)
        else:
            failures.append(path)

    print(f"\n{'='*60}")
    print(f"FILE ASSERTIONS  —  {len(passes)} passed / {len(failures)} failed")
    for p in passes:
        print(f"  PASS  {p}")
    for f in failures:
        print(f"  FAIL  {f}  ← missing")
    print("=" * 60)

    return len(failures) == 0


# ── Scoring smoke-check ───────────────────────────────────────────────────────
def check_scoring(predictions_df: pd.DataFrame):
    """
    Quick sanity check: Alice predicted Mexico 2-1 South Africa exactly right
    on Day 1 → should earn 15 points for that match.
    """
    results_day1 = build_results(DAY1_SCORED)
    alice_df = (predictions_df[predictions_df["d_name"] == "Alice Sm"]
                .reset_index(drop=True))
    alice_df = eval_match_predictions(alice_df, results_day1)

    col = "Group A Predictions [Mexico - South Africa]"
    pts = alice_df.at[2, col]
    ok  = (pts == 15)
    status = "PASS" if ok else "FAIL"
    print(f"\nSCORING CHECK  —  Alice exact score (Mexico 2-1 SA) → {pts} pts  [{status}]")
    return ok


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("\n" + "=" * 60)
    print("WC 2026 Pipeline Integration Test")
    print("=" * 60)

    print("\n⚠  KNOWN ISSUES TO FIX BEFORE WC 2026 LAUNCH:")
    print("   1. eval_groups() hardcoded 'for i in range(6)' → must be")
    print("      range(12) (or dynamic) for the 12 WC groups.")
    print("   2. eval_groups() contains 'if i == 2: res2nd = Denmark'")
    print("      — EURO 2024 hack that must be removed.")
    print("   3. main.py scores special predictions via hardcoded column")
    print("      indices 52-55.  New WC CSV has different column count;")
    print("      replace iloc references with column-name lookups.\n")

    setup()
    all_ok = True
    try:
        # Load dummy CSV and derive name columns (same logic as main.py)
        predictions_df = pd.read_csv(os.path.join(SCRIPT_DIR, "test_data.csv"))
        predictions_df["f_name"] = [
            f"{r['First name']}_{str(r['Last name'])[:2]}".replace(" ", "_").replace('"', "_")
            for _, r in predictions_df.iterrows()
        ]
        predictions_df["d_name"] = [
            f"{r['First name']} {str(r['Last name'])[:2]}"
            for _, r in predictions_df.iterrows()
        ]

        # Scoring smoke-check (does not require filesystem setup)
        all_ok &= check_scoring(predictions_df)

        # Simulate 3 match days
        for date_str, scored, n_played in SIMULATED_DAYS:
            print(f"\n--- Day {date_str}  ({n_played}/12 group matches resolved) ---")
            run_day(predictions_df.copy(), date_str, scored)

        # Verify all expected output files were created
        all_ok &= assert_files(predictions_df)

        if all_ok:
            print("\n✅  All checks passed.\n")
        else:
            print("\n❌  One or more checks failed — see output above.\n")
            raise SystemExit(1)

    finally:
        teardown()


if __name__ == "__main__":
    main()
