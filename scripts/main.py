import time
import pandas as pd
from loguru import logger
from get_results import *
from eval_funcs import *
from insert_pages import *
from create_pages import *
from datetime import datetime, timezone, timedelta
import os
cwd = os.getcwd()

# Copenhagen summer time (CEST = UTC+2) for correct date labelling
_CEST = timezone(timedelta(hours=2))


def run_pipeline(results, today, raw=None,
                 topscorer=None, topscorer_goals=None,
                 finale_winner=None, finale_loser=None):
    """
    Core pipeline: score all participants, persist data, regenerate pages.

    Parameters
    ----------
    results         : list of (matchid, score_str) from get_results()
    today           : date object used as the row key in group_dfs
    raw             : raw API match list (optional — used for schedule sections)
    topscorer       : list of top scorer name(s), e.g. ["Harry Kane"]
    topscorer_goals : int goals scored by top scorer, or None
    finale_winner   : name of final winner, or None
    finale_loser    : name of final runner-up, or None
    """
    if topscorer is None:
        topscorer = []

    t0 = time.time()

    csv_path = "data/FIFA World Cup 2026 - Predictions.csv"
    if not os.path.isfile(csv_path):
        logger.warning("[CSV] Predictions file not found — add the CSV to start scoring")
        return

    predictions_df = pd.read_csv(csv_path)

    # Support both the real form column names and the simpler test-CSV column names
    fn_col = 'First name (one name)' if 'First name (one name)' in predictions_df.columns else 'First name'
    ln_col = 'Last name (one name)'  if 'Last name (one name)'  in predictions_df.columns else 'Last name'

    df_fname = pd.DataFrame({'f_name': [
        (f"{row[fn_col]}_" + f"{str(row[ln_col])[0:2]}").replace(" ", "_").replace('"', "_")
        for _, row in predictions_df.iterrows()
    ]})
    df_dname = pd.DataFrame({'d_name': [
        f"{row[fn_col]} {str(row[ln_col]).split()[-1]}"
        for _, row in predictions_df.iterrows()
    ]})
    predictions_df = predictions_df.join(df_fname)
    predictions_df = predictions_df.join(df_dname)

    logger.info(f"[CSV] {len(predictions_df)} participants loaded")

    # ── Duplicate detection ───────────────────────────────────────────────────
    idx_duplicate = predictions_df.duplicated(subset=[fn_col, ln_col], keep=False)
    idx_remove = {"first name": [], "last name": [], "idx": []}
    for idx in range(len(idx_duplicate)):
        if idx_duplicate[idx]:
            fn = predictions_df.at[idx, fn_col]
            ln = predictions_df.at[idx, ln_col]
            if fn in idx_remove["first name"] and ln in idx_remove["last name"]:
                continue
            name_match = ((predictions_df[fn_col] == fn) &
                          (predictions_df[ln_col] == ln))
            idx_remove["first name"] += [fn]
            idx_remove["last name"]  += [ln]
            idx_remove["idx"] += [np.where(np.array(name_match.tolist()) > 0)[0][0]]

    if len(idx_remove["idx"]) > 0:
        logger.warning(f"[DUPLICATES] Removed {len(idx_remove['idx'])} duplicate submission(s): "
                       f"{list(zip(idx_remove['first name'], idx_remove['last name']))}")
        predictions_df = predictions_df.drop(idx_remove["idx"])

    # ── Group winner completion summary ───────────────────────────────────────
    group_winners  = find_group_winners(results)
    n_gw_complete  = sum(1 for v in group_winners.values() if v.get("1st"))
    logger.info(f"[GROUPS] {n_gw_complete}/{len(group_winners)} groups complete")

    # ── Score each participant ────────────────────────────────────────────────
    max_val = 0
    todays_schmeichel = {"Nobody": {"value": max_val, "group": "Nobody", "fname": ""}}

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
                logger.debug(f"[GUARD] {user} score unchanged ({user_total} pts) — skipping write")
                continue

            df_grp.loc[today, user] = user_total_float
            df_grp.to_pickle(gfile)

            if df_grp.shape[0] > 1:
                prev_date = df_grp.index[
                    np.where(np.array(df_grp.index.tolist()) == today)[0][0] - 1
                ]
                user_val = df_grp.loc[today, user] - df_grp.at[prev_date, user]
            else:
                user_val = user_total_float

            if user_val > max_val:
                todays_schmeichel = {
                    user_df.at[0, "d_name"]: {
                        "value": user_val,
                        "group": user_df.at[0, "Which team(s) do you belong to?"].replace(";", " and "),
                        "fname": user_df.at[0, "f_name"],
                    }
                }
                max_val = user_val
            elif user_val == max_val:
                todays_schmeichel[user_df.at[0, "d_name"]] = {
                    "value": user_val,
                    "group": user_df.at[0, "Which team(s) do you belong to?"].replace(";", " and "),
                    "fname": user_df.at[0, "f_name"],
                }

        if len(df_grp) > 1 and df_grp.iloc[-1, 0] < df_grp.iloc[-2, 0]:
            logger.error(f"[INTEGRITY] Score decreased for participant in group '{group}' — investigate!")

    # ── Schmeichel persistence ────────────────────────────────────────────────
    last_schm_path  = os.path.join(cwd, "data", "last_schmeichel.pickle")
    schmeichel_name = list(todays_schmeichel.keys())[0]

    if schmeichel_name == "Nobody":
        if os.path.isfile(last_schm_path):
            todays_schmeichel = load_results(last_schm_path)
            saved_name = list(todays_schmeichel.keys())[0]
            logger.info(f"[SCHMEICH] No new scores — showing last real winner: {saved_name}")
        else:
            logger.info("[SCHMEICH] No scores yet")
    else:
        schmeichel_pts = int(round(todays_schmeichel[schmeichel_name]["value"]))
        logger.success(f"[SCHMEICH] {schmeichel_name} — {schmeichel_pts} pts this round")
        save_results(last_schm_path, todays_schmeichel)

    # ── Group averages ────────────────────────────────────────────────────────
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
            logger.warning(f"[WARN] Could not read group_dfs/{group}: {e} — skipping")
            continue
        if today in df_grp.index:
            df_group_avg.loc[today, group] = df_grp.ffill().loc[today].mean()

    df_group_avg.to_pickle("data/group_avg")

    create_pages(predictions_df)
    create_group_pages(predictions_df)
    update_pages(predictions_df, todays_schmeichel, raw_matches=raw)

    logger.success(f"[DONE] Pipeline finished in {time.time() - t0:.1f}s")


