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
START_DATE = '07/01/2010'

'''
Every Monday through Friday (except holidays) the University of Chicago Police 
Department posts daily crime incidents and fire incidents that were reported to 
the UCPD over the previous 24 hours. Weekend incident reports (Friday, Saturday, 
and Sunday) are added on the following Monday. The UCPD patrol area includes 
the area between 37th and 64th streets and Cottage Grove Avenue to Lake Shore 
Drive (not including Jackson Park).
'''

# <li class="page-count"><span style="width:50px; border:none; color:#800;">1 / 1663 </span></li>
# <li class="next "><a href="incidentReportArchive.php?startDate=1277960400&amp;endDate=1475470800&amp;offset=5">Next <span aria-hidden="true">→</span></a></li>
# <input class="ss-date hasDatepicker" value="07/10/2010" type="text" name="startDate" id="start-date">

def scrape():
    '''
    '''
    pass


cur_day = time.strftime('%A')
cur_date = time.strftime('%m/%d/%Y')

sesh = requests.Session()
archive_resp = sesh.get(ARCHIVE_URL)

soup = BeautifulSoup(archive_resp.content, 'html.parser')

def seed():
    '''
    '''
    sesh = requests.Session()
    archive_resp = sesh.get(ARCHIVE_URL)
    all_reports = sesh.post(ARCHIVE_URL, data = {'startDate': START_DATE})

    # Try different *.parser or else use selenium to accomplish scraping.
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    soup = BeautifulSoup(all_reports.content, 'html.parser') 

    dates = []
    for t in soup.findAll('input', attrs = {'class': 'ss-date'}):
        dates.append(t.get('value')) # Scrape the date
        print(dates)

    for t in soup.findAll('li', attrs = {'class': 'page-count'}):
        pc_string = t.text
        break

    cur_page, num_pages = re.split('/', pc_string)
    cur_page.split()
    num_pages.split()


    


if __name__ == '__main__':
    pass



