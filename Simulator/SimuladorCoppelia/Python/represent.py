from processing_py import *
import numpy as np
import socket
import json
import time

serverAddressPort   = ("localhost", 20000)
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.bind(("localhost", 19999))

Ball = [0, 0]
Robots = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

class Draw:
    def __init__(self, SCALE):
        self.FIELD_SIZE = [220, 140]
        self.FIELD_COLOR = (13, 85, 10)
        self.WIDTH = self.FIELD_SIZE[0]+20
        self.HEIGHT = self.FIELD_SIZE[1]+20
        self.SCALE = SCALE
        self.app = App(int(self.WIDTH)*SCALE, int(self.HEIGHT)*SCALE)

    def reDraw(self):
        self.app.redraw()
        self.app.background(self.FIELD_COLOR[0], self.FIELD_COLOR[1], self.FIELD_COLOR[2])
        self.Background()
    
    def Background(self):
        self.app.fill(self.FIELD_COLOR[0], self.FIELD_COLOR[1], self.FIELD_COLOR[2])
        self.app.strokeWeight(self.SCALE)
        self.app.stroke(255, 255, 255)
        self.app.rect(10*self.SCALE, 10*self.SCALE, self.FIELD_SIZE[0]*self.SCALE, self.FIELD_SIZE[1]*self.SCALE)
        self.app.rect(10*self.SCALE, 10*self.SCALE, self.FIELD_SIZE[0]/2*self.SCALE, self.FIELD_SIZE[1]*self.SCALE)
        self.app.rect((10+self.FIELD_SIZE[0]/2)*self.SCALE, 10*self.SCALE, self.FIELD_SIZE[0]*self.SCALE/2, self.FIELD_SIZE[1]*self.SCALE)
        self.app.noFill()
        self.app.ellipse((self.WIDTH/2)*self.SCALE, (self.HEIGHT/2)*self.SCALE, 20*self.SCALE, 20*self.SCALE)
        #self.app.strokeWeight(self.SCALE)

    def Robot(self, Robot):
        kick = pol2cart(5, -Robot[-1])
        self.app.stroke(0, 0, 0)
        self.app.fill(255, 255, 255)
        self.app.ellipse((Robot[0]*10+self.WIDTH/2)*self.SCALE,(-Robot[1]*10+self.HEIGHT/2)*self.SCALE,8*self.SCALE,8*self.SCALE)
        self.app.noStroke()
        self.app.fill(self.FIELD_COLOR[0], self.FIELD_COLOR[1], self.FIELD_COLOR[2])
        self.app.ellipse((Robot[0]*10+self.WIDTH/2+kick[0])*self.SCALE,(-Robot[1]*10+self.HEIGHT/2+kick[1])*self.SCALE,6*self.SCALE,6*self.SCALE)
   
    def Ball(self, Ball):
        self.app.noStroke()
        self.app.fill(242, 232, 0)
        self.app.ellipse((Ball[0]*10+self.WIDTH/2)*self.SCALE,(-Ball[1]*10+self.HEIGHT/2)*self.SCALE,3*self.SCALE,3*self.SCALE)
        self.app.stroke(0, 0, 0)


if __name__ == "__main__":
    App = Draw(3)

    while 1:
        message = UDPClientSocket.recvfrom(1024)
        ToDraw = eval(message[0].decode())
        Robots = ToDraw['Robots']
        Ball = ToDraw['Ball']

        tempo = time.time()
        App.Background()
        for Robot in Robots:
            App.Robot(Robot)
        App.Ball(Ball)
        App.reDraw()
        print(int((time.time()-tempo)*1000), "ms")