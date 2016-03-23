import random 
from azure.storage.table import TableService, Entity
import os

TABLE_STORAGE_KEY = os.getenv('AZURE_STORAGE_KEY')
STORAGE_NAME = os.getenv('STORAGE_NAME')

if TABLE_STORAGE_KEY == None:
    from tokens import *  
    TABLE_STORAGE_KEY = TABLE_STORAGE_ACCESS_KEY
    STORAGE_NAME = STORAGE_ACCOUNT_NAME

#implemented in azure_managed
def connect_to_service():
    table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=TABLE_STORAGE_KEY)
    print TableService
    return table_service 


def get_random_lat():
    return random.uniform(37,38)
    
def get_random_long():
    return random.uniform(-122,-123)
    
def get_random_color_list():
    return [random.randint(50,100), random.randint(50,150), random.randint(50,200), random.randint(100,200)]

def get_random_accel_data():
    return random.randint(0, 255)

def get_random_color_int():
    return random.randint(0,7)
    
def load_table(max=10, table_service=connect_to_service(), table_name='test', partitionKey='default'):
    for i in range(max):
        entry = create_random_entry() 
        insert_entry_to_azure(table_service, i, entry, table_name='test', partitionKey='default')
        print entry 

def clear_table(max=10, table_service=connect_to_service(), table_name='test', partitionKey='default'):
    for i in range(max):
        print i 
        table_service.delete_entity(table_name, partitionKey, i)

#implemented in azure_managed    
def get_table_list(table_service, max=10, table_name='test', partitionKey='default'):
    x = table_service.query_entities(table_name)
    print(x)
    return x 

def create_table_if_doesnt_exist(table_name, table_service=connect_to_service()):
    if does_table_exist(table_name):
        return 'already exists'
    else:
        table_service.create_table(table_name)
        return 'now it exists'
        
#implemented in azure_managed
def create_table_if_does_not_exist(table_name, table_service=connect_to_service()):
    if does_table_exist_pi(table_name):
        return 'already exists'
    else:
        table_service.create_table(table_name)
        return 'now it exists'

#implemented in azure_managed        
def create_table_if_does_not_exist_windows(table_name, table_service=connect_to_service()):
    if does_table_exist(table_name):
        return 'already exists'
    else:
        table_service.create_table(table_name)
        return 'now it exists'

#implemented in azure_managed    
def does_table_exist(table_name, table_service=connect_to_service()):
    for i in table_service.query_tables():
        if i.name == table_name:
            return True
    return False 

#implemented in azure_managed    
def does_table_exist_pi(table_name, table_service=connect_to_service()):
    for i in table_service.list_tables():
        if i.name == table_name:
            return True
    return False 
    

def get_lat_long_random(x):
    list = []
    for i in range(0,x): 
        list.append(
            {
                "list_a":[get_random_lat(), get_random_long()],
                "list_b":[get_random_lat(), get_random_long()],
                "color":get_random_color_int()
            }
        )
    return list 

def get_entry_two(table_service, rowKey, table_name='test', partitionKey='default'):
    x = table_service.get_entity(table_name, partitionKey, rowKey)
    list = []
    list.append(
        {
            "list_a":[float(x.latA), float(x.longA)],
            "list_b":[float(x.latB), float(x.longB)],
            "color":int(x.colorKey)
        }
    )
    print list 
    return list 

def get_entry(table_service, rowKey, table_name='test', partitionKey='default'):
    x = table_service.get_entity(table_name, partitionKey, rowKey)
    print x.latA 
    print x.RowKey
    return x 

def create_random_entry():
    x = {
        'latA':get_random_lat(),
        'longA':get_random_long(),
        'latB':get_random_lat(),
        'longB':get_random_long(),
        'color': get_random_color_int()
    }
    return x 
def create_entry(latA, lonA, latB, lonB, bumpiness):
    x = {
        'latA':latA,
        'longA':lonA,
        'latB':latB,
        'longB':lonB,
        'color': bumpiness
    }
    return x 

def create_entry_with_raw_accel(latA, lonA, latB, lonB, bumpiness, x, y, z):
    x = {
        'latA':latA,
        'longA':lonA,
        'latB':lbatB,
        'longB':lonB,
        'color': bumpiness,
        'x': x,
        'y': y,
        'z': z 
    }
    return x 