# ── Entry point (production) ──────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("Pipeline started")

    #### Fill out when final is finished
    topscorer       = []
    topscorer_goals = None  # e.g. 5  ← integer, NOT a string
    finale_loser    = None  # e.g. "France"
    finale_winner   = None  # e.g. "Brazil"

    try:
        raw = fetch_raw_matches()
    except Exception as e:
        logger.error(f"API call failed: {e}")
        raise

    finished_count = sum(1 for m in raw if m.get("status") == "FINISHED")
    logger.info(f"[API] {len(raw)} matches fetched — {finished_count} finished")

    results      = get_results(raw)
    today        = datetime.now(timezone.utc).astimezone(_CEST).date()
    n_file       = get_highest_result_number()
    prev_results = load_results(cwd + f"/results/data_{n_file}.pickle")

    if prev_results[0] != results:
        prev_finished = sum(1 for _, score in prev_results[0] if "None" not in str(score))
        logger.info(f"[CHANGE] {prev_finished} → {finished_count} finished — running full pipeline")
        save_results(cwd + f"/results/data_{n_file+1}.pickle", [results, today])
        run_pipeline(results, today, raw=raw,
                     topscorer=topscorer, topscorer_goals=topscorer_goals,
                     finale_winner=finale_winner, finale_loser=finale_loser)
    else:
        logger.info(f"[NO CHANGE] {finished_count} finished — refreshing schedule only")
        update_next_matches_only(raw)
