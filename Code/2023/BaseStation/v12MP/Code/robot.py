import socket
import pygame
import consts 
import numpy as np
import strategy
import guiFuncs
import time
import probField as pF
import logFile
import guiElements
import time
import message_pb2
import message_pb2_grpc
import grpc

class Robot:
    def __init__(self, robotID, myIP, robotIP, Aport, Bport):
        """_Class Robot Initializer_

        Args:
            robotID (int): Defines the ID of the Robot
            myIP (string): It's the basestation IP, localhost for the simulator or the real world IP.
            robotIP (string): It's the IP assigned to the Robot being initialized, localhost on the Simulator or the Real World IP (Ex. 192.168.1.51)
            Aport (int): Define the communication origin:\n
                            0 - Basestation
                            1 - Real World
                            2 - Webots
            Bport (int):  Define the communication destiny: \n
                            0 - Basestation
                            1 - Real World
                            2 - Webots
        """
        self.robotID = robotID
        self.myIP = myIP
        self.robotIP = robotIP

        self.rfrMASocket = (
            self.myIP,
            20000 + Bport * 1000 + Aport * 100 + self.robotID * 10 + 0,
        )
        self.rfrRASocket = (
            self.robotIP,
            20000 + Bport * 1000 + Aport * 100 + self.robotID * 10 + 1,
        )
        self.s2rMASocket = (
            self.myIP,
            20000 + Aport * 1000 + Bport * 100 + self.robotID * 10 + 1,
        )
        self.s2rRASocket = (
            self.robotIP,
            20000 + Aport * 1000 + Bport * 100 + self.robotID * 10 + 0,
        )
        self.MyDebugSocket = (
            self.myIP,
            30000 + self.robotID,
        )
        self.RoDebugSocket = (
            self.robotIP,
            30000 + self.robotID + 10,
        )

        self.s2rSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.s2rSocket.bind(self.s2rMASocket)
        self.s2rSocket.setblocking(0)
        
        self.rfrSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.rfrSocket.bind(self.rfrMASocket)
        self.rfrSocket.setblocking(0)
        
        self.debSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.debSocket.bind(self.MyDebugSocket)
        self.debSocket.setblocking(0)
        
        self.grpcSocket = self.robotIP + ":40000"
        self.grpcChannel = grpc.insecure_channel(self.grpcSocket)
        self.grpcConnection = message_pb2_grpc.Base_SatationStub(self.grpcChannel)
        self.grpcChoice = -1
        self.grpcReply = 0
        
        self.position = [-8.7, -7.4, 0] #posição deles no ecra em cima da info do primeiro
        self.orientation = 0
        self.ball_position = [0, 0, 0]
        self.ball_handler = 0
        self.dist2Ball = 0

        self.skill = ""
        self.packet = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.info = ""

        # self.otherRobots = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        self.otherRobots = [[-12, -12]]
        self.myTeamRobots = [[-12, -12]]
        self.myTeamRobotsRelative = [[-12, -12]]
        self.nearestOpponent = [-1000, -1000]
        # self.otherRobotsPoints = []

        self.linesOfPass = []
        self.linesOfPassCutted = []

        # self.probField = probField.pField("a", True, 21)
        ############ PROBABILITY MAPS ############
        self.probField = pF.initFields(robotID)
        # self.probField = pF.pField(str(robotID), False, 0)
        self.zoneID = robotID

        self.battery = 69
        self.battery12 = 25
        self.pcbattery = 14
        self.QC1 = 22
        self.Omni = 45

        self.Cap = 0
        self.Bussola_bearing = 0
  
        self.linear_vel = 0
        self.angular_vel = 0
        self.direction = 0
        
        self.vel_db_r = 65
        self.vel_db_l = 67
        self.disp_db_r = 23
        self.disp_db_l = 24
        self.OMNI_temp = 0
        
        self.cpu = 0
        self.cpuTemp = 0
        self.gpu = 0
        self.gpuTemp = 0
        self.dt = 0
        self.commit = "2a23da0"
        self.ID = 0
        
        self.fps = 0
        self.lastTime = 0
        
        self.calibSkillValues = [[], [], [], [], [], [], [], []]
        for i in self.calibSkillValues:
            for a in range(12):
                i.append(0)
        self.calibSkillValuesRobot = list(self.calibSkillValues)
        

    def __str__(self):
        return ("Robot"+ str(self.robotID) + str(self.rfrRASocket) + " ----> " + str(self.rfrMASocket) + " BS" + "\nRobot" + str(self.robotID) + str(self.s2rRASocket)  + " <---- " + str(self.s2rMASocket) + " BS" + "\n" )

    def checkPosition(self, x, y):
        """***Check Position*** - Checks if the position of a specific robot is near the robot position
        Args:
            x (float): Position X on the field
            y (float): Position Y on the field
        Returns:
            bool: Returns true of false if the position given is "the same" as the robot position
        """
        if abs(self.position[0] - x) < 0.1 and abs(self.position[1] - y) < 0.1:
            return True
        else:
            return False

    def draw_robot(self, selectedFlag = 0):
        if self.fps != -1:
            x, y = guiFuncs.coord2FieldCoord(self.position[0], self.position[1])
            # x = self.position[0] * 10 * consts.FACTOR + consts.FIELD_SIZE["wall"][1] / 2
            # y = -self.position[1] * 10 * consts.FACTOR + consts.FIELD_SIZE["wall"][1] / 2 + consts.YOFFSET
            ball_x, ball_y = guiFuncs.coord2FieldCoord(self.ball_position[0], self.ball_position[1])

            ang = self.orientation

            points = []
            points.append((x + consts.ROBOT_SIZE / 2 * np.cos(np.radians(30 - ang)),y +consts.ROBOT_SIZE / 2 * np.sin(np.radians(30 - ang)),))
            NumberOfPoints = 6
            angOffset = 360 / NumberOfPoints / 2
            for i in range(NumberOfPoints):
                angInc = i * 360 / NumberOfPoints
                points.append((x + consts.ROBOT_SIZE * np.cos(np.radians(angInc + angOffset - ang)),y +consts.ROBOT_SIZE * np.sin(np.radians(angInc + angOffset - ang)),))
            points.append((x + consts.ROBOT_SIZE / 2 * np.cos(np.radians(-30 - ang)),y +consts.ROBOT_SIZE / 2 * np.sin(np.radians(-30 - ang)),))
            if selectedFlag:
                pygame.draw.polygon(consts.SCREEN, consts.COLORS["brightblue"], points)
            else:
                pygame.draw.polygon(consts.SCREEN, consts.COLORS["blue"], points)

            pygame.draw.circle(consts.SCREEN,consts.COLORS["yellow"],(ball_x, ball_y),consts.FACTOR,)
            
            # pygame.draw.circle(consts.SCREEN,consts.COLORS["yellow"],(x, y),70*consts.FACTOR, width=1)
            
            
            # guiElements.drawLine(self.position, self.ball_position, color=consts.COLORS["yellow"])
            
            text = consts.SMALLFONT.render(str(self.robotID), True, (255, 255, 255))
            consts.SCREEN.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
            
            # for a in self.myTeamRobotsRelative:
            #     ang = np.arctan2((self.position[1]-a[1]), (self.position[0]-a[0]))
            #     guiElements.drawLine((self.position[0], self.position[1]), (self.position[0]+(2*np.cos(ang+np.radians(90))), self.position[1]+(2*np.sin(ang+np.radians(90)))))
            
        

    def draw_opponents(self):
        for opponent in self.otherRobots:
            # return
            pygame.draw.circle(consts.SCREEN,consts.COLORS["red"],guiFuncs.coord2FieldCoord(opponent[0], opponent[1]),consts.ROBOT_SIZE,)

    def draw_robotInfo(self, selectedRobot = 0):
        robotID = self.robotID - 1
        if selectedRobot:
            pygame.draw.rect(consts.SCREEN,consts.COLORS["hover"],(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS), consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1],int(consts.RESOLUTION[0] /consts.NUMBER_OF_ROBOTS) - consts.FACTOR, consts.RESOLUTION[1] - consts.MENUS_SIZE * consts.RESOLUTION[1] - consts.FIELD_SIZE["wall"][1],),border_radius=5,)
        else:
            pygame.draw.rect(consts.SCREEN,consts.COLORS["button"],(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS), consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1],int(consts.RESOLUTION[0] /consts.NUMBER_OF_ROBOTS) -consts.FACTOR, consts.RESOLUTION[1] - consts.MENUS_SIZE * consts.RESOLUTION[1] - consts.FIELD_SIZE["wall"][1],),border_radius=5,)
        text = consts.SMALLFONT.render("\U0001F916 " + str(self.robotID), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR,),)

        if self.battery < 0:
            cor = consts.COLORS["pink"]
            emoji = "\U0001FAAB"
            text = consts.SMALLFONT.render(emoji+ str("NOT CON."), True, cor)
        else:
            if self.battery < 15:
                cor = consts.COLORS["batRed"]
                emoji = "\U0001FAAB"
            elif self.battery < 30:
                cor = consts.COLORS["batYellow"]
                emoji = "\U0001F50B"
            else:
                cor = consts.COLORS["white"]
                emoji = "\U0001F50B"
            text = consts.SMALLFONT.render(emoji+ str(self.battery) + "%", True, cor)
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + int(int(consts.RESOLUTION[0]/consts.NUMBER_OF_ROBOTS)/6) + 2 * consts.FACTOR, consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR,),)

        if self.battery12 < 0:
            cor = consts.COLORS["pink"]
            emoji = "\U0001FAAB"
            text = consts.SMALLFONT.render(emoji+ str("NOT CON."), True, cor)
        else:
            if self.battery12 < 15:
                cor = consts.COLORS["batRed"]
                emoji = "\U0001FAAB"
            elif self.battery12 < 30:
                cor = consts.COLORS["batYellow"]
                emoji = "\U0001F50B"
            else:
                cor = consts.COLORS["white"]
                emoji = "\U0001F50B"
            text = consts.SMALLFONT.render(str("\U0001F4F7")+emoji+ str(self.battery12) + "%", True, cor)
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + int(5*int(consts.RESOLUTION[0]/consts.NUMBER_OF_ROBOTS)/12), consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR,),)
            
        if abs(self.pcbattery) < 15:
            cor = consts.COLORS["batRed"]
            emoji = "\U0001FAAB"
        elif abs(self.pcbattery) < 30:
            cor = consts.COLORS["batYellow"]
            emoji = "\U0001F50B"
        else:
            cor = consts.COLORS["white"]
            emoji = "\U0001F50B"
        if self.pcbattery > 0:
            text = consts.SMALLFONT.render("\U0001F4BB"+emoji+ str(abs(self.pcbattery)) + "%" + "\U0001F50C", True, cor)
        else:
            text = consts.SMALLFONT.render("\U0001F4BB"+emoji+ str(abs(self.pcbattery)) + "%", True, cor)
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + int(7*int(consts.RESOLUTION[0]/consts.NUMBER_OF_ROBOTS)/10), consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR,),)

        text = consts.SMALLFONT.render("\U0001F30D " + str(round(self.position[0], 2)) + " " + str(round(self.position[1], 2)) + " " + str(self.position[2]), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 6 *consts.FACTOR,),)
        text = consts.SMALLFONT.render("\U000026BD " + str(round(self.ball_position[0], 2)) + " " + str(round(self.ball_position[1], 2)) + " " + str(self.ball_handler), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 35 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 6 *consts.FACTOR,),)
        text = consts.SMALLFONT.render("\U0001F4E9 " + consts.SKILLSGUI[self.packet[0]] + " " + str(self.packet[1:]) + "   |   \U000023F1: " + str(self.dt), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 12 *consts.FACTOR,),)
        text = consts.SMALLFONT.render("\U0001F4F6 " + str(self.QC1) + "% | " + str(self.ID) + "/128" + "  |  FPS: " + str(self.fps), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 18 *consts.FACTOR,),)
        text = consts.SMALLFONT.render(" Git \U00002601 : " + str(self.commit), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 20 * consts.FACTOR+ 21*consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 18.4 *consts.FACTOR,),)
        text = consts.SMALLFONT.render(" CPU \U0001F532 :" + str(self.cpu) + "% \U0001F321: " + str(self.cpuTemp) + "ºC    |    GPU : " + str(self.gpu) + "% \U0001F321: " + str(self.gpuTemp) + "ºC", True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 24 *consts.FACTOR,),)
        
        text = consts.SMALLFONT.render("OMNI - \U000023EB:" + str(self.linear_vel) + "  \U0001F504:" + str(self.angular_vel) + "  \U00002199:" + str(self.direction) + " \U0001F321: " + str(self.OMNI_temp) + "ºC", True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 30 *consts.FACTOR,),)
        text = consts.SMALLFONT.render("Dribbler - \U00002197  " + str(self.disp_db_l) + "  v-> " + str(self.vel_db_l) + "  \U0001F94E  " + str(self.vel_db_l) + " <-v  " + str(self.disp_db_r) + "  \U00002196", True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 36 *consts.FACTOR,),)
         
        text = consts.SMALLFONT.render("\U0001F9BF\U0001F3C8: " + str(self.Cap) + " %", True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 42 *consts.FACTOR,),)
        
        # text = consts.SMALLFONT.render("CanShoot: " + str(strategy.CanShoot), True, (255, 255, 255))
        # consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 21 *consts.FACTOR,),)
        # text = consts.SMALLFONT.render("CanGoal: " + str(strategy.CanGoal), True, (255, 255, 255))
        # consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 30 * consts.FACTOR+ 2 *consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 28 *consts.FACTOR,),)
        # text = consts.SMALLFONT.render("CanPass: " + str(strategy.CanPass), True, (255, 255, 255))
        # consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 28 *consts.FACTOR,),)
        # text = consts.TINYFONT.render(str(strategy.args[1:]), True, (255, 255, 255))
        # consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 35 *consts.FACTOR,),)
        # text = consts.TINYFONT.render(str(self.skill), True, (255, 255, 255))
        # consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 42 *consts.FACTOR,),)

    def draw_lines_of_pass(self, Robots):
        points = []
        allpoints = []
        self.linesOfPass = [1, 2, 3, 4, 5]
        self.linesOfPass.remove(self.robotID)
        self.linesOfPassCutted = [[], [], [], [], [], []]
        for robot in Robots:
            myLocation = [self.position[0], self.position[1]]
            if robot.ball_handler != 1:
                linesOfPassID = robot.robotID
                buddyLocation = [robot.position[0], robot.position[1]]
            else:
                buddyLocation = [11, 0]
                linesOfPassID = 0
            ang2Robots = np.round(np.arctan2(myLocation[1] - buddyLocation[1],myLocation[0] - buddyLocation[0],),2,)
            angOponent = ang2Robots + 3.14 / 2
            x = consts.MARGIN2PASS/2 * np.cos(angOponent)
            y = consts.MARGIN2PASS/2 * np.sin(angOponent)
            points = [
                guiFuncs.coord2FieldCoord(myLocation[0] - x, myLocation[1] - y),
                guiFuncs.coord2FieldCoord(myLocation[0] + x, myLocation[1] + y),
                guiFuncs.coord2FieldCoord(buddyLocation[0] + x, buddyLocation[1] + y),
                guiFuncs.coord2FieldCoord(buddyLocation[0] - x, buddyLocation[1] - y),
                guiFuncs.coord2FieldCoord(myLocation[0] - x, myLocation[1] - y),
            ]
            allpoints.append(points)
            if self.ball_handler == 1 and consts.REPRESENT_LINES_OF_PASS:
                pygame.draw.polygon(consts.SCREEN, consts.COLORS["yellow"], points, width=1)
                pygame.draw.line(consts.SCREEN,consts.COLORS["yellow"],guiFuncs.coord2FieldCoord(myLocation[0], myLocation[1]),guiFuncs.coord2FieldCoord(buddyLocation[0], buddyLocation[1]),width=1,)

            for opponent in robot.otherRobots:
                positionCollision = insidePolygon(myLocation,buddyLocation,ang2Robots,angOponent,opponent,consts.MARGIN2PASS,self.ball_handler)
                if positionCollision[0] != 0:
                    self.linesOfPassCutted[linesOfPassID].append([round(positionCollision[1], 2), round(positionCollision[2], 2), round(positionCollision[3], 2)])
                    if positionCollision[0] == 1:
                        if self.ball_handler == 1 and consts.REPRESENT_LINES_OF_PASS:
                            pygame.draw.polygon(consts.SCREEN, consts.COLORS["red"], points, width=2)
                        if robot.robotID in self.linesOfPass:
                            self.linesOfPass.remove(robot.robotID)
            
