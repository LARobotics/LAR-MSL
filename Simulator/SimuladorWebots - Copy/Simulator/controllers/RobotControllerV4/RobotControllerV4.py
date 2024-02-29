"""supervisor_controller controller."""

from controller import Supervisor, Keyboard, Connector
from Robot import *
from comms import *
import socket
import time

TIME_STEP = 1
Bport = 2
Aport = 0

supervisor = Supervisor()
RobotName = supervisor.getSelf().getDef()

ROBOTID = int(RobotName[5])
robot = Robot(supervisor, RobotName)
comms = communication(ROBOTID, 2)
print(comms.recvSocket)

#time.sleep(5)
velocity = [0, 0, 0, 0, 0, 0]

loopTime = time.time()
while supervisor.step(TIME_STEP) != -1:
    mens = ""
    try:
        message = comms.recvSocket.recvfrom(1024)
        mens = message[0].decode('utf8', 'strict')
        comms.sendSocket.sendto("a".encode(), comms.SocketAdress2send)
    except:
        pass
    print(RobotName, ": ", mens)
    if mens != "":
        mens = mens.replace("[", "")
        mens = mens.replace("]", "")
        mens = mens.replace(" ", "")
        vel = mens.split(",")
        velocity = [int(numeric_string) for numeric_string in vel]

    info = robot.getInfo()              # it is unstable in timestep - needto findalternative
    if robot.ball_handler == 0:
        robot.orientate()
    robot.dribblerHandler()
    robot.move(velocity)
    
    #print((time.time()-loopTime)*1000)
    
