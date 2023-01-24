#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics

# df_im = pd.read_json('pistachio_im_indexes.json')

swp_root = 'C:/Users/Students/Box/Research/IoT4ag/Project_ Water Stress/' \
                +'Data Collection/Almond/Ground Data'
df_swp = pd.read_csv(swp_root+'/swp.csv')
df_lt = pd.read_csv(swp_root+'/leaf_temp.csv')
# df_swp.to_json('almond_SWP.json')
# df_lt.to_json('almond_leaftemp.json')

# df_sap = pd.read_json('pistachio_sap_data.json')
# df_weather = pd.read_json('pistachio_weather_data.json')

arable_root = 'C:/Users/Students/Box/Research/IoT4ag'\
    +'/Project_ Water Stress/Data Collection/Almond/Arable_A'
df_arable_T15 = pd.read_csv(arable_root+
'/arable___012564___ 2022_06_23 19_18_17__012564_daily_20220930.csv', skiprows=10)
df_arable_T2 = pd.read_csv(arable_root+
'/arable___lmond2__012373_daily_20220930.csv', skiprows=10)
df_arable_T15.insert(1,"tree_idx",'15')
df_arable_T2.insert(1,"tree_idx",'2')
df_arable_T15.insert(1,"orchard",'Almond')
df_arable_T2.insert(1,"orchard",'Almond')
arable = pd.concat([df_arable_T2, df_arable_T15], ignore_index=True)
arable.to_json('almond_arable.json')

# testnum = 7
# treenum = 18
# indexnum = 5
# testdic = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7']
# idxdic = ['NDVI', 'GNDVI', 'OSAVI', 'LCI' ,'NDRE']
# DOY = [158, 172, 186, 194, 207, 214, 224]

# #%%
# ndvi = df_im.loc[df_im['spec_idx'] == idxdic[0]]['median']
# gndvi = df_im.loc[df_im['spec_idx'] == idxdic[1]]['median']
# osavi = df_im.loc[df_im['spec_idx'] == idxdic[2]]['median']
# lci = df_im.loc[df_im['spec_idx'] == idxdic[3]]['median']
# ndre = df_im.loc[df_im['spec_idx'] == idxdic[4]]['median']
# swp_mn = np.array(df_swp['SWP'])
# lt_mn = np.array(df_lt['leaf_temp'])

# dfcsv = {}
# %%
