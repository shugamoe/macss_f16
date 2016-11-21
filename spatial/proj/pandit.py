# Mess with the incident reports in pandas


import pandas as pd

# UCPD Stuff
UCPD_RAW = pd.read_csv('foundation/hp_crimes_points.csv')
UCPD_INCIDENT_TYPES = UCPD_RAW['Incident']
UCPD_UNIQUE_TYPES = UCPD_INCIDENT_TYPES.unique()
UCPD_TYPE_COUNTS = UCPD_INCIDENT_TYPES.value_counts()

# CPD Stuff
CPD_RAW = pd.read_csv('foundation/cpd/CPD_in_UCPD_zone_2011-2015.csv')
CPD_INCIDENT_TYPES = CPD_RAW['Primary Type']
CPD_UNIQUE_TYPES = CPD_INCIDENT_TYPES.unique()
CPD_TYPE_COUNTS = CPD_INCIDENT_TYPES.value_counts()

def kw_count(kw):
    '''
    This function takes a keyword (kw) and determines how many crime reports
    have the incident category include this word
    '''
    kw_cnt = 0
    for inc_type in UCPD_UNIQUE_TYPES:
        if kw.lower() in inc_type.lower():
            kw_cnt += inc_type_cnts[inc_type]

    return(kw_cnt)

def make_kw_df(kw, write = False, df = UCPD_RAW):
    '''
    This function takes a keyword (kw) and returns a dataframe that only includes
    crimes containing the entered keyword.
    '''
    indices = []
    for index, inc_type in enumerate(UCPD_INCIDENT_TYPES):
        if kw.lower() in inc_type.lower():
            indices.append(index)

    kw_df = UCPD_RAW.iloc[indices]
    if write:
        kw_df.to_csv('ready/hp_crimes_points_{}.csv'.format(kw))
        print('CSV Written')
    return(kw_df)
