#!/usr/bin/env python '''This version of the readserial program demonstrates using python to write an output file'''
import pynmea2
import os
import RPi.GPIO as GPIO
import datetime
import serial
import io
import time
#from time import sleep, time
import math
import struct


#configure serial
ser = serial.Serial('/dev/serial0',9600, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1), encoding='ascii', newline='\r')
first = True
#readdestination
LatB = input("Destination latitute:")
LonB = input("Destination longitude:")
lonB = float(LonB)
latB = float(LatB)
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

datastring = sio.readline()
isRunning = True
global currLat
global currLon
currLat = 2.2000
currLon = 1.2000

def main():
    currLat = 2.2000
    currLon = 1.2000
    isRunning = True
    first = True
    while True:
        reload(time)
        time.sleep(0.1)	
        print("working??")
        #start recording GPS data
        if not NearDest():
            print("recording")
            #define output file
            millis = int(round(time.time() * 1000))
            outfile = './Files/gps-log-'+str(millis)+'.nmea'	
            with open(outfile,'a') as f:
                while isRunning:
                    time.sleep(0.1)
                    datastring = sio.readline()
                    comp = "$GPRM"
                    if datastring[1:6] == comp :
                        msg = pynmea2.parse(datastring)
                        print("ONE")
                        print(datastring)
                        print(msg.longitude)
                        print(msg.latitude)
                        currLat = msg.latitude
                        currLon = msg.longitude
                        print("TWO")
                        print(currLat)
                        print(currLon)
                        if first:
                            dest0 = open("./Files/Start_lat.bin","wb")
                            dest1 = open("./Files/Start_lon.bin","wb")
                            dest0.close ()
                            dest1.close ()
                            dest0 = open("./Files/Start_lat.bin","wb")
                            dest1 = open("./Files/Start_lon.bin","wb")
                            format = "f"
                            print("THREE")
                            print(currLat)
                            print(currLon)
                            data0 = struct.pack(format, currLat)
                            data1 = struct.pack(format, currLon)
                            dest0.write(data0)
                            dest1.write(data1)
                            dest0.close()
                            dest1.close()
                            first = False
                    print("FOUR")
                    print(currLat)
                    print(currLon)
                    f.write(datastring + '\n')
                    f.flush()

                    if NearDest():
                        f.close()
                        isRunning = False			
                        print("stop recording")
                        #write turn direction in file
                        f = open("./Files/Direction.txt", "a")
                        f.write("stop")
                        f.close()
	
	#shutdown
        elif NearDest():
            break;

#check if drone is near destination
def NearDest():
    isThere = 0
    if math.fabs(currLat - latB)<= 0.01 and math.fabs(currLon - lonB) <= 0.01:
        print(math.fabs(currLat - latB))
        print(currLat)
        isThere = 0
    return isThere

main()
