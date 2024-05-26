import pandas as pd
from get_results import *
from eval_funcs import *
from plot_funcs import *
import pickle
from datetime import date
import os
cwd = os.getcwd()
import pdb

if __name__ == "__main__":
    #### Fill out when final is finished
    topscorer = ""
    topscorer_goals = ""
    finale_loser = ""
    finale_winner = ""
    testing = True
    
    results = get_results()
    
    if not testing:
        results = get_results()
        date = date.today()
        datafile = [results,date]
        n_file = get_highest_result_number()
        
        prev_results = load_results(cwd + f"/results/data_{n_file}.pickle")
        if prev_results[0] != results:
            print("New results saved")
            save_results(cwd + f"/results/data_{n_file+1}.pickle",datafile)
    
    predictions_df = pd.read_csv("EM spillet 2024.csv")
    
    # Simulate days are going by and results are coming in
    
    for day in range(12):
        date = "June "+str(day+1)
    
        for i in range(3):
            list_var = list( results[day*3:day*3+3][i])
            list_var[1] = str(random.randint(0,4))+" - "+str(random.randint(0,4))
            results[day*3 + i] = tuple(list_var)
        
        for user in predictions_df["Your Name"]:
            user_df = predictions_df[predictions_df["Your Name"] == user]
                 
            # Calc totalt score as of today 
            points = 0
            points_match , user_df = eval_match_predictions(user_df , results)
            points += points_match
            
            # Only eval when group stage is finished (so intermediate standings not are counted)
            results_dict = {results[x][0]:results[x][1] for x in range(len(results)) if "Group" in results[x][0]}
            if len([k for k,v in results_dict.items() if "None" in v[1]]) == 0:
                points += eval_groups(user_df , results)

            # Only eval when group stage is finished (ie round of 16 matches are in results)
            if len({results[x][0]:results[x][1] for x in range(len(results)) if "LAST_16" not in results[x][0]}) > 1:
                # Add also DK knock out stage 
                points += dk_finish(results, user_df)
            
            # Eval when DK is out
            # Add DK goals
            #points += dk_goals_scored(results, user_df)
            
            # Add Top scorer
            #if topscorer == user_df.iloc[0,53]:
                #points += 20
            
            # Add Topscorer goals
            #if topscorer_goals == user_df.iloc[0,54]:
                #points += 10
            
            # Add finale winner team
            #if finale_winner == predictions_df[predictions_df["Your Name"] == "Test"].iloc[0,51]:
                #points += 25
            
            # Add finale loser team
            #if finale_loser == predictions_df[predictions_df["Your Name"] == "Test"].iloc[0,52]:
                #points += 15

            # Save in user_dfs
            user_df.to_pickle("data/user_dfs/"+user)
            
            # Load data frame containing group results
            for group in user_df.iloc[0,2].split(";"):
                if group not in os.listdir("data/group_dfs"):
                    # Create an empty df
                    df_results = pd.DataFrame()
                else:
                    df_results = pd.read_pickle("data/group_dfs/"+group) 
                
                # Upload dataframe with new results
                df_results.loc[date,user] = points
                df_results.to_pickle("data/group_dfs/"+group)
    
    pdb.set_trace()
       
    # Save plots in "pages/" and save names with _ (use replace func)
    for group in os.listdir("data/group_dfs"):
        df_results = pd.read_pickle("data/group_dfs"+user) 
        plot(df_results,group)
    
    #predictions[results[0][0]]
        
    
    #response1= requests.get(uri, headers=headers)
    #for match in response.json()['matches']:
    #    print(match)
      
    #filename = "countries.txt"
    #save_countries_to_file(countries, filename)
    #print(f"Countries saved to {filename}")

#curl -XGET 'https://api.football-data.org/v4/competitions/PL' -H "X-Auth-Token: 242e02ff31ea497fbe4b85978fe70b81"