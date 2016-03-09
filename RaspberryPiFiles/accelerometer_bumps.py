import spidev, time, math, sys

spi = spidev.SpiDev()
spi.open(0,0)

def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out 
    

    
    
ADAPTIVE_ACCEL_FILTER = True 
lastAccel = [0,0,0]
accelFilter = [0,0,0] 

def norm(x, y, z):
    return math.sqrt(x * x + y * y + z * z)
    
def clamp(v, min, max):
    if v > max:
        return max 
    elif v < min: 
        return min 
    else:
        return v 

def onAccelerometerChanged(x, y, z, lastAccel):
    #high pass filter
    updateFreq = 10
    cutOffFreq = 0.9
    RC = 1.0 / cutOffFreq
    dt = 1.0 / updateFreq
    filterConstant = RC / (dt + RC)
    alpha = filterConstant
    kAccelerometerMinStep = 0.033 
    kAccelerometerNoiseAttenuation = 3.0 
    
    if ADAPTIVE_ACCEL_FILTER:
        d = clamp(abs(norm(accelFilter[0], accelFilter[1], accelFilter[2]) - norm(x, y, z)) / kAccelerometerMinStep - 1.0, 0.0, 1.0)
        alpha = d * filterConstant / kAccelerometerNoiseAttenuation + (1.0 - d) * filterConstant
        
    accelFilter[0] = (alpha * (accelFilter[0] + x - lastAccel[0]))
    accelFilter[1] = (alpha * (accelFilter[1] + y - lastAccel[1]))
    accelFilter[2] = (alpha * (accelFilter[2] + z - lastAccel[2]))
    
    lastAccel[0] = x
    lastAccel[1] = y 
    lastAccel[2] = z 
    
    print("lastAccel ", lastAccel)
    print("accelFilter ", accelFilter)
    if accelFilter[0] > 1:
        print "HOLY POOP THATs a SHAKE"
        #sys.exit("HOLY Poop")
        
    onFilteredAccelerometerChanged(accelFilter[0], accelFilter[1], accelFilter[2])
    
    
def onFilteredAccelerometerChanged(x, y, z): 
    print (x, y, z, "x y z")
    if x > 1.0:
        "#### X TOOK A BUMP ####" 
    elif y > 1.0: 
        "#### Y TOOK A BUMP ####"    
    elif z > 1.0: 
        "#### Z TOOK A BUMP ####"
        
    
while True:
    x = analog_read(0)
    y = analog_read(1)
    z = analog_read(2)
    print(" NOT FILTERED? X=%d\tY=%d\tZ=%d" % (x, y, z))
    onAccelerometerChanged(x, y, z, lastAccel)
    time.sleep(0.1)