def getInfo(Robots):
    a = 0
    for robot in Robots:
        try:
            # NOTE: As divisoes por 100 sao pelo facto dos valores chegarem em centimetros e aqui as coisas funcionam em metros
            
            message = robot.rfrSocket.recvfrom(1024)
            # print(1, robot.robotID, message)
            newMessage = message[0].decode("utf8", "strict")
            # print(robot.robotID, newMessage)
            logFile.log_message(str(str(robot.robotID) + ";" + str(newMessage)))
            
            robot.info = (newMessage.replace(" ", "").split(";"))
            # print(2, robot.info)
            ball_position = [float(num)/100 for num in robot.info[0].replace("[", "").replace("]","").split(",")]
            
            # print(3, ball_position)
            
            myTeamRobots = robot.info[1].replace("[", "")[0:-1].split("],")
            # print(4, robot.myTeamRobots, myTeamRobots[0])
            if myTeamRobots[0] != "":#.replace("[", "").replace("]","").split(",") != '':
                robot.position = [float(num) for num in myTeamRobots[0].replace("[", "").replace("]","").split(",")]
                robot.position[0] /= 100
                robot.position[1] /= 100
                robot.position[2] /= 100
                robot.orientation = robot.position[3]
                robot.position[2] = robot.position[3]
                # print("5 pos: ",robot.position, robot.orientation)
            else:
                print("NO POSITION????")
                
            myTeamRobots = myTeamRobots[1:]
            # print(myTeamRobots)
            robot.myTeamRobots = []
            robot.myTeamRobotsRelative = []    
            
            for teamRobot in myTeamRobots:
                if teamRobot != '':
                    teamRobot = teamRobot.split(',')
                    robot.myTeamRobotsRelative.append([float(teamRobot[0])/100, float(teamRobot[1])/100])
                    #print("A", teamRobot[0], teamRobot[1])
                    robot.myTeamRobots.append(convertRelativeToAbsolute(robot.position[0], robot.position[1], float(teamRobot[0])/100, float(teamRobot[1])/100, robot.orientation))
                
            
            robot.ball_position = convertRelativeToAbsolute(robot.position[0], robot.position[1], ball_position[0], ball_position[1], robot.orientation)
            robot.ball_handler = ball_position[5]*100
            # print(6, robot.ball_position)
            
            otherRobots = robot.info[2].replace("[", "")[:-1].split("],")
            robot.otherRobots = []
            for i in range(len(otherRobots)):
                if otherRobots[i] != "":
                    tempAray = [float(num) for num in otherRobots[i].split(",")]
                    robot.otherRobots.append(convertRelativeToAbsolute(robot.position[0], robot.position[1], tempAray[0]/100, tempAray[1]/100, robot.orientation))
                    
            if len(robot.info[3]) > 0:
                robot.esp32Info = robot.info[3].replace("[", "").replace("]", "").replace(";", "").split(",")
                robot.esp32Info = [float(num) for num in robot.esp32Info]
                robot.battery12 = robot.esp32Info[0]
                robot.battery = robot.esp32Info[1]
                robot.QC1 = robot.esp32Info[2]
                robot.Omni = robot.esp32Info[3]
                robot.Cap = robot.esp32Info[4]
                robot.Bussola_bearing = robot.esp32Info[5]
                robot.linear_vel = robot.esp32Info[6]
                robot.angular_vel = robot.esp32Info[7]
                robot.direction = robot.esp32Info[8]
                robot.vel_db_r = robot.esp32Info[9]
                robot.vel_db_l = robot.esp32Info[10]
                robot.disp_db_r = robot.esp32Info[11]
                robot.disp_db_l = robot.esp32Info[12]
                robot.OMNI_temp = robot.esp32Info[13]
            
            # robot.fps = round(1/(time.time()-robot.lastTime))
            # robot.lastTime = time.time()
            a = 1
            
        except Exception as e:
            if str(e) != "[WinError 10035] A non-blocking socket operation could not be completed immediately":
                print(e)
            # if time.time()-robot.lastTime > 3:
            #     robot.fps = -1
    return a


