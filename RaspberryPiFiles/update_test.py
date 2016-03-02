from pi_helper import *

table_service=connect_to_service()
MAX = 20 

while True:
    entry = create_random_entry()
    for i in range(MAX):
        insert_or_replace_entity_to_azure(table_service, i, entry, 'test', 'default')
        print entry 
