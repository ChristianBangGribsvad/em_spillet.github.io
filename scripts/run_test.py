"""
Test pipeline runner — simulates a pipeline run with a controlled date and
injected match results (no real API call needed).

Usage:
  python scripts/run_test.py <YYYY-MM-DD> [results_file]

  <YYYY-MM-DD>   : the date to stamp on this run (e.g. 2026-06-10)
  [results_file] : optional JSON file with {matchid: "H - A"} (omit = pre-tournament)

Examples:
  python scripts/run_test.py 2026-06-10
  python scripts/run_test.py 2026-06-12 scripts/test_results_day1.json

The script is a drop-in replacement for running main.py directly, but
reads its inputs from arguments rather than the live API and system clock.
"""

import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta, date
from loguru import logger
from eval_funcs    import eval_match_predictions, eval_groups, find_group_winners
from insert_pages  import (update_pages, update_next_matches_only,
                            create_group_pages)
from create_pages  import create_pages
from get_results   import (save_results, load_results,
                           get_highest_result_number, process_match)

cwd   = os.getcwd()
_CEST = timezone(timedelta(hours=2))

# ── Parse arguments ────────────────────────────────────────────────────────────
if len(sys.argv) < 2:
    sys.exit("Usage: python scripts/run_test.py <YYYY-MM-DD> [results_json]")

today = date.fromisoformat(sys.argv[1])

# Optional injected results file:  { "Group A Predictions [Mexico - South Africa]": "2 - 1", ... }
injected: dict[str, str] = {}
if len(sys.argv) >= 3:
    with open(sys.argv[2], encoding="utf-8") as f:
        injected = json.load(f)

CSV        = "data/FIFA World Cup 2026 - Predictions.csv"
FNAME_COL  = "First name (one name)"
LNAME_COL  = "Last name (one name)"

logger.info(f"Test pipeline — date: {today}  |  injected results: {len(injected)}")

# ── Build results list from injected dict (mirrors process_match output) ───────
# We derive all known match IDs from the Predictions columns in the CSV so that
# unplayed matches correctly appear as "None - None" (just like the real API).
_csv_df       = pd.read_csv(CSV)
ALL_MATCH_IDS = [c for c in _csv_df.columns if "Predictions [" in c]

results = [
    (match_id, injected.get(match_id, "None - None"))
    for match_id in ALL_MATCH_IDS
]
# Pre-tournament sentinel: ensures we differ from the bootstrap [] even when
# ALL_MATCH_IDS is empty (shouldn't happen with a real CSV).
if not results:
    results = [("PRE_TOURNAMENT_SENTINEL", "None - None")]

# ── Manual special-prediction values (fill in when known) ─────────────────────
topscorer       = []
topscorer_goals = None
finale_loser    = None
finale_winner   = None

# ── Change detection ───────────────────────────────────────────────────────────
eval_res     = True
datafile     = [results, today]
n_file       = get_highest_result_number()
prev_results = load_results(cwd + f"/results/data_{n_file}.pickle")

if prev_results[0] != results:
    logger.info(f"[CHANGE] Saving as data_{n_file+1}.pickle — running full pipeline")
    save_results(cwd + f"/results/data_{n_file+1}.pickle", datafile)
else:
    logger.info("[NO CHANGE] Results identical — refreshing schedule sections only")
    update_next_matches_only(raw_matches=None)
    logger.success(f"[DONE] {time.time():.1f}s  (no-op run)")
    sys.exit(0)

# ── Full pipeline ──────────────────────────────────────────────────────────────
t0 = time.time()

predictions_df = pd.read_csv(CSV)

predictions_df["f_name"] = [
    (f"{r[FNAME_COL]}_{str(r[LNAME_COL])[:2]}").replace(" ", "_").replace('"', "_")
    for _, r in predictions_df.iterrows()
]
predictions_df["d_name"] = [
    f"{r[FNAME_COL]} {str(r[LNAME_COL]).split()[-1]}"
    for _, r in predictions_df.iterrows()
]

logger.info(f"[CSV] {len(predictions_df)} participants loaded from {CSV}")

