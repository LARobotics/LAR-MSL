import socket

STOP = 0
MOVE = 1
ATTACK = 2
KICK = 3
RECIEVE = 4
COVER = 5
DEFEND = 6
CONTROL = 7

class Robot:
    def __init__(self, robotID, myIP, robotIP, Aport, Bport):
        self.robotID = robotID
        self.myIP = myIP
        self.robotIP = robotIP

        self.rfrMASocket = (self.myIP, 20000+Bport*1000+Aport*100+self.robotID*10+0)
        self.rfrRASocket = (self.robotIP, 20000+Bport*1000+Aport*100+self.robotID*10+1)
        self.s2rMASocket = (self.myIP, 20000+Aport*1000+Bport*100+self.robotID*10+1)
        self.s2rRASocket = (self.robotIP, 20000+Aport*1000+Bport*100+self.robotID*10+0)

        self.s2rSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.s2rSocket.bind(self.s2rMASocket)
        self.s2rSocket.settimeout(0.001)
        self.rfrSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.rfrSocket.bind(self.rfrMASocket)
        self.rfrSocket.settimeout(0.001)
        
        self.position = [-100, -100, -100]
        self.orientation = 0
        self.ball_position = [0, 0, 0]
        self.ball_handler = 0

        self.packet = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.info = ""
    
    def __str__(self):
        return "Robot" + str(self.robotID) + str(self.rfrRASocket) + " ----> " + str(self.rfrMASocket) + " BS" + "\nRobot" + str(self.robotID) + str(self.s2rRASocket) + " <---- " + str(self.s2rMASocket) + " BS" + "\n"
    
    def checkPosition(self, x, y):
        if (abs(self.position[0] - x) < 0.1 and abs(self.position[1] - y) < 0.1):
            return True
        else:
            return False



def getInfo(Robots):
    a = 0
    for robot in Robots:
        try:
            message = robot.rfrSocket.recvfrom(1024)
            tt = message[0].decode('utf8', 'strict').replace(";", ",").replace("]", "").replace("[", "").replace(" ", "").split(",")
            robot.info = [float(numeric_string) for numeric_string in tt]
            robot.position = robot.info[0:3]
            robot.orientation = int(robot.info[3])
            robot.ball_position = robot.info[4:7]
            robot.ball_handler = int(robot.info[7])
            a = 1
        except:
            pass
    return a

def sendInfo(Robots):
    for robot in Robots:
        robot.s2rSocket.sendto(str(robot.packet).encode(), robot.s2rRASocket)
    #i += 1
