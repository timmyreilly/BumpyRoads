import os, time
import threading
from gps import *  

class GpsPoller(threading.Thread):

    def __init__(self):
        
        threading.Thread.__init__(self)
        self.session = gps() 
        self.session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)
        self.current_value = None
        
    def get_current_value(self):
        return self.current_value
        
    def run(self):
        try:
            while True:
                self.current_value = self.session.next()
        except StopIteration:
            pass 
            
if __name__ == '__main__':
    gpsp = GpsPoller()
    gpsp.start()
    
    while 1:
        time.sleep(.5)
        print gpsp.get_current_value() 