"""
WC 2026 Pipeline Integration Test
==================================
Tests:
  1. check_group_winners  - unit-tests for find_group_winners() tiebreaker logic
  2. check_scoring        - match-prediction + group-winner scoring with known results
  3. Full pipeline run    - 3 simulated match days (all 12 groups), file assertions

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
import numpy as np
import pandas as pd

# ── Path setup (must happen before chdir) ────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT       = os.path.dirname(SCRIPT_DIR)
TEST_DIR   = os.path.join(SCRIPT_DIR, "test-results")

sys.path.insert(0, os.path.join(ROOT, 'scripts'))

from eval_funcs   import eval_match_predictions, eval_groups, find_group_winners
from plot_funcs   import plot_user, plot_group_progress, plot_best_round, plot_standings
from create_pages import create_pages
from insert_pages import update_pages, create_group_pages

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
GROUP_C_IDS = [
    "Group C Predictions [Brazil - Morocco]",
    "Group C Predictions [Haiti - Scotland]",
    "Group C Predictions [Scotland - Morocco]",
    "Group C Predictions [Brazil - Haiti]",
    "Group C Predictions [Morocco - Haiti]",
    "Group C Predictions [Scotland - Brazil]",
]
GROUP_D_IDS = [
    "Group D Predictions [United States - Paraguay]",
    "Group D Predictions [Australia - Turkey]",
    "Group D Predictions [United States - Australia]",
    "Group D Predictions [Turkey - Paraguay]",
    "Group D Predictions [Turkey - United States]",
    "Group D Predictions [Paraguay - Australia]",
]
GROUP_E_IDS = [
    "Group E Predictions [Germany - Curaçao]",
    "Group E Predictions [Ivory Coast - Ecuador]",
    "Group E Predictions [Germany - Ivory Coast]",
    "Group E Predictions [Ecuador - Curaçao]",
    "Group E Predictions [Ecuador - Germany]",
    "Group E Predictions [Curaçao - Ivory Coast]",
]
GROUP_F_IDS = [
    "Group F Predictions [Netherlands - Japan]",
    "Group F Predictions [Sweden - Tunisia]",
    "Group F Predictions [Netherlands - Sweden]",
    "Group F Predictions [Tunisia - Japan]",
    "Group F Predictions [Tunisia - Netherlands]",
    "Group F Predictions [Japan - Sweden]",
]
GROUP_G_IDS = [
    "Group G Predictions [Belgium - Egypt]",
    "Group G Predictions [Iran - New Zealand]",
    "Group G Predictions [Belgium - Iran]",
    "Group G Predictions [New Zealand - Egypt]",
    "Group G Predictions [New Zealand - Belgium]",
    "Group G Predictions [Egypt - Iran]",
]
GROUP_H_IDS = [
    "Group H Predictions [Spain - Cape Verde Islands]",
    "Group H Predictions [Saudi Arabia - Uruguay]",
    "Group H Predictions [Spain - Saudi Arabia]",
    "Group H Predictions [Uruguay - Cape Verde Islands]",
    "Group H Predictions [Uruguay - Spain]",
    "Group H Predictions [Cape Verde Islands - Saudi Arabia]",
]
GROUP_I_IDS = [
    "Group I Predictions [France - Senegal]",
    "Group I Predictions [Iraq - Norway]",
    "Group I Predictions [France - Iraq]",
    "Group I Predictions [Norway - Senegal]",
    "Group I Predictions [Norway - France]",
    "Group I Predictions [Senegal - Iraq]",
]
GROUP_J_IDS = [
    "Group J Predictions [Argentina - Algeria]",
    "Group J Predictions [Austria - Jordan]",
    "Group J Predictions [Argentina - Austria]",
    "Group J Predictions [Jordan - Algeria]",
    "Group J Predictions [Jordan - Argentina]",
    "Group J Predictions [Algeria - Austria]",
]
GROUP_K_IDS = [
    "Group K Predictions [Portugal - Congo DR]",
    "Group K Predictions [Uzbekistan - Colombia]",
    "Group K Predictions [Portugal - Uzbekistan]",
    "Group K Predictions [Colombia - Congo DR]",
    "Group K Predictions [Colombia - Portugal]",
    "Group K Predictions [Congo DR - Uzbekistan]",
]
GROUP_L_IDS = [
    "Group L Predictions [England - Croatia]",
    "Group L Predictions [Ghana - Panama]",
    "Group L Predictions [England - Ghana]",
    "Group L Predictions [Panama - Croatia]",
    "Group L Predictions [Panama - England]",
    "Group L Predictions [Croatia - Ghana]",
]

ALL_GROUP_IDS = (
    GROUP_A_IDS + GROUP_B_IDS + GROUP_C_IDS + GROUP_D_IDS +
    GROUP_E_IDS + GROUP_F_IDS + GROUP_G_IDS + GROUP_H_IDS +
    GROUP_I_IDS + GROUP_J_IDS + GROUP_K_IDS + GROUP_L_IDS
)

def build_results(scored: dict) -> list:
    """
    Return a results list in the same format as get_results().
    Unscored matches get 'None - None' to signal 'not yet played'.
    """
    return [(mid, scored.get(mid, "None - None")) for mid in ALL_GROUP_IDS]


# ── Three days of incremental results ────────────────────────────────────────
# Final group standings (actual 1st / 2nd):
#   A: Mexico / South Korea    B: Canada / Switzerland
#   C: Brazil / Scotland       D: United States / Turkey
#   E: Germany / Ivory Coast   F: Netherlands / Sweden
#   G: Belgium / Iran          H: Spain / Uruguay
#   I: France / Norway         J: Argentina / Austria
#   K: Portugal / Colombia     L: England / Croatia

# ── Matchday 1 (first 2 matches of each group) ───────────────────────────────
DAY1_SCORED = {
    # Group A
    "Group A Predictions [Mexico - South Africa]":        "2 - 1",
    "Group A Predictions [South Korea - Czechia]":        "1 - 1",
    # Group B
    "Group B Predictions [Canada - Bosnia-Herzegovina]":  "3 - 0",
    "Group B Predictions [Qatar - Switzerland]":          "0 - 2",
    # Group C  →  Brazil 9 pts, Scotland 6 pts
    "Group C Predictions [Brazil - Morocco]":             "2 - 0",
    "Group C Predictions [Haiti - Scotland]":             "0 - 2",
    # Group D  →  United States 9 pts, Turkey 6 pts
    "Group D Predictions [United States - Paraguay]":     "2 - 0",
    "Group D Predictions [Australia - Turkey]":           "0 - 2",
    # Group E  →  Germany 9 pts, Ivory Coast 6 pts
    "Group E Predictions [Germany - Curaçao]":            "4 - 0",
    "Group E Predictions [Ivory Coast - Ecuador]":        "2 - 1",
    # Group F  →  Netherlands 9 pts, Sweden 6 pts
    "Group F Predictions [Netherlands - Japan]":          "2 - 0",
    "Group F Predictions [Sweden - Tunisia]":             "2 - 0",
    # Group G  →  Belgium 9 pts, Iran 6 pts
    "Group G Predictions [Belgium - Egypt]":              "3 - 0",
    "Group G Predictions [Iran - New Zealand]":           "2 - 0",
    # Group H  →  Spain 9 pts, Uruguay 6 pts
    "Group H Predictions [Spain - Cape Verde Islands]":   "3 - 0",
    "Group H Predictions [Saudi Arabia - Uruguay]":       "0 - 2",
    # Group I  →  France 9 pts, Norway 6 pts
    "Group I Predictions [France - Senegal]":             "2 - 0",
    "Group I Predictions [Iraq - Norway]":                "0 - 2",
    # Group J  →  Argentina 9 pts, Austria 6 pts
    "Group J Predictions [Argentina - Algeria]":          "3 - 0",
    "Group J Predictions [Austria - Jordan]":             "2 - 0",
    # Group K  →  Portugal 9 pts, Colombia 6 pts
    "Group K Predictions [Portugal - Congo DR]":          "3 - 0",
    "Group K Predictions [Uzbekistan - Colombia]":        "0 - 2",
    # Group L  →  England 9 pts, Croatia 6 pts
    "Group L Predictions [England - Croatia]":            "2 - 1",
    "Group L Predictions [Ghana - Panama]":               "0 - 1",
}

# ── Matchday 2 (adds matches 3–4 of each group) ──────────────────────────────
DAY2_SCORED = {
    **DAY1_SCORED,
    # Group A
    "Group A Predictions [Czechia - South Africa]":            "2 - 0",
    "Group A Predictions [Mexico - South Korea]":              "1 - 1",
    # Group B
    "Group B Predictions [Switzerland - Bosnia-Herzegovina]":  "2 - 1",
    "Group B Predictions [Canada - Qatar]":                    "1 - 0",
    # Group C
    "Group C Predictions [Scotland - Morocco]":                "1 - 0",
    "Group C Predictions [Brazil - Haiti]":                    "3 - 0",
    # Group D
    "Group D Predictions [United States - Australia]":         "2 - 1",
    "Group D Predictions [Turkey - Paraguay]":                 "2 - 0",
    # Group E
    "Group E Predictions [Germany - Ivory Coast]":             "2 - 1",
    "Group E Predictions [Ecuador - Curaçao]":                 "1 - 0",
    # Group F
    "Group F Predictions [Netherlands - Sweden]":              "2 - 1",
    "Group F Predictions [Tunisia - Japan]":                   "0 - 1",
    # Group G
    "Group G Predictions [Belgium - Iran]":                    "2 - 1",
    "Group G Predictions [New Zealand - Egypt]":               "0 - 1",
    # Group H
    "Group H Predictions [Spain - Saudi Arabia]":              "2 - 0",
    "Group H Predictions [Uruguay - Cape Verde Islands]":      "3 - 0",
    # Group I
    "Group I Predictions [France - Iraq]":                     "3 - 0",
    "Group I Predictions [Norway - Senegal]":                  "2 - 0",
    # Group J
    "Group J Predictions [Argentina - Austria]":               "2 - 1",
    "Group J Predictions [Jordan - Algeria]":                  "0 - 1",
    # Group K
    "Group K Predictions [Portugal - Uzbekistan]":             "2 - 0",
    "Group K Predictions [Colombia - Congo DR]":               "2 - 0",
    # Group L
    "Group L Predictions [England - Ghana]":                   "2 - 0",
    "Group L Predictions [Panama - Croatia]":                  "0 - 2",
}

# ── Matchday 3 (final round — all groups complete) ───────────────────────────
DAY3_SCORED = {
    **DAY2_SCORED,
    # Group A
    "Group A Predictions [Czechia - Mexico]":            "0 - 1",
    "Group A Predictions [South Africa - South Korea]":  "1 - 2",
    # Group B
    "Group B Predictions [Switzerland - Canada]":        "1 - 1",
    "Group B Predictions [Bosnia-Herzegovina - Qatar]":  "1 - 2",
    # Group C
    "Group C Predictions [Morocco - Haiti]":             "1 - 1",
    "Group C Predictions [Scotland - Brazil]":           "0 - 2",
    # Group D
    "Group D Predictions [Turkey - United States]":      "0 - 2",
    "Group D Predictions [Paraguay - Australia]":        "1 - 0",
    # Group E
    "Group E Predictions [Ecuador - Germany]":           "0 - 3",
    "Group E Predictions [Curaçao - Ivory Coast]":       "0 - 2",
    # Group F
    "Group F Predictions [Tunisia - Netherlands]":       "0 - 3",
    "Group F Predictions [Japan - Sweden]":              "0 - 2",
    # Group G
    "Group G Predictions [New Zealand - Belgium]":       "0 - 2",
    "Group G Predictions [Egypt - Iran]":                "0 - 2",
    # Group H
    "Group H Predictions [Uruguay - Spain]":             "0 - 2",
    "Group H Predictions [Cape Verde Islands - Saudi Arabia]": "1 - 0",
    # Group I
    "Group I Predictions [Norway - France]":             "0 - 2",
    "Group I Predictions [Senegal - Iraq]":              "1 - 1",
    # Group J
    "Group J Predictions [Jordan - Argentina]":          "0 - 3",
    "Group J Predictions [Algeria - Austria]":           "0 - 2",
    # Group K
    "Group K Predictions [Colombia - Portugal]":         "0 - 2",
    "Group K Predictions [Congo DR - Uzbekistan]":       "1 - 0",
    # Group L
    "Group L Predictions [Panama - England]":            "0 - 3",
    "Group L Predictions [Croatia - Ghana]":             "2 - 0",
}

# (date, scored_dict, n_played, expected_schmeichel_name, expected_schmeichel_delta)
SIMULATED_DAYS = [
    ("2026-06-12", DAY1_SCORED, 24, "Alice Sm",   299),
    ("2026-06-16", DAY2_SCORED, 48, "Bob Jo",     250.0),
    ("2026-06-20", DAY3_SCORED, 72, "Alice Sm",   397.0),
]

# ── Special prediction results (only known after the final is played) ─────────
# Alice: Spain winner ✓ (25), England loser ✗ (0), Harry Kane ✓ (20), 5 goals ✓ (10)
# Bob:   Brazil predicted as winner but is actual loser → partial swap (5)
# Carol: nothing correct → 0
ACTUAL_FINALE_WINNER  = "Spain"
ACTUAL_FINALE_LOSER   = "Brazil"
ACTUAL_TOP_SCORER     = ["Harry Kane"]
ACTUAL_SCORER_GOALS   = 5      # int — pandas reads numeric CSV columns as int64


# ── Directory setup / teardown ───────────────────────────────────────────────
def setup():
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    for sub in ["data/user_dfs", "data/group_dfs",
                "pages/user_plots", "pages/group_plots", "_data"]:
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


# ── 2b. Special prediction helper (mirrors main.py) ──────────────────────────
def run_special_predictions(user_df, topscorer, topscorer_goals, finale_winner, finale_loser):
    col_winner       = "FIFA World Cup 2026 final winner"
    col_loser        = "FIFA World Cup 2026 final loser"
    col_scorer       = "Who is going to be the top scorer throughout FIFA World Cup 2026? (20 points)"
    col_scorer_goals = "How many goals does the top scorer score? (10 points)"

    if topscorer:
        if user_df.at[0, col_scorer] in topscorer:
            user_df.at[2, col_scorer] = 20
        user_df.at[1, col_scorer] = ",".join(topscorer)

    if topscorer_goals is not None:
        if topscorer_goals == user_df.at[0, col_scorer_goals]:
            user_df.at[2, col_scorer_goals] = 10
        user_df.at[1, col_scorer_goals] = topscorer_goals

    if finale_winner is not None and finale_loser is not None:
        user_df.at[1, col_winner] = finale_winner
        user_df.at[1, col_loser]  = finale_loser

        if finale_winner == user_df.at[0, col_winner]:
            user_df.at[2, col_winner] = 25
        if finale_loser == user_df.at[0, col_loser]:
            user_df.at[2, col_loser] = 15

        if finale_loser == user_df.at[0, col_winner] and finale_winner == user_df.at[0, col_loser]:
            user_df.at[2, col_loser] = 10
        elif finale_loser == user_df.at[0, col_winner] or finale_winner == user_df.at[0, col_loser]:
            user_df.at[2, col_loser] = 5

    return user_df


# ── 2c. Special scoring checks ────────────────────────────────────────────────
def check_special_scoring(predictions_df: pd.DataFrame) -> bool:
    """
    Actual: winner=Spain, loser=Brazil, scorer=Harry Kane (5 goals)

    Alice  Spain winner ✓→25, England loser ✗→0, Kane ✓→20, 5 goals ✓→10  = 55
    Bob    Brazil as winner but is actual loser → partial swap→5, Mbappe ✗→0 =  5
    Carol  everything wrong → 0
    """
    results_day3 = build_results(DAY3_SCORED)

    col_winner       = "FIFA World Cup 2026 final winner"
    col_loser        = "FIFA World Cup 2026 final loser"
    col_scorer       = "Who is going to be the top scorer throughout FIFA World Cup 2026? (20 points)"
    col_scorer_goals = "How many goals does the top scorer score? (10 points)"

    # (name, exp_winner, exp_loser, exp_scorer, exp_scorer_goals)
    expectations = [
        ("Alice Sm",  25,  0, 20, 10),
        ("Bob Jo",     0,  5,  0,  0),
        ("Carol Da",   0,  0,  0,  0),
    ]

    all_ok = True
    rows = []
    for name, exp_w, exp_l, exp_s, exp_sg in expectations:
        df = (predictions_df[predictions_df["d_name"] == name]
              .reset_index(drop=True))
        df = eval_match_predictions(df, results_day3)
        df = eval_groups(df, results_day3)
        df = run_special_predictions(
            df,
            topscorer=ACTUAL_TOP_SCORER,
            topscorer_goals=ACTUAL_SCORER_GOALS,
            finale_winner=ACTUAL_FINALE_WINNER,
            finale_loser=ACTUAL_FINALE_LOSER,
        )

        got_w  = df.at[2, col_winner]
        got_l  = df.at[2, col_loser]
        got_s  = df.at[2, col_scorer]
        got_sg = df.at[2, col_scorer_goals]

        ok = (got_w == exp_w) and (got_l == exp_l) and (got_s == exp_s) and (got_sg == exp_sg)
        all_ok &= ok
        rows.append((name, got_w, exp_w, got_l, exp_l, got_s, exp_s, got_sg, exp_sg, ok))

    def fmt(got, exp):
        return f"{got}+" if got == exp else f"{got}!={exp}"

    print(f"\n{'='*60}")
    print("SPECIAL PREDICTION CHECKS  (Day-3 results)")
    print(f"{'='*60}")
    print(f"  {'Name':<12}  {'Winner':>8}  {'Loser':>8}  {'Scorer':>8}  {'Goals':>7}  Status")
    print(f"  {'-'*12}  {'-'*8}  {'-'*8}  {'-'*8}  {'-'*7}  ------")
    for name, gw, ew, gl, el, gs, es, gsg, esg, ok in rows:
        status = "PASS" if ok else "FAIL"
        print(f"  {name:<12}  {fmt(gw,ew):>8}  {fmt(gl,el):>8}  {fmt(gs,es):>8}  {fmt(gsg,esg):>7}  [{status}]")
    print("=" * 60)
    return all_ok


# ── 2d. All-group winner scoring check ───────────────────────────────────────
def check_all_group_winner_scoring(predictions_df: pd.DataFrame) -> bool:
    """
    Verify eval_groups() correctly scores all 12 group winner predictions.

    Expected total group-winner points per participant (Day-3 results):
      Alice  all 12 groups predicted exactly            12 × 15  = 180
      Bob    B swapped (+10), H-L exact (+75), rest partial (+30) = 115
      Carol  C,E,F,G,H,K,L exact (+105), A,B,D,I,J one-correct  = 130
    """
    results_day3 = build_results(DAY3_SCORED)

    expectations = [
        ("Alice Sm", 180.0),
        ("Bob Jo",   115.0),
        ("Carol Da", 130.0),
    ]

    all_ok = True
    rows = []
    for name, exp_total in expectations:
        df = (predictions_df[predictions_df["d_name"] == name]
              .reset_index(drop=True))
        df = eval_match_predictions(df, results_day3)
        df = eval_groups(df, results_day3)

        place_cols = [c for c in df.columns if "place" in c]
        total = sum(df.at[2, c] for c in place_cols)

        ok = (total == exp_total)
        all_ok &= ok
        rows.append((name, total, exp_total, ok))

    print(f"\n{'='*60}")
    print("ALL-GROUP WINNER SCORING  (12 groups, Day-3 results)")
    print(f"{'='*60}")
    print(f"  {'Name':<12}  {'Total':>8}  Status")
    print(f"  {'-'*12}  {'-'*8}  ------")
    for name, total, exp, ok in rows:
        status = "PASS" if ok else "FAIL"
        val_str = f"{total}+" if total == exp else f"{total}!={exp}"
        print(f"  {name:<12}  {val_str:>8}  [{status}]")
    print("=" * 60)
    return all_ok


# ── 2e. Duplicate submission handling ────────────────────────────────────────
def apply_dedup(df: pd.DataFrame) -> pd.DataFrame:
    """Mirror of the duplicate-detection block in main.py."""
    idx_duplicate = df.duplicated(subset=['First name', 'Last name'], keep=False)
    idx_remove = {"first name": [], "last name": [], "idx": []}
    for idx in range(len(idx_duplicate)):
        if idx_duplicate[idx]:
            if (df.at[idx, "First name"] in idx_remove["first name"]
                    and df.at[idx, "Last name"] in idx_remove["last name"]):
                continue
            else:
                first_name = df.at[idx, "First name"]
                last_name  = df.at[idx, "Last name"]
                name_match = ((df["First name"] == first_name) &
                              (df["Last name"]  == last_name))
                idx_remove["first name"] += [first_name]
                idx_remove["last name"]  += [last_name]
                idx_remove["idx"] += [
                    np.where(np.array(name_match.tolist()) > 0)[0][0]
                ]
    if len(idx_remove["idx"]) > 0:
        df = df.drop(idx_remove["idx"])
    return df


def check_duplicate_handling(predictions_df: pd.DataFrame) -> bool:
    """
    Alice re-submits the Google Form with a changed Group A prediction
    (2-1 → 3-2).  After apply_dedup:
      - 3 rows remain (not 4)
      - Alice appears exactly once
      - Her retained prediction is 3-2 (latest submission, not original)
      - Bob and Carol are unaffected
    """
    resubmit_col  = "Group A Predictions [Mexico - South Africa]"
    original_pred = predictions_df.loc[
        predictions_df["d_name"] == "Alice Sm", resubmit_col
    ].values[0]
    resub_pred = "3-2"

    # Build 4-row df: [Alice_orig, Bob, Carol, Alice_resub]
    alice_resub = predictions_df[predictions_df["d_name"] == "Alice Sm"].copy()
    alice_resub.loc[alice_resub.index[0], resubmit_col] = resub_pred
    alice_resub.loc[alice_resub.index[0], "Timestamp"] = "2026/06/10 09:00:00"

    df4 = pd.concat([predictions_df, alice_resub], ignore_index=True)
    deduped = apply_dedup(df4)

    kept_pred  = deduped.loc[deduped["First name"] == "Alice", resubmit_col].values[0]
    alice_count = (deduped["First name"] == "Alice").sum()

    checks = [
        ("row count == 3",                len(deduped) == 3,     f"got {len(deduped)}"),
        ("Alice appears exactly once",    alice_count == 1,      f"got {alice_count}"),
        (f"re-submission kept ({resub_pred})", kept_pred == resub_pred,
         f"got '{kept_pred}' (original was '{original_pred}')"),
        ("Bob and Carol unaffected",
         set(deduped["First name"]) == {"Alice", "Bob", "Carol"}, ""),
    ]

    all_ok = all(ok for _, ok, _ in checks)
    print(f"\n{'='*60}")
    print("DUPLICATE HANDLING  (Alice re-submits with changed prediction)")
    print(f"{'='*60}")
    for desc, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        suffix = f"  ← {detail}" if (not ok and detail) else ""
        print(f"  [{status}]  {desc}{suffix}")
    print("=" * 60)
    return all_ok


# ── 3. Full pipeline run ──────────────────────────────────────────────────────
def check_schmeichel(todays_schmeichel: dict, exp_name: str, exp_delta) -> bool:
    winner = list(todays_schmeichel.keys())[0]
    delta  = list(todays_schmeichel.values())[0]["value"]
    ok = (winner == exp_name) and (delta == exp_delta)
    status = "PASS" if ok else "FAIL"
    print(f"  Schmeichel: [{status}]  {winner} ({delta} pts)  "
          f"expected {exp_name} ({exp_delta} pts)")
    return ok


def check_monotonicity(df_grp: pd.DataFrame, group_name: str) -> bool:
    """Assert no participant's cumulative score decreases between adjacent days."""
    if df_grp.shape[0] < 2:
        return True
    prev = df_grp.iloc[-2]
    curr = df_grp.iloc[-1]
    failures = [(u, float(prev[u]), float(curr[u]))
                for u in df_grp.columns if curr[u] < prev[u]]
    for user, p, c in failures:
        print(f"  [FAIL] monotonicity: '{group_name}' / {user}  {p} → {c}")
    return len(failures) == 0


