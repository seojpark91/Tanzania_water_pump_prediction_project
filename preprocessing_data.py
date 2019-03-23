import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import scipy
from string import punctuation


def make_season(df):
    """
    create a new column with data_recorded column
    """
    def season(n):
        if n>=3 and n<=5:
            return 'long rains'
        elif n>=6 and n<=10:
            return 'long dry'
        elif n>=11 and n<=12:
            return 'short rains'
        else:
            return 'short dry'
    df["date_recorded_year"] = df.date_recorded.apply(lambda date: int(date.split("-")[0]))
    df["date_recorded_month"] = df.date_recorded.apply(lambda date: date.split("-")[1])
    df["date_recorded_month"] = df.date_recorded_month.apply(lambda month: int(month[1]) if month[0] == '0' else int(month))
    
    df['season'] = df["date_recorded_month"].apply(lambda x: season(x))
    df.drop(columns=['date_recorded', 'date_recorded_month'], inplace = True, axis=1)
    
    return df

def impute_construction_yr(df):
    """
    impute missing values in construction_year column by imputing mode values 
    """
    df.loc[df['construction_year'] == 0,'construction_year'] = np.nan
    df['construction_1'] = df.groupby(['installer'], sort=False)['construction_year']\
                .apply(lambda x: x.fillna(scipy.stats.mode(x)[0][0]))
    df['construction_year'] = df.groupby(['funder'], sort=False)['construction_1']\
                .apply(lambda x: x.fillna(scipy.stats.mode(x)[0][0]))
    df.drop('construction_1', axis=1, inplace = True)
    
    return df

def clean_funder_installer(df, threshold = None):
    """
    "clean funder and installer columns manually. If threshold is given, replace values under the threshold as "rare"
    """
    df["funder"] = df["funder"].fillna('unknown') 
    df["installer"] = df["installer"].fillna('unknown')
    df.loc[df.funder=='none', 'funder'] = 'unknown'
    
    df["funder"] = df["funder"].apply(lambda x: x.lower())
    df["installer"] = df["installer"].apply(lambda x: x.lower())
    
    df["funder"] = df["funder"].apply(lambda x: "oxfam" if x == "oxfarm" else x)
    df["installer"] = df["installer"].apply(lambda x: "oxfam" if x == "oxfarm" else x)
    
    df.loc[df.installer == '-', 'installer'] = 'others'
    df.loc[df.installer == "villagerd", "installer"] = 'villagers'
    df.loc[df.installer == "villager", "installer"] = 'villagers'
    df.loc[df.installer == "worldvission", "installer"] = 'worldvision'
    df.loc[df.installer == 'worldvisiin', 'installer'] = 'worldvision'
    df.loc[df.installer == 'wordlbank', "installer"] = 'worldbank'
    df.loc[df.installer == 'worldbanks', 'installer'] = 'worldbank'
    df.loc[df.installer == 'worldnk', 'installer'] = 'worldbank'
    df.loc[df.installer == 'wouldbank', 'installer'] = 'worldbank'
    df.loc[df.installer == 'wamissionariwakikatoriki', 'installer'] = 'wamisionariwakikatoriki'
    df.loc[df.installer == 'ampcontractor', 'installer'] = 'ampcontract'
    df.loc[df.installer == 'ampcontracts', 'installer'] = 'ampcontract'
    df.loc[df.installer == 'wdeco', 'installer'] = 'wedeco'
    df.loc[df.installer =='africamuslimagenc', 'installer'] = 'africamuslimagency'
    df.loc[df.installer == 'zaowaterspringx', 'installer'] = 'zaowaterspring'
    df.loc[df.installer == 'word', 'installer'] = 'worldbank'
    df.loc[df.installer == 'wordbank', 'installer'] = 'worldbank'
    df.loc[df.installer =='worddivisio', 'installer'] = 'worlddivision'
    

    df.loc[df.funder == 'zaowaterspringx', 'funder'] = 'zaowaterspring'
    df.loc[df.funder =="unwfp", "funder"] = "wfp"
    df.loc[df.funder == "overnment", "funder"] = 'government'
    df.loc[df.installer == "overnment", "installer"] = 'government'
    df.loc[df.installer == 'gove', "installer"] = 'government'
    df.loc[df.installer == 'gover', "installer"] = 'government'
    df.loc[df.installer == 'govern', "installer"] = 'government'
    df.loc[df.installer == 'centralgovt', "installer"] = 'centralgovernment'
    df.loc[df.installer == 'cebtralgovernment', "installer"] = 'centralgovernment'
    df.loc[df.installer == 'centalgovernment', "installer"] = 'centralgovernment'
    df.loc[df.installer == 'centr', "installer"] = 'centralgovernment'
    df.loc[df.installer == 'commu', "installer"] = 'community'
    df.loc[df.installer == 'communit', "installer"] = 'community'  
    
    if threshold:
        low_freq_installer = list(df.installer.value_counts()[df.installer.value_counts() < threshold].index)
        df["installer"] = df["installer"].apply(lambda x: "rare" if x in low_freq_installer else x)
        low_freq_funder = list(df.funder.value_counts()[df.funder.value_counts() < threshold].index)
        df["funder"] = df["funder"].apply(lambda x: "rare" if x in low_freq_funder else x)
    
    return df

