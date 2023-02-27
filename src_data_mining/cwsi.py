#%%

import pandas as pd
import numpy as np

df_swp = pd.read_json('../results/almond_SWP.json')
df_lt = pd.read_json('../results/almond_leaftemp.json')
df_im = pd.read_json('../results/almond_im_indexes.json')
df_sap = pd.read_json('../results/almond_sap_data.json')
df_weather = pd.read_json('../results/almond_weather_data.json')
df_arable = pd.read_json('../results/almond_arable.json')
df_visnir = pd.read_json('../results/almond_visnir.json')
df_ram = pd.read_json('../results/almond_raman.json')
Dict = {'T1': '2022-06-08', 'T2': '2022-06-23', 'T3': '2022-07-08', 'T4': '2022-07-15', \
            'T5': '2022-07-30', 'T6': '2022-08-03', 'T7': '2022-08-31'}

#%%
###### Temp capture #####

df= df_weather
df['Date and Time'] = pd.to_datetime(df['Date and Time'])
# df3 = df[df['Station ID']=='Weather 3']
# df4 = df[df['Station ID']=='Weather 4']

dfmax = df.groupby([df['Date and Time'].dt.date])['Temperature [℃]'].max()
# df4max = df4.groupby([df4['Date and Time'].dt.date])['Temperature [℃]'].max()
dfmax = dfmax.to_frame()
# df4max = df4max.to_frame()
dfmax.index = dfmax.index.map(str)
# df4max.index = df4max.index.map(str)
# df3max.plot.scatter(x=0, y=3,rot=90)

            
# %%
##### Dates DF Creation CWSI #####
def dfcreate(daynum):
    df = pd.DataFrame([],columns=['Dates'])
    for i in Dict:
        temp = pd.date_range(end=Dict[i], periods=daynum)
        temp = temp.to_frame(index=False, name='Dates')
        df = pd.concat([df,temp],ignore_index=True)
    return df

df_dates = dfcreate(1)
# df_dates['Dates'] = df_dates['Dates'].dt.date
df_dates['Dates'] = df_dates['Dates'].dt.strftime('%Y-%m-%d')

def Tfinder(dfT,dfD):
    for i in dfD['Dates']:
        dfT.loc[i]
        print(i)   
Tfinder(dfmax,df_dates)

#%%
##### CWSI #####
# df_swp['tree_idx']=df_swp['tree_idx'].add(1)
df_cwsi = df_lt[['tree_idx','test_number','leaf_temp','STD']]
df_cwsi.insert(4,'Ta','')
df_cwsi.insert(5,'cwsi','')
for i in Dict:
    print(i)
    print(dfmax.loc[Dict[i]])
    df_cwsi.loc[df_cwsi[df_cwsi['test_number']==i].index,'Ta']= dfmax.loc[Dict[i]]['Temperature [℃]']

for i in df_cwsi.index:
    Tc = df_cwsi.iloc[i][2]
    Ta = df_cwsi.iloc[i][4]
    Tcl = df_cwsi['leaf_temp'].min()
    Tcu = df_cwsi['leaf_temp'].max()
    df_cwsi.loc[i,'cwsi'] = ((Tc-Ta)-(Tcl-Ta))/((Tcu-Ta)-(Tcl-Ta))

df_cwsi.to_json('../results/almond_cwsi.json') 

# %%