# Duplicate detection
idx_dup = predictions_df.duplicated(subset=[FNAME_COL, LNAME_COL], keep=False)
idx_remove: dict = {"first name": [], "last name": [], "idx": []}
for idx in range(len(idx_dup)):
    if idx_dup[idx]:
        fn = predictions_df.at[idx, FNAME_COL]
        ln = predictions_df.at[idx, LNAME_COL]
        if fn in idx_remove["first name"] and ln in idx_remove["last name"]:
            continue
        mask = ((predictions_df[FNAME_COL] == fn) & (predictions_df[LNAME_COL] == ln))
        idx_remove["first name"].append(fn)
        idx_remove["last name"].append(ln)
        idx_remove["idx"].append(np.where(np.array(mask.tolist()) > 0)[0][0])
if idx_remove["idx"]:
    logger.warning(f"[DUPLICATES] Removing {len(idx_remove['idx'])} duplicate(s)")
    predictions_df = predictions_df.drop(idx_remove["idx"])

# Group winner summary
group_winners = find_group_winners(results)
n_complete    = sum(1 for v in group_winners.values() if v.get("1st"))
logger.info(f"[GROUPS] {n_complete}/{len(group_winners)} groups complete")

# Score each participant
max_val = 0
todays_schmeichel = {"Nobody": {"value": 0, "group": "Nobody", "fname": ""}}

for user in predictions_df["d_name"]:
    user_df = predictions_df[predictions_df["d_name"] == user].reset_index(drop=True)
    user_df = eval_match_predictions(user_df, results)
    user_df = eval_groups(user_df, results)

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

    user_df.to_pickle("data/user_dfs/" + user_df.at[0, "f_name"])

    user_total       = int(round(pd.to_numeric(user_df.loc[2], errors='coerce').sum()))
    user_total_float = user_df.loc[2].sum()
    logger.info(f"[SCORE] {user}: {user_total} pts")

    for group in user_df.at[0, "Which team(s) do you belong to?"].split(";"):
        group = group.strip()
        gfile = f"data/group_dfs/{group}"
        df_grp = pd.read_pickle(gfile) if os.path.isfile(gfile) else pd.DataFrame()

        if (not df_grp.empty and user in df_grp.columns
                and df_grp[user].iloc[-1] == user_total_float):
            logger.debug(f"[GUARD] {user} unchanged — skip")
            continue

        df_grp.loc[today, user] = user_total_float
        df_grp.to_pickle(gfile)

        if df_grp.shape[0] > 1:
            prev_date = df_grp.index[np.where(np.array(df_grp.index.tolist()) == today)[0][0] - 1]
            user_val  = df_grp.loc[today, user] - df_grp.at[prev_date, user]
        else:
            user_val = user_total_float

        if user_val > max_val:
            todays_schmeichel = {user: {"value": user_val,
                                         "group": user_df.at[0, "Which team(s) do you belong to?"].replace(";", " and "),
                                         "fname": user_df.at[0, "f_name"]}}
            max_val = user_val
        elif user_val == max_val:
            todays_schmeichel[user] = {"value": user_val,
                                        "group": user_df.at[0, "Which team(s) do you belong to?"].replace(";", " and "),
                                        "fname": user_df.at[0, "f_name"]}

# Schmeichel persistence
last_schm_path  = os.path.join(cwd, "data", "last_schmeichel.pickle")
schmeichel_name = list(todays_schmeichel.keys())[0]
if schmeichel_name == "Nobody":
    if os.path.isfile(last_schm_path):
        todays_schmeichel = load_results(last_schm_path)
        logger.info(f"[SCHMEICH] No new scores — showing last winner")
    else:
        logger.info("[SCHMEICH] No scores yet")
else:
    pts = int(round(todays_schmeichel[schmeichel_name]["value"]))
    logger.success(f"[SCHMEICH] {schmeichel_name} — {pts} pts this round")
    save_results(last_schm_path, todays_schmeichel)

# Group averages
if "group_avg" not in os.listdir("data/"):
    df_group_avg = pd.DataFrame()
else:
    df_group_avg = pd.read_pickle("data/group_avg")

for group in os.listdir("data/group_dfs"):
    if group.startswith('.'):
        continue
    try:
        df_grp = pd.read_pickle(f"data/group_dfs/{group}")
    except Exception as e:
        logger.warning(f"[WARN] group_dfs/{group}: {e}")
        continue
    if today in df_grp.index:
        df_group_avg.loc[today, group] = df_grp.ffill().loc[today].mean()

df_group_avg.to_pickle("data/group_avg")

create_pages(predictions_df)
create_group_pages(predictions_df)
update_pages(predictions_df, todays_schmeichel, raw_matches=None)

logger.success(f"[DONE] Test pipeline finished in {time.time()-t0:.1f}s")
