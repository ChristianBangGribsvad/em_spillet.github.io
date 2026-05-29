import requests
import json
import pickle
import os
from datetime import datetime, timezone, timedelta
cwd = os.getcwd()

# Copenhagen is CEST (UTC+2) for the entire WC 2026 (Jun–Jul)
_CEST = timezone(timedelta(hours=2))
_TOURNAMENT_START = datetime(2026, 6, 11, 21, 0, 0, tzinfo=_CEST)


def get_upcoming_matches():
    """
    Return a list of upcoming match strings for the next 24-hour window.

    Before the tournament opens (Jun 11 2026 21:00 Copenhagen time) the
    window is fixed to the opening day so the first fixtures are always
    shown on the front page. Once the tournament starts the window rolls
    forward with the current time.
    """
    now_cph = datetime.now(timezone.utc).astimezone(_CEST)
    window_start = _TOURNAMENT_START if now_cph < _TOURNAMENT_START else now_cph
    window_end   = window_start + timedelta(hours=24)

    uri     = 'https://api.football-data.org/v4/competitions/WC/matches'
    headers = {'X-Auth-Token': '242e02ff31ea497fbe4b85978fe70b81'}
    matches = requests.get(uri, headers=headers).json()["matches"]

    upcoming = []
    for m in matches:
        try:
            match_cph = (datetime
                         .fromisoformat(m["utcDate"].replace("Z", "+00:00"))
                         .astimezone(_CEST))
        except (KeyError, ValueError):
            continue
        if window_start <= match_cph < window_end:
            home = m["homeTeam"]["name"]
            away = m["awayTeam"]["name"]
            time_str = match_cph.strftime("%a %d %b, %H:%M")
            upcoming.append(f"{home} vs {away} &mdash; {time_str}")

    return upcoming

def process_match(match):
    hometeam = match["homeTeam"]["name"]
    awayteam = match["awayTeam"]["name"]
    homescore = match["score"]["fullTime"]["home"]
    awayscore = match["score"]["fullTime"]["away"]
    group =  match["group"]
    stage = match["stage"]
    score = f"{homescore} - {awayscore}"
    if stage == "GROUP_STAGE":
        letter = group[-1]
        matchid = f"Group {letter} Predictions [{hometeam} - {awayteam}]"
    else:
        matchid = f"{stage} Predictions [{hometeam} - {awayteam}]"
    return matchid,score

def get_results():
    # Specify competition in endpoint, in this case World Cup (WC)
    uri = 'https://api.football-data.org/v4/competitions/WC/matches'
    headers = { 'X-Auth-Token': '242e02ff31ea497fbe4b85978fe70b81' }

    response = requests.get(uri, headers=headers)

    matches  = response.json()["matches"]
    results = []
    for m in matches:
        results.append(process_match(m))
    return results


def save_results(filename,a):
    with open(filename, 'wb') as handle:
        pickle.dump(a, handle)

def load_results(filename):
    with open(filename, 'rb') as handle:
        b = pickle.load(handle)
    return b

# Function that fetches the largest index of downloaded data
def get_highest_result_number():
    n_file = 0
    for i in range(100):
        isf = os.path.isfile(cwd + f"/results/data_{i}.pickle")
        if isf:
            n_file = i
    return n_file
