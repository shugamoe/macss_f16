# Scrape the UCPD archive of incident reports

import requests
from bs4 import BeautifulSoup
import re
import os
import os.path
import urllib.parse
import shutil
import getpass
import argparse
import time
import pickle
import sqlite3

ARCHIVE_URL = 'https://incidentreports.uchicago.edu/incidentReportArchive.php'

'''
Every Monday through Friday (except holidays) the University of Chicago Police 
Department posts daily crime incidents and fire incidents that were reported to 
the UCPD over the previous 24 hours. Weekend incident reports (Friday, Saturday, 
and Sunday) are added on the following Monday. The UCPD patrol area includes 
the area between 37th and 64th streets and Cottage Grove Avenue to Lake Shore 
Drive (not including Jackson Park).
'''

def scrape():
    '''
    '''
    pass


cur_day = time.strftime('%A')
cur_date = time.strftime('%m/%d/%Y')

sesh = requests.Session()
archive_resp = sesh.get(ARCHIVE_URL)

soup = BeautifulSoup(archive_resp.text, 'html.parser')

def seed():
    '''
    '''
    sesh = requests.Session()
    archive_resp = sesh.get(ARCHIVE_URL)

    soup = BeautifulSoup(archive_resp.text, 'html.parser')

    dates = []
    for t in soup.findAll('input', attrs = {'class': 'ss-date'}):
        dates.append(t.get('value'))

    assert(length(dates) == 2)




if __name__ == '__main__':
    scrape():



