import pandas as pd
from get_results import *
import pickle
from datetime import date
import os
cwd = os.getcwd()
import pdb
import numpy as np
import random

def eval_match_predictions(predictions_df , results):
    # Convert results to a dict (and select only group stage matches)
    results_dict = {results[x][0]:results[x][1] for x in range(len(results)) if "Group" in results[x][0]}
    # Select the group stage matches in predictions
    predictions = predictions_df.iloc[:,3:39]
    
    # Initialize empty points var
    points = 0
    for i in range(len(predictions.columns)):
        pred = predictions.iloc[0,i]
        res = results_dict[predictions.columns[i]]

        # If empty prediction we skip
        if pred != pred or "None" in res:
            continue
        
        # Make sure no white space messes up the eval        
        pred = pred.replace(" ","")
        res = res.replace(" ","")
                
        # Check for nan (to be able to do temporary standings)
        if res != res or pred != pred:
            continue
        else:
            ### 15 points, correct score for both teams
            if pred == res:
                points += 15
        
            ### 10 points, correct outcome and score for one team
            # Home team wins and correct score of home team    
            elif res[0]>res[2] and pred[0]>pred[2] and res[0] == pred[0]:
                points += 10
            # Home team wins and correct score of away team  
            elif res[0]>res[2] and pred[0]>pred[2] and res[2] == pred[2]:
                points += 10
            # Away team wins and correct score of home team  
            elif res[0]<res[2] and pred[0]<pred[2] and res[0] == pred[0]:
                points += 10
            # Away team wins and correct score of away team  
            elif res[0]<res[2] and pred[0]<pred[2] and res[2] == pred[2]:
                points += 10
            
            ### 5 points, correct outcome (winner or tie)
            # Home team wins
            elif res[0]>res[2] and pred[0]>pred[2]:
                points += 5
            # Away team wins
            elif res[0]<res[2] and pred[0]<pred[2]:
                points += 5
            # Tie
            elif res[0]==res[2] and pred[0]==pred[2]:
                points += 5   
                
            ### 2 points, correct score for one team
            # Home team correct score
            elif res[0]==pred[0]:
                points += 2
            # Away team correct score
            elif res[2]==pred[2]:
                points += 2
                
    return points

