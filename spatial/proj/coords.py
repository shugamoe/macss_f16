# Python Script to Convert Data addresses to GPS coordinates.

import csv
import re

LOC_CONTEXT = ', Chicago, IL'
ADDR_NORM = {}
WORDS_PROB = ['between', 'at', 'near', 'Between']
ADDR_PROB = {}
CORNER_COORDS = {}
TEST_BW = ['University between 64th & 65th', 'Midway Pl. between Greenwood & University']


def address_handler(simple_addr):
    '''
    This function should take an address string and convert it to a set of GPS
    coordinates.
    '''
    if 'between' in simple_addr:
        # Must also match the first street, right now only the last 2 are matched.
        match = re.search(r'between(.*$)', simple_addr) 
        if match:
            streets = match.groups()[0]
            street0, street1 = streets.split('&')
            street0 = street0.strip()
            street1 = street1.strip()
        else:
            print('What the fuck')
            
    elif simple_addr.startswith('Between'):
        match = re.search(r'Between(.*$)', simple_addr)
        if match:
            streets = match.groups()[0]
            street0, street1 = streets.split('&')
            street0 = street0.strip()
            street1 = streeet1.strip()
        else:
            print('What the fuck')


with open('ucpd_daily_incidents_clean.csv', 'r') as f, \
     open('incidents_gps', 'w') as out:

    reader = csv.reader(f)

    fieldnames = []
    for row in reader:
        # Save and write fieldnames of input file to output file.
        if not fieldnames:
            fieldnames = row
            writer = csv.writer(out)
            writer.writerow(fieldnames)
            continue

        full_addr = row[1]

        # The full_addr might have something in parantheses giving 
        # additional information. I.e. 5121 S. Kenwood (Grandma's House)
        # We want to remove 'Grandma's House' since the Google Maps API 
        # might get confused with this shit.
        match = re.search('(\(.*\))', full_addr)
        if match: 
            simple_addr = full_addr.replace(match.group(), '')
            simple_addr.strip()
        else:
            simple_addr = full_addr.strip()

        ADDR_NORM[simple_addr] = ADDR_NORM.setdefault(simple_addr, 0) + 1
        
        # Clear ADDR_NORM of all problem addresses and add them to ADDR_PROB
        all_addr = list(ADDR_NORM.keys())
        for addr in all_addr:
            for word in WORDS_PROB:
                if word in addr:
                    ADDR_PROB[addr] = ADDR_NORM.pop(addr)

