import random 
from azure.storage.table import TableService, Entity
import os 

DEFAULT_TABLE = 'test'

class az(object):
    
    def __init__(self, default_table_name=DEFAULT_TABLE, partitionKey='default'):
        self.TABLE_STORAGE_KEY = os.getenv('AZURE_STORAGE_KEY')
        self.STORAGE_NAME = os.getenv('STORAGE_NAME')
        self.default_table_name = default_table_name
        self.default_partition = partitionKey 
        if self.TABLE_STORAGE_KEY == None: 
            from tokens import TABLE_STORAGE_ACCESS_KEY, STORAGE_ACCOUNT_NAME
            self.TABLE_STORAGE_KEY = TABLE_STORAGE_ACCESS_KEY
            self.STORAGE_NAME = STORAGE_ACCOUNT_NAME
        self.table_service = TableService(account_name=self.STORAGE_NAME, account_key=self.TABLE_STORAGE_KEY)
        #create_table_if_does_not_exists(self.default_table_name)
        
    def insert_or_replace_entity_to_azure(self, rowKey, entry, t_name=DEFAULT_TABLE):
        '''
        takes table service
        
        Takes a list 
        Uploads to azure table storage 
        '''
        segment = Entity()
        segment.PartitionKey = self.default_partition
        segment.RowKey = str(rowKey).zfill(8)
        segment.latA = str(entry['latA'])
        segment.longA = str(entry['longA'])
        segment.latB = str(entry['latB'])
        segment.longB = str(entry['longB'])
        segment.colorKey = str(entry['color'])
            
        #print segment.colorKey 
        
        if os.name == 'nt':
            self.table_service.insert_or_replace_entity(t_name, self.default_partition, str(rowKey).zfill(8), segment)
        else:
            table_service.insert_or_replace_entity(t_name, segment) 
            
    def create_table(self, name):
        return self.table_service.create_table(name) 
        
    def delete_table(self, name):
        return self.table_service.delete_table(name)
        
    def delete_entity_by_rowKey(self, rowKey, table_name=DEFAULT_TABLE):
        return self.table_service.delete_entity(table_name, self.default_partition, rowKey)
        
        
    def does_table_exist(self, table_name):
        if os.name == 'nt':
            for i in self.table_service.query_tables():
                if i.name == table_name:
                    return True
        else:
            for i in self.table_service.list_tables():
                if i.name == table_name:
                    return True 
        return False 
        
    def list_tables(self):
        if os.name == 'nt':
            for j in self.table_service.query_tables():
                print j.name 
        else:
            for j in self.table_service.list_tables():
                print j.name 
                      
    def create_table_if_does_not_exist(self, table_name=DEFAULT_TABLE):
        if self.does_table_exist(table_name):
            return 'already exists'
        else:
            self.table_service.create_table(table_name)
            
            
    def create_entry(self, latA, lonA, latB, lonB, bumpiness):
        x = {
            'latA':latA,
            'longA':lonA,
            'latB':latB,
            'longB':lonB,
            'color': bumpiness
        }
        return x
        
    def create_random_entry(self):
        x = {
            'latA':random.uniform(37,38),
            'longA':random.uniform(-122,-123),
            'latB':random.uniform(37,38),
            'longB':random.uniform(-122,-123),
            'color': random.randint(0,7)
        }
        return x 
        
    def create_and_insert_or_replace_entity_azure(self, latA, lonA, latB, lonB, bumpiness, rowKey, table_name=DEFAULT_TABLE ):
        return self.insert_or_replace_entity_to_azure(rowKey, create_entry(latA, lonA, latB, lonB, bumpiness), table_name)
        
            
    
            
    
        
            