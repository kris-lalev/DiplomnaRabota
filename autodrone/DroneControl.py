#########
# firstTry.py
# This program is part of the online PS-Drone-API-tutorial on www.playsheep.de/drone.
# It shows how to do basic movements with a Parrot AR.Drone 2.0 using the PS-Drone-API.
# Dependencies: a POSIX OS, PS-Drone-API 2.0 beta or higher.
# (w) J. Philipp de Graaff, www.playsheep.de, 2014
##########
# LICENCE:
#   Artistic License 2.0 as seen on http://opensource.org/licenses/artistic-license-2.0 (retrieved December 2014)
#   Visit www.playsheep.de/drone or see the PS-Drone-API-documentation for an abstract from the Artistic License 2.0.
###########

import time
import ps_drone         # Imports the PS-Drone-API
import struct

check = 0
dest = open("./Files/Angle.bin", "rb")
data = dest.read()
dest.close()
format = "f"
angle, = struct.unpack(format, data) # note the ',' in 'value,': unpack  returns a n-uple
print(angle)

drone = ps_drone.Drone()       # Initializes the PS-Drone-API
drone.startup()   # Connects to the drone and starts subprocesses
drone.setSpeed(0.7)     #Set default moving speed to 50%

drone.takeoff()                # Drone starts
time.sleep(8)                # Gives the drone time to start
filed = open("./Files/Direction.txt","r")
direction = filed.read()
print(direction)
if direction == "right":
    angle = angle - 2*angle
    drone.turnAngle(angle)
    check = 1
if direction == "left":
    drone.turnAngle(angle)
    check = 1
time.sleep(8)
while check == 1: 
    drone.moveForward()
    filed = open("./Files/Direction.txt","r")
    direction = filed.read()
    print("check")
    if direction == "stop":
        check = 1
    
drone.land()                   # Drone lands
