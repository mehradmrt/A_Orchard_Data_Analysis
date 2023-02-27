#%%#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from BaselineRemoval import BaselineRemoval

# df_swp = pd.read_json('../results/almond_SWP.json')
# df_lt = pd.read_json('../results/almond_leaftemp.json')
# df_im = pd.read_json('../results/almond_im_indexes.json')
# df_sap = pd.read_json('../results/almond_sap_data.json')
# df_weather = pd.read_json('../results/almond_weather_data.json')
# df_arable = pd.read_json('../results/almond_arable.json')
df_visnir = pd.read_json('../results/almond_visnir.json')
# df_ram = pd.read_json('../results/almond_raman.json')
# df_cwsi = pd.read_json('../results/almond_cwsi.json')

tdays = ['T5','T6','T7']
ramdict = {'T5': '07_30_22', 'T6': '08_03_22', 'T7': '08_31_22'}
samdict = ['S1','S2','S3']
treenum = 17

#%%
def plt_nirvis(df):
    for k in range(len(tdays)):
        for i in range(treenum):
            plt.figure()
            plt.title("Test " + str(tdays[k]) + "   Tree " + str(i+1))
            for j in range(len(samdict)):
                test2=(df[df['test_number']==tdays[k]]\
                    [df['tree_id']==i+1][df['sample_number']==samdict[j]])
                yval = (test2['Reflect. %'])
                xval = (test2['Wvl'])           

                plt.plot(xval,yval)
                # plt.xticks([0 ,500 ,1000, 1500, 2000])  

plt_nirvis(df_visnir)
# %%
