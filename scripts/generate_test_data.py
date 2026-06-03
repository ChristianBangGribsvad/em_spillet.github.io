#!/usr/bin/env python3
"""
Generate engineered test CSV for badge testing.
10 participants with predictions designed to trigger 6 of 8 badge types:

  🔮 Crystal Ball        — Mexico vs SA (actual 2-1): only Alice correct (1/10 = 10%)
  🎯 Sharp Eye           — SK vs Czechia (actual 1-1): Alice + Emma correct (2/10 = 20%)
  😬 Rare Miss           — Canada vs Bosnia (actual 1-0): 8/10 correct, Isabella+James wrong
  🙈 The One Who Missed  — Qatar vs Switzerland (actual 0-2): 9/10 correct, Carol wrong
  💀 Nobody Saw That     — Brazil vs Morocco (actual 3-0): 0/10 correct
  🤝 In Good Company     — USA vs Paraguay (actual 2-1): Alice+David+Frank correct (3/10)

Hidden Gem + Unicorn require > 20 participants to trigger (min ratio with 10 people = 10%,
above their 5% / 6% thresholds). They will work with real participant counts.

Run from repo root:
  python scripts/generate_test_data.py
"""
import csv
import os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT = "data/FIFA World Cup 2026 - Predictions.csv"

# ─── Column definitions ───────────────────────────────────────────────────────

MATCH_COLS = [
    # Group A
    "Group A Predictions [Mexico - South Africa]",        # idx 0  PLAYED 2-1
    "Group A Predictions [South Korea - Czechia]",        # idx 1  PLAYED 1-1
    "Group A Predictions [Czechia - South Africa]",
    "Group A Predictions [Mexico - South Korea]",
    "Group A Predictions [Czechia - Mexico]",
    "Group A Predictions [South Africa - South Korea]",
    # Group B
    "Group B Predictions [Canada - Bosnia-Herzegovina]",  # idx 6  PLAYED 1-0
    "Group B Predictions [Qatar - Switzerland]",          # idx 7  PLAYED 0-2
    "Group B Predictions [Switzerland - Bosnia-Herzegovina]",
    "Group B Predictions [Canada - Qatar]",
    "Group B Predictions [Switzerland - Canada]",
    "Group B Predictions [Bosnia-Herzegovina - Qatar]",
    # Group C
    "Group C Predictions [Brazil - Morocco]",             # idx 12 PLAYED 3-0
    "Group C Predictions [Haiti - Scotland]",
    "Group C Predictions [Scotland - Morocco]",
    "Group C Predictions [Brazil - Haiti]",
    "Group C Predictions [Morocco - Haiti]",
    "Group C Predictions [Scotland - Brazil]",
    # Group D
    "Group D Predictions [United States - Paraguay]",     # idx 18 PLAYED 2-1
    "Group D Predictions [Australia - Turkey]",
    "Group D Predictions [United States - Australia]",
    "Group D Predictions [Turkey - Paraguay]",
    "Group D Predictions [Turkey - United States]",
    "Group D Predictions [Paraguay - Australia]",
    # Group E
    "Group E Predictions [Germany - Curaçao]",            # idx 24 PLAYED 4-0
    "Group E Predictions [Ivory Coast - Ecuador]",
    "Group E Predictions [Germany - Ivory Coast]",
    "Group E Predictions [Ecuador - Curaçao]",
    "Group E Predictions [Ecuador - Germany]",
    "Group E Predictions [Curaçao - Ivory Coast]",
    # Group F
    "Group F Predictions [Netherlands - Japan]",          # idx 30 PLAYED 2-0
    "Group F Predictions [Sweden - Tunisia]",
    "Group F Predictions [Netherlands - Sweden]",
    "Group F Predictions [Tunisia - Japan]",
    "Group F Predictions [Tunisia - Netherlands]",
    "Group F Predictions [Japan - Sweden]",
    # Group G
    "Group G Predictions [Belgium - Egypt]",              # idx 36 PLAYED 2-0
    "Group G Predictions [Iran - New Zealand]",           # idx 37 PLAYED 1-0
    "Group G Predictions [Belgium - Iran]",               # idx 38 PLAYED 3-1
    "Group G Predictions [New Zealand - Egypt]",          # idx 39 PLAYED 0-1
    "Group G Predictions [New Zealand - Belgium]",        # idx 40 PLAYED 0-3
    "Group G Predictions [Egypt - Iran]",                 # idx 41 PLAYED 0-1
    # Groups H–L (all unplayed)
    "Group H Predictions [Spain - Cape Verde Islands]",
    "Group H Predictions [Saudi Arabia - Uruguay]",
    "Group H Predictions [Spain - Saudi Arabia]",
    "Group H Predictions [Uruguay - Cape Verde Islands]",
    "Group H Predictions [Uruguay - Spain]",
    "Group H Predictions [Cape Verde Islands - Saudi Arabia]",
    "Group I Predictions [France - Senegal]",
    "Group I Predictions [Iraq - Norway]",
    "Group I Predictions [France - Iraq]",
    "Group I Predictions [Norway - Senegal]",
    "Group I Predictions [Norway - France]",
    "Group I Predictions [Senegal - Iraq]",
    "Group J Predictions [Argentina - Algeria]",
    "Group J Predictions [Austria - Jordan]",
    "Group J Predictions [Argentina - Austria]",
    "Group J Predictions [Jordan - Algeria]",
    "Group J Predictions [Jordan - Argentina]",
    "Group J Predictions [Algeria - Austria]",
    "Group K Predictions [Portugal - Congo DR]",
    "Group K Predictions [Uzbekistan - Colombia]",
    "Group K Predictions [Portugal - Uzbekistan]",
    "Group K Predictions [Colombia - Congo DR]",
    "Group K Predictions [Colombia - Portugal]",
    "Group K Predictions [Congo DR - Uzbekistan]",
    "Group L Predictions [England - Croatia]",
    "Group L Predictions [Ghana - Panama]",
    "Group L Predictions [England - Ghana]",
    "Group L Predictions [Panama - Croatia]",
    "Group L Predictions [Panama - England]",
    "Group L Predictions [Croatia - Ghana]",
]

