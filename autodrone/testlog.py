#!/usr/bin/env python '''This version of the readserial program demonstrates using python to write an output file'''

import os
import datetime
import serial
import time
import io
from time import sleep
import math
import struct


#configure serial
#ser = serial.Serial('/dev/ttyAMA0',9600, timeout=1)
#sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1), encoding='ascii', newline='\r')
port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
print("recording")
#datastring = sio.readline()
#with open("Start.txt",'a') as g:
# g.write(datastring)
# g.flush() g.close()
#print(datastring)

port.write("\r\nSay something:")
print("test")
rcv = port.read(10)
port.write("\r\nYou sent:" + repr(rcv))
