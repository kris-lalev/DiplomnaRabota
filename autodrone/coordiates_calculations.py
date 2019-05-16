
from math import pi, atan2, radians, cos, sin, asin, sqrt
import struct

LatA = 49.8587 #current
LonA = 17.8522
LatB_In = input("Destination latitute:") #destination
LonB_In = input("Destination longitute:")
LatB = float(LatB_In)
LonB = float(LonB_In)
LatC = 90 #Nort pole ; in need of a triangle
LonC = 0
sideAB = 0
sideAC = 0
sideBC = 0
turnHor = "none"
turnVer = "none"
angle = 0
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

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    return c * r *1000 #meters

def findAngle():
    global angle
    sideAB_r = (sideAB/1000)/r
    sideAC_r = (sideAC/1000)/r
    sideBC_r = (sideBC/1000)/r
    angle = (hav(sideBC_r) - hav(sideAB_r - sideAC_r)) / (sin(sideAB_r)*sin(sideAC_r)) #This gives us hav(angle)
    angle = inhav(angle)
    angle = angle*(180 / pi)

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
    a = 20
    a = hav(a)
    a= inhav(a)
    print (a)
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
    dest0 = open("./Files/Destination_lat.bin","wb")
    dest1 = open("./Files/Destination_lon.bin","wb")
    format = "f"
    data0 = struct.pack(format, LatB)
    data1 = struct.pack(format, LonB)
    dest0.write(data0)
    dest1.write(data1)
    dest0.close()
    dest1.close()
    #write turn direction in file
    f = open("./Files/Direction.txt", "a")
    f.write(turnHor)
    f.close()

                       
main()
