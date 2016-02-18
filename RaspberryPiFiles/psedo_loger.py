# log using randomly generated numbers and store them to Azure table storage? 
# or local stoge. 

from helper import * 
import azure 

'''
Collect random lat long and bumpiness rating

Send to Azure Table storage 

'''

segment = Entity()
segment.PartitionKey = 'default'
segment.RowKey = '1'
segment.latA = entry['latA']
segment.longA = entry['longA']
segment.latB = entry['latB']
segment.longB = entry['longB']
segment.colorKey = entry['color']

