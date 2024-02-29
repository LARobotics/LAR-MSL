import math
import time
import numpy as np
import sys
import time
import socket
from coppelia import *
from comunication import *

DRAW = 2                # 0 - NO DRAW | 1 - Draw here every loop | 2 - Draw on separate python code (Need to Uncomment main in represent.py)
coppelia = Coppelia()
comPackets = ComPackets(2)
LBall = [0, 0]
LRobots = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
lastTime = 0

if DRAW == 1:
    from represent import Draw
    App = Draw(3)
elif DRAW == 2:
    serverAddressPort = ("localhost", 19999)
    ProcessingSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    ProcessingSocket.bind(("localhost", 20000))

print("SIGA")

while LBall != -1:
    loopTime = time.time()
    LBall, LRobots, LBalizaMine, LBalizaOpo, BallHandler = coppelia.getInfo()

    print(int((time.time()-loopTime)*1000), "ms", end=' | ')
    comPackets.Robots["Robot1"].state = ATTACK

    comPackets.Robots["Robot2"].state = MOVE
    comPackets.Robots["Robot3"].state = MOVE
    comPackets.Robots["Robot4"].state = MOVE
    comPackets.Robots["Robot5"].state = MOVE
    if(BallHandler == "1"):
        comPackets.Robots["Robot1"].state = KICK
        comPackets.Robots["Robot1"].args[0] = LRobots[1][0]
        comPackets.Robots["Robot1"].args[1] = LRobots[1][1]
        comPackets.Robots["Robot1"].args[2] = PASS
    
    print(int((time.time()-loopTime)*1000), "ms", end=' | ')
    comPackets.sendToCoppelia(coppelia)
    
    print(int((time.time()-loopTime)*1000), "ms", end=' | ')
    if LBall != -1:
        if DRAW == 1:
            App.Background()
            for Robot in LRobots:
                App.Robot(Robot)
            App.Ball(LBall)
            App.reDraw()
        elif DRAW == 2 and time.time() - lastTime > 0.1:
            ToDraw = {'Robots': LRobots, 'Ball': LBall}
            ProcessingSocket.sendto(str.encode(str(ToDraw)),("localhost", 19999))
            lastTime = time.time()
    else:
        pass#break

    #print("B:", Ball, end=' | ')
    #print("R1:",Robots[0], end=' | ')
    #print("BH:",BallHandler, end=' | ')    
    print(int((time.time()-loopTime)*1000), "ms")
