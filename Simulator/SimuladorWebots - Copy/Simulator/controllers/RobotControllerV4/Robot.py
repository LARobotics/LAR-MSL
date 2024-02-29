import numpy as np
from controller import Supervisor, Keyboard, Connector

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
    
    def __str__(self):
        return str(self.rootNode)

    def getInfo(self):
        a = self.rootNode.getPosition()
        self.position = [round(a[0], 2), round(a[1], 2), round(a[2], 2)]
        a = self.ballNode.getPosition()
        self.ball_position = [round(a[0], 2), round(a[1], 2), round(a[2], 2)]
        self.orientation = rot2eul(self.rootNode.getOrientation())
        return str(self.position) + ";" + str(self.orientation) + ";" + str(self.ball_position)

    def move(self, velocity):
        '''
        print(self.rootNode.getVelocity())
        key = keyboard.getKey()
        velocity = [0, 0, 0, 0, 0, 0]
        if key == keyboard.UP:
            velocity[0] = 5
        if  key == keyboard.DOWN:
            velocity[0] = -5
        if key == keyboard.LEFT:
            velocity[1] = 5
        if  key == keyboard.RIGHT:
            velocity[1] = -5
        '''    
        self.rootNode.setVelocity(velocity[0:5])
        if self.ball_handler == 1 and velocity[6] == 1:
            self.ball_handler = 0
            self.connector.unlock()
            x, y = pol2cart(2, np.radians(self.orientation[2]))
            #print(x, y)
            self.ballNode.addForce([x, y, 0], False)
        #self.translation.setSFVec3f(self.position)
        #if self.ball_handler == 1:
        #    a = self.position
        #    a[0] += 0.3
        #    a[2] = 0.099
        #    self.ball_translation.setSFVec3f(a)
        
    
    def orientate(self):
        dis, ang = cart2pol(self.ball_position[0]-self.position[0], self.ball_position[1]-self.position[1])
        self.rotation.setSFRotation([0,0,1,ang])
    
    def dribblerHandler(self):

        dist2ball = np.sqrt((self.ball_position[0]-self.position[0])**2 + (self.ball_position[1]-self.position[1])**2)
        if(dist2ball < 0.5 and self.ball_handler == 0):
            #self.ball_rotation.setSFRotation([0,0,1,0])
            self.ball_handler = 1
            self.connector.lock()
