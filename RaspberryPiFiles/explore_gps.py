import os, time
import threading
from gps import *  

class GpsPoller(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.session = gps() 
        self.session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)
        self.current_value = None
        self.exitApp = False 
        
    def get_current_value(self):
        return self.current_value
        
    def time_to_exit():
        exitApp = True 
        os._exit()
        
    def run(self):
        while not self.exitApp: 
            try:
                while True:
                    self.current_value = self.session.next()
            except StopIteration:
                pass 
        os._exit() 
            
if __name__ == '__main__':
    gpsp = GpsPoller()
    gpsp.start()
    
    while 1:
        try:
            time.sleep(.5)
            print gpsp.get_current_value()  
        except KeyboardInterrupt:
            gpsdp.time_to_exit()