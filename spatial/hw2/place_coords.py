# Pair the GPS coordinates of traffic measurement points to San Francisco 
# neighborhoods

import json 
from shapely.geometry import shape, Point
import csv
from datetime import datetime
import re

THREE_VARS = ['Owner Move In', 'Nuisance', 'Breach']
EVICT_TYPES = ['Non Payment','Breach','Nuisance','Illegal Use','Failure to Sign Renewal','Access Denial','Unapproved Subtenant','Owner Move In','Demolition','Capital Improvement','Substantial Rehab','Ellis Act WithDrawal','Condo Conversion','Roommate Same Unit','Other Cause','Late Payments','Lead Remediation','Development','Good Samaritan Ends']

GEOJSON_FILE = 'SF Find Neighborhoods.geojson'
COORDS_FILE = 'Eviction_Notices.csv'

with open(GEOJSON_FILE, 'r') as f:
	geojs = json.load(f)

with open(COORDS_FILE, 'r') as f:
	reader = csv.DictReader(f)

	for row in reader:
		col_names = row.keys()
		break

	# Track the count, location points, and year filed for each type of eviction.
	et_tracker = {et:[0, [], []] for et in EVICT_TYPES}
	for row in reader:
		for et in EVICT_TYPES:
			if (row[et] == 'true') and row['Location'] and row['File Date']:
				et_tracker[et][0] += 1 
				
				# Add location point
				lat, lon = row['Location'].split(',')
				lat = float(lat.lstrip('('))
				lon = float(lon.rstrip(')'))
				et_tracker[et][1].append(Point(lon, lat))

				# Add year filed
				parser = re.search('[0-9]{4}$', row['File Date'])
				year = parser.group()
				et_tracker[et][2].append(int(year))

	print('Eviction Types and Locations Recorded\n')

print('Assigning Eviction Types and Corresponding Locations to Neighborhoods\n')
frac_done = 0
frac_boom = 0
tot_evicts = sum([tracker[0] for et, tracker in et_tracker.items()])
for et, tracker in et_tracker.items():
	et_count = tracker[0]
	points = tracker[1]
	years = tracker[2]

	for index_yr, point in enumerate(points):
		for hood in geojs['features']:
			polygon = shape(hood['geometry'])
			if polygon.contains(point):
				year = years[index_yr] 
				hood_dict = hood['properties']

				hood_dict['et_' + et] = hood_dict.setdefault('et_' + et, 0) + 1
				hood_dict['tot_evicts'] = hood_dict.setdefault('tot_evicts', 0)\
				+ 1

				# Track evictions occurring during the latest real estate boom.
				if year >= 2012:
					hood_dict['boom_' + et] = hood_dict.setdefault('boom_' + 
						et, 0) + 1
					hood_dict['boom_evicts'] = hood_dict.setdefault('boom_evic'
						'ts', 0) + 1
					frac_boom += 1 / tot_evicts
					print('Boom Eviction Notice Found')

				frac_done += 1 / tot_evicts
				print("~{:.2f} complete | {:.2f} Current Boom Evicts | {} Eviction Type found in {}\n".format(\
					frac_done, frac_boom, et, hood_dict['name']))
				
				break

for hood in geojs['features']:
	hood_dict = hood['properties']
	hood_dict['frac_boom_evicts'] = hood_dict.get('boom_evicts', 0) / hood_dict.get('tot_evicts', 1)
	for et in et_tracker.keys():	
		if 'et_' + et in hood_dict:
			hood_dict['frac_' + et] = hood_dict['et_' + et] / hood_dict['tot_evicts']
			if 'boom_' + et in hood_dict:
				hood_dict['frac_boom_' + et] = hood_dict['boom_'+ et] / hood_dict['boom_evicts']
			
print('Fractions generated')


	
with open('eviction_types_2012boom_SF_hoods.geojson', 'w') as outfile:
	json.dump(geojs, outfile)
	print('New JSON file written')