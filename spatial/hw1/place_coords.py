# Pair the GPS coordinates of traffic measurement sensors to Chicago 
# neighborhoods (1-77)

import json 
from shapely.geometry import shape, Point
import csv
import pandas as pd


class TrafficSensor(object):
	'''
	A Class for the traffic sensor data
	'''
	def __init__(self, id_num, vol, lon, lat):
		self.id = id_num
		self.coords = Point(lon, lat)
		self.vol = vol
		self.hood_code = None # Don't know neighborhood yet.

	def __repr__(self):
		return "{} Vehicles at {}".format(self.vol, self.coords)


with open('Boundaries-Community Areas_(current).geojson', 'r') as f:
	geojs = json.load(f)

with open('traf_less.csv', 'r') as f:
	reader = csv.DictReader(f)

	traf_sensors = []
	for row in reader:
		sensor = TrafficSensor(int(row['']), 
							   int(row['Total.Passing.Vehicle.Volume']), \
							   float(row['Longitude']), float(row['Latitude']))
		traf_sensors.append(sensor)

# Find the neighborhood each sensor is located in
for sensor in traf_sensors:
	for hood in geojs['features']:
		polygon = shape(hood['geometry'])
		if polygon.contains(sensor.coords):
			# Assign neighborhood code to sensor
			sensor.hood_code = hood['properties']['area_num_1']
			print('Sensor {} allocated to neighborhood {}'.format(sensor.id, \
				sensor.hood_code))


# Extract hood codes to list and write a new CSV file
hood_codes = [sensor.hood_code for sensor in traf_sensors]
hcodes_df = pd.DataFrame(hood_codes, columns = ['hood_codes'])
traf_csv = pd.read_csv('traf_less.csv')
traf_csv['hood_code'] = hcodes_df['hood_codes']
traf_csv.to_csv('traf_with_hoods.csv')


		