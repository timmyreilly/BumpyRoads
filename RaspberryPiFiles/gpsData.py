import os, time, threading 
from gps import * 


gpsd = None 

os.system('clear')

class GpsPoller(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd 
        gpsd = gps(mode=WATCH_ENABLE)
        self.current_value = None 
        self.running = True 
        
    def run(self):
        global gpsd 
        while gpsd.running:
            gpsd.next() 
            
if __name__ == '__main__':
    gpsp = GpsPoller() 
    try: 
        gpsp.start()
        while True:
            os.system('clear')
            
            print 
            print 'GPS reading'
            print '-----------------------'
            print 'latitude      ', gpsd.fix.latitude
            print 'longitude     ', gpsd.fix.longitude
            
        
    except (KeyboardInterrupt, SystemExit):
        print "\nKilling Thread..."
        gpsp.running = False 
        gpsp.join() 
        
    print "Done.\nExiting" 