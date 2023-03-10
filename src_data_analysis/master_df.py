#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_swp = pd.read_json('../results/almond_SWP.json')
df_cwsi = pd.read_json('../results/almond_cwsi.json')
df_im = pd.read_json('../results/almond_im_indexes.json')
df_lt = pd.read_json('../results/almond_leaftemp.json')

df_ram_c = pd.read_json('../results_cleaned/almond_raman_c.json')
df_visnir_c = pd.read_json('../results_cleaned/almond_visnir_c.json')


mdf = pd.DataFrame()

tdays_all = ['T1','T2','T3','T4','T5','T6','T7']
tdays_r = ['T5','T6','T7']
treenum = 17

#%%
##### MDF All test days #####
def image_edit(df,arg):
    df = df[df['spec_idx']==arg]
    df = df[['median']]
    df.rename(columns={'median': arg + ' median'},inplace=True)
    df.reset_index(inplace=True,drop=True)
    return df

ndvi = image_edit(df_im,'NDVI')
gndvi= image_edit(df_im,'GNDVI')
osavi = image_edit(df_im,'OSAVI')
lci  = image_edit(df_im,'LCI')
ndre  = image_edit(df_im,'NDRE')

def swp_class(swp,qvals):
    swp['SWPc'] = swp.loc[:, 'SWP']
    qs = swp.quantile(qvals)
    q1 = qs.iloc[0,0]
    q2 = qs.iloc[1,0]
    swp['SWPc'].mask((swp['SWP'] < q1) ,'WL-1',inplace=True )
    swp['SWPc'].mask((swp['SWP'] >= q1) & (swp['SWP'] < q2),'WL-2' ,inplace=True)
    swp['SWPc'].mask((swp['SWP'] >= q2),'WL-3',inplace=True )

    # bins = (3,7,10,15)
    # group_names = ['WL1','WL2','WL3']
    # main['SWPc2'] = pd.cut(main['SWP'], bins=bins , labels=group_names)
    # main['SWPc2'].isnull()
    return swp

# plt.scatter(mdf.index,mdf['SWP'])
swp = swp_class(df_swp[['SWP']],[.33,.66])
cwsi = df_cwsi[['tree_idx','test_number','leaf_temp','Ta','cwsi']]

dfs = [cwsi,ndvi,gndvi,osavi,lci,ndre,swp]
mdf = pd.concat(dfs, axis=1)
mdf.to_json('../results_cleaned/mdf_all.json')

# %%
#### MDF ram








# #%%
# ##### For Raman and visnir #####

# def Xcreate_r_vn(df,phrase):
#     mylist = list()
#     for k in range(len(tdays_r)):
#         for i in range(treenum):
#             dfn =(df[df['test_number']==tdays_r[k]]\
#                 [df['tree_id']==i+1])
#             yval = dfn[phrase].values
#             mylist.append(yval)
    
#     return np.array(mylist)

# X_ram = Xcreate_r_vn(df_ram_c,'Dark Subtracted #1')
# X_visnir = Xcreate_r_vn(df_visnir_c,'Reflect. %')


# # %%
# ##### SWP and CWSI and lt #####
# def Xcreate_s_c_lt(df,phrase):
#     mylist = list()
#     for k in range(len(tdays_all)):
#         for i in range(treenum):
#             dfn =(df[df['test_number']==tdays_all[k]]\
#                 [df['tree_idx']==i+1])
#             yval = dfn[phrase].values
#             mylist.append(yval)

#     return np.array(mylist)

# Y_swp = Xcreate_s_c_lt(df_swp,'SWP')
# X_cwsi = Xcreate_s_c_lt(df_cwsi,'cwsi')
# X_lt = Xcreate_s_c_lt(df_lt,'leaf_temp')

# #%%
# ##### images #####
# def Xcreate_im(df,phrase1,phrase2):
#     mylist = list()
#     for k in range(len(tdays_all)):
#         for i in range(treenum):
#             dfn =(df[df['spec_idx']==phrase1][df['test_number']==tdays_all[k]]\
#                 [df['image_id']==i+1])
#             yval = dfn[phrase2].values
#             mylist.append(yval)

#     return np.array(mylist)

# X_ndvi = Xcreate_im(df_im,'NDVI','median')
# X_gndvi = Xcreate_im(df_im,'GNDVI','median')
# X_osavi = Xcreate_im(df_im,'OSAVI','median')
# X_lci = Xcreate_im(df_im,'LCI','median')
# X_ndre = Xcreate_im(df_im,'NDRE','median')

# # %%
# def argchk(arr):
#     return np.argwhere(np.isnan(arr).all(axis=1))

# # argchk(Y_swp)
# # argchk(X_cwsi)
# # argchk(X_ram)
# argchk(X_visnir)