def clean_population(df):
    """
    replace entire population feature with the data from Tanzania Statistics Portal 
    """
    pop_for_merge = pd.read_csv('data/pop_for_merge.csv', index_col = 0)
    pop_median = pd.read_csv('data/pop_median.csv', index_col = 0)
    remove = ['Urban', 'District', 'City', 'Municipal', 'Town', 'Rural', 'Council', 'TC', 'Township']
    df.region = df.region.apply(lambda x: x.lower())
    df.lga = df.lga.apply(lambda x: [d for d in x.split(' ') if d not in remove])
    df.lga = df.lga.apply(lambda x: " ".join(x))
    df.lga = df.lga.apply(lambda x: [alpha for word in x for alpha in word if (alpha.isalpha() or alpha.isspace())])
    df.lga = df.lga.apply(lambda x: "".join(x).lower())

    df.ward = df.ward.apply(lambda x: [alpha for word in x for alpha in word if (alpha.isalpha() or alpha.isspace())])
    df.ward = df.ward.apply(lambda x: "".join(x).lower())
    
    main = df[['id','region', 'lga', 'ward', 'population']]
    merged = main.merge(pop_for_merge, on = ["ward", 'lga'], how = "inner")
    df = df.merge(merged[['id', 'population_y']], how='left')
    df.drop('population', axis = 1, inplace = True)
    df = df.merge(pop_median, on = 'lga', how = 'left')
    
    df["new_population"] = np.where(df.population_y.isnull(), df.population, df.population_y)
    df.drop(['population_y', 'population'], axis = 1, inplace = True)
    df = df.rename(index=str, columns={"new_population": "population"})
    
    return df


def space_data(df, ep_val=1.5, threshold=None):
    """
    Using Dbscan clustering, create new feature with longitude and latitude columns
    """
    #replace NA values 
    loc_dict = {'Bariadi': [33.983333, -2.8], 'Geita' : [32.25, -2.916667], 'Magu': [-2.583333, 33.433333]}
    long_0 = list(int(i) for i in df[['lga', 'longitude', 'latitude']][df[['lga', 'longitude', 'latitude']].longitude == 0].index)

    for idx in long_0:
        if df.iloc[idx].lga in loc_dict:
            lga_name = df.iloc[idx].lga
            df.at[idx, 'longitude'] = loc_dict[lga_name][0]
            df.at[idx, 'latitude'] = loc_dict[lga_name][1]
            
    kms_per_radian = 6371.0088
    epsilon = ep_val / kms_per_radian
    coords = df.as_matrix(columns=['latitude', 'longitude'])
    
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    df['clustered_space'] = db.labels_
    df['clustered_space'] = df['clustered_space'].astype('category')
    new_df = df.drop(['longitude', 'latitude'], axis=1)
    
    if threshold:
        space = list(df.clustered_space.value_counts()[df.clustered_space.value_counts() < threshold].index)
        df["clustered_space"] = df["clustered_space"].apply(lambda x: "rare" if x in space else x)
    return new_df


def to_category(df):
    """
    make all object data type columns to category
    """
    df['region_code'] = df['region_code'].astype('category')
    df['district_code'] = df['district_code'].astype('category')
    df['construction_year'] = df['construction_year'].astype('category')
    df['date_recorded_year'] = df['date_recorded_year'].astype('category')
    
    for col in df.columns:
        if df[col].dtype == 'O':
            df[col] = df[col].astype('category')
    
    return df

def remove(df):
    """
    remove unncessary columns
    """
    df.drop(['recorded_by', 'amount_tsh', 'payment_type', 'region', 'management_group', 'extraction_type', 'quality_group',\
             'extraction_type_group',"source", "gps_height", "source_type", 'scheme_name','scheme_management','subvillage',\
             'num_private','wpt_name','waterpoint_type_group','quantity_group'], axis=1, inplace=True)
    return df

def make_meta(df):
    """
    For the model, I used pipeline which is much convenient. However, in order to see feature importance, one should use
    pandas get_dummies function since with pipeline, one cannot extract feature importance
    """
    df = make_season(df)
    df = clean_funder_installer(df)
    df = impute_construction_yr(df)
    df = clean_population(df)
    df = space_data(df)
    df = remove(df)
    df = to_category(df)
    df.set_index('id', inplace =True)
    
    permit_mode = True
    public_meeting_mode = True
    pop_median = 10497.0
    construction_yr_mode = 2008.0
    
    df["permit"].fillna(permit_mode, inplace = True)
    df["public_meeting"].fillna(public_meeting_mode, inplace = True)
    df["population"].fillna(pop_median, inplace = True)
    df["construction_year"].fillna(construction_yr_mode, inplace = True)

    cat_cols = []
    for col in df.columns:
        if hasattr(df[col], 'cat'):
            cat_cols.append(col)
    
    meta = pd.get_dummies(df[cat_cols])
    meta['population'] = df['population']

    return meta
