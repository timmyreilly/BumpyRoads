from gps_poll import *

if __name__ == '__main__':
    gpsp = GpsPoller()
    try: 
        gpsp.start() 
        while True:
            os.system('clear')
            report = gpsp.get_current_value()
            print report 
            # try: 
            #     if report.keys()[0] == 'epx':
            #         print report 
            #     time.sleep(.5)
            # except(AttributeError, KeyError):
            #     pass 
            
    except(KeyboardInterrupt, SystemExit):
        print "\nKilling Thread.."
        gpsp.running = False 
        gpsp.join()
    
    print "Done.\nExiting." 
        