WINNER_COLS = [
    f"Group {g} {p} place"
    for g in "ABCDEFGHIJKL"
    for p in ("1st", "2nd")
]

SPECIAL_COLS = [
    "FIFA World Cup 2026 final winner",
    "FIFA World Cup 2026 final loser",
    "Who is going to be the top scorer throughout FIFA World Cup 2026? (20 points)",
    "How many goals does the top scorer score? (10 points)",
]

HEADER = (
    ["Timestamp", "First name", "Last name", "Which team(s) do you belong to?"]
    + MATCH_COLS + WINNER_COLS + SPECIAL_COLS
)

# ─── Participants ─────────────────────────────────────────────────────────────

PARTICIPANTS = [
    # (first, last, team, timestamp)
    ("Alice",    "Smith",    "Team Alpha",             "2026/06/01 10:00:00"),
    ("Bob",      "Johnson",  "Team Beta",              "2026/06/01 10:15:00"),
    ("Carol",    "Davis",    "Team Alpha;Team Beta",   "2026/06/01 10:30:00"),
    ("David",    "Lee",      "Team Alpha",             "2026/06/01 10:45:00"),
    ("Emma",     "Wilson",   "Team Beta",              "2026/06/01 11:00:00"),
    ("Frank",    "Brown",    "Team Alpha",             "2026/06/01 11:15:00"),
    ("Grace",    "Taylor",   "Team Beta",              "2026/06/01 11:30:00"),
    ("Henry",    "Martinez", "Team Alpha;Team Beta",   "2026/06/01 11:45:00"),
    ("Isabella", "Anderson", "Team Alpha",             "2026/06/01 12:00:00"),
    ("James",    "White",    "Team Beta",              "2026/06/01 12:15:00"),
]

# ─── Engineered predictions for played matches ────────────────────────────────
#
# Badge targets:
#   idx 0  Mexico-SA   (actual 2-1, Mex win) → Crystal Ball:  Alice alone correct (1/10)
#   idx 1  SK-Czechia  (actual 1-1, draw)    → Sharp Eye:     Alice+Emma correct   (2/10)
#   idx 6  Canada-Bos  (actual 1-0, Can win) → Rare Miss:     8/10 correct, Isabella+James wrong
#   idx 7  Qatar-Switz (actual 0-2, Swi win) → One Who Missed: 9/10 correct, Carol wrong
#   idx 12 Brazil-Mor  (actual 3-0, Bra win) → Nobody Saw:    0/10 correct (everyone wrong)
#   idx 18 USA-Para    (actual 2-1, USA win) → In Good Company: Alice+David+Frank correct (3/10)
#
# Non-trigger played matches (cols 24,30,36-41) kept between 40-70% correct → no badge.

