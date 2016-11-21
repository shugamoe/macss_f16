# Integrate 2010 Census population and crimes into the 2010 Census Block Polygons

import json
import csv
import pandit
from shapely.geometry import shape, Point


def merge_pop():
    '''
    This function merges the population counts from the census tracts CSV to the
    geojson file with the polygons of the neighborhoods.
    '''
    with open('census_hp_blocks.geojson', 'r') as f0, open('census_chicago_population.csv', 'r') as f1:
        geojs = json.load(f0)
        reader = csv.reader(f1)

        count = 0
        tot = len(geojs['features'])
        for block in geojs['features']:
            block_id = int(block['properties']['tract_bloc'])
            f1.seek(0) # Set iterator to beginning of input file
            next(reader) # Skip header
            for other_block in reader:
                other_block_id = other_block[0]
                if int(other_block_id) == block_id:
                    count += 1
                    block_pop = int(other_block[1])
                    print('Found {}%'.format(round(100 * (count / tot), 3)))
                    block['properties']['pop'] = block_pop
                    break

    with open('census_hp_blocks_pop.geojson', 'w') as outfile:
        json.dump(geojs, outfile)
        print('New JSON file written')


def merge_crime(*keywords, make_csv = False, 
                cpd = 'foundation/cpd/CPD_in_UCPD_zone_2011-2015.csv', 
                infile = 'foundation/census_hp_blocks_pop.geojson', 
                outfile = 'ready/hp_blocks_pop_'):
    '''
    This function takes crimes that contain the given keyword and merges them
    into the census tract polygons within the geojson file

    Inputs:
        keyword: string(s) to filter Incident reports by
        infile: string indicating the source file for the census track block 
                polygons with population counts (2010)
        outfile: string indicating the output file with the merged crime data

    Ouputs:
        None: Writes a geojson file with merged crime data.
    '''
    ucpd_dataframes = {}
    for kw in keywords:
        if kw == '':
            title = 'incident_reports'
        else:
            title = kw
        ucpd_dataframes[title] = pandit.make_kw_df(kw, write = make_csv)
    num_types = len(ucpd_dataframes)

    with open(infile, 'r') as f:
        geojs = json.load(f)

    
    for kw, kw_df in ucpd_dataframes.items():
        num_processed = 0
        tot = len(kw_df.values)
        
        for loc, lon, lat, report_date, disp in zip(kw_df.Location, kw_df.LON, 
                                                    kw_df.LAT, 
                                                    kw_df.Reported,
                                                    kw_df.Disposition):
            yr = report_date[-2:]
            if (11 <= int(yr) <= 15):
                point = Point(lon, lat)
                found = False
                min_dist = float('inf')
                for i, block in enumerate(geojs['features']):
                    polygon = shape(block['geometry'])
                    dist_from_point = polygon.distance(point)

                    if dist_from_point < min_dist:
                        min_dist = dist_from_point
                        closest_tract_index = i

                block = geojs['features'][closest_tract_index]
                block['properties'][kw + '_tot'] = block['properties'].setdefault(kw, 0) + 1
                block['properties'][kw + '_{}'.format(yr)] = block['properties'].setdefault(kw, 0) + 1
                num_processed += 1
                print('{} assigned to {} | {}% done for {}'.format(loc, block['properties']['tract_bloc'], round(100 * (num_processed / tot), 3), kw))

    for 
    with open(outfile + '{}.geojson'.format(num_processed), 'w') as outfile:
        json.dump(geojs, outfile),
        print('File written with code: {}'.format(num_processed))