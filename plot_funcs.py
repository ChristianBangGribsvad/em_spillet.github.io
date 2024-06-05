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
import matplotlib as mpl

def plot_group_progress(df_results,group_name,out_path='pages/group_plots/lines_'):
    xs = df_results.index.tolist()
    
    fig = plt.subplots(1,figsize=(12,6))
    for i in range(len(df_results.columns)):
        plt.plot(xs,df_results.iloc[:,i]+random.uniform(-0.1,0.1),label=str(df_results.columns[i]),marker='o',markersize=7)
    plt.grid(linestyle= "--")
    plt.ylabel('Score')
    if len(df_results.columns) > 10:
        plt.legend(ncol=2)
    else: 
        plt.legend()
    plt.title('Standings')
    plt.tight_layout()
    plt.savefig(out_path+group_name.replace(" ","_")+'.svg')
    plt.close()
    
def plot_best_round(df_results,group_name):
    # Cannot plot improvement if we only have 1 row
    if len(df_results) > 1:
        # Compute best round
        best_round = df_results.iloc[-1,:]-df_results.iloc[-2,:]
        best_round = best_round.sort_values()
        y_pos = np.arange(len(best_round)) 
        fig= plt.subplots(1,figsize=(12,6))
        bars = plt.bar(y_pos, best_round.values,color=["dodgerblue"])
        plt.xticks(y_pos,best_round.index.to_list(),rotation=60)
        plt.title('Best round ('+df_results.index[-2]+' to '+df_results.index[-1]+')')
        plt.ylabel('Points')
        plt.bar_label(bars)
        plt.tight_layout()
        plt.savefig('pages/group_plots/bars_'+group_name.replace(" ","_")+'.svg')
        plt.close()
    

def plot_standings(df_results,group_name):
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
        rowColours =["dodgerblue"]*rows,  
        colColours =["dodgerblue"]*cols, 
        cellLoc ='center',  
        loc ='upper left')         
    
    ax.set_title('Standings', 
                fontweight ="bold",
                loc = 'left') 

    for (row, col), cell in table.get_celld().items():
        if (row == 0) or (col == -1):
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    plt.savefig('pages/group_plots/standing_'+group_name.replace(" ","_")+'.svg',bbox_inches="tight")
    plt.close()
    
def plot_user(user_df):
    trans_df = user_df.iloc[:,4:-2].T
    trans_df.columns = ["Predictions", "Results","Points"]
    trans_df = trans_df.reset_index()
    colors = []
    for _, row in trans_df.iterrows():
        colors_in_column = [mpl.colormaps["autumn"](0)]*4
        if row["Results"] == "-":
            colors_in_column = [mpl.colormaps["Greys"](0.3)]*4
        elif row["Points"] == 2:
            colors_in_column = [mpl.colormaps["Greens"](0.2)]*4
        elif row["Points"] == 5:
            colors_in_column = [mpl.colormaps["Greens"](0.4)]*4
        if row["Points"] == 7.5:
            colors_in_column = [mpl.colormaps["Greens"](0.6)]*4
        elif row["Points"] == 10:
            colors_in_column = [mpl.colormaps["Greens"](0.8)]*4
        elif row["Points"] == 15 or row["Points"] == 20:
            colors_in_column = [mpl.colormaps["Greens"](0.99)]*4
        colors.append(colors_in_column)

    fig, ax = plt.subplots()
    ax.axis('off')
    the_table = ax.table(cellText = trans_df.values,colWidths=[0.65,0.15,0.15,0.10] ,colLabels = trans_df.columns, loc='center', cellColours=colors)
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(14)
    the_table.scale(2, 2)
    

    plt.savefig("pages/user_plots/"+user_df.at[0,"f_name"]+".svg",bbox_inches='tight', pad_inches=0)
    plt.close()
    