def sendInfo(Robots):
    
    #NOTE TO DO: 
    
    
    for robot in Robots:
        packetTemp = list(robot.packet)
        if robot.packet[0] == consts.MOVE:
            if robot.packet[1] < 100: packetTemp[1] *= 100
            if robot.packet[2] < 100: packetTemp[2] *= 100
            if robot.packet[4] < 100: packetTemp[4] *= 100
            if robot.packet[5] < 100: packetTemp[5] *= 100
        elif robot.packet[0] == consts.ATTACK:
            if robot.packet[1] < 100: packetTemp[1] *= 100
            if robot.packet[2] < 100: packetTemp[2] *= 100
        elif robot.packet[0] == consts.KICK:
            if robot.packet[1] < 100: packetTemp[1] *= 100
            if robot.packet[2] < 100: packetTemp[2] *= 100
            if robot.packet[4] < 100: packetTemp[4] *= 100
            if robot.packet[5] < 100: packetTemp[5] *= 100
        elif robot.packet[0] == consts.RECIEVE:
            if robot.packet[1] < 100: packetTemp[1] *= 100
            if robot.packet[2] < 100: packetTemp[2] *= 100
        elif robot.packet[0] == consts.COVER:
            if robot.packet[1] < 100: packetTemp[1] *= 100
            if robot.packet[2] < 100: packetTemp[2] *= 100
            if robot.packet[3] < 100: packetTemp[3] *= 100
            if robot.packet[4] < 100: packetTemp[4] *= 100
            if robot.packet[5] < 100: packetTemp[5] *= 100
            if robot.packet[6] < 100: packetTemp[6] *= 100
        elif robot.packet[0] == consts.DEFEND:
            if robot.packet[1] < 100: packetTemp[1] *= 100
            if robot.packet[2] < 100: packetTemp[2] *= 100
        elif robot.packet[0] == consts.CONTROL:
            if robot.packet[1] < 100: packetTemp[1] *= 100
            if robot.packet[2] < 100: packetTemp[2] *= 100
        packetTemp = [ int(x) for x in packetTemp ]
        # print(robot.robotID, " -- ", packetTemp)

        robot.s2rSocket.sendto(str(packetTemp).encode(), robot.s2rRASocket)


