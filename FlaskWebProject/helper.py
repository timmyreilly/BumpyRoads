import random 

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
        
    