# #%%
# from sklearn.pipeline import make_pipeline
# from sklearn.preprocessing import StandardScaler
# from sklearn.svm import SVR
# from sklearn.naive_bayes import GaussianNB
# from sklearn.neural_network import MLPRegressor
# from sklearn.model_selection import cross_val_score
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import r2_score


# #%%
# #########    visnir   ############
# x = X_visnir
# y = Y_swp[-51:].flatten()
# x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.1,random_state=2)
# # ml = make_pipeline(StandardScaler(), SVR())
# ml = make_pipeline(StandardScaler(),MLPRegressor(solver='lbfgs',hidden_layer_sizes=(70, 3)))
# ml.fit(x_train,y_train)
# ml.score(x_test,y_test)

# # ml.score(x_train,y_train)

# # %%
# ######## Raman ########
# x = X_ram
# x = np.delete(x, (47), axis=0)
# y = np.delete(Y_swp[-51:], (47), axis=0)
# y=  y.flatten()
# x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.1, shuffle=True, random_state=2)
# # ml = make_pipeline(StandardScaler(), SVR(kernel='poly',C=1,degree=1,cache_size=1000))
# # ml = make_pipeline(StandardScaler(), GaussianNB())
# ml = make_pipeline(StandardScaler(),MLPRegressor(solver='lbfgs',hidden_layer_sizes=(70, 3)))
# # cross_val_score(ml, x, y, cv=5, scoring='recall_macro')
# ml.fit(x_train,y_train)
# ml.score(x_test,y_test)
# # cross_val_score(ml,x, y, cv=5)
# # r2_score(y_test, ml.predict(x_test))

# # %%
# ######## cwsi ########
# x = np.delete(X_cwsi, (argchk(Y_swp)), axis=0)
# y = np.delete(Y_swp, (argchk(Y_swp)), axis=0)
# y = y.flatten()
# x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.1,random_state=2)
# ml = make_pipeline(StandardScaler(), SVR(kernel='poly',degree=1))
# ml.fit(x_train,y_train)
# ml.score(x_test,y_test)
# cross_val_score(ml,x, y, cv=5)
# # ml.score(x_train,y_train)

# # %%
# ######## lt ########
# x = np.delete(X_lt, (argchk(Y_swp)), axis=0)
# y = np.delete(Y_swp, (argchk(Y_swp)), axis=0)
# y = y.flatten()
# x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.1,random_state=2)
# ml = make_pipeline(StandardScaler(), SVR())
# ml.fit(x_train,y_train)
# ml.score(x_test,y_test)

# # %%
# ####### RAMAN and CWSI #######
# x = np.concatenate((X_ram,X_cwsi[-51:]),axis=1)
# x = np.delete(x, (47), axis=0)
# y = np.delete(Y_swp[-51:], (47), axis=0)
# y=  y.flatten()
# x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.1,random_state=2)
# # ml = make_pipeline(StandardScaler(), SVR(kernel='poly',degree=1))
# ml = make_pipeline(StandardScaler(),MLPRegressor(solver='lbfgs',hidden_layer_sizes=(50, 3)))
# ml.fit(x_train,y_train)
# ml.score(x_test,y_test)
# # cross_val_score(ml,x, y, cv=5)

# # %%
# ####### CWSI and INDEXES #######
# x = np.concatenate((X_cwsi,X_ndvi,X_gndvi,X_osavi,X_lci,X_ndre),axis=1)
# x = np.delete(x, (argchk(Y_swp)), axis=0)
# y = np.delete(Y_swp, (argchk(Y_swp)), axis=0)
# y = y.flatten()
# x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.1,random_state=2)
# # ml = make_pipeline(StandardScaler(), SVR())
# ml = make_pipeline(StandardScaler(),MLPRegressor(solver='lbfgs',hidden_layer_sizes=(100, 5)))
# ml.fit(x_train,y_train)
# ml.score(x_test,y_test)

# # %%
# ####### VISNIR and indexes #######
# x = np.concatenate((X_visnir,X_ndre[-51:]),axis=1)
# y = Y_swp[-51:]
# x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.1,random_state=2)
# ml = make_pipeline(StandardScaler(), SVR())
# ml.fit(x_train,y_train)
# ml.score(x_test,y_test)

# # %%
# ####### Raman and indexes #######
# x = np.concatenate((X_ram,X_ndre[-51:],X_osavi[-51:]),axis=1)
# x = np.delete(x, (47), axis=0)
# y = np.delete(Y_swp[-51:], (47), axis=0)
# y = y.flatten()
# x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.1,random_state=2)
# ml = make_pipeline(StandardScaler(), SVR(kernel='poly',degree=1))
# ml.fit(x_train,y_train)
# ml.score(x_test,y_test)

# # %%

# %%
