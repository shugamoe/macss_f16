# Pair the GPS coordinates of traffic measurement points to San Francisco 
# neighborhoods

import json 
from shapely.geometry import shape, Point
import csv
import pandas as pd

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

	# Track the count of and list of location points for each type of eviction
	et_tracker = {et:[0, []] for et in EVICT_TYPES}
	for row in reader:
		for et in EVICT_TYPES:
			if (row[et] == 'true') and row['Location']:
				et_tracker[et][0] += 1 
				lat, lon = row['Location'].split(',')
				lat = float(lat.lstrip('('))
				lon = float(lon.rstrip(')'))

				# Add location point
				et_tracker[et][1].append(Point(lon, lat))

	print('Eviction Types and Locations Recorded\n')

tot_evicts = sum([tracker[0] for et, tracker in et_tracker.items()])

print('Assigning Eviction Types and Corresponding Locations to Neighborhoods\n')
frac_done = 0
for et, tracker in et_tracker.items():
	et_count = tracker[0]
	points = tracker[1]

	for point in points:
		for hood in geojs['features']:
			polygon = shape(hood['geometry'])
			if polygon.contains(point):


				hood['properties']['et_' + et] = hood['properties'].setdefault(\
				'et_' + et, 0) + 1 
				hood['properties']['tot_evicts'] = hood['properties'].setdefault(\
					'tot_evicts', 0) + 1
				print("~{:.2f} complete | {} Eviction Type found in {}".format(\
					frac_done, et, hood['properties']['name']))
				frac_done += 1 / tot_evicts
				break

for hood in geojs['features']:
	for et in et_tracker.keys():
		if 'et_' + et in hood['properties']:
			hood['properties']['frac_' + et] = hood['properties']['et_' + et] / hood['properties']['tot_evicts']
print('Fractions generated')


	
with open('Eviction_type_density_SF_hoods.geojson', 'w') as outfile:
	json.dump(geojs, outfile)
	print('New JSON file written')