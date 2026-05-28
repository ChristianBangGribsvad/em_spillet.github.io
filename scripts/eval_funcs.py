import pandas as pd
import numpy as np

def eval_match_predictions(predictions_df , results):
    # Convert results to a dict (and select only group stage matches)
    results_dict = {results[x][0]:results[x][1] for x in range(len(results)) if "Group" in results[x][0]}
    # Add extra row to save correct result, then a row for points.
    # Cast to object first so mixed str/int/float columns don't raise a FutureWarning.
    predictions_df = predictions_df.astype(object)
    predictions_df.loc[len(predictions_df), predictions_df.columns] = ["-"] * len(predictions_df.columns)
    predictions_df.loc[len(predictions_df), predictions_df.columns] = [0]   * len(predictions_df.columns)

    # Initialize empty points var
    points = 0
    for col_name in [x for x in predictions_df.columns if "Predictions" in x]:
        pred = predictions_df.at[0,col_name]
        res = results_dict.get(col_name, "None - None")

        # If empty prediction or match not yet played, skip
        if pred != pred or "None" in res:
            continue

        # Make sure no white space messes up the eval
        pred = pred.replace(" ","")
        res = res.replace(" ","")

        # Check for nan (to be able to do temporary standings)
        if res != res or pred != pred:
            continue
        else:
            # Save correct results
            predictions_df.at[1,col_name] = res

            home_res,  away_res  = int(res.split("-")[0]),  int(res.split("-")[1])
            home_pred, away_pred = int(pred.split("-")[0]), int(pred.split("-")[1])

            ### 15 points, correct score for both teams
            if pred == res:
                points += 15
                predictions_df.at[2,col_name] = 15

            ### 10 points, correct outcome and score for one team
            # Home team wins and correct score of home team
            elif home_res > away_res and home_pred > away_pred and home_res == home_pred:
                points += 10
                predictions_df.at[2,col_name] = 10
            # Home team wins and correct score of away team
            elif home_res > away_res and home_pred > away_pred and away_res == away_pred:
                points += 10
                predictions_df.at[2,col_name] = 10
            # Away team wins and correct score of home team
            elif home_res < away_res and home_pred < away_pred and home_res == home_pred:
                points += 10
                predictions_df.at[2,col_name] = 10
            # Away team wins and correct score of away team
            elif home_res < away_res and home_pred < away_pred and away_res == away_pred:
                points += 10
                predictions_df.at[2,col_name] = 10

            ### 5 points, correct outcome (winner or tie)
            # Home team wins
            elif home_res > away_res and home_pred > away_pred:
                points += 5
                predictions_df.at[2,col_name] = 5
            # Away team wins
            elif home_res < away_res and home_pred < away_pred:
                points += 5
                predictions_df.at[2,col_name] = 5
            # Tie
            elif home_res == away_res and home_pred == away_pred:
                points += 5
                predictions_df.at[2,col_name] = 5

            ### 2 points, correct score for one team
            # Home team correct score
            elif home_res == home_pred:
                points += 2
                predictions_df.at[2,col_name] = 2
            # Away team correct score
            elif away_res == away_pred:
                points += 2
                predictions_df.at[2,col_name] = 2

    return predictions_df

# Based on results_dict, find group winners
def find_group_winners(results):
    results_dict = {results[x][0]:results[x][1] for x in range(len(results)) if "Group" in results[x][0]}
    all_group_names = np.unique([k[:7] for k,v in results_dict.items()]).tolist()
    all_group_res = {group:{"1st":"","2nd":""} for group in all_group_names}


    for group_name in all_group_names:
        group_results = {k: v for k,v in results_dict.items() if k[:7] == group_name}
        group_home_countries = [k.split("[")[-1].split("]")[0].split(" - ", 1)[0].strip() for k in list(group_results.keys())]
        group_away_countries = [k.split("[")[-1].split("]")[0].split(" - ", 1)[1].strip() for k in list(group_results.keys())]
        group_countries = np.unique(group_home_countries + group_away_countries).tolist()

        group_eval = {country:{"points":0,"goals_for":0,"goals_against":0}  for country in group_countries}

        # Variable to skip calc if None score is present
        skip_group = False
        for k,v in group_results.items():
            home_team = k.split("[")[-1].split("]")[0].split(" - ", 1)[0].strip()
            away_team = k.split("[")[-1].split("]")[0].split(" - ", 1)[1].strip()

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

            #if group_name == all_group_names[-1]:
                #return {"Skip":0}
            #else:
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
                    all_group_res[group_name]["2nd"] = list(equal_teams_match.keys())[0].split("[")[-1].split("]")[0].split(" - ", 1)[0].strip()
                elif home_score < away_score:
                    all_group_res[group_name]["2nd"] = list(equal_teams_match.keys())[0].split("[")[-1].split("]")[0].split(" - ", 1)[1].strip()
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
                all_group_res[group_name]["1st"] = list(equal_teams_match.keys())[0].split("[")[-1].split("]")[0].split(" - ", 1)[0].strip()
                all_group_res[group_name]["2nd"] = list(equal_teams_match.keys())[0].split("[")[-1].split("]")[0].split(" - ", 1)[1].strip()
            elif home_score < away_score:
                all_group_res[group_name]["1st"] = list(equal_teams_match.keys())[0].split("[")[-1].split("]")[0].split(" - ", 1)[1].strip()
                all_group_res[group_name]["2nd"] = list(equal_teams_match.keys())[0].split("[")[-1].split("]")[0].split(" - ", 1)[0].strip()
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

        elif sum(np.array(list(group_stand.values())) == max(list(group_stand.values()))) >= 3:
            # The scenario where 3 or 4 teams have max points - look into goal difference
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

    group_winner_cols = [x for x in predictions_df.columns if "place" in x]
    # Give points
    for i in range(len(group_winner_cols) // 2):
        col_1st = group_winner_cols[i*2]
        col_2nd = group_winner_cols[i*2 + 1]
        # Derive group name from column e.g. "Group A 1st place" → "Group A"
        group_name = " ".join(col_1st.split()[:2])

        # Skip groups with no results yet (e.g. only a subset of groups in test)
        if group_name not in all_group_res:
            continue

        pred1st = predictions_df.at[0, col_1st]
        pred2nd = predictions_df.at[0, col_2nd]
        res1st  = all_group_res[group_name]["1st"]
        res2nd  = all_group_res[group_name]["2nd"]

        # If current group is not finished we skip it
        if res1st == "":
            continue

        predictions_df.at[1, col_1st] = res1st
        predictions_df.at[1, col_2nd] = res2nd

        if res1st == pred1st and res2nd == pred2nd:
            predictions_df.at[2, col_1st] = 7.5
            predictions_df.at[2, col_2nd] = 7.5
        elif res1st == pred2nd and res2nd == pred1st:
            predictions_df.at[2, col_1st] = 5
            predictions_df.at[2, col_2nd] = 5
        elif res1st == pred1st:
            predictions_df.at[2, col_1st] = 5
        elif res2nd == pred2nd:
            predictions_df.at[2, col_2nd] = 5

    return predictions_df