# Based on results_dict, find group winners
def find_group_winners(results):
    results_dict = {results[x][0]:results[x][1] for x in range(len(results)) if "Group" in results[x][0]}
    all_group_names = np.unique([k[:7] for k,v in results_dict.items()]).tolist()
    all_group_res = {group:{"1st":"","2nd":""} for group in all_group_names}


    for group_name in all_group_names:
        group_results = {k: v for k,v in results_dict.items() if k[:7] == group_name}
        group_home_countries = [k.split("[")[-1].split("]")[0].split("-")[0].strip() for k in list(group_results.keys())]
        group_away_countries = [k.split("[")[-1].split("]")[0].split("-")[1].strip() for k in list(group_results.keys())]
        group_countries = np.unique(group_home_countries + group_away_countries).tolist()
        
        group_eval = {country:{"points":0,"goals_for":0,"goals_against":0}  for country in group_countries}
        
        # Variable to skip calc if None score is present
        skip_group = False
        for k,v in group_results.items():
            home_team = k.split("[")[-1].split("]")[0].split("-")[0].strip()
            away_team = k.split("[")[-1].split("]")[0].split("-")[1].strip()    
            
            home_score = v.split("-")[0].strip()
            away_score = v.split("-")[1].strip()
            
            if home_score == "None" or away_score == "None":
                print("No results for",home_team,"-",away_team)
                skip_group = True
                break
            else:
                group_eval[home_team]["goals_for"] += int(home_score)
                group_eval[home_team]["goals_against"] += int(away_score)
                
                group_eval[away_team]["goals_for"] += int(away_score)
                group_eval[away_team]["goals_against"] += int(home_score)
                
                if int(home_score) > int(away_score):
                    group_eval[home_team]["points"] += 3
                elif int(home_score) < int(away_score):
                    group_eval[away_team]["points"] += 3
                elif int(home_score) == int(away_score):
                    group_eval[away_team]["points"] += 1
                    group_eval[home_team]["points"] += 1
        
        if skip_group:
            # If None value is present in current group we skip current group and go to next group
            print("Skipping",group_name," due to None values")
            
            if group_name == all_group_names[-1]:
                return {"Skip":0}
            else:
                continue                           
        ### Find 1st and 2nd place in group
        
        # Sort group after points
        group_stand = {k:v["points"] for k,v in group_eval.items()}
        group_stand = dict(sorted(group_stand.items(), key=lambda item: item[1], reverse = True))
        
        if sum(np.array(list(group_stand.values())) == max(list(group_stand.values()))) == 1:
            # The scenario where only 1 team has max points
            all_group_res[group_name]["1st"] = list(group_stand.keys())[0]
            # Remove 1st team
            del group_stand[list(group_stand.keys())[0]]
            
            # Find 2nd best team
            if sum(np.array(list(group_stand.values())) == max(list(group_stand.values()))) == 1:
                # The scenario where only 1 team has 2nd most points
                all_group_res[group_name]["2nd"] = list(group_stand.keys())[0]
            elif sum(np.array(list(group_stand.values())) == max(list(group_stand.values()))) == 2:
                # The scenario where 2 teams have 2nd most points - look into match results
                equal_teams = np.array(list(group_stand.keys()))[np.array(list(group_stand.values())) == max(list(group_stand.values()))].tolist()
                equal_teams_match = {k:v for k,v in group_results.items() if equal_teams[0] in k and equal_teams[1] in k}
                
                home_score = int(list(equal_teams_match.values())[0].split("-")[0])
                away_score = int(list(equal_teams_match.values())[0].split("-")[1])
                
                if home_score > away_score:
                    all_group_res[group_name]["2nd"] = list(equal_teams_match.keys())[0].split("[")[-1].split("]")[0].split("-")[0].strip()
                elif home_score < away_score:
                    all_group_res[group_name]["2nd"] = list(equal_teams_match.keys())[0].split("[")[-1].split("]")[0].split("-")[1].strip()
                elif home_score == away_score:
                    # The scenario where the 2 teams drew against each other - Look into goal difference
                    equal_points = {team:group_eval[team]["goals_for"]-group_eval[team]["goals_against"] for team in equal_teams}
                    equal_points = dict(sorted(equal_points.items(), key=lambda item: item[1], reverse = True))
                    
                    if equal_points[equal_teams[0]] > equal_points[equal_teams[1]]:
                        all_group_res[group_name]["2nd"] = equal_teams[0]
                    elif equal_points[equal_teams[0]] < equal_points[equal_teams[1]]:
                        all_group_res[group_name]["2nd"] = equal_teams[1]  
                    elif equal_points[equal_teams[0]] == equal_points[equal_teams[1]]:
                        # The scenario where the 2 teams also have the same goal difference - look into goals scored
                        equal_goals = {team:group_eval[team]["goals_for"] for team in equal_teams}
                        equal_goals = dict(sorted(equal_goals.items(), key=lambda item: item[1], reverse = True))
                        
                        if equal_goals[equal_teams[0]] > equal_goals[equal_teams[1]]:
                            all_group_res[group_name]["2nd"] = equal_teams[0]
                        elif equal_goals[equal_teams[0]] < equal_goals[equal_teams[1]]:
                            all_group_res[group_name]["2nd"] = equal_teams[1]
                        elif equal_goals[equal_teams[0]] == equal_goals[equal_teams[1]]:
                            print("Its a coin toss - manual assign:",equal_teams[0],"-",equal_teams[1]) 
                            all_group_res[group_name]["2nd"] = "---"  
                
            elif sum(np.array(list(group_stand.values())) == max(list(group_stand.values()))) == 3:
                # The scenario where 3 teams have 2nd most points - look into goal difference
                equal_teams = np.array(list(group_stand.keys()))[np.array(list(group_stand.values())) == max(list(group_stand.values()))].tolist()
                equal_points = {team:group_eval[team]["goals_for"]-group_eval[team]["goals_against"] for team in equal_teams}
                equal_points = dict(sorted(equal_points.items(), key=lambda item: item[1], reverse = True))
                
                if sum(np.array(list(equal_points.values())) == max(list(equal_points.values()))) == 1:
                    # The scenario where 1 of 3 teams have the best goal difference
                    all_group_res[group_name]["2nd"] =  list(equal_points.keys())[0]
                elif sum(np.array(list(equal_points.values())) == max(list(equal_points.values()))) == 2:
                    # The scenario where 2 of 3 teams have the best goal difference - look into goals scored
                    equal_teams = np.array(list(equal_points.keys()))[np.array(list(equal_points.values())) == max(list(equal_points.values()))].tolist()
                    equal_goals = {team:group_eval[team]["goals_for"]for team in equal_teams}
                    equal_goals = dict(sorted(equal_goals.items(), key=lambda item: item[1], reverse = True))
                    
                    if equal_goals[equal_teams[0]] > equal_goals[equal_teams[1]]:
                        all_group_res[group_name]["2nd"] = equal_teams[0]
                    elif equal_goals[equal_teams[0]] < equal_goals[equal_teams[1]]:
                        all_group_res[group_name]["2nd"] = equal_teams[1]
                    elif equal_goals[equal_teams[0]] == equal_goals[equal_teams[1]]:
                        print("Its a coin toss - manual assign:",equal_teams[0],"-",equal_teams[1]) 
                        all_group_res[group_name]["2nd"] = "---"
                        
                elif sum(np.array(list(equal_points.values())) == max(list(equal_points.values()))) == 3:
                    # The scenario where all 3 teams have the same goal difference - look into goals scored
                    equal_goals = {team:group_eval[team]["goals_for"] for team in equal_teams}
                    equal_goals = dict(sorted(equal_goals.items(), key=lambda item: item[1], reverse = True))
                    
                    if sum(np.array(list(equal_goals.values())) == max(list(equal_goals.values()))) == 1:
                        all_group_res[group_name]["2nd"] =  list(equal_goals.keys())[0]
                    else:
                        print("Its a coin toss - manual assign:",equal_teams[0],",",equal_teams[1],",",equal_teams[2]) 
                        all_group_res[group_name]["2nd"] = "---"
                    
                    
        elif sum(np.array(list(group_stand.values())) == max(list(group_stand.values()))) == 2:
            # The scenario where 2 teams have max points - look into match results
            equal_teams = np.array(list(group_stand.keys()))[np.array(list(group_stand.values())) == max(list(group_stand.values()))].tolist()
            equal_teams_match = {k:v for k,v in group_results.items() if equal_teams[0] in k and equal_teams[1] in k}
            
            home_score = int(list(equal_teams_match.values())[0].split("-")[0])
            away_score = int(list(equal_teams_match.values())[0].split("-")[1])
            
            if home_score > away_score:
                all_group_res[group_name]["1st"] = list(equal_teams_match.keys())[0].split("[")[-1].split("]")[0].split("-")[0].strip()
                all_group_res[group_name]["2nd"] = list(equal_teams_match.keys())[0].split("[")[-1].split("]")[0].split("-")[1].strip()
            elif home_score < away_score:
                all_group_res[group_name]["1st"] = list(equal_teams_match.keys())[0].split("[")[-1].split("]")[0].split("-")[1].strip()
                all_group_res[group_name]["2nd"] = list(equal_teams_match.keys())[0].split("[")[-1].split("]")[0].split("-")[0].strip()
            elif home_score == away_score:
                # The scenario where the 2 teams drew against each other - Look into goal difference
                equal_points = {team:group_eval[team]["goals_for"]-group_eval[team]["goals_against"] for team in equal_teams}
                equal_points = dict(sorted(equal_points.items(), key=lambda item: item[1], reverse = True))
                
                if equal_points[equal_teams[0]] > equal_points[equal_teams[1]]:
                    all_group_res[group_name]["1st"] = equal_teams[0]
                    all_group_res[group_name]["2nd"] = equal_teams[1]
                elif equal_points[equal_teams[0]] < equal_points[equal_teams[1]]:
                    all_group_res[group_name]["1st"] = equal_teams[1]
                    all_group_res[group_name]["2nd"] = equal_teams[0]  
                elif equal_points[equal_teams[0]] == equal_points[equal_teams[1]]:
                    # The scenario where the 2 teams also have the same goal difference - look into goals scored
                    equal_goals = {team:group_eval[team]["goals_for"] for team in equal_teams}
                    equal_goals = dict(sorted(equal_goals.items(), key=lambda item: item[1], reverse = True))
                    
                    if equal_goals[equal_teams[0]] > equal_goals[equal_teams[1]]:
                        all_group_res[group_name]["1st"] = equal_teams[0]
                        all_group_res[group_name]["2nd"] = equal_teams[1]
                    elif equal_goals[equal_teams[0]] < equal_goals[equal_teams[1]]:
                        all_group_res[group_name]["1st"] = equal_teams[1]
                        all_group_res[group_name]["2nd"] = equal_teams[0]
                    elif equal_goals[equal_teams[0]] == equal_goals[equal_teams[1]]:
                        print("Its a coin toss - manual assign:",equal_teams[0],"-",equal_teams[1]) 
                        all_group_res[group_name]["1st"] = "---"
                        all_group_res[group_name]["2nd"] = "---"
            
        elif sum(np.array(list(group_stand.values())) == max(list(group_stand.values()))) == 3:
            # The scenario where 3 teams have max points - look into goal difference
            equal_teams = np.array(list(group_stand.keys()))[np.array(list(group_stand.values())) == max(list(group_stand.values()))].tolist()
            equal_points = {team:group_eval[team]["goals_for"]-group_eval[team]["goals_against"] for team in equal_teams}
            equal_points = dict(sorted(equal_points.items(), key=lambda item: item[1], reverse = True))
            
            if sum(np.array(list(equal_points.values())) == max(list(equal_points.values()))) == 1:
                # The scenario where 1 team has best goal difference
                all_group_res[group_name]["1st"] = list(equal_points.keys())[0]
                del equal_points[list(equal_points.keys())[0]]
                
                # Find 2nd best goal difference 
                if sum(np.array(list(equal_points.values())) == max(list(equal_points.values()))) == 1:
                    # The scenario where there's 1 team with 2nd best goal difference
                    all_group_res[group_name]["2nd"] = list(equal_points.keys())[0]
                elif sum(np.array(list(equal_points.values())) == max(list(equal_points.values()))) == 2:
                    # The scenario where 2 teams have 2nd best goal difference - look into goals scored
                    equal_teams = [list(equal_points.keys())[0] , list(equal_points.keys())[1] ]
                    equal_goals = {team:group_eval[team]["goals_for"] for team in equal_teams}
                    equal_goals = dict(sorted(equal_goals.items(), key=lambda item: item[1], reverse = True))
                    
                    if equal_goals[equal_teams[0]] > equal_goals[equal_teams[1]]:
                        all_group_res[group_name]["2nd"] = equal_teams[0]
                    elif equal_goals[equal_teams[0]] < equal_goals[equal_teams[1]]:
                        all_group_res[group_name]["2nd"] = equal_teams[1]
                    elif equal_goals[equal_teams[0]] == equal_goals[equal_teams[1]]:
                        print("Its a coin toss - manual assign:",equal_teams[0],"-",equal_teams[1]) 
                        all_group_res[group_name]["2nd"] = "---"
                
            elif sum(np.array(list(equal_points.values())) == max(list(equal_points.values()))) == 2:
                # The scenario where 2 teams have the best goal difference - look into goals scored
                equal_teams = [list(equal_points.keys())[0] , list(equal_points.keys())[1] ]
                
                equal_goals = {team:group_eval[team]["goals_for"] for team in equal_teams}
                equal_goals = dict(sorted(equal_goals.items(), key=lambda item: item[1], reverse = True))
                
                if equal_goals[equal_teams[0]] > equal_goals[equal_teams[1]]:
                    all_group_res[group_name]["1st"] = equal_teams[0]
                    all_group_res[group_name]["2nd"] = equal_teams[1]
                elif equal_goals[equal_teams[0]] < equal_goals[equal_teams[1]]:
                    all_group_res[group_name]["1st"] = equal_teams[1]
                    all_group_res[group_name]["2nd"] = equal_teams[0]
                elif equal_goals[equal_teams[0]] == equal_goals[equal_teams[1]]:
                    print("Its a coin toss - manual assign:",equal_teams[0],"-",equal_teams[1]) 
                    all_group_res[group_name]["1st"] = "---"
                    all_group_res[group_name]["2nd"] = "---"
                
            elif sum(np.array(list(equal_points.values())) == max(list(equal_points.values()))) == 3:
                # The scenario where 3 teams have the best goal difference - look into goals scored
                equal_goals = {team:group_eval[team]["goals_for"] for team in list(equal_points.keys())}
                equal_goals = dict(sorted(equal_goals.items(), key=lambda item: item[1], reverse = True))
                
                if sum(np.array(list(equal_goals.values())) == max(list(equal_goals.values()))) == 1:
                    # The scenario where 1 team has most scored goals
                    all_group_res[group_name]["1st"] = list(equal_goals.keys())[0]
                    del equal_goals[list(equal_goals.keys())[0]]
                    
                    # find 2nd best team
                    if sum(np.array(list(equal_goals.values())) == max(list(equal_goals.values()))) == 1:
                        # The scenario where there's 1 team with 2nd best goal scored
                        all_group_res[group_name]["2nd"] = list(equal_goals.keys())[0]
                    elif sum(np.array(list(equal_goals.values())) == max(list(equal_goals.values()))) == 2:
                        # The scenario where there's 2 teams with 2nd best goals scored - its a coin toss
                        print("Its a coin toss - manual assign:",list(equal_goals.keys())[0],"-",list(equal_goals.keys())[1],"-",list(equal_goals.keys())[2]) 
                        all_group_res[group_name]["1st"] = "---"
                        all_group_res[group_name]["2nd"] = "---"
                                
                elif sum(np.array(list(equal_goals.values())) == max(list(equal_goals.values()))) > 1:
                    # The scenario where 2 or more teams have same points, goal difference and goals scored - coin toss
                    print("Its a coin toss - manual assign:",list(equal_goals.keys())[0],"-",list(equal_goals.keys())[1],"-",list(equal_goals.keys())[2]) 
                    all_group_res[group_name]["1st"] = "---"
                    all_group_res[group_name]["2nd"] = "---"
    return all_group_res

