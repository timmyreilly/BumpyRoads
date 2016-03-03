import spidev, time

spi = spidev.SpiDev()
spi.open(0,0)

def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out 
    
while True:
    x = analog_read(0)
    y = analog_read(1)
    z = analog_read(2)
    if x < 450:
        print("left \tX=%d" % (x))
        print (x)
    elif x > 550:
        print("right \tX=%d" % (x))
        print x 
    elif y < 450:
        print("Back \tY=%d" % (y) )
        print y 
    elif y > 550:
        print("Forward \tY=%d" % (y))
        print y 
    time.sleep(0.2)