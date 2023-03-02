#%%
import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

#%%
#########    RAMAN    ############
df_ram_c = pd.read_json('../results_cleaned/almond_raman_c.json')

