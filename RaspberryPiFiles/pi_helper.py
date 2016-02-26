import random 
from azure.storage.table import TableService, Entity
import os

TABLE_STORAGE_KEY = os.getenv('AZURE_STORAGE_KEY')
STORAGE_NAME = os.getenv('STORAGE_NAME')

if TABLE_STORAGE_KEY == None:
    from tokens import *  
    TABLE_STORAGE_KEY = TABLE_STORAGE_ACCESS_KEY
    STORAGE_NAME = STORAGE_ACCOUNT_NAME


def get_random_lat():
    return random.uniform(30,40)
    
def get_random_long():
    return random.uniform(120,140)
    
def get_random_color_list():
    return [random.randint(50,100), random.randint(50,150), random.randint(50,200), random.randint(100,200)]

def get_random_color_int():
    return random.randint(0,7)
    
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

def create_entry():
    x = {
        'latA':get_random_lat(),
        'longA':get_random_long(),
        'latB':get_random_lat(),
        'longB':get_random_long(),
        'color': get_random_color_int()
    }
    return x 

def insert_or_update_entity_to_azure(table_service, rowKey, entry, table_name='test', partitionKey='default'):
    '''
    takes table service
    
    Takes a list 
    Uploads to azure table storage 
    '''
    segment = Entity()
    segment.PartitionKey = partitionKey
    segment.RowKey = str(rowKey)
    segment.latA = str(entry['latA'])
    segment.longA = str(entry['longA'])
    segment.latB = str(entry['latB'])
    segment.longB = str(entry['longB'])
    segment.colorKey = str(entry['color'])

    print segment
    table_service.insert_or_replace_entity(table_name, segment)    

def insert_entry_to_azure(table_service, rowKey, entry, table_name='test', partitionKey='default'):
    '''
    takes table service
    
    Takes a list 
    Uploads to azure table storage 
    '''
    segment = Entity()
    segment.PartitionKey = partitionKey
    segment.RowKey = str(rowKey)
    segment.latA = str(entry['latA'])
    segment.longA = str(entry['longA'])
    segment.latB = str(entry['latB'])
    segment.longB = str(entry['longB'])
    segment.colorKey = str(entry['color'])

    print segment
    #table_service.insert_or_replace_entity(table_name, segment)
    table_service.insert_entity(table_name, segment)
    
    
def create_table(name, table_service):
    '''
    table_service = TableService(account_name='myaccount', account_key='mykey')

    table_service.create_table('tasktable')
    '''
    table_service.create_table(name)

def delete_table(name):
    table_service.delete_table('tasktable')
    
def connect_to_service():
    table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=TABLE_STORAGE_KEY)
    print TableService
    return table_service 
