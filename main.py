import pandas as pd
from get_results import *
from eval_funcs import *
from plot_funcs import *
from insert_pages import *
from create_pages import *
import pickle
from datetime import date
import os
cwd = os.getcwd()
import pdb
import matplotlib.pyplot as plt

if __name__ == "__main__":
    #### Fill out when final is finished
    topscorer = ""
    topscorer_goals = ""
    finale_loser = ""
    finale_winner = ""
    testing = True
    
    results = get_results()
    
    with open('test_results.pkl', 'rb') as f:
        test_results = pickle.load(f)
    
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
    df_fname = pd.DataFrame({'f_name': [f"{row['First name']}"+"_"+f"{str(row['Last name'])[0:2]}" for _, row in predictions_df.iterrows()]})
    df_dname = pd.DataFrame({'d_name': [f"{row['First name']}"+" "+f"{str(row['Last name'])[0:2]}" for _, row in predictions_df.iterrows()]})
    predictions_df =predictions_df.join(df_fname)
    predictions_df =predictions_df.join(df_dname)
    
    # Simulate days are going by and results are coming in
    
    for day in range(13):
        date = "June "+str(day+1)
        if day < 12:
            n_matches = 4
        else:
            n_matches = 3
    
        for i in range(n_matches):
            results[day*4 + i] = test_results[day*4 + i]
        
        max_val = 0
        todays_schmeichel = {"ko":{"value":max_val,"group":"Friends and Family","fname":""}}
        
        for user in predictions_df["d_name"]:
            user_df = predictions_df[predictions_df["d_name"] == user]
            user_df = user_df.reset_index(drop=True)    
            
            # Calc totalt score as of today 
            user_df = eval_match_predictions(user_df , results)
  
            # Add group stage winners points
            user_df = eval_groups(user_df , results)

            # Add DK finishing-stage points
            user_df , dk_end = dk_finish(results, user_df)
            
            # Add DK goals
            if len(dk_end) > 0:
                print("DENMARK is out at",dk_end," at day",day)
                # Only when DK is out
                user_df = dk_goals_scored(results, user_df)
            
            # Add Top scorer
            if topscorer == user_df.iloc[0,53]:
                user_df.iloc[2,53] = 20
                user_df.iloc[1,53] = topscorer
            
            # Add Topscorer goals
            if topscorer_goals == user_df.iloc[0,54]:
                user_df.iloc[2,54] = 10
                user_df.iloc[1,54] = topscorer_goals
            
            # Add finale winner team
            if finale_winner == user_df.iloc[0,51]:
                user_df.iloc[2,51] = 25
                user_df.iloc[1,51] = finale_winner
            
            # Add finale loser team
            if finale_loser == user_df.iloc[0,52]:
                user_df.iloc[2,52] = 15
                user_df.iloc[1,52] = finale_loser
            
            # Save in user_dfs
            user_df.to_pickle("data/user_dfs/"+user)
            
            # Load data frame containing group results
            
            for group in user_df.at[0,"Which team(s) do you belong to?"].split(";"):
                if group not in os.listdir("data/group_dfs"):
                    # Create an empty df
                    df_results = pd.DataFrame()
                else:
                    df_results = pd.read_pickle("data/group_dfs/"+group) 
                
                # Plot user df
                plot_user(user_df)
                
                # Upload dataframe with new results
                df_results.loc[date,user] = user_df.loc[2].sum()
                df_results.to_pickle("data/group_dfs/"+group)
                
                # Todays Schmeichel (be careful not to count people in multiple groups twice)
                if df_results.shape[0] > 1:
                    user_val = df_results.loc[date,user] - df_results.at[df_results.index[df_results.shape[0]-2],user]
                else:
                    user_val = user_df.loc[2].sum()
                
                if user_val > max_val:
                    todays_schmeichel = {user_df.at[0,"d_name"]:{"value":user_val,"group":user_df.at[0,"Which team(s) do you belong to?"].replace(";"," and "),"fname":user_df.at[0,"f_name"]}}
                    max_val = user_val
                elif user_val == max_val:
                    todays_schmeichel[user_df.at[0,"d_name"]] = {"value":user_val,"group":user_df.at[0,"Which team(s) do you belong to?"].replace(";"," and "),"fname":user_df.at[0,"f_name"]}
            
            
            # Check if anythin goes wrong in points addition (ie there is an error if you have less point today than you had yesterday)
            if len(df_results) > 1:
                if df_results.iloc[-1,0] < df_results.iloc[-2,0]:
                    print("ERROR- something went wrong in adding points")
                    
        print(date,todays_schmeichel)
    
    # Save plots in "pages/" and save names with _ (use replace func)
    for group in os.listdir("data/group_dfs"):
        df_results = pd.read_pickle("data/group_dfs/"+group)
        plot_group_progress(df_results,group) 
        plot_best_round(df_results,group)
        plot_standings(df_results,group)
    
    create_pages(predictions_df)
    update_pages(predictions_df,todays_schmeichel)    


    #predictions[results[0][0]]
        
    
    #response1= requests.get(uri, headers=headers)
    #for match in response.json()['matches']:
    #    print(match)
      
    #filename = "countries.txt"
    #save_countries_to_file(countries, filename)
    #print(f"Countries saved to {filename}")

#curl -XGET 'https://api.football-data.org/v4/competitions/PL' -H "X-Auth-Token: 242e02ff31ea497fbe4b85978fe70b81"