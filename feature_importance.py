import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import scipy
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from preprocessing_data import *

def get_feature_importance(df):
    """
    get the model's feature importance table
    """
    target = pd.read_csv('data/labels.csv')
    target.set_index('id', inplace = True)
    
    df = impute_construction_yr(df)
    df = clean_funder_installer(df, threshold =31)
    df = clean_population(df)
    df = make_season(df)
    df = space_data(df, ep_val=1.5, threshold=31)
    df = to_category(df)
    df.set_index('id', inplace =True)
    remove(df)
    
    permit_mode = True
    public_meeting_mode = True
    pop_median = 10497.0
    construction_yr_mode = 2008.0
    
    cat_cols = []
    for col in df.columns:
        if hasattr(df[col], 'cat'):
            cat_cols.append(col)
    
    df["permit"].fillna(permit_mode, inplace = True)
    df["public_meeting"].fillna(public_meeting_mode, inplace = True)
    df["population"].fillna(pop_median, inplace = True)
    df["construction_year"].fillna(construction_yr_mode, inplace = True)
    
    meta = pd.get_dummies(df[cat_cols])
    meta['population'] = df['population']
    
    rf = RandomForestClassifier(n_estimators=200, 
                             min_samples_split=3, 
                             random_state=412, 
                             n_jobs = 3, 
                             class_weight = {0:0.25, 1: 0.5, 2:0.25})
    
    le = LabelEncoder()
    target["status_group_binarized"] = le.fit_transform(target["status_group"])
    
    model = rf.fit(meta, target["status_group_binarized"])
    
    importance_table = pd.concat((pd.DataFrame(meta.columns, columns = ['variable']), 
           pd.DataFrame(model.feature_importances_, columns = ['importance'])), 
          axis = 1).sort_values(by='importance', ascending = False)[:40]
    
    return importance_table
