import pandas as pd
from get_results import *
import pickle
from datetime import date
import os
cwd = os.getcwd()

if __name__ == "__main__":
    results = get_results()
    date = date.today()
    datafile = [results,date]
    n_file = get_highest_result_number()
    
    prev_results = load_results(cwd + f"/results/data_{n_file}.pickle")
    if prev_results[0] != results:
        print("New results saved")
        save_results(cwd + f"/results/data_{n_file+1}.pickle",datafile)
    
    
    
    predictions = pd.read_csv("EM spillet 2024.csv")
    
    
    
    
    #predictions[results[0][0]]
        
    
    #response1= requests.get(uri, headers=headers)
    #for match in response.json()['matches']:
    #    print(match)
      
    #filename = "countries.txt"
    #save_countries_to_file(countries, filename)
    #print(f"Countries saved to {filename}")

#curl -XGET 'https://api.football-data.org/v4/competitions/PL' -H "X-Auth-Token: 242e02ff31ea497fbe4b85978fe70b81"