def dataFusion(Robots):
    """This gets the recieved data from the robots, and cleans it
       So that you only have 5 opponents but everyone of the robots knows where they are

    Args:
        Robots (list): Robots
    """
    # robotPositions = [[robot.position[0], robot.position[1]] for robot in Robots]
    # for robot in Robots:
    #     for robotpos in robotPositions:
    #         for oo in robot.otherRobots:
    #             if abs(robotpos[0] - oo[0]) + abs(robotpos[1] - oo[1]) < 0.25:
    #                 robot.otherRobots.remove(oo)

    # otherRobotsPosition = []
    # otherRobotsPosition2 = []

    # for robot in Robots:
    #     for otherRobot in robot.otherRobots:
    #         otherRobotsPosition.append(otherRobot)

    # for robot1 in otherRobotsPosition:
    #     got = 0
    #     for robot2 in otherRobotsPosition2:
    #         if abs(robot1[0] - robot2[0]) + abs(robot1[1] - robot2[1]) < 0.25:
    #             got = 1
    #     if got == 0:
    #         otherRobotsPosition2.append(robot1)
            
    # otherRobotsPosition2 = np.array(otherRobotsPosition2)
    # otherRobotsPosition2 = otherRobotsPosition2[otherRobotsPosition2[:, 0].argsort()]
    # # print(otherRobotsPosition2)
    # for robot in Robots:
    #     robot.otherRobots = list(otherRobotsPosition2)

