# Pair the GPS coordinates of traffic measurement points to Chicago 
# neighborhoods (1-77)

import json 
from shapely.geometry import shape, Point
import csv
import pandas as pd


def main(geojson_file, coords_file, separate = False):
	'''
	'''
	with open('Boundaries-Community Areas_(current).geojson', 'r') as f:
		geojs = json.load(f)

	with open('traf_less.csv', 'r') as f:
		reader = csv.DictReader(f)

		points = []
		p_volume = []
		for row in reader:
			point = Point(float(row['Longitude']), float(row['Latitude']))
			points.append(point)
			p_volume.append(int(row['Total.Passing.Vehicle.Volume']))

	# Find the corresponding neighborhood int for each point and add the traffic
	# volume measured at that point to the geojs file.
	i = 0 # Row Counter
	for point in points:
		i += 1
		for hood in geojs['features']:
			polygon = shape(hood['geometry'])
			if polygon.contains(point):
				print("Data from Sensor {} assigned to hood code {}".format(i, \
					hood['properties']['area_num_1']))
				hood['properties']['traf_vol'] = \
					hood['properties'].setdefault('traf_vol', 0) + \
					p_volume.pop(0)
				hood['properties']['num_sensors'] = \
					hood['properties'].setdefault('num_sensors', 0) + 1

	for hood in geojs['features']:
		if 'traf_vol' in hood['properties']:
			hood['properties']['traf_per_sensor'] = \
				hood['properties']['traf_vol'] / hood['properties']['num_sensors']
				
	with open('Chicago_neighborhoods_traf_vol.geojson', 'w') as outfile:
		json.dump(geojs, outfile) 
		print('New JSON file written')


if __name__ == '__main__':
	main(None, None)
