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
        self.report = None 
        
    def run(self):
        global gpsd 
        while gpsd.running:
            self.report = gpsd.next() 
            if report.keys() == 'epx':
                self.current_value = self.report 
            
    def get_current_value(self):
        return self.current_value
            
if __name__ == '__main__':
    gpsp = GpsPoller() 
    try: 
        gpsp.start()
        while True:
            os.system('clear')
            
            print gpsp.get_current_value() 
            
            
            print 
            print 'GPS reading'
            print '-----------------------'
            print 'latitude    ' , gpsd.fix.latitude
            print 'longitude   ' , gpsd.fix.longitude
            print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
            print 'altitude (m)' , gpsd.fix.altitude
            print 'eps         ' , gpsd.fix.eps
            print 'epx         ' , gpsd.fix.epx
            print 'epv         ' , gpsd.fix.epv
            print 'ept         ' , gpsd.fix.ept
            print 'speed (m/s) ' , gpsd.fix.speed
            print 'climb       ' , gpsd.fix.climb
            print 'track       ' , gpsd.fix.track
            print 'mode        ' , gpsd.fix.mode
            print
            print 'sats        ' , gpsd.satellites
            
            time.sleep(2) 

        
    except (KeyboardInterrupt, SystemExit):
        print "\nKilling Thread..."
        gpsp.running = False 
        gpsp.join() 
        
    print "Done.\nExiting" 