def insidePolygon(a, b, ang2Robots, angOponent, point, margin, ball_handler):
    """Checks if a specific point is near to break a line of pass

    Args:
        a (tuple): robotA location
        b (tuple): robotB location
        ang2Robots (float): angle between 2 robots
        angOponent (float): angle between the line of my two robots and the enemy robot to get the minimum distance between the enemy robot and the line of pass
        point (tuple): opponent Robot location
        margin (int): Margin to check in lines of pass

    Returns:
        bool: If the robot interferes to the line of pass between 2 robots
    """
    x = margin * np.cos(angOponent)
    y =  margin * np.sin(angOponent)
    x, y = get_intersect((point[0] - x, point[1] - y), (point[0] + x, point[1] + y), a, b)
    
    if a[0] <= x <= b[0] or b[0] <= x <= a[0]:
        dist = np.sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2)
        if dist < consts.MARGIN2CHECKPASS*margin:
            if ball_handler == 1 and consts.REPRESENT_LINES_OF_PASS:
                pygame.draw.line(consts.SCREEN,consts.COLORS["yellow"],guiFuncs.coord2FieldCoord(point[0], point[1]),guiFuncs.coord2FieldCoord(x, y),width=1,)
                pygame.draw.circle(consts.SCREEN, consts.COLORS["yellow"], guiFuncs.coord2FieldCoord(x, y), radius=3)
            if dist < margin:
                return 1, x, y, dist
            return 2, x, y, dist
    return 0, x, y, 10000