BADGE_OVERRIDES = {
    #            [0]Mex-SA  [1]SK-Cze  [6]Can-Bos  [7]Qat-Swi  [12]Bra-Mor  [18]USA-Par
    "Alice":    {"0":"2-1", "1":"1-1", "6":"1-0",  "7":"0-2",  "12":"0-0",  "18":"2-1"},  # ✓ ✓ ✓ ✓ ✗ ✓
    "Bob":      {"0":"0-1", "1":"2-0", "6":"2-0",  "7":"0-1",  "12":"0-1",  "18":"0-1"},  # ✗ ✗ ✓ ✓ ✗ ✗
    "Carol":    {"0":"1-2", "1":"1-0", "6":"2-1",  "7":"1-0",  "12":"1-1",  "18":"1-2"},  # ✗ ✗ ✓ ✗ ✗ ✗
    "David":    {"0":"0-2", "1":"0-1", "6":"3-0",  "7":"0-3",  "12":"0-0",  "18":"1-0"},  # ✗ ✗ ✓ ✓ ✗ ✓
    "Emma":     {"0":"1-3", "1":"0-0", "6":"1-0",  "7":"0-2",  "12":"0-2",  "18":"0-0"},  # ✗ ✓ ✓ ✓ ✗ ✗
    "Frank":    {"0":"0-1", "1":"0-2", "6":"2-1",  "7":"1-3",  "12":"0-2",  "18":"3-1"},  # ✗ ✗ ✓ ✓ ✗ ✓
    "Grace":    {"0":"1-2", "1":"1-0", "6":"1-0",  "7":"0-1",  "12":"1-1",  "18":"0-1"},  # ✗ ✗ ✓ ✓ ✗ ✗
    "Henry":    {"0":"0-0", "1":"2-1", "6":"2-0",  "7":"0-2",  "12":"0-1",  "18":"1-2"},  # ✗ ✗ ✓ ✓ ✗ ✗
    "Isabella": {"0":"1-1", "1":"0-1", "6":"0-1",  "7":"0-3",  "12":"1-2",  "18":"0-2"},  # ✗ ✗ ✗ ✓ ✗ ✗
    "James":    {"0":"0-2", "1":"1-0", "6":"1-2",  "7":"1-2",  "12":"0-0",  "18":"0-1"},  # ✗ ✗ ✗ ✓ ✗ ✗
}

NON_TRIGGER_PLAYED = {
    #            Ger-Cur Ned-Jpn Bel-Egy Ira-NZ  Bel-Ira NZ-Egy  NZ-Bel  Egy-Ira
    #            [24]    [30]    [36]    [37]    [38]    [39]    [40]    [41]
    "Alice":    ["3-0",  "2-0",  "2-0",  "1-0",  "2-1",  "0-1",  "0-2",  "1-0"],  # ✓✓✓✓✓✓✓✗
    "Bob":      ["2-0",  "1-0",  "1-0",  "0-1",  "3-0",  "1-0",  "0-3",  "0-1"],  # ✓✓✓✗✓✗✓✓
    "Carol":    ["2-1",  "0-1",  "2-1",  "1-1",  "1-0",  "0-2",  "0-2",  "1-1"],  # ✓✗✓✗✓✓✓✗
    "David":    ["4-0",  "0-2",  "0-1",  "1-0",  "0-1",  "1-1",  "1-2",  "0-2"],  # ✓✗✗✓✗✗✓✓
    "Emma":     ["3-0",  "1-0",  "1-0",  "0-1",  "2-0",  "0-1",  "0-3",  "1-0"],  # ✓✓✓✗✓✓✓✗
    "Frank":    ["0-1",  "2-1",  "2-0",  "2-0",  "1-1",  "1-0",  "0-1",  "0-1"],  # ✗✓✓✓✗✗✓✓
    "Grace":    ["1-0",  "0-1",  "0-0",  "1-0",  "2-1",  "0-2",  "1-0",  "0-0"],  # ✓✗✗✓✓✓✗✗
    "Henry":    ["0-0",  "1-1",  "1-0",  "0-0",  "0-0",  "1-0",  "0-2",  "0-1"],  # ✗✗✓✗✗✗✓✓
    "Isabella": ["0-1",  "2-0",  "0-1",  "1-1",  "1-0",  "0-1",  "1-1",  "1-0"],  # ✗✓✗✗✓✓✗✗
    "James":    ["2-0",  "0-0",  "0-2",  "2-1",  "0-1",  "1-1",  "2-0",  "0-2"],  # ✓✗✗✓✗✗✗✓
}
NON_TRIGGER_IDX = [24, 30, 36, 37, 38, 39, 40, 41]

# Generic score used for all unplayed match slots
GENERIC = {
    "Alice":    "2-0", "Bob":      "1-0", "Carol":    "2-1",
    "David":    "1-1", "Emma":     "0-1", "Frank":    "1-0",
    "Grace":    "2-1", "Henry":    "0-0", "Isabella": "1-2",
    "James":    "2-0",
}

