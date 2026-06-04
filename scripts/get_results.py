import requests
import json
import pickle
import os
from datetime import datetime, timezone, timedelta
cwd = os.getcwd()

# Copenhagen is CEST (UTC+2) for the entire WC 2026 (Jun–Jul)
_CEST = timezone(timedelta(hours=2))
_TOURNAMENT_START = datetime(2026, 6, 11, 21, 0, 0, tzinfo=_CEST)
_API_URI     = 'https://api.football-data.org/v4/competitions/WC/matches'
_API_HEADERS = {'X-Auth-Token': '242e02ff31ea497fbe4b85978fe70b81'}


def fetch_raw_matches():
    """
    Single HTTP request for all WC matches.
    Call this once per pipeline run and share the result between
    get_results(), get_upcoming_matches(), and get_recent_results()
    to avoid redundant API calls.
    """
    return requests.get(_API_URI, headers=_API_HEADERS).json()["matches"]


def get_upcoming_matches(raw=None):
    """
    Return upcoming match strings for the next 24-hour window.
    Pass raw=fetch_raw_matches() to reuse an already-fetched response.
    """
    matches = raw if raw is not None else fetch_raw_matches()

    now_cph      = datetime.now(timezone.utc).astimezone(_CEST)
    window_start = _TOURNAMENT_START if now_cph < _TOURNAMENT_START else now_cph
    window_end   = window_start + timedelta(hours=24)

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
            time_str = match_cph.strftime("%a %d %B, %H:%M")
            upcoming.append(f"{home} vs {away} &mdash; {time_str}")

    return upcoming


def get_recent_results(raw=None):
    """
    Return finished matches from the 24-hour window that just closed.
    Pass raw=fetch_raw_matches() to reuse an already-fetched response.
    """
    matches = raw if raw is not None else fetch_raw_matches()

    now_cph      = datetime.now(timezone.utc).astimezone(_CEST)
    anchor       = _TOURNAMENT_START if now_cph < _TOURNAMENT_START else now_cph
    window_end   = anchor
    window_start = window_end - timedelta(hours=24)

    results = []
    for m in matches:
        if m.get("status") != "FINISHED":
            continue
        try:
            match_cph = (datetime
                         .fromisoformat(m["utcDate"].replace("Z", "+00:00"))
                         .astimezone(_CEST))
        except (KeyError, ValueError):
            continue
        if window_start <= match_cph < window_end:
            home       = m["homeTeam"]["name"]
            away       = m["awayTeam"]["name"]
            home_score = m["score"]["fullTime"]["home"]
            away_score = m["score"]["fullTime"]["away"]
            results.append(f"{home} {home_score} - {away_score} {away}")

    return results


def process_match(match):
    hometeam = match["homeTeam"]["name"]
    awayteam = match["awayTeam"]["name"]
    group    = match["group"]
    stage    = match["stage"]

    if stage == "GROUP_STAGE":
        matchid = f"Group {group[-1]} Predictions [{hometeam} - {awayteam}]"
    else:
        matchid = f"{stage} Predictions [{hometeam} - {awayteam}]"

    # Only extract a real score when the match is officially FINISHED.
    # Guards against the API returning 0-0 for TIMED/IN_PLAY matches.
    if match.get("status") == "FINISHED":
        h = match["score"]["fullTime"]["home"]
        a = match["score"]["fullTime"]["away"]
        score = f"{h} - {a}"
    else:
        score = "None - None"

    return matchid, score


def get_results(raw=None):
    """
    Return the full scored results list for all WC matches.
    Pass raw=fetch_raw_matches() to reuse an already-fetched response.
    """
    matches = raw if raw is not None else fetch_raw_matches()
    return [process_match(m) for m in matches]


_MONTHS = ['Jan','Feb','Mar','Apr','May','Jun',
           'Jul','Aug','Sep','Oct','Nov','Dec']
_ORD    = {1:'st',2:'nd',3:'rd'}

def get_match_dates(raw=None):
    """
    Return {match_id: 'Jun 12th · 21:00'} for all matches, in CEST.
    Pass raw=fetch_raw_matches() to reuse an already-fetched response.
    """
    matches = raw if raw is not None else fetch_raw_matches()
    dates = {}
    for m in matches:
        try:
            match_id, _ = process_match(m)
            dt = (datetime
                  .fromisoformat(m["utcDate"].replace("Z", "+00:00"))
                  .astimezone(_CEST))
            day = dt.day
            suf = _ORD.get(day % 10 if day % 100 not in (11,12,13) else 0, 'th')
            dates[match_id] = f'{_MONTHS[dt.month-1]} {day}{suf} · {dt.strftime("%H:%M")}'
        except Exception:
            continue
    return dates


def save_results(filename, a):
    with open(filename, 'wb') as handle:
        pickle.dump(a, handle)

def load_results(filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)

def get_highest_result_number():
    import glob
    files = glob.glob(os.path.join(cwd, "results", "data_*.pickle"))
    if not files:
        return 0
    return max(
        int(os.path.basename(f).replace("data_", "").replace(".pickle", ""))
        for f in files
    )
