# log using randomly generated numbers and store them to Azure table storage? 
# or local stoge. 

from pi_helper import * 
import azure 
import time


'''
Collect random lat long and bumpiness rating

Send to Azure Table storage 

Send to table with trip name as entry 

'''

table_service=connect_to_service()

oldLat = None
oldLon = None 
i = 0 



table_name = raw_input("Enter table name: ")

create_table_if_does_not_exist_windows(table_name)


while True: 
    x = get_random_accel_data()
    y = get_random_accel_data()
    z = get_random_accel_data()
    print("X=%d\tY=%d\tZ=%d" % (x, y, z))
        
    colorInt = get_random_color_int()
    
    print("colorInt=%d" % (colorInt))
    
    if True:
        lat = get_random_lat()
        lon = get_random_long()
        if oldLat == None:
            oldLat = lat
            oldLon = lon 
        entry = create_entry(oldLat, oldLon, lat, lon, colorInt)
        oldLat = lat 
        oldLon = lon 
        insert_or_replace_entity_to_azure(table_service, i, entry, table_name, 'default')
        i = i+1 
        print("lat=%f\tlon=%f\ttime=%s" % (lat, lon, time.time()))
        time.sleep(0.5)
    else:
        print('no gps')
        time.sleep(1.0)