# log the data

# log using randomly generated numbers and store them to Azure table storage? 
# or local stoge. 

from pi_helper import * 
from accelerometer_bumps import * 
import azure 
import spidev, time, math, sys 
from gps import * 

'''
Collect random lat long and bumpiness rating

Send to Azure Table storage 

Send to table with trip name as entry 

'''
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
    

for j in table_service.list_tables():
    print j.name 

print "^^ current tables ^^"

table_name = raw_input("Enter table name: ")

create_table_if_does_not_exist(table_name)

report = session.next() 

while True: 
    if report.keys()[0] == 'epx':
        j = 1 
        b_index = 0 
        b_average = 0
        while True:
            b_index = get_quarter_second_of_data() # returns number between 1 - 10 
            b_average = b_index/i 
            j = j + 1 
            report = session.next() 
            if report.keys()[0] == 'epx':
                break 
        lat = float(report['lat'])
        lon = float(report['lon'])
        if oldLat == None: 
            oldLat = lat 
            oldLon = lon 
        entry = create_entry_with_raw_accel(oldLat, oldLon, lat, lon, b_average, x, y, z)
        insert_or_replace_entity_from_pi_azure(table_service, i, entry, table_name, 'default')
        oldLat = lat 
        oldLon = lon 
        i = i + 1 
        print("lat=%f\tlon=%f\ttime=%s" % (lat, lon, report['time']))
    else: 
        time.sleep(0.2)
        print('no gps', report.keys())
        report = session.next() 

