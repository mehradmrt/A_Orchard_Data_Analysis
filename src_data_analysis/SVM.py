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