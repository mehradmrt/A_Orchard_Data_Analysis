
#%% Vis-NIR Extract
import pandas as pd
import glob
import os

tdays = ['T5','T6','T7']
samdict = ['S1','S2','S3']
nirdict = {'T5': '07_30_22', 'T6': '08_03_22', 'T7': '08_31_22'}
vnir_dir = '../VIS_NIR/Almond_' # TODO update the directories 
treenum = 17

def file_rename():
    for i in range(len(nirdict)):
        root  = vnir_dir + nirdict[tdays[i]]
        files = glob.glob(root+'/*.sed')
        for filename in files:
            base = os.path.splitext(filename)[0]
            newfiles = os.rename(filename, base + '.csv')
# ext_create = file_rename()        

def vis_nir():
    mdf = pd.DataFrame()
    df = pd.DataFrame()
    for i in range(len(nirdict)):
        root  = vnir_dir + nirdict[tdays[i]]
        files = glob.glob(root+'/*.csv')

        tree_idx = 1
        sampnum = 0
        counter=0
        for filename in files:
            check=True
            if sampnum==3:
                tree_idx+=1
                sampnum=0

            if i==1 and counter==9:
                check=False
                sampnum-=1
            elif i==1 and counter==38:
                check=False
                sampnum-=1

            if check==True:
                
                df = pd.read_csv(filename, skiprows=32, delimiter='\t')
                df.insert(0,"sample_number",samdict[sampnum])
                df.insert(0,"tree_id",tree_idx)
                df.insert(0,"test_number",tdays[i])
                # print(filename)
                # print(i,sampnum,tree_idx,counter)
                # print(df)
                
                mdf = pd.concat([mdf,df])
            
            sampnum += 1
            counter += 1
    
    return mdf

master_visnir = vis_nir()
master_visnir.reset_index(inplace=True)    

#%% Raman Extract
import pandas as pd
import glob

tdays = ['T5','T6','T7']
ramdict = {'T5': '07_30_22', 'T6': '08_03_22', 'T7': '08_31_22'}
samdict = ['S1','S2','S3']
ram_dir = '../Ramandata/Almond-Leaves-Ramandata-' # TODO update the directories 
treenum = 17

def Raman():
    mdf = pd.DataFrame()
    df = pd.DataFrame()
    
    for i in range(len(ramdict)):
        root  = ram_dir + ramdict[tdays[i]] 
        files = glob.glob(root+ '/*.csv')
        tree_idx = 1
        sampnum = 0
        counter=1  
        for j in range(len(files)):
            check=True
            if sampnum==3:
                tree_idx+=1
                sampnum=0

            if check==True:
                filename = glob.glob(root+ '/SP_'+ str(counter) +'.csv')
                # print(filename)

                df = pd.read_csv(filename[0], skiprows=105)
                df.insert(0,"sample_number",samdict[sampnum])
                df.insert(0,"tree_id",tree_idx)
                df.insert(0,"test_number",tdays[i])
                mdf = pd.concat([mdf,df])
                sampnum +=1
                counter +=1
                # print(df.iloc[:,0:3])
    return mdf

master_ram = Raman()
master_ram.reset_index(inplace=True)    

# %%
####### Save results in .json
master_visnir.to_json('../results/almond_visnir.json')
master_ram.to_json('../results/almond_raman.json')