def insert_or_replace_entity_to_azure(table_service, rowKey, entry, table_name='test', partitionKey='default'):
    '''
    takes table service
    
    Takes a list 
    Uploads to azure table storage 
    '''
    segment = Entity()
    segment.PartitionKey = partitionKey
    segment.RowKey = str(rowKey).zfill(8)
    rowKey = str(rowKey).zfill(8)
    segment.latA = str(entry['latA'])
    segment.longA = str(entry['longA'])
    segment.latB = str(entry['latB'])
    segment.longB = str(entry['longB'])
    segment.colorKey = str(entry['color'])
    if entry['x']:
        segment.x = str(entry['x'])
        segment.y = str(entry['y'])
        segment.z = str(entry['z'])

    print segment
    table_service.insert_or_replace_entity(table_name, partitionKey, rowKey, segment) 
    
def insert_or_replace_entity_from_pi_azure_raw_accel(table_service, rowKey, entry, table_name='test', partitionKey='default'):
    '''
    takes table service
    
    Takes a list 
    Uploads to azure table storage 
    '''
    segment = Entity()
    segment.PartitionKey = partitionKey
    segment.RowKey = str(rowKey).zfill(8)
    segment.latA = str(entry['latA'])
    segment.longA = str(entry['longA'])
    segment.latB = str(entry['latB'])
    segment.longB = str(entry['longB'])
    segment.colorKey = str(entry['color'])
    if entry['x']:
        segment.x = str(entry['x'])
        segment.y = str(entry['y'])
        segment.z = str(entry['z'])
        
    print segment
    table_service.insert_or_replace_entity(table_name, segment) 

#implemented in azure_managed
def insert_or_replace_entity_from_pi_azure(table_service, rowKey, entry, table_name='test', partitionKey='default'):
    '''
    takes table service
    
    Takes a list 
    Uploads to azure table storage 
    '''
    segment = Entity()
    segment.PartitionKey = partitionKey
    segment.RowKey = str(rowKey).zfill(8)
    segment.latA = str(entry['latA'])
    segment.longA = str(entry['longA'])
    segment.latB = str(entry['latB'])
    segment.longB = str(entry['longB'])
    segment.colorKey = str(entry['color'])
        
    #print segment.colorKey 
    
    table_service.insert_or_replace_entity(table_name, segment) 
          
#implemented in azure_managed   
def update_entity_to_azure(table_service, rowKey, entry, table_name='test', partitionKey='default'):
    '''
    takes table service
    
    Takes a list 
    Uploads to azure table storage 
    '''
    segment = Entity()
    segment.PartitionKey = partitionKey
    segment.RowKey = str(rowKey).zfill(8)
    segment.latA = str(entry['latA'])
    segment.longA = str(entry['longA'])
    segment.latB = str(entry['latB'])
    segment.longB = str(entry['longB'])
    segment.colorKey = str(entry['color'])

    print segment
    table_service.update_entity(table_name, segment)     

def insert_entry_to_azure(table_service, rowKey, entry, table_name='test', partitionKey='default'):
    '''
    takes table service
    
    Takes a list 
    Uploads to azure table storage 
    '''
    segment = Entity()
    segment.PartitionKey = partitionKey
    segment.RowKey = str(rowKey).zfill(8)
    segment.latA = str(entry['latA'])
    segment.longA = str(entry['longA'])
    segment.latB = str(entry['latB'])
    segment.longB = str(entry['longB'])
    segment.colorKey = str(entry['color'])

    print segment
    table_service.insert_entity(table_name, segment)
    
#implemented in azure_managed    
def create_table(name, table_service=connect_to_service()):
    '''
    table_service = TableService(account_name='myaccount', account_key='mykey')

    table_service.create_table('tasktable')
    '''
    table_service.create_table(name)

#implemented in azure_managed    
def delete_entity(rowKey, table_service=connect_to_service(), table_name='test', partitionKey='default'):
    table_service.delete_entity(table_name, partitionKey, rowKey)

#implemented in azure_managed
def delete_table(name, table_service=connect_to_service()):
    return table_service.delete_table(name)
    



### 