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

SMALL_BUMP = 0.8
MED_BUMP = 1.0 
LARGE_BUMP = 2.0 

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
    updateFreq = 5
    cutOffFreq = 0.9
    RC = 1.0 / cutOffFreq
    dt = 1.0 / updateFreq
    filterConstant = RC / (dt + RC)
    alpha = filterConstant
    kAccelerometerMinStep = 0.033 
    kAccelerometerNoiseAttenuation = 3.0 
    
    if ADAPTIVE_ACCEL_FILTER:
        d = clamp(abs(norm(accelFilter[0], accelFilter[1], accelFilter[2]) - norm(x, y, z)) / kAccelerometerMinStep - 1.0, 0.0, 2.0)
        alpha = d * filterConstant / kAccelerometerNoiseAttenuation + (1.0 - d) * filterConstant
        
    accelFilter[0] = (alpha * (accelFilter[0] + x - lastAccel[0]))
    accelFilter[1] = (alpha * (accelFilter[1] + y - lastAccel[1]))
    accelFilter[2] = (alpha * (accelFilter[2] + z - lastAccel[2]))
    
    
    print "lastAccel ", lastAccel
    print "currxyz   ", [x, y, z]  
    print "accelFilter ", accelFilter
    # print "filterConstant: ", filterConstant 
    
    
    lastAccel[0] = x
    lastAccel[1] = y 
    lastAccel[2] = z 
    
    
        
    return onFilteredAccelerometerChanged(accelFilter[0], accelFilter[1], accelFilter[2])
    
    
def onFilteredAccelerometerChanged(x, y, z):
    #print 'abs x: ', abs(x) 
    #print 'jus x: ', x 
    # print (x, y, z, "x y z")
    x = abs(x) 
    y = abs(y)
    z = abs(z) 
    print 'abs x y z: ', x, y, z 
    
    if x > LARGE_BUMP or y > LARGE_BUMP or z > LARGE_BUMP:
        print "LARGE BUMP!", [x, y, z]
        return 3 
    elif x > MED_BUMP or y > MED_BUMP or Z > MED_BUMP:
        print "Medium Bump", [x, y, z]
        return 2 
    elif x > SMALL_BUMP or y > SMALL_BUMP or z > SMALL_BUMP:
        print "small bump", [x, y, z]
        return 1 
    else:
        print "no bump", [x, y, z]
        return 0 
    
        
    
        

def get_quarter_second_of_data(): 
    sum = 0 
    for i in range(5):
        x = analog_read(0)
        y = analog_read(1)
        z = analog_read(2)
        sum = sum + int(onAccelerometerChanged(x, y, z, lastAccel)) 
        time.sleep(0.05)
    return sum 
    
    
while True:
    s = get_quarter_second_of_data()
    print s 

    