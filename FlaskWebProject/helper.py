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
    return table_service 

def get_table_entities(table_service=connect_to_service(), max=10, table_name='test', partitionKey='default'):
    x = table_service.query_entities(table_name)
    #print(x)
    return x 
    
def get_json_list(entity_list=get_table_entities()):
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

def get_data_from_table(table_name, table_service=connect_to_service()):
    entity_list = table_service.query_entities(table_name)
    i = 0 
    response = []
    for r in entity_list:
        c = smart_color_key(int(entity_list[i].colorKey))
        #print c 
        t = (entity_list[i].latA, entity_list[i].longA, entity_list[i].latB, entity_list[i].longB, entity_list[i].colorKey, c[0], c[1], c[2])
        response.append(t)
        i += 1 
    #print response 
    return response   

def get_all_tables_list(table_service=connect_to_service()):
    '''
    Return data from all tables 
    '''
    routes_list = []
    for i in table_service.query_tables():
        print i.name
        routes_list.append(json.dumps(get_data_from_table(i.name)))
        
    return routes_list
        
        
def smart_color_key(colorKey):
    red = (255 * colorKey) / 25
    green = (255 * (25 - colorKey)) / 25
    blue = 0 
    return [red, green, blue]
        
        

def convert_color_key_to_rgb(colorKey):
    return {
        0: [0, 255, 0], 
        1: [0, 255, 80],
        2: [0, 255, 160],
        3: [0, 255, 255],
        4: [0, 160, 255],
        5: [0, 80, 255],
        6: [0, 0, 255],
        7: [140, 0, 255],
        8: [255, 0, 255],
        9: [255, 0, 204],
        10: [255, 0, 162],
        11: [255, 0, 102],
        12: [255, 0, 0]
    }.get(colorKey, [255, 0, 0] )

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
        
    