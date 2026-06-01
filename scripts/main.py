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

if __name__ == "__main__":
    t0 = time.time()
    logger.info("Pipeline started")

    #### Fill out when final is finished
    topscorer = []       # e.g. ["Player Name"]
    topscorer_goals = None  # e.g. 5  ← integer, NOT a string. pandas reads this CSV column as int64.
    finale_loser = None  # e.g. "France"
    finale_winner = None # e.g. "Brazil"
    eval_res = True

    # ── Single API call shared by the whole pipeline ──────────────────────────
    try:
        raw = fetch_raw_matches()
    except Exception as e:
        logger.error(f"API call failed: {e}")
        raise

    finished_count = sum(1 for m in raw if m.get("status") == "FINISHED")
    logger.info(f"[API] {len(raw)} matches fetched — {finished_count} finished")

    results      = get_results(raw)
    today   = datetime.now(timezone.utc).astimezone(_CEST).date()  # date in Copenhagen time
    datafile     = [results, today]
    n_file       = get_highest_result_number()
    prev_results = load_results(cwd + f"/results/data_{n_file}.pickle")

    if prev_results[0] != results:
        prev_finished = sum(1 for _, score in prev_results[0] if "None" not in str(score))
        logger.info(f"[CHANGE] {prev_finished} → {finished_count} finished — running full pipeline")
        save_results(cwd + f"/results/data_{n_file+1}.pickle", datafile)
    else:
        logger.info(f"[NO CHANGE] {finished_count} finished — refreshing schedule only")
        eval_res = False
        update_next_matches_only(raw)

    # ── Full pipeline — only when results changed ─────────────────────────────
    if eval_res:
        predictions_df = pd.read_csv("data/FIFA World Cup 2026 - Predictions.csv")

        df_fname = pd.DataFrame({'f_name': [
            (f"{row['First name (one name)']}_" + f"{str(row['Last name (one name)'])[0:2]}").replace(" ", "_").replace('"', "_")
            for _, row in predictions_df.iterrows()
        ]})
        df_dname = pd.DataFrame({'d_name': [
            f"{row['First name (one name)']} {str(row['Last name (one name)']).split()[-1]}"
            for _, row in predictions_df.iterrows()
        ]})
        predictions_df = predictions_df.join(df_fname)
        predictions_df = predictions_df.join(df_dname)

        logger.info(f"[CSV] {len(predictions_df)} participants loaded")

        ### Detect duplicates
        idx_duplicate = predictions_df.duplicated(subset=['First name (one name)', 'Last name (one name)'], keep=False)
        idx_remove = {"first name": [], "last name": [], "idx": []}
        for idx in range(len(idx_duplicate)):
            if idx_duplicate[idx]:
                if (predictions_df.at[idx, "First name (one name)"] in idx_remove["first name"] and
                        predictions_df.at[idx, "Last name (one name)"]  in idx_remove["last name"]):
                    continue
                else:
                    first_name = predictions_df.at[idx, "First name (one name)"]
                    last_name  = predictions_df.at[idx, "Last name (one name)"]
                    name_match = ((predictions_df["First name (one name)"] == first_name) &
                                  (predictions_df["Last name (one name)"]  == last_name))
                    idx_remove["first name"] += [first_name]
                    idx_remove["last name"]  += [last_name]
                    idx_remove["idx"] += [np.where(np.array(name_match.tolist()) > 0)[0][0]]

        if len(idx_remove["idx"]) > 0:
            logger.warning(f"[DUPLICATES] Removed {len(idx_remove['idx'])} duplicate submission(s): "
                           f"{list(zip(idx_remove['first name'], idx_remove['last name']))}")
            predictions_df = predictions_df.drop(idx_remove["idx"])

        # ── Group winner completion summary ───────────────────────────────────
        group_winners  = find_group_winners(results)
        n_gw_complete  = sum(1 for v in group_winners.values() if v.get("1st"))
        logger.info(f"[GROUPS] {n_gw_complete}/{len(group_winners)} groups complete")

        # ── Score each participant ────────────────────────────────────────────
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

            user_total = int(round(pd.to_numeric(user_df.loc[2], errors='coerce').sum()))
            logger.info(f"[SCORE] {user}: {user_total} pts")

            user_total_float = user_df.loc[2].sum()

            for group in user_df.at[0, "Which team(s) do you belong to?"].split(";"):
                if group not in os.listdir("data/group_dfs"):
                    df_results = pd.DataFrame()
                else:
                    df_results = pd.read_pickle("data/group_dfs/" + group)

                # Guard: only write a new date row when the score actually changed.
                # Skipping zero-delta writes prevents phantom "rounds" in the knockout
                # stage when group-stage predictions can no longer gain points.
                if (not df_results.empty and user in df_results.columns
                        and df_results[user].iloc[-1] == user_total_float):
                    logger.debug(f"[GUARD] {user} score unchanged ({user_total} pts) — skipping write")
                    continue

                df_results.loc[today, user] = user_total_float
                df_results.to_pickle("data/group_dfs/" + group)

                if df_results.shape[0] > 1:
                    prev_date = df_results.index[
                        np.where(np.array(df_results.index.tolist()) == today)[0][0] - 1
                    ]
                    user_val = df_results.loc[today, user] - df_results.at[prev_date, user]
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

            if len(df_results) > 1 and df_results.iloc[-1, 0] < df_results.iloc[-2, 0]:
                logger.error(f"[INTEGRITY] Score decreased for participant in group '{group}' — investigate!")

        # ── Schmeichel persistence ────────────────────────────────────────────
        # During the knockout stage no group-stage prediction scores change, so
        # todays_schmeichel would default to "Nobody".  Rather than display that
        # on the front page for five weeks, we fall back to the last real winner.
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

        # ── Group averages ────────────────────────────────────────────────────
        if "group_avg" not in os.listdir("data/"):
            df_group_avg = pd.DataFrame()
        else:
            df_group_avg = pd.read_pickle("data/group_avg")

        for group in os.listdir("data/group_dfs"):
            if group.startswith('.'):
                continue
            try:
                df_results = pd.read_pickle("data/group_dfs/" + group)
            except Exception as e:
                logger.warning(f"[WARN] Could not read group_dfs/{group}: {e} — skipping")
                continue
            # Only record group avg for dates that actually have new data.
            # ffill ensures participants with unchanged scores (guard fired) are
            # still included in the average at their last known value.
            if today in df_results.index:
                df_group_avg.loc[today, group] = df_results.ffill().loc[today].mean()

        df_group_avg.to_pickle("data/group_avg")

        create_pages(predictions_df)
        create_group_pages(predictions_df)
        update_pages(predictions_df, todays_schmeichel, raw_matches=raw)

    logger.success(f"[DONE] Pipeline finished in {time.time() - t0:.1f}s")