def run_day(predictions_df: pd.DataFrame, date_str: str, scored: dict,
            exp_schmeichel_name: str = None, exp_schmeichel_delta=None) -> bool:
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

    day_ok = True
    gfile_avg = "data/group_avg"
    df_group_avg = pd.read_pickle(gfile_avg) if os.path.isfile(gfile_avg) else pd.DataFrame()

    for group in os.listdir("data/group_dfs"):
        df_grp = pd.read_pickle(f"data/group_dfs/{group}")
        day_ok &= check_monotonicity(df_grp, group)
        plot_group_progress(df_grp, group)
        plot_best_round(df_grp, group)
        plot_standings(df_grp, group)
        df_group_avg.loc[date_str, group] = df_grp.loc[date_str].mean()

    plot_group_progress(df_group_avg, "group_avg", out_path="pages/group_plots/")
    df_group_avg.to_pickle(gfile_avg)

    create_pages(predictions_df)
    create_group_pages(predictions_df)
    update_pages(predictions_df, todays_schmeichel)

    if exp_schmeichel_name is not None:
        day_ok &= check_schmeichel(todays_schmeichel, exp_schmeichel_name, exp_schmeichel_delta)
    return day_ok


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
    expected.append("data/group_avg")
    expected.append("pages/group_plots/group_avg.svg")
    expected.append("_data/groups.yml")
    for group in (predictions_df["Which team(s) do you belong to?"]
                  .str.split(";").explode().str.strip().unique()):
        expected.append(f"pages/{group.replace(' ', '_')}.md")

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