def get_intersect(a1, a2, b1, b2):
    """get_intersect function gets the intersection of two lines based on two points from each line
        This is a new much faster version
    Args:
        a1 (tuple): Point 1 of line 1
        a2 (tuple): Point 2 of line 1
        b1 (tuple): Point 1 of line 2
        b2 (tuple): Point 2 of line 2

    Returns:
        tuple: point of intersection of the two lines
    """
    a1 = np.array(a1)
    a2 = np.array(a2)
    b1 = np.array(b1)
    b2 = np.array(b2)
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    b = np.empty_like(da)
    b[0] = -da[1]
    b[1] = da[0]
    dap = b
    denom = np.dot( dap, db)
    num = np.dot( dap, dp )
    return list((num / denom.astype(float))*db + b1)

def convertRelativeToAbsolute(xAbs, yAbs, xr, yr, alpha):
    absoluteValues = [0, 0, 0]
    
    absoluteValues[0] = round(np.cos(np.radians(-alpha-90))*xr-np.sin(np.radians(-alpha-90))*yr+xAbs, 2)
    absoluteValues[1] = round(-np.sin(np.radians(-alpha-90))*xr-np.cos(np.radians(-alpha-90))*yr+yAbs, 2)
    return absoluteValues

    
def convertAbsoluteToRelative(xRob, yRob, xa, ya, alpha):
    xa -= xRob
    ya -= yRob
    A = np.array([[np.cos(np.radians(-alpha+180+90)), -np.sin(np.radians(-alpha+180+90))],
                    [np.sin(np.radians(-alpha+180+90)), np.cos(np.radians(-alpha+180+90))]])
    b = np.array([[-ya], [-xa]])
    temp = np.linalg.inv(A) @ b
    xr, yr = round(temp[0,0], 2), round(temp[1,0], 2)
    return xr, yr
    
if __name__ == "__main__":
    a = convertRelativeToAbsolute(5, -5, -8, 3, -45) # tem que dar 0, -6
    print(a)
    b = convertAbsoluteToRelative(5, -5, a[0], a[1], 45)
    print(b)
    