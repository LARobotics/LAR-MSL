"""supervisor_controller controller."""
from controller import Supervisor, Keyboard, Connector, Display
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

Skill = {0: robot.STOP,
            1: robot.MOVE,
            2: robot.ATTACK,
            3: robot.KICK,
            4: robot.RECIEVE,
            5: robot.COVER,
            6: robot.DEFEND,
            7: robot.CONTROL}

loopTime = time.time()

noTrama = 0
packet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

while supervisor.step(TIME_STEP) != -1:
    #a = time.time()
    info = robot.getInfo()              # it is unstable in timestep - needto findalternative
    #print(info)
    packetG = comms.getMessage(info)
    
    
    if(ROBOTID == 1):
#        robot.send2Display("background", [0xFF0000, 1, 1], [0, 0, 240, 160])
        robot.localSocket.sendto("local".encode(), ("localhost", 22290))

    #robot.send2Display("drawPixel", [0xFF0000, 1, 1], [69, 69, 240, 160])
    #robot.send2Display("drawLine", [0xFF0000, 1, 1], [0, 0, 240, 160])
    #robot.send2Display("drawRectangle", [0xFF0000, 1, 1], [20, 0, 40, 40])
#    robot.send2Display("drawOval", [0x000FF0, 1, 0.25], [coord2Dcoord([robot.position[0], robot.position[1]]), DIST2SEE*10, DIST2SEE*10])

    #robot.send2Display("fillOval", [0xFF0000, 1, 1], [, 80, 80])
    #robot.send2Display("drawPolygon", [0xFF0000, 1, 1], [[10,20,10, 0, 10], [0, 10, 20, 10, 0]])
    #robot.send2Display("drawText", [0xFF0000, 1, 1], ["SIGA", 100, 30, 40])
    #robot.send2Display("fillRectangle", [0xFF0000, 1, 1], [220, 0, 40, 40])
    #robot.send2Display("fillOval", [0xFF0000, 1, 1], [50, 220, 10, 20])
    #robot.send2Display("fillPolygon", [0xFF0000, 1, 1], [{100, 110, 100, 95, 90}, {10, 15, 20, 25, 30}, 40, 40])

    robot.dribblerHandler()
    if packetG[0] != -1:
        packet = packetG
        noTrama = 0
        if packet[0] == 1:
            packet[1] /= 100
            packet[2] /= 100
            packet[4] /= 100
            packet[5] /= 100
        elif packet[0] == 2:
            packet[1] /= 100
            packet[2] /= 100
        elif packet[0] == 3:
            packet[1] /= 100
            packet[2] /= 100
            packet[4] /= 100
            packet[5] /= 100
        elif packet[0] == 4:
            packet[1] /= 100
            packet[2] /= 100
        elif packet[0] == 5:
            packet[1] /= 100
            packet[2] /= 100
            packet[3] /= 100
            packet[4] /= 100
            packet[5] /= 100
            packet[6] /= 100
        elif packet[0] == 6:
            packet[1] /= 100
            packet[2] /= 100
        elif packet[0] == 7:
            packet[1] /= 100
            packet[2] /= 100
    else:
        noTrama += 1
        #print("No Trama", noTrama)
        
            
    Skill[packet[0]](packet[1:8])
    #robot.CONTROL([1, 0.75, 0, 1, 0, 0, 0, 0])

    if robot.ball_position[0] < -12 or robot.ball_position[0] > 12 or robot.ball_position[1] < -8 or robot.ball_position[1] > 8 and ROBOTID == 1:
        robot.ballNode.getField('translation').setSFVec3f([0, 0, 0])

    
    #print(time.time()-a)
    
    #print((time.time()-loopTime)*1000)
