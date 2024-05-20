import pandas as pd
from get_results import *
from eval_funcs import *
import pickle
from datetime import date
import os
cwd = os.getcwd()
import pdb

if __name__ == "__main__":
    results = get_results()
    date = date.today()
    datafile = [results,date]
    n_file = get_highest_result_number()
    
    prev_results = load_results(cwd + f"/results/data_{n_file}.pickle")
    if prev_results[0] != results:
        print("New results saved")
        save_results(cwd + f"/results/data_{n_file+1}.pickle",datafile)
    
    # Load predictions
    predictions_df = pd.read_csv("EM spillet 2024.csv")
    
    # Calc totalt score as of today 
    points = 0
    points += eval_match_predictions(predictions_df , results)
    points += eval_groups(predictions_df , results)
    
    # Add also DK knock out stage (auto)
    
    # Add DK goals (auto)
    
    # Add Top scorer (api?)
    
    # Add Topscorer goals (api?)
    
    # Add Final teams (auto)
    
    # Save results in a df with todays date
    
    
    #predictions[results[0][0]]
        
    
    #response1= requests.get(uri, headers=headers)
    #for match in response.json()['matches']:
    #    print(match)
      
    #filename = "countries.txt"
    #save_countries_to_file(countries, filename)
    #print(f"Countries saved to {filename}")

#curl -XGET 'https://api.football-data.org/v4/competitions/PL' -H "X-Auth-Token: 242e02ff31ea497fbe4b85978fe70b81"