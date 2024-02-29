import numpy as np
import time
import socket
import random
from controller import Supervisor, Keyboard, Connector


MARGIN = 0.1
DIST2SEE = 7
MAXERROR_BALL = 15
MAXERROR_MINE = 0
MAXERROR_OPPONENT = 5
MAXERROR_BUDDIE = 1


FIELD_DIMENSIONS = {
    # "A" : 180,
    # "B" : 120,
    "A" : 220,
    "B" : 140,
    # "A" : 112,
    # "B" : 50,
    "C" : 69,
    "D" : 39,
    "E" : 22.5,
    "F" : 7.5,
    "G" : 7.5,
    "H" : 40,
    "I" : 36,
    "J" : 1.5,
    "K" : 1.25,
    "L" : 10,
    "M" : 10,
    "N" : 70,
    "O" : 10,
    "P" : 5,
    "Q" : 35,
}

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def rot2eul(R):
    beta = -np.arcsin(R[6])
    alpha = np.arctan2(R[7]/np.cos(beta),R[8]/np.cos(beta))
    gamma = np.arctan2(R[3]/np.cos(beta),R[0]/np.cos(beta))
    return np.degrees(np.array((alpha, beta, gamma))).astype(int)

class Robot:
    def __init__(self, supervisor, RobotName):
        self.supervisor = supervisor
        self.rootNode = self.supervisor.getFromDef(RobotName)
        self.ballNode = self.supervisor.getFromDef("Bola")
        self.connector = Connector("connector")
        #print(self.connector.enablePresence(1))
        #print(self.connector)
        self.translation = self.rootNode.getField('translation')
        self.rotation = self.rootNode.getField('rotation')
        self.ball_translation = self.ballNode.getField('translation')
        self.ball_rotation = self.ballNode.getField('rotation')
        self.position = [0, 0, 0]
        self.orientation = [0, 0, 0]
        self.ball_position = [0, 0, 0]
        self.ball_handler = 0
        self.lastKickTime = 0
        self.OrientateFix = 0
        
        self.dispSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dispSocket.bind(("localhost", 22200+int(RobotName[5])))
        #self.dispSocket.settimeout(0.001)
        self.dispSocket.setblocking(0)

        self.localSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.localSocket.bind(("localhost", 22290+int(RobotName[5])))
        #self.localSocket.settimeout(0.001)
        self.localSocket.setblocking(0)
        
        b = ["Robot1", "Robot2", "Robot3", "Robot4", "Robot5"]
        b.remove(RobotName)
        self.buddies = [self.supervisor.getFromDef(name) for name in b]
        self.opponents = [self.supervisor.getFromDef(name) for name in ["Opo1", "Opo2", "Opo3", "Opo4", "Opo5"]]
        #print(self.buddies, self.opponents)

    def __str__(self):
        return str(self.rootNode)

    def getInfo(self):
        a = self.rootNode.getPosition()
        self.position = [round(a[0], 2), round(a[1], 2), round(a[2], 2), 0, 0, 0]
        a = self.ballNode.getPosition()
        self.ball_position = [round(a[0], 2), round(a[1], 2), round(a[2], 2), 0, 0, 0]
        self.orientation = rot2eul(self.rootNode.getOrientation())

        MARGINTILT = 1.5
        if self.orientation[0] > MARGINTILT or self.orientation[1] > MARGINTILT or self.orientation[0] < -MARGINTILT or self.orientation[1] < -MARGINTILT:            
            self.rotation.setSFRotation([0,0,1,np.radians(self.orientation[2])])

        try:
            message = self.localSocket.recvfrom(1024)
            robots = message[0].decode('utf8', 'strict').replace("]", "").replace("[", "").replace(" ", "").split(";")
            
            robots[0] = robots[0].split(",")
            robots[1] = robots[1].split(",")
            buddies = [[float(robots[0][i]), float(robots[0][i+1]), 0, 0, 0, 0] for i in range(0, len(robots[0]), 2)]
            buddies = [item for item in buddies if dist2Point(item, self.position) < DIST2SEE]
            opponents = [[float(robots[1][i]), float(robots[1][i+1]), 0, 0, 0, 0] for i in range(0, len(robots[1]), 2)]
            opponents = [item for item in opponents if dist2Point(item, self.position) < DIST2SEE]
            
        except Exception as e:
            print(e)
            buddies = []
            opponents = []
            
        buddies1 = list(buddies)
        opponents1 = list(opponents)
        
        position1 = list(self.position)
        position1[0] = round(self.position[0]*FIELD_DIMENSIONS["A"]/220, 2)*100 + random.SystemRandom().uniform(-MAXERROR_MINE, MAXERROR_MINE)
        position1[1] = round(self.position[1]*FIELD_DIMENSIONS["B"]/140, 2)*100 + random.SystemRandom().uniform(-MAXERROR_MINE, MAXERROR_MINE)
        position1[2] = 0 #round(self.position[0]*FIELD_DIMENSIONS["A"]/220, 2)*100
        position1[3] = self.orientation[2] #round(self.position[1]*FIELD_DIMENSIONS["B"]/140, 2)*100
        position1[4] = 0 #round(self.position[0]*FIELD_DIMENSIONS["A"]/220, 2)*100
        position1[5] = 0 #round(self.position[1]*FIELD_DIMENSIONS["B"]/140, 2)*100
        
        for a in range(len(buddies1)):
            buddies1[a][0] = round(buddies1[a][0]*FIELD_DIMENSIONS["A"]/220, 2)*100 + random.SystemRandom().uniform(-MAXERROR_BUDDIE, MAXERROR_BUDDIE)
            buddies1[a][1] = round(buddies1[a][1]*FIELD_DIMENSIONS["B"]/140, 2)*100 + random.SystemRandom().uniform(-MAXERROR_BUDDIE, MAXERROR_BUDDIE)
            #buddies1[a] = self.convertAbsoluteToRelative(position1[0], position1[1], buddies1[a][0], buddies1[a][1], position1[2])
                    
        for a in range(len(opponents1)):
            opponents1[a][0] = round(opponents1[a][0]*FIELD_DIMENSIONS["A"]/220, 2)*100 + random.SystemRandom().uniform(-MAXERROR_OPPONENT, MAXERROR_OPPONENT)
            opponents1[a][1] = round(opponents1[a][1]*FIELD_DIMENSIONS["B"]/140, 2)*100 + random.SystemRandom().uniform(-MAXERROR_OPPONENT, MAXERROR_OPPONENT)
            #opponents1[a] = self.convertAbsoluteToRelative(position1[0], position1[1], opponents1[a][0], opponents1[a][1], position1[2])
            
        try:
            buddies1.remove(position1)
        except:
            pass
        buddies1.insert(0, position1)
        
        print(opponents1, end=' - ')
        
        for a in range(len(buddies1)-1):
            buddies1[a+1] = self.convertAbsoluteToRelative(position1[0], position1[1], buddies1[a+1][0], buddies1[a+1][1], position1[3])
           
        for a in range(len(opponents1)):
            opponents1[a] = self.convertAbsoluteToRelative(position1[0], position1[1], opponents1[a][0], opponents1[a][1], position1[3])        
            
        print(opponents1)
        
        buddiesSTR = "["
        for a in buddies1:
            buddiesSTR += str(a) + str(",")
        buddiesSTR += str("]")
                    
        opponentSTR = "["
        for a in opponents1:
            opponentSTR += str(a) + str(",")
        opponentSTR += str("]")
        
        ball_position1 = list(self.ball_position)
        ball_position1[0] = round(self.ball_position[0]*FIELD_DIMENSIONS["A"]/220, 2)*100 + random.SystemRandom().uniform(-MAXERROR_BALL, MAXERROR_BALL)
        ball_position1[1] = round(self.ball_position[1]*FIELD_DIMENSIONS["B"]/140, 2)*100 + random.SystemRandom().uniform(-MAXERROR_BALL, MAXERROR_BALL)
        
        ball_position1 = self.convertAbsoluteToRelative(position1[0], position1[1], ball_position1[0], ball_position1[1], position1[3])
        
        ball_position1[2] = 0 #round(self.ball_position[0]*FIELD_DIMENSIONS["A"]/220, 2)*100
        ball_position1[3] = -1 #round(self.ball_position[1]*FIELD_DIMENSIONS["B"]/140, 2)*100
        ball_position1[4] = -1 #round(self.ball_position[0]*FIELD_DIMENSIONS["A"]/220, 2)*100
        ball_position1[5] = self.ball_handler #round(self.ball_position[1]*FIELD_DIMENSIONS["B"]/140, 2)*100
        
        ESP = [14, -100, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        
        PC = [20, 30, 40, 50, 60, 70, "2f2fLG", 80]
        
        #print(" --- ", str(ball_position1) + ";" + buddiesSTR + ";" + opponentSTR + ";" + str(ESP))
        return str(ball_position1) + ";" + buddiesSTR + ";" + opponentSTR + ";" + str(ESP) + ";" + str(PC)

    '''
    def move(self, args):
        self.rootNode.setVelocity(args[0:5])
        if self.ball_handler == 1 and args[6] == 1:
            self.ball_handler = 0
            self.connector.unlock()
            x, y = pol2cart(3, np.radians(self.orientation[2]))
            self.ballNode.addForce([x, y, 0], False)
    '''
    
    def convertAbsoluteToRelative(self, xRob, yRob, xa, ya, alpha):
        # print(xRob, yRob, xa, ya, alpha)
        
        xa -= xRob
        ya -= yRob
        A = np.array([[np.cos(np.radians(-alpha+180)), -np.sin(np.radians(-alpha+180))],
                        [np.sin(np.radians(-alpha+180)), np.cos(np.radians(-alpha+180))]])
        b = np.array([[-ya], [-xa]])
        temp = np.linalg.inv(A) @ b
        xr, yr = temp[0,0], temp[1,0]
        
        # print(-alpha+180)
        
        
        
        
        # absoluteValues = [0, 0, 0]
        
        # xr = np.cos(np.radians(-alpha-90))*xa-np.sin(np.radians(-alpha-90))*ya-yRob
        # yr = -np.sin(np.radians(-alpha-90))*xa-np.cos(np.radians(-alpha-90))*ya-xRob

        return [xr, yr, 0, 0, 0, 0, 0]
    
    def orientate(self, x, y):
        ORIENTATIONMARGIN = 0.5
        ORIENTATIONSPEED = 7
        dis, angOri = cart2pol(x-self.position[0], y-self.position[1])
        #print(np.degrees(angOri), end=" | ")
        #print(np.degrees(angOri) - self.orientation[2], end= " <-> ")
        self.objective_angle = (-self.orientation[2] + np.degrees(angOri))
        if (self.objective_angle < -180):
            self.objective_angle += 360
        if (self.objective_angle > 180):
            self.objective_angle -= 360
        #print(self.objective_angle)
        self.objective_angle = self.objective_angle/18
        if self.objective_angle < ORIENTATIONMARGIN and self.objective_angle > -ORIENTATIONMARGIN:
            return 0
        elif self.objective_angle < ORIENTATIONSPEED and self.objective_angle > 0:
            return ORIENTATIONSPEED
        elif self.objective_angle > -ORIENTATIONSPEED  and self.objective_angle < 0:
            return -ORIENTATIONSPEED
        else:
            return self.objective_angle

        #self.rotation.setSFRotation([0,0,1,ang])
    
    def dribblerHandler(self):
        connector = pol2cart(0.35, np.radians(self.orientation[2]))
        connectorX = connector[0] + self.position[0]
        connectorY = connector[1] + self.position[1]
        dist2ball = np.sqrt((self.ball_position[0]-connectorX)**2 + (self.ball_position[1]-connectorY)**2)
        #print(dist2ball, self.ball_handler)
        #dist2ball = np.sqrt((self.ball_position[0]-self.position[0])**2 + (self.ball_position[1]-self.position[1])**2)
        #print(dist2ball, self.ball_handler)
        if(dist2ball < 0.2 and self.ball_handler == 0 and time.time()-self.lastKickTime > 0.5):
            self.ball_handler = 1
            self.connector.lock()
        #if self.ball_position[2] > 0.2 and self.ball_handler == 1:
        #    self.ball_translation.setSFTranslation([self.ball_position[0], self.ball_position[1], 0.1])

    def STOP(self, args):
        # print("STOP")
        angVel = self.orientate(self.ball_position[0], self.ball_position[1])
        self.rootNode.setVelocity([0, 0, 0, 0, 0, angVel])
        self.send2Display("fillOval", [0xFF0000, 1, 1], [coord2Dcoord([self.position[0], self.position[1]]), 3, 3])
        return 0
        
    def MOVE(self, args, vel=2, one = 0):
        if one == 0:
            args[0] = args[0]*220/FIELD_DIMENSIONS["A"]
            args[1] = args[1]*140/FIELD_DIMENSIONS["B"]
            
            args[3] = args[3]*220/FIELD_DIMENSIONS["A"]
            args[4] = args[4]*140/FIELD_DIMENSIONS["B"]
        
        
        if args[2] == 1:
            angVel = self.orientate(args[3], args[4])
        else:
            angVel = self.orientate(self.ball_position[0], self.ball_position[1])
        if abs(self.position[0]-args[0]) > MARGIN or abs(self.position[1]-args[1]) > MARGIN:
            dist, ang = cart2pol(args[0]-self.position[0], args[1]-self.position[1])
            x, y = pol2cart(vel, ang)        
            self.rootNode.setVelocity([x, y, 0, 0, 0, angVel])
        else:
            self.rootNode.setVelocity([0, 0, 0, 0, 0, angVel])
        return 0
        
    def ATTACK(self, args):
        args[0] = args[0]*220/FIELD_DIMENSIONS["A"]
        args[1] = args[1]*140/FIELD_DIMENSIONS["B"]
        args[2] = 0
        # print("ATTACK")
        self.MOVE(args, one = 1)
        self.send2Display("drawLine", [0xFF0000, 1, 1], [coord2Dcoord([self.position[0], self.position[1]]), coord2Dcoord([self.ball_position[0], self.ball_position[1]])])
        
        #self.rootNode.setVelocity([0, 0, 0, 0, 0, 0])
        return 0
        
    def KICK(self, args):                           # NOT READY!
        #print("KICK")
        args[0] = args[0]*220/FIELD_DIMENSIONS["A"]
        args[1] = args[1]*140/FIELD_DIMENSIONS["B"]
        args[3] = args[3]*220/FIELD_DIMENSIONS["A"]
        args[4] = args[4]*140/FIELD_DIMENSIONS["B"]
        
        dist, angOri = cart2pol(args[0]-self.position[0], args[1]-self.position[1])
        #ang = -np.degrees(angOri)# + 180
        #print("KICK", ang, self.orientation[2])
        #print(np.degrees(ang)+180 - self.orientation[2])
        #print(self.orientate(args[0], args[1]), end=" -- ")
        if self.ball_handler == 1:
            if abs(self.orientate(args[0], args[1])) < 0.1:
                x, y = pol2cart(40 if args[2] == 0 else 80, angOri)
                self.rootNode.setVelocity([0, 0, 0, 0, 0, 0])
                self.ballNode.setVelocity([0, 0, 0, 0, 0, 0])
                self.connector.unlock()
                self.ball_handler = 0
                self.ballNode.addForce([x, y, 0], False)
                self.lastKickTime = time.time()
            else:
                angVel = self.orientate(args[0], args[1])
                self.rootNode.setVelocity([0, 0, 0, 0, 0, angVel])
        else:
            self.rootNode.setVelocity([0, 0, 0, 0, 0, 0])
        self.send2Display("drawLine", [0x0FF000, 1, 1], [coord2Dcoord([self.position[0], self.position[1]]), coord2Dcoord([args[0], args[1]])])
        
        return 0
        
    def RECIEVE(self, args):
        args[0] = args[0]*220/FIELD_DIMENSIONS["A"]
        args[1] = args[1]*140/FIELD_DIMENSIONS["B"]
        # print("RECIEVE")
        self.MOVE(args, 1, one = 1)
        self.send2Display("drawLine", [0x0000FF, 1, 1], [coord2Dcoord([self.position[0], self.position[1]]), coord2Dcoord([args[0], args[1]])])
        
        #self.dribblerHandler()
        return 0
        
    def COVER(self, args):
        args[0] = args[0]*220/FIELD_DIMENSIONS["A"]
        args[1] = args[1]*140/FIELD_DIMENSIONS["B"]
        args[2] = args[2]*220/FIELD_DIMENSIONS["A"]
        args[3] = args[3]*140/FIELD_DIMENSIONS["B"]
        # print("COVER")
        dist, ang = cart2pol(args[3]-args[1], args[2]-args[0])
        agress = dist * args[5]
        # o seno e cosseno não estão trocados, o X é na horizontal, e Y na verticxal, e no simulador é assim
        x = args[0] + agress * np.sin(ang)
        y = args[1] + agress * np.cos(ang)
        #print(args[5], args[0], args[1], args[2], args[3], x, y, agress, dist, np.degrees(ang))
        self.MOVE([x, y, 0, 0, 0, 0, 0], one=1)
        self.send2Display("drawLine", [0x000FF0, 1, 1], [coord2Dcoord([args[0], args[1]]), coord2Dcoord([args[2], args[3]])])
        self.send2Display("fillOval", [0x000FF0, 1, 1], [coord2Dcoord([x, y]), 3, 3])
        return 0
        
    def DEFEND(self, args):
        
        args[0] = args[0]*220/FIELD_DIMENSIONS["A"]
        args[1] = args[1]*140/FIELD_DIMENSIONS["B"]
        # print("DEFEND")
        XDEFEND = -10.4
        YDEFENDMAX = 1
        if args[1] > YDEFENDMAX:
            args[1] = YDEFENDMAX
        if args[1] < -YDEFENDMAX:
            args[1] = -YDEFENDMAX
        
        self.MOVE([XDEFEND, args[1], 0, 0, 0, 0, 0], 2, one=1)
        return 0
        
    def CONTROL(self, args):
        
        args[0] = args[0]*220/FIELD_DIMENSIONS["A"]
        args[1] = args[1]*140/FIELD_DIMENSIONS["B"]
        
        moveX = self.position[0]+args[0]
        moveY = self.position[1]+args[1]
        oriX = self.position[0]+np.cos(np.radians(args[2]))
        oriY = self.position[1]+np.sin(np.radians(args[2]))
        self.MOVE([moveX, moveY, 1, oriX, oriY, 0, 0], one=1)
        
        if self.ball_handler == 1 and args[3] > 0:
            self.ball_handler = 0
            x, y = pol2cart(40 if args[3] == 1 else 80, np.radians(self.orientation[2]))
            self.rootNode.setVelocity([0, 0, 0, 0, 0, 0])
            self.ballNode.setVelocity([0, 0, 0, 0, 0, 0])
            self.connector.unlock()
            self.ballNode.addForce([x, y, 0], False)
            self.lastKickTime = time.time()
    
    def send2Display(self, func, cao, args):
        packet = str(func)+";"+str(cao)+";"+str(args)
        self.dispSocket.sendto(packet.encode(), ("localhost", 22200))

def coord2Dcoord(coord):
    coord[0] = int((coord[0]+12)*10)
    coord[1] = int((-coord[1]+8)*10)
    return coord

def dist2Point(a, b):
    #print(round(np.sqrt(np.power((a[0]-b[0]), 2)+np.power((a[1]-b[1]), 2)), 2))
    return round(np.sqrt(np.power((a[0]-b[0]), 2)+np.power((a[1]-b[1]), 2)), 2)
