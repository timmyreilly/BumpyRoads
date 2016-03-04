import spidev, time
from gps import * 
from pi_helper import *

spi = spidev.SpiDev()
spi.open(0,0)

session = gps() 
session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)

table_service=connect_to_service()
MAX = 200

oldLat = None
oldLon = None 


def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out
    
def get_normalized_number(lists, x, y, z):
    lists.pop()
    lists.insert(0, [x,y,z])
    average = 0 
    return 

while True:
    for i in range(MAX):
        x = analog_read(0)
        y = analog_read(1)
        z = analog_read(2)
        print("X=%d\tY=%d\tZ=%d" % (x, y, z))
        
        report = session.next()
        
        colorInt = (int(x/10))
        print("colorInt=%d" % (x))
        time.sleep(0.2)
        if report.keys()[0] == 'epx':
            lat = float(report['lat'])
            lon = float(report['lon'])
            if oldLat == None:
                oldLat = lat
                oldLon = lon 
            entry = create_entry(oldLat, oldLon, lat, lon, colorInt)
            oldLat = lat 
            oldLon = lon 
            insert_or_replace_entity_from_pi_azure(table_service, i, entry, 'test', 'default')
            print("lat=%f\tlon=%f\ttime=%s" % (lat, lon, report['time']))
        else:
            print('no gps' , report.keys()[0])
    
    




