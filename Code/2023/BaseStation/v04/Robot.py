import socket
import pygame
from consts import *
import numpy as np
import strategy


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
        # for some reason this needs to be non blocking, otherwise the webots simulation behaviour is not right, i need to find out why
        self.s2rSocket.setblocking(0)
        #self.s2rSocket.settimeout(0.000001)
        self.rfrSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.rfrSocket.bind(self.rfrMASocket)
        # for some reason this needs to be non blocking, otherwise the webots simulation behaviour is not right, i need to find out why
        self.rfrSocket.setblocking(0)
        #self.rfrSocket.settimeout(0.000001)
        
        self.position = [-100, -100, -100]
        self.orientation = 0
        self.ball_position = [0, 0, 0]
        self.ball_handler = 0

        self.packet = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.info = ""
        self.temp = ""

    def __str__(self):
        return "Robot" + str(self.robotID) + str(self.rfrRASocket) + " ----> " + str(self.rfrMASocket) + " BS" + "\nRobot" + str(self.robotID) + str(self.s2rRASocket) + " <---- " + str(self.s2rMASocket) + " BS" + "\n"
    
    def checkPosition(self, x, y):
        if (abs(self.position[0] - x) < 0.1 and abs(self.position[1] - y) < 0.1):
            return True
        else:
            return False

    def draw_robot(self, screen):
        x = self.position[0]*10*FACTOR+FIELD_SIZE["wall"][0]/2
        y = -self.position[1]*10*FACTOR+FIELD_SIZE["wall"][1]/2+YOFFSET
        ang = self.orientation

        points = []
        points.append((x+ROBOT_SIZE/2*np.cos(np.radians(30-ang)),   y+ROBOT_SIZE/2*np.sin(np.radians(30-ang))))
        NumberOfPoints = 6
        angOffset = 360/NumberOfPoints/2
        for i in range(NumberOfPoints):
            angInc = i*360/NumberOfPoints
            points.append((x+ROBOT_SIZE*np.cos(np.radians(angInc+angOffset-ang)), y+ROBOT_SIZE*np.sin(np.radians(angInc+angOffset-ang))))
        points.append((x+ROBOT_SIZE/2*np.cos(np.radians(-30-ang)),   y+ROBOT_SIZE/2*np.sin(np.radians(-30-ang))))
        
        pygame.draw.polygon(screen,COLORS["blue"],points)
        pygame.draw.circle(screen, COLORS["yellow"],(self.ball_position[0]*10*FACTOR+FIELD_SIZE["wall"][0]/2, -self.ball_position[1]*10*FACTOR+FIELD_SIZE["wall"][1]/2+YOFFSET), 2*FACTOR)
        
        text = SMALLFONT.render(str(self.robotID), True , (255, 255, 255))
        
        screen.blit(text, (x-text.get_width()/2, y-text.get_height()/2))

    def draw_robotInfo(self, screen):
        robotID = self.robotID-1
        pygame.draw.rect(screen,COLORS["button"],(robotID*int(RESOLUTION[0]/NUMBER_OF_ROBOTS), 160*FACTOR+MENUS_SIZE*RESOLUTION[1], int(RESOLUTION[0]/NUMBER_OF_ROBOTS)-FACTOR , RESOLUTION[1]-MENUS_SIZE*RESOLUTION[1]-160*FACTOR), border_radius = 5)
        text = SMALLFONT.render("Robot_"+str(self.robotID), True , (255, 255, 255))
        screen.blit(text, (robotID*int(RESOLUTION[0]/NUMBER_OF_ROBOTS)+2*FACTOR, 160*FACTOR+MENUS_SIZE*RESOLUTION[1]+2*FACTOR))
        text = SMALLFONT.render("Skill: "+str(SKILLSGUI[self.packet[0]]), True , (255, 255, 255))
        screen.blit(text, (robotID*int(RESOLUTION[0]/NUMBER_OF_ROBOTS)+2*FACTOR, 160*FACTOR+MENUS_SIZE*RESOLUTION[1]+2*FACTOR+7*FACTOR))
        text = SMALLFONT.render("Args: "+str(self.packet[1:]), True , (255, 255, 255))
        screen.blit(text, (robotID*int(RESOLUTION[0]/NUMBER_OF_ROBOTS)+2*FACTOR, 160*FACTOR+MENUS_SIZE*RESOLUTION[1]+2*FACTOR+14*FACTOR))
        text = SMALLFONT.render("BallHandler: "+str(strategy.BallHandler), True , (255, 255, 255))
        screen.blit(text, (robotID*int(RESOLUTION[0]/NUMBER_OF_ROBOTS)+30*FACTOR+2*FACTOR, 160*FACTOR+MENUS_SIZE*RESOLUTION[1]+2*FACTOR+21*FACTOR))
        text = SMALLFONT.render("CanShoot: "+str(strategy.CanShoot), True , (255, 255, 255))
        screen.blit(text, (robotID*int(RESOLUTION[0]/NUMBER_OF_ROBOTS)+2*FACTOR, 160*FACTOR+MENUS_SIZE*RESOLUTION[1]+2*FACTOR+21*FACTOR))
        text = SMALLFONT.render("CanGoal: "+str(strategy.CanGoal), True , (255, 255, 255))
        screen.blit(text, (robotID*int(RESOLUTION[0]/NUMBER_OF_ROBOTS)+30*FACTOR+2*FACTOR, 160*FACTOR+MENUS_SIZE*RESOLUTION[1]+2*FACTOR+28*FACTOR))
        text = SMALLFONT.render("CanPass: "+str(strategy.CanPass), True , (255, 255, 255))
        screen.blit(text, (robotID*int(RESOLUTION[0]/NUMBER_OF_ROBOTS)+2*FACTOR, 160*FACTOR+MENUS_SIZE*RESOLUTION[1]+2*FACTOR+28*FACTOR))
        text = TINYFONT.render(str(strategy.args), True , (255, 255, 255))
        screen.blit(text, (robotID*int(RESOLUTION[0]/NUMBER_OF_ROBOTS)+2*FACTOR, 160*FACTOR+MENUS_SIZE*RESOLUTION[1]+2*FACTOR+35*FACTOR))
        text = TINYFONT.render(str(self.temp), True , (255, 255, 255))
        screen.blit(text, (robotID*int(RESOLUTION[0]/NUMBER_OF_ROBOTS)+2*FACTOR, 160*FACTOR+MENUS_SIZE*RESOLUTION[1]+2*FACTOR+42*FACTOR))

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
            return a
    return a

def sendInfo(Robots):
    for robot in Robots:
        robot.s2rSocket.sendto(str(robot.packet).encode(), robot.s2rRASocket)
