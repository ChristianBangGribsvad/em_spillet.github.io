import requests
import json
import pickle
import os
cwd = os.getcwd()

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
    uri = 'https://api.football-data.org/v4/competitions/EC/matches'
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