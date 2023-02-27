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
def raman_void(df):
    low_lim = 500 #Try 50 and 500
    high_lim = 2000
    dfn = df[df['index'] >low_lim]
    dfn = dfn[dfn['index'] < high_lim]
    dfn = dfn.reset_index(drop=True)
    return dfn

df_ram_c = raman_void(df_ram)
len(df_ram_c[df_ram_c['Raman Shift'] == '   '].index)


#%%
def max_psamp(df_ram_c):
    for k in range(len(tdays)):
        print('\n\n\nTest Number ',tdays[k],'\n')
        for i in range(treenum):
            print()
            for j in range(len(samdict)):
                test2=(df_ram_c[df_ram_c['test_number']==tdays[k]]\
                    [df_ram_c['tree_id']==i+1][df_ram_c['sample_number']==samdict[j]])
                test3 = test2['Dark Subtracted #1']
                # test2.plot.scatter(x=7,y=11  )
                print('Max Tree ',i+1,' ', samdict[j],' = ',test3.max())

max_psamp(df_ram_c)   
print('Results estimate that for T7 ,  Tree 14, S1 S2 S3 are bad data')
# print('Results estimate that for T7 ,  Tree 2, S3 is bad data')

""" To visualize:
test2=(df_ram_c[df_ram_c['test_number']=='T7']\
    [df_ram_c['tree_id']==][df_ram_c['sample_number']=='S'])
test2.plot.scatter(x=7,y=11  ) 

"""
#%%
def sat_psamp(df_ram_c):
    cnst = 150
    for k in range(len(tdays)):
        print('\n\n\nTest Number ',tdays[k],'\n')
        for i in range(treenum):
            print()
            for j in range(len(samdict)):
                test2=(df_ram_c[df_ram_c['test_number']==tdays[k]]\
                    [df_ram_c['tree_id']==i+1][df_ram_c['sample_number']==samdict[j]])
                testy = (test2['Dark Subtracted #1'][0:cnst])
                testx = (test2['Raman Shift'][0:cnst])
                # frst = test2['Dark Subtracted #1'][0]
                # last = test2['Dark Subtracted #1'][cnst]
                
                plt.figure()
                plt.scatter(testx,testy)
                plt.title('Test '+tdays[k]+'Saturation Tree '+ str(i+1) +' '+ samdict[j]+' :')
                plt.show

# sat_psamp(df_ram_c)   



#%%
###### Baseline Removal ######
from BaselineRemoval import BaselineRemoval

def bsl_rmv(df):
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
                plt.xticks([0 ,500 ,1000, 1500, 2000])         

bsl_rmv(df_ram_c)


# %%
def raman_c2(df_ram_c):
    idxrmv1= df_ram_c[df_ram_c['test_number']=='T7']\
        [df_ram_c['tree_id']==14].index
    # idxrmv2= df_ram_c[df_ram_c['test_number']=='T7']\
    #     [df_ram_c['tree_id']==2][df_ram_c['sample_number']=='S3'].index    
    df_ram_c.drop(idxrmv1,inplace=True)
    # df_ram_c.drop(idxrmv2,inplace=True)

    df_ram_c.reset_index(inplace=True,drop=True)

    return df_ram_c

df_ram_c = raman_c2(df_ram_c)