# Group winner predictions (24 values: 1st+2nd for Groups A-L)
WINNERS = {
    "Alice":    ["Mexico","South Korea","Canada","Switzerland","Brazil","Scotland","United States","Turkey","Germany","Ivory Coast","Netherlands","Sweden","Belgium","Iran","Spain","Uruguay","France","Norway","Argentina","Austria","Portugal","Colombia","England","Croatia"],
    "Bob":      ["Czechia","South Korea","Switzerland","Canada","Brazil","Morocco","United States","Paraguay","Germany","Ecuador","Netherlands","Japan","Belgium","New Zealand","Spain","Uruguay","France","Norway","Argentina","Austria","Portugal","Colombia","England","Croatia"],
    "Carol":    ["Mexico","Czechia","Canada","Qatar","Brazil","Scotland","United States","Australia","Germany","Ivory Coast","Netherlands","Sweden","Belgium","Iran","Spain","Uruguay","France","Senegal","Argentina","Algeria","Portugal","Colombia","England","Croatia"],
    "David":    ["Mexico","South Korea","Canada","Switzerland","Brazil","Haiti","United States","Turkey","Germany","Ivory Coast","Netherlands","Sweden","Belgium","Iran","Spain","Uruguay","France","Norway","Argentina","Austria","Portugal","Colombia","England","Croatia"],
    "Emma":     ["South Korea","Mexico","Switzerland","Canada","Morocco","Scotland","Paraguay","United States","Germany","Ecuador","Netherlands","Japan","Belgium","Iran","Spain","Uruguay","France","Norway","Argentina","Jordan","Portugal","Colombia","England","Croatia"],
    "Frank":    ["Mexico","South Korea","Canada","Switzerland","Brazil","Scotland","United States","Turkey","Germany","Ivory Coast","Netherlands","Sweden","Belgium","Iran","Spain","Uruguay","France","Norway","Argentina","Austria","Portugal","Colombia","England","Croatia"],
    "Grace":    ["Mexico","South Korea","Canada","Switzerland","Brazil","Scotland","United States","Turkey","Germany","Ivory Coast","Netherlands","Sweden","Belgium","New Zealand","Spain","Uruguay","France","Norway","Argentina","Austria","Portugal","Colombia","England","Croatia"],
    "Henry":    ["Mexico","South Korea","Canada","Switzerland","Brazil","Scotland","United States","Turkey","Germany","Ivory Coast","Netherlands","Sweden","Belgium","Iran","Spain","Uruguay","France","Norway","Argentina","Austria","Portugal","Colombia","England","Panama"],
    "Isabella": ["Mexico","South Korea","Canada","Switzerland","Brazil","Scotland","United States","Turkey","Germany","Ivory Coast","Netherlands","Sweden","Belgium","Iran","Spain","Uruguay","France","Norway","Argentina","Austria","Colombia","Portugal","England","Croatia"],
    "James":    ["Mexico","South Korea","Switzerland","Canada","Brazil","Scotland","United States","Turkey","Germany","Ivory Coast","Japan","Netherlands","Belgium","Iran","Spain","Uruguay","France","Norway","Argentina","Austria","Portugal","Colombia","Croatia","England"],
}

# Special predictions
SPECIALS = {
    "Alice":    ["Spain",     "England",  "Harry Kane",        "5"],
    "Bob":      ["Brazil",    "France",   "Kylian Mbappe",     "6"],
    "Carol":    ["Mexico",    "Argentina","Lionel Messi",       "4"],
    "David":    ["Germany",   "Brazil",   "Erling Haaland",    "7"],
    "Emma":     ["France",    "Brazil",   "Kylian Mbappe",     "8"],
    "Frank":    ["Brazil",    "England",  "Neymar",            "5"],
    "Grace":    ["Spain",     "France",   "Pedri",             "4"],
    "Henry":    ["Argentina", "Brazil",   "Lautaro Martinez",  "6"],
    "Isabella": ["Brazil",    "Germany",  "Vinicius Jr",       "5"],
    "James":    ["England",   "Spain",    "Marcus Rashford",   "4"],
}


def make_match_row(first):
    preds = [GENERIC[first]] * 72
    for idx_str, val in BADGE_OVERRIDES[first].items():
        preds[int(idx_str)] = val
    for list_pos, col_idx in enumerate(NON_TRIGGER_IDX):
        preds[col_idx] = NON_TRIGGER_PLAYED[first][list_pos]
    return preds


with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(HEADER)
    for first, last, team, ts in PARTICIPANTS:
        row = (
            [ts, first, last, team]
            + make_match_row(first)
            + WINNERS[first]
            + SPECIALS[first]
        )
        w.writerow(row)

print(f"OK: Wrote {len(PARTICIPANTS)} participants -> {OUTPUT}")
print("Run: python scripts/run_test.py 2026-06-14 scripts/test_results_r3.json")
