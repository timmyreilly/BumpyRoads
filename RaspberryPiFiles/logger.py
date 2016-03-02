# log the data

import os 

if os.name == 'posix':
    print 'on pi'
else:
    print 'on nt' 