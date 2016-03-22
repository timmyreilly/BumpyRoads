# log the data

# log using randomly generated numbers and store them to Azure table storage? 
# or local stoge. 

from pi_helper import * 
from accelerometer import * 
import azure 
import spidev, time, math, sys 
from gps_poll import * 

'''
Collect random lat long and bumpiness rating

Send to Azure Table storage 

Send to table with trip name as entry 

'''


def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out
    

 

if __name__ == '__main__':

    table_service=connect_to_service()
    oldLat = None
    oldLon = None 
    i = 0 
    
    for j in table_service.list_tables():
        print j.name 
    print "^^ current tables ^^"
    table_name = raw_input("Enter table name: ")
    create_table_if_does_not_exist(table_name)

    gpsp = GpsPoller()
    
    try: 
        gpsp.start()
        while True: 
            #os.system('clear')
            report = gpsp.get_current_value()
            try:
                if report.keys()[0] == 'epv':
                    j = 1
                    b_index = 0 
                    b_average = 0 
                    while True:
                        b_index = get_quarter_second_of_data()
                        b_average = b_index/j 
                        j = j + 1 
                        report = gpsp.get_current_value()
                        if report.keys[0] == 'epv':
                            break 
                    lat = float(report['lat'])
                    lon = float(report['lat'])
                    if oldLat == None: 
                        oldLat = lat 
                        oldLon = lon 
                    entry = create_entry(oldLat, oldLon, lat, lon, b_average)
                    insert_or_replace_entity_from_pi_azure(table_service, i, entry, table_name, 'default')
                    oldLat = lat 
                    oldLon = lon 
                    i = i + 1 
                else:
                    print('no gps right meow', report.keys())
            except(AttributeError, KeyError):
                pass        
    except(KeyboardInterrupt, SystemExit):
        gpsp.running = False 
        gpsp.join()
        print "\nKilling Thread.."
        
        
    print "Done.\nExiting."