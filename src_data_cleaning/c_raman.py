#%%
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
# df_visnir = pd.read_json('../results/almond_visnir.json')
df_ram = pd.read_json('../results/almond_raman.json')
# df_cwsi = pd.read_json('../results/almond_cwsi.json')

tdays = ['T5','T6','T7']
ramdict = {'T5': '07_30_22', 'T6': '08_03_22', 'T7': '08_31_22'}
samdict = ['S1','S2','S3']
treenum = 17


#%%
##### Clean #1 #####
def raman_void(df,ll,hl):
    low_lim = ll #Try 50 and 500
    high_lim = hl
    dfn = df[df['index'] >low_lim]
    dfn = dfn[dfn['index'] < high_lim]
    dfn = dfn.reset_index(drop=True)
    return dfn

df_ram_c1 = raman_void(df_ram,209,2000)
len(df_ram_c1[df_ram_c1['Raman Shift'] == '   '].index)
df_ram.isnull().sum()

#%%
def max_psamp(df):
    for k in range(len(tdays)):
        print('\n\n\nTest Number ',tdays[k],'\n')
        for i in range(treenum):
            print()
            for j in range(len(samdict)):
                test2=(df[df['test_number']==tdays[k]]\
                    [df['tree_id']==i+1][df['sample_number']==samdict[j]])
                test3 = test2['Dark Subtracted #1']
                # test2.plot.scatter(x=7,y=11  )
                print('Max Tree ',i+1,' ', samdict[j],' = ',test3.max())

# max_psamp(df_ram_c1)   
print('Results estimate that for T7 ,  Tree 14, S1 S2 S3 are bad data')

""" To visualize:
test2=(df_ram_c[df_ram_c['test_number']=='T7']\
    [df_ram_c['tree_id']==][df_ram_c['sample_number']=='S'])
test2.plot.scatter(x=7,y=11  ) 
"""

#%%
###### Baseline Removal ######
from BaselineRemoval import BaselineRemoval
def bsl_rmv(df):
    dfn = df
    for k in range(len(tdays)):
        for i in range(treenum):
            # fig, ax = plt.subplots(1,1)
            plt.figure()
            plt.title("Test " + str(tdays[k]) + "   Tree " + str(i+1))
            for j in range(len(samdict)):
                test2=(df[df['test_number']==tdays[k]]\
                    [df['tree_id']==i+1][df['sample_number']==samdict[j]])
                input_array = (test2['Dark Subtracted #1'])
                xval = (test2['Raman Shift'])           
                baseObj=BaselineRemoval(input_array)
                Zhangfit_output=baseObj.ZhangFit()
                plt.plot(xval,Zhangfit_output)
                plt.xticks([0,100,200,300,400 ,500, 688 ,1000, 1500, 2000],rotation=90)   

                idx = dfn[dfn['test_number']==tdays[k]]\
                    [dfn['tree_id']==i+1][dfn['sample_number']==samdict[j]]\
                        ['Dark Subtracted #1'].index
                dfn.loc[idx,'Dark Subtracted #1'] = Zhangfit_output
    return dfn 

df_ram_bl_c =  bsl_rmv(df_ram_c1)

#%%###### Average per day for each tree
def avg_pday(df):
    dfn = pd.DataFrame(columns=['index','test_number','tree_id','Raman Shift','Dark Subtracted #1'])
    dfmaster = pd.DataFrame(columns=['index','test_number','tree_id','Raman Shift','Dark Subtracted #1'])
    for k in range(len(tdays)):
        for i in range(treenum):
            avg = list([])
            for j in range(len(samdict)):
                val=(df[df['test_number']==tdays[k]]\
                    [df['tree_id']==i+1][df['sample_number']==samdict[j]])
                yval = (val['Dark Subtracted #1']).values
                
                avg.append(yval)
            avg = sum(avg)/len(avg)
            xval = (val['Raman Shift']).values
            dfn['index']=val['index'].values
            dfn['Raman Shift']=xval
            dfn['Dark Subtracted #1']=avg
            dfn['test_number']=tdays[k]
            dfn['tree_id']= i+1

            dfmaster = pd.concat([dfmaster,dfn],ignore_index=True)
            # plt.plot(xval,yval)
            
    return dfmaster

df_ram_avg_c = avg_pday(df_ram_bl_c)

#%%
#### Check Values are in between
def chk_val(df,df1):
    for k in range(len(tdays)):
        for i in range(treenum):
            plt.figure()
            test2=(df1[df1['test_number']==tdays[k]]\
                [df1['tree_id']==i+1])
            yval = test2['Dark Subtracted #1']
            xval = (test2['Raman Shift'])
            
            for j in range(len(samdict)):
                test3=(df[df['test_number']==tdays[k]]\
                    [df['tree_id']==i+1][df['sample_number']==samdict[j]])
                input_array = (test3['Dark Subtracted #1'])
                xvaln = (test3['Raman Shift'])
                plt.plot(xvaln,input_array)
                plt.xticks([0,200,400 ,500, 688 ,1000, 1500],rotation=90)   
                plt.title("Test " + str(tdays[k]) + "   Tree " + str(i+1))
 
            plt.plot(xval,yval,'k')

# chk_val(df_ram_bl_c,df_ram_avg_c)

# %%
##### Remove the bad data and cut the first x datapoints to get rid of spikes #####
def raman_c2(df,cutlim):
    idxrmv1= df[df['test_number']=='T7']\
        [df['tree_id']==14].index 
    df.loc[idxrmv1,'Dark Subtracted #1'] = np.nan
    dfn = df[df['index'] >cutlim]

    return dfn

df_ram_c2 = raman_c2(df_ram_avg_c,-1)
chk_val(df_ram_bl_c,df_ram_c2)
df_ram_c2.isnull().sum()

# %%
# df_ram_c2.to_json('../results_cleaned/almond_raman_c.json')