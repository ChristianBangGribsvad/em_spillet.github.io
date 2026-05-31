# Import packages
import numpy as np
import matplotlib.pyplot as plt
import random



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




