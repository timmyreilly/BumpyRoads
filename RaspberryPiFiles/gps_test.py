from gps import * 
from pi_helper import *

session = gps() 
session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)

table_service=connect_to_service()
MAX = 20 

oldLat = None
oldLon = None 

while True:
    for i in range(MAX):
        report = session.next()
        if report.keys()[0] == 'epx':
            lat = float(report['lat'])
            lon = float(report['lon'])
            if oldLat = None:
                oldLat = lat
                oldLon = lon 
            entry = create_entry(oldLat, oldLon, lat, lon, get_random_color_int())
            insert_or_replace_entity_to_azure(table_service, i, entry, 'test', 'default')
            print("lat=%f\tlon=%f\ttime=%s" % (lat, lon, report['time']))
            
            time.sleep(0.5)
