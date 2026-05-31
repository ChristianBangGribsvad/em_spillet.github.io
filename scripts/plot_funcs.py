# Import packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import warnings
from datetime import datetime
from pathlib import Path
import os
import random


def plot_group_progress(df_results, group_name, out_path='pages/group_plots/lines_', colors=None):
    """
    colors: optional dict mapping column name → hex color string.
    When supplied each series is drawn in its assigned team color.
    """
    xs = df_results.index.tolist()

    fig, ax = plt.subplots(1, figsize=(12, 6))
    for i in range(len(df_results.columns)):
        col_name = str(df_results.columns[i])
        kw = {'color': colors[col_name]} if (colors and col_name in colors) else {}
        ax.plot(xs, df_results.iloc[:,i]+random.uniform(-0.1,0.1),
                label=col_name, marker='o', markersize=7, **kw)
    ax.grid(linestyle="--")
    ax.set_ylabel('Score')
    ax.set_title('Standings')
    ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0)
    plt.tight_layout()
    plt.savefig(out_path+group_name.replace(" ","_")+'.svg', bbox_inches='tight')
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
        plt.title('Best round ('+str(df_results.index[-2])+' to '+str(df_results.index[-1])+')')
        plt.ylabel('Points')
        plt.bar_label(bars)
        plt.tight_layout()
        plt.savefig('pages/group_plots/bars_'+group_name.replace(" ","_")+'.svg')
        plt.close()




