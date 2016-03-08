# log the data

# log using randomly generated numbers and store them to Azure table storage? 
# or local stoge. 

from pi_helper import * 
import azure 
import spidev, time
from gps import * 

'''
Collect random lat long and bumpiness rating

Send to Azure Table storage 

Send to table with trip name as entry 

'''
spi = spidev.SpiDev()
spi.open(0,0)

session = gps() 
session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)

table_service=connect_to_service()

oldLat = None
oldLon = None 
i = 0 

def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out
    
print "current tables:"
for j in table_service.list_tables():
    print j.name 

table_name = raw_input("Enter table name: ")

create_table_if_does_not_exist(table_name)


while True: 
    x = analog_read(0)
    y = analog_read(1)
    z = analog_read(2)
    print("X=%d\tY=%d\tZ=%d" % (x, y, z))
    
    report = session.next()
    
    colorInt = (int(x/10))
    
    print("colorInt=%d" % (colorInt))
    
    if report.keys()[0] == 'epx':
        lat = float(report['lat'])
        lon = float(report['lon'])
        if oldLat == None:
            oldLat = lat
            oldLon = lon 
        # entry = create_entry(oldLat, oldLon, lat, lon, colorInt)
        entry = create_entry_with_raw_accel(oldLat, oldLon, lat, lon, colorInt, x, y, z)
        oldLat = lat 
        oldLon = lon 
        insert_or_replace_entity_from_pi_azure(table_service, i, entry, table_name, 'default')
        i = i+1 
        print("lat=%f\tlon=%f\ttime=%s" % (lat, lon, report['time']))
        time.sleep(0.5)
    else:
        print('no gps' , report.keys()[0])
        time.sleep(1.0)