# ── 5. Multi-group data integrity ────────────────────────────────────────────
def check_group_data() -> bool:
    """
    After the pipeline run, verify Carol's cumulative scores are identical in
    both Team Alpha and Team Beta (she is a member of both groups).
    """
    df_alpha = pd.read_pickle("data/group_dfs/Team Alpha")
    df_beta  = pd.read_pickle("data/group_dfs/Team Beta")

    alpha_scores = df_alpha["Carol Da"].tolist()
    beta_scores  = df_beta["Carol Da"].tolist()
    match = (alpha_scores == beta_scores)

    print(f"\n{'='*60}")
    print("MULTI-GROUP INTEGRITY  (Carol Da: Team Alpha + Team Beta)")
    print(f"{'='*60}")
    status = "PASS" if match else "FAIL"
    print(f"  [{status}]  scores consistent across both groups: {alpha_scores}")
    if not match:
        print(f"         Team Alpha: {alpha_scores}")
        print(f"         Team Beta:  {beta_scores}")
    print("=" * 60)
    return match


# ── 6. Group average integrity ───────────────────────────────────────────────
def check_group_avg() -> bool:
    """
    Verify the group_avg pickle is correct after the full pipeline run:
    - Has one row per simulated day and one column per team group.
    - Each cell equals the mean of the corresponding group_df row (i.e. the
      formula in main.py is exercised correctly).
    """
    df_avg = pd.read_pickle("data/group_avg")

    exp_dates  = [d for d, *_ in SIMULATED_DAYS]
    exp_groups = sorted(os.listdir("data/group_dfs"))

    checks = []

    # Shape
    ok_rows = list(df_avg.index) == exp_dates
    checks.append(("date index correct", ok_rows,
                   f"got {list(df_avg.index)}"))

    ok_cols = sorted(df_avg.columns) == exp_groups
    checks.append(("team-group columns correct", ok_cols,
                   f"got {sorted(df_avg.columns)}"))

    # Value correctness: each avg must equal the group_df row mean
    value_ok = True
    for date_str in exp_dates:
        for group in exp_groups:
            df_grp    = pd.read_pickle(f"data/group_dfs/{group}")
            expected  = df_grp.loc[date_str].mean()
            actual    = df_avg.loc[date_str, group]
            if actual != expected:
                checks.append((f"avg {group} on {date_str}", False,
                                f"{actual} != {expected}"))
                value_ok = False
    if value_ok:
        checks.append(("all avg values match group_df means", True, ""))

    all_ok = all(ok for _, ok, _ in checks)
    print(f"\n{'='*60}")
    print("GROUP AVG INTEGRITY")
    print(f"{'='*60}")
    for desc, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        suffix = f"  ← {detail}" if (not ok and detail) else ""
        print(f"  [{status}]  {desc}{suffix}")
    print("=" * 60)
    return all_ok


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
        all_ok &= check_special_scoring(predictions_df)
        all_ok &= check_all_group_winner_scoring(predictions_df)
        all_ok &= check_duplicate_handling(predictions_df)

        for date_str, scored, n_played, exp_name, exp_delta in SIMULATED_DAYS:
            print(f"\n--- Day {date_str}  ({n_played}/72 group-stage matches resolved) ---")
            all_ok &= run_day(predictions_df.copy(), date_str, scored, exp_name, exp_delta)

        all_ok &= assert_files(predictions_df)
        all_ok &= check_group_data()
        all_ok &= check_group_avg()

        if all_ok:
            print("\n[PASS]  All checks passed.\n")
        else:
            print("\n[FAIL]  One or more checks failed - see output above.\n")
            raise SystemExit(1)

    finally:
        teardown()


if __name__ == "__main__":
    main()
