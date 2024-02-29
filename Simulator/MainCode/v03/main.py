import math
import time
import numpy as np
import sys
import time
import socket
import json
#import keyboard
from Robot import *
from strategy import *

with open('./decisionTree.json', 'r') as f:
  StrategyDT = json.load(f)

print(StrategyDT)
print(f'{globals()[(StrategyDT["RefBox"]["Start"][0])]}')
print(f'{eval(StrategyDT["RefBox"]["Start"][0])}')

DRAW = 0                # 0 - NO DRAW | 1 - Draw here every loop | 2 - Draw on separate python code (Need to Uncomment main in represent.py)
if DRAW == 1:
    from represent import Draw
    App = Draw(3)
elif DRAW == 2:
    serverAddressPort = ("localhost", 19998)
    ProcessingSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    ProcessingSocket.bind(("localhost", 20000))

IPS = ["localhost", "localhost", "localhost", "localhost", "localhost", "localhost", 2]
Robots = [Robot(a+1, IPS[0], IPS[a+1], 0, IPS[-1]) for a in range(5)]

kick = 0
recebe = 0

initTime = time.time()
while initTime != -1:
    loopTime = time.time()
    time.sleep(0.05)
    print("I:", getInfo(Robots), end=" | ")
    #checkLineOfPass(Robots)
    #print("".join(str([robot.ball_handler for robot in Robots])), end=" | ")

    
    if Robots[1].ball_handler == 0 and kick == 0:
        Robots[1].packet = [ATTACK, Robots[1].ball_position[0], Robots[1].ball_position[1], 0, 0, 0, 0, 0]
    else:
        kick = 1
        print(Robots[0].position[0], Robots[0].position[1], end = " | ")
        Robots[1].packet = [KICK, Robots[0].position[0], Robots[0].position[1], 0, 0, 0, 0, 0]
        if Robots[1].ball_handler == 0:
            Robots[1].packet = [STOP, 0, 0, 0, 0, 0, 0, 0]

    if Robots[0].ball_handler == 1:
        if Robots[0].checkPosition(Robots[0].packet[1], Robots[0].packet[2]):
            Robots[0].packet = [KICK, -14, -2, 1, 0, 0, 0, 0]
        else:
            Robots[0].packet = [MOVE, -7, 3, 1, -14, -2, 0, 0]
    else:
        if Robots[0].checkPosition(Robots[0].packet[1], Robots[0].packet[2]) or kick == 1:
            Robots[0].packet = [RECIEVE, Robots[1].ball_position[0], Robots[1].ball_position[1], 0, 0, 0, 0, 0]
        else:
            Robots[0].packet = [MOVE, 0, 0, 0, 0, 0, 0, 0]

    Robots[2].packet = [STOP, 0, 0, 0, 0, 0, 0, 0]
    Robots[3].packet = [STOP, 0, 0, 0, 0, 0, 0, 0]

    Robots[4].packet = [DEFEND, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
    if Robots[4].ball_handler == 1:
        Robots[4].packet = [KICK, Robots[2].position[0], Robots[2].position[1], 0, 0, 0, 0, 0]
        recebe = 1
    if recebe == 1:
        Robots[2].packet = [RECIEVE, Robots[1].ball_position[0], Robots[1].ball_position[1], 0, 0, 0, 0, 0]
        if Robots[2].ball_handler == 1:
            Robots[2].packet = [KICK, Robots[3].position[0], Robots[3].position[1], 0, 0, 0, 0, 0]
            Robots[3].packet = [RECIEVE, Robots[2].ball_position[0], Robots[2].ball_position[1], 0, 0, 0, 0, 0]
    elif kick == 0:
        Robots[2].packet = [COVER, Robots[0].position[0], Robots[0].position[1], Robots[3].ball_position[0], Robots[3].ball_position[1], 1, 0.5, 0]    
    else:
        Robots[2].packet = [MOVE, -5, -4, 0, 0, 0, 0, 0]
    '''
    Robots[0].pakcet = [2, 0, 0, 0]
    if Robots[0].packet[0] == 0:
        kick(args)
    elif Robots[0].packet[0] == 1:
        move(args)
    elif Robots[0].packet[0] == 2:
        goto(args)
    else:
        print("funcção inesperada")
    '''
    #Robots[0].packet = [STOP, 0, 0, 0, 0, 0, 0, 0]
    #Robots[2].packet = [STOP, 0, 0, 0, 0, 0, 0, 0]
    #Robots[3].packet = [STOP, 0, 0, 0, 0, 0, 0, 0]
    #Robots[4].packet = [STOP, 0, 0, 0, 0, 0, 0, 0]

    sendInfo(Robots)
    print(Robots[0].position)
    


