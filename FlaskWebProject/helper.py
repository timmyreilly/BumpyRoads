import random, json 
from azure.storage.table import TableService, Entity
import os

TABLE_STORAGE_KEY = os.getenv('AZURE_STORAGE_KEY')
STORAGE_NAME = os.getenv('STORAGE_NAME')

if TABLE_STORAGE_KEY == None:
    from tokens import *  
    TABLE_STORAGE_KEY = TABLE_STORAGE_ACCESS_KEY
    STORAGE_NAME = STORAGE_ACCOUNT_NAME
    
def connect_to_service():
    table_service = TableService(account_name=STORAGE_ACCOUNT_NAME, account_key=TABLE_STORAGE_KEY)
    print TableService
    return table_service 

def get_table_list(table_service=connect_to_service(), max=10, table_name='test', partitionKey='default'):
    x = table_service.query_entities(table_name)
    #print(x)
    return x 
    
def get_json_list(entity_list=get_table_list()):
    '''
    Takes azure table list and returns json list 
    '''
    i = 0 
    response = [] 
    for r in entity_list:
        c = convert_color_key_to_rgb(int(entity_list[i].colorKey))
        t = (entity_list[i].latA, entity_list[i].longA, entity_list[i].latB, entity_list[i].longB, entity_list[i].colorKey, c[0], c[1], c[2])
        response.append(t)
        i += 1 
    # print response 
    return response 
    

def convert_color_key_to_rgb(colorKey):
    return {
        0: [100, 100, 100], 
        1: [240, 0, 255],
        2: [0, 0, 255],
        3: [0, 255, 0],
        4: [255, 255, 0],
        5: [255, 85, 0],
        6: [255, 0, 0],
    }.get(colorKey, [100, 100, 100] )

def get_data():
    d =[
        {
            "list_a": [37.767111,-122.445811],
            "list_b": [37.792111, -122.403611],
            "list_c": [37, -122, 38, -122.445811],
            "color": [200, 200, 0, 100]
        }
    ]
    
    return d 
    
def get_random_lat():
    return random.uniform(30,40)
    
def get_random_long():
    return random.uniform(120,140)
    
def get_random_color_list():
    return [random.randint(50,100), random.randint(50,150), random.randint(50,200), random.randint(100,200)]
    
    
def get_lat_long_dict(x):
    list = []
    for i in range(0,x): 
        list.append(
            {
                "list_a":[get_random_lat(), get_random_long()],
                "list_b":[get_random_lat(), get_random_long()],
                "color":get_random_color_list()
            }
        )
    return list 
        
    