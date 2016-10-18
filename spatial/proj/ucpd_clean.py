# Clean the scarped UCPD Data

import csv

thing = []
with open('ucpd_daily_incidents.csv', 'r') as inp, open('ucpd_daily_incidents_clean.csv', 'w') as out:
    reader = csv.reader(inp)

    fieldnames = []
    tot, empty = 0, 0 
    for row in reader:
        if not fieldnames:
            fieldnames = row
            writer = csv.writer(out)
            writer.writerow(fieldnames)

        tot += 1
        if row[0] in [':', 'VOID']:
            empty += 1
            print('Empty row found')
        elif tot != 1: # Don't double write header row
            writer.writerow(row)
            print('Row written to cleaned version')

    print("{} Empty entries out of {} Total".format(empty, tot))



    
