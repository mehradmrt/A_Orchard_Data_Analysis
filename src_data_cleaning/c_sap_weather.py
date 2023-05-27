#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# df_swp = pd.read_json('../results/almond_SWP.json')
df_lt = pd.read_json('../results/almond_leaftemp.json')
# df_im = pd.read_json('../results/almond_im_indexes.json')
df_sap = pd.read_json('../results/almond_sap_data.json')
df_weather = pd.read_json('../results/almond_weather_data.json')
# df_arable = pd.read_json('../results/almond_arable.json')
# df_visnir = pd.read_json('../results/almond_visnir.json')
# df_ram = pd.read_json('../results/almond_raman.json')
# df_cwsi = pd.read_json('../results/almond_cwsi.json')

Dict = {'T1': '2022-06-08', 'T2': '2022-06-23', 'T3': '2022-07-08', 'T4': '2022-07-15', \
            'T5': '2022-07-30', 'T6': '2022-08-03', 'T7': '2022-08-31'}
sensornum = 6

#%%
def T_pday(df):
    df['Date and Time'] = pd.to_datetime(df['Date and Time'])
    wmax = df.groupby([df['Date and Time'].dt.date])['Temperature [℃]'].max()
    wmin =df.groupby([df['Date and Time'].dt.date])['Temperature [℃]'].min()
    wmean =df.groupby([df['Date and Time'].dt.date])['Temperature [℃]'].mean()
    wsiz =df.groupby([df['Date and Time'].dt.date])['Temperature [℃]'].size()
    df_w_d = pd.DataFrame({ 'Max T[℃]': wmax, 'Mean T[℃]': wmean,'Min T[℃]': wmin,\
                            'Number of data points': wsiz})
    df_w_d=df_w_d.reset_index()
    return df_w_d

def RH_pday(df):
    df['Date and Time'] = pd.to_datetime(df['Date and Time'])
    wmax = df.groupby([df['Date and Time'].dt.date])['Humidity [RH%]'].max()
    wmin =df.groupby([df['Date and Time'].dt.date])['Humidity [RH%]'].min()
    wmean =df.groupby([df['Date and Time'].dt.date])['Humidity [RH%]'].mean()
    wsiz =df.groupby([df['Date and Time'].dt.date])['Humidity [RH%]'].size()
    df_w_d = pd.DataFrame({ 'Max RH%': wmax, 'Mean RH%': wmean,'Min RH%': wmin,\
                            'Number of data points': wsiz})
    df_w_d=df_w_d.reset_index()
    return df_w_d

def P_pday(df):
    df['Date and Time'] = pd.to_datetime(df['Date and Time'])
    wmax = df.groupby([df['Date and Time'].dt.date])['Pressure [hPa]'].max()
    wmin =df.groupby([df['Date and Time'].dt.date])['Pressure [hPa]'].min()
    wmean =df.groupby([df['Date and Time'].dt.date])['Pressure [hPa]'].mean()
    wsiz =df.groupby([df['Date and Time'].dt.date])['Pressure [hPa]'].size()
    df_w_d = pd.DataFrame({ 'Max P[hPa]': wmax, 'Mean P[hPa]': wmean,'Min P[hPa]': wmin,\
                            'Number of data points': wsiz})
    df_w_d = df_w_d.reset_index()      
    return df_w_d

def sap_pday(df):
    df_sap_all = pd.DataFrame()
    for i in range(sensornum):
        dfn = df[df['Sensor ID']== 'TREW '+str(i+1)]
        dfn['Date and Time'] = pd.to_datetime(dfn['Date and Time'])
        val = dfn.groupby([dfn['Date and Time'].dt.date])['Value 1'].max()
        leng = dfn.groupby([dfn['Date and Time'].dt.date])['Value 1'].size()
        df_sap_d = pd.DataFrame({ 'Sap': val, 'Number of data points': leng})
        df_sap_d.insert(0, 'Sensor ID', 'TREW '+str(i+1))

        df_sap_all = pd.concat([df_sap_all, df_sap_d])
    df_sap_all = df_sap_all.reset_index()  

    return df_sap_all

