"""MainAsyncController controller"""
from controller import Robot, Display, Supervisor
import socket
import numpy as np
import time

supervisor = Supervisor()

localSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
localSocket.bind(("localhost", 22290))
localSocket.setblocking(0)
#dispSocket.settimeout(0.001)

comms = [("localhost", 22291), ("localhost", 22292), ("localhost", 22293), ("localhost", 22294), ("localhost", 22295)]

buddies = [supervisor.getFromDef(name) for name in ["Robot1", "Robot2", "Robot3", "Robot4", "Robot5"]]
opponents = [supervisor.getFromDef(name) for name in ["Opo1", "Opo2", "Opo3", "Opo4", "Opo5"]]
buddiesPositions = []
opponentPositions = []

# print(buddiesPositions, opponentPositions)
while supervisor.step() != -1:
    buddiesPositions = [np.around(bud.getPosition(), 2).tolist()[0:2] for bud in buddies]
    opponentPositions = [np.around(bud.getPosition(), 2).tolist()[0:2] for bud in opponents]
    # print(buddiesPositions, opponentPositions)
    try:
        message = localSocket.recvfrom(1024)
        for sock in comms:
            localSocket.sendto((str(buddiesPositions)+";"+str(opponentPositions)).encode(), sock)
    except Exception as e:
        pass

    
	
