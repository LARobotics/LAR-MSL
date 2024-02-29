from dataclasses import dataclass

# SKILLS
STOP = 0
MOVE = 1
ATTACK = 2
KICK = 3
RECIEVE = 4
COVER = 5
DEFEND  = 6
CONTROL = 7

PASS =  0
GOAL = 1

@dataclass
class Packet:
    state: int
    args: list[int]
    
class ComPackets:
    def __init__(self, numberOfRobots):
        
        self.Robots = {"Robot1": Packet(0, [0, 0, 0, 0, 0, 0, 0]),
                        "Robot2": Packet(0, [0, 0, 0, 0, 0, 0, 0]),
                        "Robot3": Packet(0, [0, 0, 0, 0, 0, 0, 0]),
                        "Robot4": Packet(0, [0, 0, 0, 0, 0, 0, 0]),
                        "Robot5": Packet(0, [0, 0, 0, 0, 0, 0, 0]),}
        self.numberOfRobots = numberOfRobots
    
    def sendToCoppelia(self, coppelia):
        Trama = ""
        for robot in self.Robots:
            Trama += self.packetToString(self.Robots[robot]) + ";"
        coppelia.sendInfo(Trama)
    
    def packetToString(self, packet):
        localPacket = str(packet.state)
        for i in range(len(packet.args)):
            localPacket += " " + str(packet.args[i])
        return localPacket