def eval_groups(predictions_df , results):
    # Compute group stage winners based on results
    all_group_res = find_group_winners(results)
    
    # If no groups are finished we skip eval_groups()
    if list(all_group_res.keys())[0] == "Skip":
        print("No groups are finished, we skip eval_groups()")
        return 0
    
    # Select the group winners in predictions
    predictions = predictions_df.iloc[:,39:51]
    
    # Give points
    points = 0
    for i in range(6):
        pred1st = predictions.iloc[0,0 + i*2]
        pred2nd = predictions.iloc[0,1 + i*2]
        
        res1st = all_group_res[list(all_group_res.keys())[i]]["1st"]
        res2nd = all_group_res[list(all_group_res.keys())[i]]["2nd"]
        
        if res1st == pred1st and res2nd == pred2nd:
            points += 15
        elif res1st == pred2nd and res2nd == pred1st:
            points += 10
        elif res1st == pred1st or res2nd == pred2nd:
            points += 5
            
    return points

def dk_finish(results, predictions_df):
    # Eval DK finish
    dk_finish = ""
    df_finish_pred = predictions_df.iloc[0,55] 
    points = 0
    # Select only knockout matches from results
    results_dict = {results[x][0]:results[x][1] for x in range(len(results)) if "Group" not in results[x][0]}

    last16teams = [k for k in results_dict.keys() if "LAST_16" in k]
    quarterteams = [k for k in results_dict.keys() if "QUARTER_FINALS" in k]
    semiteams = [k for k in results_dict.keys() if "SEMI_FINALS" in k]
    finalteams = [k for k in results_dict.keys() if "FINAL" in k]

    if "Denmark" not in last16teams:
        dk_finish = "Group play"
    elif "Denmark" not in quarterteams:
        dk_finish = "Round of 16"
    elif "Denmark" not in semiteams:
        dk_finish = "Quarter final"
    elif "Denmark" not in finalteams:
        dk_finish = "Semi final"
    elif "Denmark" in finalteams:
        dk_finish = "Final"
    else:
        print("HELP, could not find which stage DK finished in")
    
    if len(dk_finish) > 0:
        if dk_finish == df_finish_pred:
            points += 15
            
    return points

def dk_goals_scored(results,predictions_df):
    # Find DK goals
    points = 0
    results_dict = {results[x][0]:results[x][1] for x in range(len(results))}
    dk_matches = {k:v for k,v in results_dict.items() if "Denmark" in k}
    dk_goals = 0
    for k,v in dk_matches.items():
        if "Denmark" in k.split("-")[0]:
            dk_goals += int(v.split("-")[0])
        elif "Denmark" in k.split("-")[1]:
            dk_goals += int(v.split("-")[1])
            
    if predictions_df.iloc[:,-1] == dk_goals:
        points = 20

    return points