def sap_len(df_,df_d):
    for i in range(sensornum):
        x1 = df_[df_['Sensor ID']== 'TREW '+str(i+1)]
        x2 = df_d[df_d['Sensor ID']== 'TREW '+str(i+1)]
        print({'Number of all datapoints in TREW '+str(i+1):len(x1),\
            'Number of datapoints per date in TREW '+str(i+1):len(x2)})
    print('There was a total of 158 days from 03/30/22 to 09/04/22')

df_T_pd = T_pday(df_weather)
df_RH_pd = RH_pday(df_weather)
df_P_pd = P_pday(df_weather)
df_sap_d = sap_pday(df_sap)
sap_len(df_sap,df_sap_d)


#%%
###### plot Sap and Temp
def plt_sap_T(df_sap_d,df_T_pd):
    for i in range(sensornum):
        
        fig, ax = plt.subplots()
        ax2 = ax.twinx()
        df_sap_d[df_sap_d['Sensor ID']=='TREW '+str(i+1)].plot.area(x=0, y=2,rot=90, ax=ax)
        df_T_pd.plot.area(x=0, y=1, ax=ax2,colormap="Pastel1")
        ax.legend(loc='upper left')
        ax2.legend(loc='lower right')
        print("Sap Sensor " + str(i+1))
        plt.show()


plt_sap_T(df_sap_d,df_T_pd)

#%%
###### Branch size effect ######
def branchsize(df):
    val = np.array([])
    for i in range(sensornum):
        val = np.append(val,df[df['Sensor ID']=='TREW '+str(i+1)]['Sap'].mean())

    means = val
    almond_bsize1 = [.239,.194,.244,.294,.239,.239]
    almond_bsize2 = [.947,.817,1.546,0.668,.548,.563]
    means_adj1 = means/almond_bsize1
    means_adj2 = means_adj1*almond_bsize2

    print(means/np.max(means))
    print(means_adj1/np.max(means_adj1))
    print(means_adj2/np.max(means_adj2))

# branchsize(df_sap_d)    


#%%
def lowpointchk(dfmain):
    df = dfmain[dfmain["Sensor ID"]=='TREW 2']
    df['Date and Time'] = pd.to_datetime(df['Date and Time'])
    df['Date and Time'] = df['Date and Time'].dt.date
    mask = "2022-06-04"
    mask2 = "2022-08-06"
    df2 = df[df["Date and Time"].isin(pd.date_range(mask,mask2))]
    
    # print(dfmain.loc[df2.index])

lowpointchk(df_sap)
#%%
###### Get test days T, RH, P #########
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
df_dates['Dates'] = df_dates['Dates'].dt.strftime('%Y-%m-%d')


df_TRHP = df_lt[['tree_idx','test_number']]
cols_to_insert = ['Tmin', 'Tmean','Tmax','Pmin', 'Pmean','Pmax','RHmin', 'RHmean','RHmax']
for i, col in enumerate(cols_to_insert, start=2):
    df_TRHP.insert(i, col, '')

def val_pday(mydf,arg1,arg2):
    for i in Dict:
        mydf['Date and Time'] = mydf['Date and Time'].map(str)
        print(i)
        print( mydf[mydf['Date and Time']==Dict[i]][arg2])
        df_TRHP.loc[df_TRHP[df_TRHP['test_number']==i].index,arg1]= mydf[mydf['Date and Time']==Dict[i]][arg2].values[0]

val_pday(df_T_pd,'Tmin','Min T[℃]')
val_pday(df_T_pd,'Tmean','Mean T[℃]')
val_pday(df_T_pd,'Tmax','Max T[℃]')

val_pday(df_P_pd,'Pmin','Min P[hPa]')
val_pday(df_P_pd,'Pmean','Mean P[hPa]')
val_pday(df_P_pd,'Pmax','Max P[hPa]')

val_pday(df_RH_pd,'RHmin','Min RH%')
val_pday(df_RH_pd,'RHmean','Mean RH%')
val_pday(df_RH_pd,'RHmax','Max RH%')

df_TRHP.to_json('../results/almond_TRHP.json') 

# %%
# df_TRHP.to_json('../results/almond_TRHP.json') 
# %%
