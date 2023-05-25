#%%
import pandas as pd
import numpy as np


#%%
#########    RAMAN   ############
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

ml = make_pipeline(StandardScaler(), SVR())
ml.fit()




# np.concatenate((arr1,arr2),axis=1)



#%%

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
