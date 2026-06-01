"""
Test pipeline runner — same code as production, controlled date and results.

Usage:
  python scripts/run_test.py <YYYY-MM-DD> [results.json]

  <YYYY-MM-DD>   date to stamp this run  (e.g. 2026-06-12)
  [results.json] optional JSON file: { "matchid": "H - A", ... }
                 omit for a pre-tournament run (no match results)

The JSON only needs to contain FINISHED matches; all other group-stage
matches from the CSV prediction columns are automatically set to "None - None"
so group-completion detection works exactly as in production.

Calls main.run_pipeline() directly — guaranteed to use the same logic as
the real pipeline with no code duplication.
"""

import sys
import os
import json

# ── Path setup ────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from datetime import date
from loguru import logger
from get_results import save_results, load_results, get_highest_result_number
from insert_pages import update_next_matches_only
from main import run_pipeline                        # ← the real pipeline function

cwd = os.getcwd()

# ── Arguments ─────────────────────────────────────────────────────────────────
if len(sys.argv) < 2:
    sys.exit("Usage: python scripts/run_test.py <YYYY-MM-DD> [results.json]")

today = date.fromisoformat(sys.argv[1])

injected: dict = {}
if len(sys.argv) >= 3:
    with open(sys.argv[2], encoding="utf-8") as f:
        injected = json.load(f)

logger.info(f"Test runner — date: {today}  |  injected results: {len(injected)}")

# ── Build full results list ───────────────────────────────────────────────────
# All match IDs are derived from the CSV prediction columns so unplayed matches
# correctly appear as "None - None" (identical to the real API response).
_csv = pd.read_csv("data/FIFA World Cup 2026 - Predictions.csv")
ALL_MATCH_IDS = [c for c in _csv.columns if "Predictions [" in c]

results = [(mid, injected.get(mid, "None - None")) for mid in ALL_MATCH_IDS]
if not results:
    results = [("PRE_TOURNAMENT_SENTINEL", "None - None")]

# ── Change detection (mirrors main.py exactly) ────────────────────────────────
n_file       = get_highest_result_number()
prev_results = load_results(cwd + f"/results/data_{n_file}.pickle")

if prev_results[0] != results:
    logger.info(f"[CHANGE] Saving as data_{n_file+1}.pickle — running full pipeline")
    save_results(cwd + f"/results/data_{n_file+1}.pickle", [results, today])
    run_pipeline(results, today)          # ← identical to what main.py calls
else:
    logger.info("[NO CHANGE] Results identical — refreshing schedule sections only")
    update_next_matches_only(raw_matches=None)
