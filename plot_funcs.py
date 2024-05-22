# Import packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import warnings
from datetime import datetime
from pathlib import Path
import os
from matplotlib.font_manager import FontProperties
import random

def plot(df_results,group_name):
    xs = df_results.index.tolist()
    scores = df_results.index.tolist()
    
    fig= plt.subplots(1,figsize=(12,6))

    for i in range(len(df_results.columns)):
        plt.plot(xs,df_results.iloc[:,i]+random.uniform(-0.1,0.1),label=str(df_results.columns[i]),marker='o',markersize=7)
    plt.grid()
    plt.ylabel('Score')
    if len(df_results.columns) > 10:
        plt.legend(ncol=2)
    else: 
        plt.legend()
    plt.title('Standings')
    plt.tight_layout()
    plt.savefig('pages/lines'+group_name+'.png')
    
    # Cannot plot improvement if we only have 1 row
    if len(df_results) > 1:
        # Compute best round
        best_round = df_results.iloc[-1,:]-df_results.iloc[-2,:]
        best_round = best_round.sort_values()
        y_pos = np.arange(len(best_round)) 
        fig= plt.subplots(1,figsize=(12,6))
        bars = plt.bar(y_pos, best_round.values,color=["firebrick"])
        plt.xticks(y_pos,best_round.index.to_list(),rotation=60)
        plt.title('Best round ('+df_results.index[-2]+' to '+df_results.index[-1]+')')
        plt.ylabel('Points')
        plt.bar_label(bars)
        plt.tight_layout()
        plt.savefig('pages/bars_'+group_name+'.png')

    sort_standing_names = df_results.iloc[-1,:].sort_values(ascending=False).index
    sort_standing_value = df_results.iloc[-1,:].sort_values(ascending=False)

    cols = 1
    rows = len(sort_standing_names)
    val1 = ["Points"] 
    val2 = [sort_standing_names[i].format(rows) for i in range(rows)] 
    val3 = [[str(sort_standing_value[r])] for r in range(rows)]
    
    fig, ax = plt.subplots(1,figsize=(2,1)) 
    ax.set_axis_off() 
    table = ax.table( 
        cellText = val3,  
        rowLabels = val2,  
        colLabels = val1, 
        rowColours =["firebrick"]*rows,  
        colColours =["firebrick"]*cols, 
        cellLoc ='center',  
        loc ='upper left')         
    
    ax.set_title('Standings', 
                fontweight ="bold",
                loc = 'left') 

    for (row, col), cell in table.get_celld().items():
        if (row == 0) or (col == -1):
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    plt.tight_layout()
    plt.savefig('pages/standing_'+group_name+'.png',bbox_inches="tight")