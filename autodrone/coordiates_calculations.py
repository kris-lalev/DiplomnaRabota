
from math import pi, atan2, radians, cos, sin, asin, sqrt, degrees, acos
import struct

#readdestination
dest = open("./Files/Destination_lon.bin", "rb")
data = dest.read()
dest.close()
format = "f"
LonB, = struct.unpack(format, data) # note the ',' in 'value,': unpack  returns a n-uple

dest = open("./Files/Destination_lat.bin", "rb")
data = dest.read()
dest.close()
LatB, = struct.unpack(format, data)

dest = open("./Files/Start_lon.bin", "rb")
data = dest.read()
dest.close()
format = "f"
LonA, = struct.unpack(format, data) # note the ',' in 'value,': unpack  returns a n-uple

dest = open("./Files/Start_lat.bin", "rb")
data = dest.read()
dest.close()
LatA, = struct.unpack(format, data)

print("Strat latitude is:" + str(LatA))
print("Strat longitude is:" + str(LonA))
print("Dest latitude is:" + str(LatB))
print("Dest longitude is:" + str(LonB))


LatC =90  #Nort pole ; in need of a triangle
LonC = 0
sideAB = 0
sideAC = 0
sideBC = 0
turnHor = "none"
turnVer = "none"
angle = 0
angle2 = 0
angle3 = 0
r = 6371 # Radius of earth in kilometers. Use 3956 for miles

def hav(x):
        x = sin(0.5 * x) * sin(0.5 * x)
        return x
def inhav(x):
        a = 2 * asin(sqrt(x)) 
        return a
def haversineFormula(lon1, lat1, lon2, lat2):

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

     #haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    return c * r *1000 #meters

def findAngle():
    global angle
    sideAB_r = ((sideAB/1000)/(r*2*pi))*2*pi
    sideAC_r = ((sideAC/1000)/(2*pi*r))*2*pi
    sideBC_r = ((sideBC/1000)/(2*pi*r))*2*pi
    #print(sideAB_r)
    #print(sideAC_r)
    #print(sideBC_r)
    #angle = (hav(sideBC_r) - hav(sideAB_r - sideAC_r)) / (sin(sideAB_r)*sin(sideAC_r)) #This gives us hav(angle)
    #angle = inhav(angle)
    #print(angle)
    #angle = degrees(2.96634)
    #print(angle)
    
    angle2 = (cos(sideBC_r) - (cos(sideAC_r) * cos(sideAB_r))) / (sin(sideAC_r) * sin(sideAB_r))
    angle2 = acos(angle2)
    angle2 = degrees(angle2)
    print(angle2)

    angle = (cos(sideAC_r) - (cos(sideAB_r) * cos(sideBC_r))) / (sin(sideAB_r) * sin(sideBC_r))
    angle = acos(angle)
    angle = degrees(angle)
    print(angle)

    angle3 = (cos(sideAB_r) - (cos(sideAC_r) * cos(sideBC_r))) / (sin(sideAC_r) * sin(sideBC_r))
    angle3 = acos(angle3)
    angle3 = degrees(angle3)
    print(angle3)

def NEQ():
    global turnVer
    global turnHor
    global angle
    global sideAB
    global sideAB2
    global sideAC
    global sideBC
    if LonA > LonB: #dest is left
        turnHor = "left"
    elif LonA < LonB: #dest is right
        turnHor = "right"   #dest is directly forward or backward
                             

    if LatA > LatB: #dest is backward
        turnVer = "backward"
    elif LatA < LatB: #dest is forward
        turnVer = "forward"
    elif (LatA == LatB) & (LonA != LonB): #dest is directly left or right
        angle = 90.0000000000

    sideAB = haversineFormula(LonA, LatA, LonB, LatB)
    #if(turnVer != "none") & (turnHor != "none"):
    sideAC = haversineFormula(LatA, LonA, LatC, LonC)
    sideBC = haversineFormula(LatB, LonB, LatC, LonC)
    if(turnVer == "backward") & (turnHor == "none"):
        angle = 180
    elif(turnVer == "forward") & (turnHor == "none"):
        angle = 0

def main():
    NEQ()
    if angle == 0:
        findAngle()
    print('Turn '+ str(turnVer) + '&' + str(turnHor) + ' at ' + str(angle) + ' degrees')
    print('Distance from A to B is ' + str(sideAB) + ' meters')
    print('Distance from A to North pole is ' + str(sideAC) + ' meters')
    print('Distance from B to North pole is ' + str(sideBC) + ' meters')
    #write angle in file
    out = open("./Files/Angle.bin", "wb")    # note: 'b' for binary mode, important on Windows
    format = "f"                   # one float
    data = struct.pack(format, angle) # pack float in a binary string
    out.write(data)
    #out.write(turnHor.encode('ascii'))
    out.close()   
    #write destination in file
    #write turn direction in file
    f = open("./Files/Direction.txt", "a")
    f.write(turnHor)
    f.close()

                       
main()
