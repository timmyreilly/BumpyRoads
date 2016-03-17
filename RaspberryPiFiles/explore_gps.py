import gps, os, time
import threading 

class GpsPoller(threading.Thread):

    def __init__(self)
        threader.Thread.__init__(self)
        self.session = gps(mode=WATCH_ENABLE)
        self.current_value = None
        
    def get_current_value(self):
        return self.current_value
        
    def run(self):
        try:
            while True:
                self.current_value = session.next()
        except StopIteration:
            pass 
            
if __name__ == '__main__':
    gpsd = GpsPoller()
    gpsp.start()
    
    while 1:
        time.sleep(3)
        print gpsp.get_current_value() 