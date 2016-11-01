# Clean the scarped UCPD Data

import csv

INVALID = ['Unknown', 'Out of Area', 'void', 'Void', 'IN', 'N/A', 'Location', 'Joliet', 'Campus Area', 'UC Campus', '61st to 65th / Cottage Grove to University', 'Various Campus Buildings', 'Quad - Haskell, Harper, Stuart, Wieboldt']


thing = []
with open('ucpd_daily_incidents.csv', 'r') as inp, open('ucpd_daily_incidents_clean.csv', 'w') as out:
    reader = csv.reader(inp)

    fieldnames = []
    tot, empty = 0, 0 
    for row in reader:
        tot += 1
        if not fieldnames:
            fieldnames = row
            writer = csv.writer(out)
            writer.writerow(fieldnames)
        
        if len(row) > 1:
            if (row[0] in [':', 'VOID', 'No Incident Reports this Date']) or row[1] == '':
                empty += 1
            elif tot != 1: # Don't double write header row
                bad_addr = False
                for word in INVALID:
                    if word in row[1]:
                        empty += 1
                        bad_addr = True
                        print('Bad address: {}'.format(row[1]))
                        break
                if not bad_addr:
                    row[1] = row[1].replace(' and', '&')
                    row[1] = row[1].replace('at', '&')
                    row[1] = row[1].replace('near', '&')
                    writer.writerow(row)
        else:
            print('Stupid row found\n', row)
        


    print("{} Empty entries out of {} Total".format(empty, tot))



    
