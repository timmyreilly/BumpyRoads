from accelerometer import * 
from azure_managed import * 
from gps_poll import *
import azure 
import spidev, time, math, sys 

if __name__ == '__main__':

    azure_table = az() 
    
    oldLat = None
    oldLon = None
    i = 0 
    
    azure_table.list_tables()
    print "Current Tables ^ "
    table_name = raw_input("Enter table name: ")
    azure_table.create_table_if_does_not_exist(table_name)
    
    gpsp = GpsPoller()
    
    try:
        gpsp.start()
        while True:
            report = gpsp.get_current_value()
            try:
                if 'lat' in report.keys():
                    j = 1 
                    b_index = 0 
                    b_average = 0 
                    while True:
                        b_index = get_quarter_second_of_data()
                        b_average = b_index/j 
                        j = j + 1 
                        report = gpsp.get_current_value()
                        if 'lat' in report.keys():
                            break
                    lat = float(report['lat'])
                    lon = float(report['lon'])
                    if oldLat = None:
                        oldLat = lat
                        oldLon = lon 
                    entry = azure_table.create_entry(oldLat, oldLon, lat, lon, b_average)
                    print entry 
                    azure_table.insert_or_replace_entity_to_azure(i, entry, table_name, 'default')
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
        print "\nKilling Thread..."
        
    

    
