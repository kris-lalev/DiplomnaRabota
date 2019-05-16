import pynmea2
import io
import serial
import time
ser = serial.Serial('/dev/serial0',9600, timeout=1)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1), encoding='ascii', newline='\r')
c = 0
while c<10:
    reload(time)
    time.sleep(1)
    datastring = sio.readline()
    print(c)
    print (datastring)
    print (datastring[1:6])
    comp = "$GPRM"
    if datastring[1:6] == comp :
        print(datastring)
        msg = pynmea2.parse(datastring)
        print(msg.timestamp)
        print(msg.lat)
        print(msg.latitude)
        print(msg.lat_dir)
        c+=1
