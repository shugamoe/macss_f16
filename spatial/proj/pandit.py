# Mess with the incident reports in pandas


import pandas as pd

INC_RAW = pd.read_csv('incidents_gps.csv', index_col = 2)

INCIDENT_TYPES = INC_RAW['Incident']

uniq_incidents = INCIDENT_TYPES.unique()

inc_type_cnts = INCIDENT_TYPES.value_counts()

theft_related_cnts = 0

def kw_count(kw):
    '''
    This function takes a keyword (kw) and determines how many crime reports
    have the incident category include this word
    '''
    kw_cnt = 0
    for inc_type in uniq_incidents:
        if kw.lower() in inc_type.lower():
            kw_cnt += inc_type_cnts[inc_type]

    return(kw_cnt)

def make_kw_df(kw, df = INC_RAW):
    '''
    This function takes a keyword (kw) and returns a dataframe that only includes
    crimes
    '''
    indices = []
    for index, inc_type in enumerate(INCIDENT_TYPES):
        if kw.lower() in inc_type.lower():
            indices.append(index)

    return(INC_RAW.iloc[indices])
