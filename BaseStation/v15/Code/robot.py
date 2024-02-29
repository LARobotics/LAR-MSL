import time
import socket
import pygame
import consts 
import numpy as np
import strategy
import guiFuncs
import probField as pF
import logFile
import time
import message_pb2
import message_pb2_grpc
import grpc
import audio
import gitCheck



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
        
        self.position = [-8.7, -7.4, 0, 0, 0, 0] #posição deles no ecra em cima da info do primeiro
        self.orientation = 0
        self.ball_position_robot = [0, 0, 0, 0, 0, 0, 0]
        self.ball_position = [0, 0, 0, 0, 0, 0, 0]
        self.ball_weight = 0
        self.ball_handler = 0
        self.dist2Ball = 0

        self.skill = ""
        self.packet = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.info = ""
        self.message = ""

        # self.otherRobots = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        self.otherRobots = [[-12, -12]]
        self.myTeamRobots = [[-12, -12]]
        self.myTeamRobotsRelative = [[-12, -12]]
        self.nearestOpponent = [-1000, -1000]
        # self.otherRobotsPoints = []

        self.linesOfPass = [[], [], [], [], [], []]
        self.linesOfPassCutted = [[], [], [], [], [], []]
        
        self.moveTo = [0, 0]

        # self.probField = probField.pField("a", True, 21)
        ############ PROBABILITY MAPS ############
        self.probField = pF.initFields(robotID)
        # self.probField = pF.pField(str(robotID), False, 0)
        self.zoneID = robotID
        self.zonePoint = [0, 0]

        self.battery = 69
        self.battery12 = 25
        self.pcbattery = 56
        self.QC1 = 22
        self.Omni = 45

        self.Cap = 66
        self.Bussola_bearing = 0
  
        self.linear_vel = 0.0
        self.angular_vel = 0.0
        self.direction = 0.0
        
        self.vel_db_r = 65
        self.vel_db_l = 67
        self.disp_db_r = 23
        self.disp_db_l = 24
        self.OMNI_temp = 0
        self.buttons= 0
       
        #? 000 - nada
        #? 001 - Liga Dribblers
        #? 010 - relocation
        #? 100 - Repair
        
        self.cpu = 61
        self.cpuTemp = 77
        self.gpu = 82
        self.gpuTemp = 69
        self.dt = 26
        self.dtComms = 0
        self.commit = consts.gitHash["playerYolo"]
        self.ID = 0
        self.IDprevious = 0
        self.commsQuality = 0
        self.total_packages = 0
        self.received_packages = 0
        self.commsReady = 0
        
        self.fps = 0
        self.lastTime = 0
        self.inGame = 1
        
        self.calibSkillValues = [[], [], [], [], [], [], [], []]
        for i in self.calibSkillValues:
            for a in range(11):
                i.append(float(0.0))
                
        self.calibSkillValuesRobot = list(self.calibSkillValues)
        self.calibSkillActivate = 0
        
        self.messagesIDs = [0]*128
        
        self.audioChannel = pygame.mixer.Channel(self.robotID)
        self.audios = {}
        self.audios["Connected"] = pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " Connected" + ".mp3")
        self.audios["Disconnected"] = pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " Disconnected" + ".mp3")
        self.audios["Low Battery"] = pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " Low Battery" + ".mp3")
        self.audios["PC Low Battery"] = pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " PC Low Battery" + ".mp3")
        self.audios["Incorrect Commit"] = pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " Incorrect Commit" + ".mp3")
        self.audios["High Temperature"] = pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " High Temperature" + ".mp3")
        self.audios["Slow Loop"] = pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " Slow Loop" + ".mp3")
        self.audios["High CPU Usage"] = pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " High CPU Usage" + ".mp3")
        self.audios["High GPU Usage"] = pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " High GPU Usage" + ".mp3")
        
        self.audioList = []
        self.prevConnected = 0
        self.connected = 0
        self.audioTimes = {}
        
        self.audioTimes["Connected"] = 0#pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " Connected" + ".mp3")
        self.audioTimes["Disconnected"] = 0#pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " Disconnected" + ".mp3")
        self.audioTimes["Low Battery"] = 0#pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " Low Battery" + ".mp3")
        self.audioTimes["PC Low Battery"] = 0#pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " PC Low Battery" + ".mp3")
        self.audioTimes["Incorrect Commit"] = 0#pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " Incorrect Commit" + ".mp3")
        self.audioTimes["High Temperature"] = 0#pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " High Temperature" + ".mp3")
        self.audioTimes["Slow Loop"] = 0#pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " Slow Loop" + ".mp3")
        self.audioTimes["High CPU Usage"] = 0#pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " High CPU Usage" + ".mp3")
        self.audioTimes["High GPU Usage"] = 0#pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " High GPU Usage" + ".mp3")

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
            ball_x, ball_y = guiFuncs.coord2FieldCoord(self.ball_position[0], self.ball_position[1])
            ball_xr, ball_yr = guiFuncs.coord2FieldCoord(self.ball_position_robot[0], self.ball_position_robot[1])

            ang = self.orientation
            
            
            pointArrow_x = x + 2.5*consts.ROBOT_SIZE * np.cos(np.radians(0 - ang))
            pointArrow_y = y + 2.5*consts.ROBOT_SIZE * np.sin(np.radians(0 - ang))
            arrow_points = [
                (x, y),
                (pointArrow_x, pointArrow_y),
                (
                    pointArrow_x - 2*consts.FACTOR * np.cos(np.radians(0 - ang) + np.pi / 6),
                    pointArrow_y - 2*consts.FACTOR * np.sin(np.radians(0 - ang) + np.pi / 6),
                ),
                (pointArrow_x, pointArrow_y),
                (
                    pointArrow_x - 2*consts.FACTOR * np.cos(np.radians(0 - ang) - np.pi / 6),
                    pointArrow_y - 2*consts.FACTOR * np.sin(np.radians(0 - ang) - np.pi / 6),
                ),
            ]
            pygame.draw.lines(consts.SCREEN, consts.COLORS["blueStealth"], False, arrow_points, int(2*consts.FACTOR/3))
                    
    
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
                
            color = list(consts.COLORS["yellowStealth"])
            weight = min((self.ball_weight*3), 1)
            weight = max(weight, 0)
            color[0] = consts.COLORS["fieldGround"][0] + (consts.COLORS["yellowStealth"][0] - consts.COLORS["fieldGround"][0])*weight
            color[1] = consts.COLORS["fieldGround"][1] + (consts.COLORS["yellowStealth"][1] - consts.COLORS["fieldGround"][1])*weight
            color[2] = consts.COLORS["fieldGround"][2] + (consts.COLORS["yellowStealth"][2] - consts.COLORS["fieldGround"][2])*weight
            # color.append(int(self.ball_weight*255))
            # print(self.robotID, self.dist2Ball, self.ball_weight, color)
            
            pygame.draw.circle(consts.SCREEN,color,(ball_xr, ball_yr),consts.FACTOR,)
            # guiFuncs.drawLine(self.position, self.ball_position_robot, color=color)
            pygame.draw.circle(consts.SCREEN,consts.COLORS["yellow"],(ball_x, ball_y),consts.FACTOR,)
            
            text, rect = consts.SMALLFONT.render(str(self.robotID), (255, 255, 255))
            consts.SMALLFONT.render_to(consts.SCREEN, (x - rect.width / 2, y - rect.height / 2),str(self.robotID), (255, 255, 255))
    
    def draw_robotCommsInfo(self):
        if self.fps != -1:
            x, y = guiFuncs.coord2FieldCoord(self.position[0], self.position[1])
            ball_x, ball_y = guiFuncs.coord2FieldCoord(self.ball_position_robot[0], self.ball_position_robot[1])
            
            match self.packet[0]:
                case consts.STOP:
                    pygame.draw.line(consts.SCREEN, consts.COLORS["purple"], (x - 4*consts.FACTOR, y - 4*consts.FACTOR), (x + 4*consts.FACTOR, y + 4*consts.FACTOR), consts.FACTOR)
                    pygame.draw.line(consts.SCREEN, consts.COLORS["purple"], (x - 4*consts.FACTOR, y + 4*consts.FACTOR), (x + 4*consts.FACTOR, y - 4*consts.FACTOR), consts.FACTOR)

                case consts.MOVE:
                    end_x, end_y = guiFuncs.coord2FieldCoord(self.packet[1], self.packet[2])
                    arrow_angle = np.arctan2(end_y - y, end_x - x)
                    arrow_points = [
                        (x, y),
                        (end_x, end_y),
                        (
                            end_x - 4*consts.FACTOR * np.cos(arrow_angle + np.pi / 6),
                            end_y - 4*consts.FACTOR * np.sin(arrow_angle + np.pi / 6),
                        ),
                        (end_x, end_y),
                        (
                            end_x - 4*consts.FACTOR * np.cos(arrow_angle - np.pi / 6),
                            end_y - 4*consts.FACTOR * np.sin(arrow_angle - np.pi / 6),
                        ),
                    ]
                    pygame.draw.lines(consts.SCREEN, consts.COLORS["gold"], False, arrow_points, consts.FACTOR)
                    
                case consts.ATTACK:
                    arrow_angle = np.arctan2(ball_y - y, ball_x - x)
                    arrow_points = [
                        (x, y),
                        (ball_x, ball_y),
                        (
                            ball_x - 4*consts.FACTOR * np.cos(arrow_angle + np.pi / 6),
                            ball_y - 4*consts.FACTOR * np.sin(arrow_angle + np.pi / 6),
                        ),
                        (ball_x, ball_y),
                        (
                            ball_x - 4*consts.FACTOR * np.cos(arrow_angle - np.pi / 6),
                            ball_y - 4*consts.FACTOR * np.sin(arrow_angle - np.pi / 6),
                        ),
                    ]
                    pygame.draw.lines(consts.SCREEN, consts.COLORS["coral"], False, arrow_points, consts.FACTOR)
                    
                case consts.KICK:
                    end_x, end_y = guiFuncs.coord2FieldCoord(self.packet[1], self.packet[2])
                    arrow_angle = np.arctan2(end_y - y, end_x - x)
                    arrow_points = [
                        (x, y),
                        (end_x, end_y),
                        (
                            end_x - 4*consts.FACTOR * np.cos(arrow_angle + np.pi / 6),
                            end_y - 4*consts.FACTOR * np.sin(arrow_angle + np.pi / 6),
                        ),
                        (end_x, end_y),
                        (
                            end_x - 4*consts.FACTOR * np.cos(arrow_angle - np.pi / 6),
                            end_y - 4*consts.FACTOR * np.sin(arrow_angle - np.pi / 6),
                        ),
                    ]
                    pygame.draw.lines(consts.SCREEN, consts.COLORS["teal"], False, arrow_points, consts.FACTOR)
                
                case consts.RECIEVE:
                    midpoint = ((x + ball_x) // 2, (y + ball_y) // 2)
                    arrow_angle = np.arctan2(ball_y - y, ball_x - x)
                    arrow_points = [
                        (x, y),
                        (midpoint[0], midpoint[1]),
                        (
                            midpoint[0] + 4*consts.FACTOR * np.cos(arrow_angle - np.pi / 6),
                            midpoint[1] + 4*consts.FACTOR * np.sin(arrow_angle - np.pi / 6),
                        ),
                        (midpoint[0], midpoint[1]),
                        (
                            midpoint[0] + 4*consts.FACTOR * np.cos(arrow_angle + np.pi / 6),
                            midpoint[1] + 4*consts.FACTOR * np.sin(arrow_angle + np.pi / 6),
                        ),
                        (midpoint[0], midpoint[1]),
                        (ball_x, ball_y),
                    ]
                    pygame.draw.lines(consts.SCREEN, consts.COLORS["indigo"], False, arrow_points, consts.FACTOR)
                    
                case consts.COVER:
                    begin_x, begin_y = guiFuncs.coord2FieldCoord(self.packet[1], self.packet[2])
                    end_x, end_y = guiFuncs.coord2FieldCoord(self.packet[3], self.packet[4])
                    midpoint = ((begin_x + end_x) // 2, (begin_y + end_y) // 2)
                    arrow_angle = np.arctan2(end_y - begin_y, end_x - begin_x)
                    arrow_points = [
                        (begin_x, begin_y),
                        (end_x, end_y),
                    ]
                    pygame.draw.lines(consts.SCREEN, consts.COLORS["purple"], False, arrow_points, consts.FACTOR)
                    arrow_angle = np.arctan2(midpoint[1] - y, midpoint[0] - x)
                    arrow_points = [
                        (x, y),
                        (midpoint[0], midpoint[1]),
                        (
                            midpoint[0] - 4*consts.FACTOR * np.cos(arrow_angle - np.pi / 6),
                            midpoint[1] - 4*consts.FACTOR * np.sin(arrow_angle - np.pi / 6),
                        ),
                        (midpoint[0], midpoint[1]),
                        (
                            midpoint[0] - 4*consts.FACTOR * np.cos(arrow_angle + np.pi / 6),
                            midpoint[1] - 4*consts.FACTOR * np.sin(arrow_angle + np.pi / 6),
                        ),
                    ]
                    pygame.draw.lines(consts.SCREEN, consts.COLORS["purple"], False, arrow_points, consts.FACTOR)

                case consts.DEFEND:
                    pygame.draw.circle(consts.SCREEN, consts.COLORS["brown"], (x, y), consts.ROBOT_SIZE*2)
                
                case consts.CONTROL:
                    pass
            


    def draw_opponents(self):
        if self.fps != -1:
            for i, opponent in enumerate(self.otherRobots):
                x, y = guiFuncs.coord2FieldCoord(opponent[0], opponent[1])
                if consts.FIELDGREEN:
                    pygame.draw.circle(consts.SCREEN,consts.COLORS["green"], (x, y), consts.ROBOT_SIZE*1.1,)
                else:
                    pygame.draw.circle(consts.SCREEN,consts.COLORS["red"], (x, y), consts.ROBOT_SIZE*1.1,)
            for i, teamMate in enumerate(self.myTeamRobots):
                x, y = guiFuncs.coord2FieldCoord(teamMate[0], teamMate[1])
                # if consts.FIELDGREEN:
                pygame.draw.circle(consts.SCREEN,consts.COLORS["blue"], (x, y), consts.ROBOT_SIZE*0.9,)
                # else:
                #     pygame.draw.circle(consts.SCREEN,consts.COLORS["blue"], (x, y), consts.ROBOT_SIZE,)
                # text, rect = consts.SMALLFONT.render(str(i), (255, 255, 255))
                # consts.SMALLFONT.render_to(consts.SCREEN, (x - rect.width / 2, y - rect.height / 2), str(i), (255, 255, 255))
    

    def draw_robotInfo(self, selectedRobot = 0):
        robotID = self.robotID - 1

        if selectedRobot:            pygame.draw.rect(consts.SCREEN,consts.COLORS["hover"],(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS), consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1],int(consts.RESOLUTION[0] /consts.NUMBER_OF_ROBOTS) - consts.FACTOR, consts.RESOLUTION[1] - 2.1*consts.MENUS_SIZE * consts.RESOLUTION[1] - consts.FIELD_SIZE["wall"][1],),border_radius=5,)
        else:            pygame.draw.rect(consts.SCREEN,consts.COLORS["button"],(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS), consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1],int(consts.RESOLUTION[0] /consts.NUMBER_OF_ROBOTS) -consts.FACTOR, consts.RESOLUTION[1] - 2.1*consts.MENUS_SIZE * consts.RESOLUTION[1] - consts.FIELD_SIZE["wall"][1],),border_radius=5,)
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR,)," \U0001F916 " + str(self.robotID), (255, 255, 255))
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 15 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 3 *consts.FACTOR,),"CPS: " + str(f"{self.fps:^5}"), self.get_text_color(self.fps))
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 34 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2.75 *consts.FACTOR,),"\U000023F1 : " + str(f"{self.dt:^5}"), self.get_text_color(self.dt))
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 50 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 3 *consts.FACTOR,),"\U00002601 : " + str(f"{self.commit:^7}"), self.get_text_color(self.commit))

        # self.audios["Low Battery"] = pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " Low Battery" + ".mp3")
        # self.audios["PC Low Battery"] = pygame.mixer.Sound("audios/Robot " + str(self.robotID) + " PC Low Battery" + ".mp3")

        if self.battery < 0:
            cor = consts.COLORS["pink"]
            consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR, consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 9 *consts.FACTOR,)," \U0001F50B "+ str("Not Con."), cor)
        else:
            if self.battery < 15:                cor = consts.COLORS["batRed"]
            elif self.battery < 30:                cor = consts.COLORS["batYellow"]
            else:                cor = consts.COLORS["white"]
            consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR, consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 9 *consts.FACTOR,)," \U0001F50B "+ str(self.battery) + "%", cor)

        if self.battery12 < 0:
            cor = consts.COLORS["pink"]
            consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + int(2*int(consts.RESOLUTION[0]/consts.NUMBER_OF_ROBOTS)/6), consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 9 *consts.FACTOR,),str("\U0001F4F7")+" \U0001F50B "+ str("Not Con."), cor)
        else:
            if self.battery12 < 15:                cor = consts.COLORS["batRed"]
            elif self.battery12 < 30:                cor = consts.COLORS["batYellow"]
            else:                cor = consts.COLORS["white"]
            consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + int(2.15*int(consts.RESOLUTION[0]/consts.NUMBER_OF_ROBOTS)/6), consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 9 *consts.FACTOR,),str("\U0001F4F7")+" \U0001F50B "+ str(self.battery12) + "%", cor)
            
        if abs(self.pcbattery) < 15:            cor = consts.COLORS["batRed"]
        elif abs(self.pcbattery) < 30:            cor = consts.COLORS["batYellow"]
        else:            cor = consts.COLORS["white"]
        if self.pcbattery > 0: 
            text = " \U0001F4BB "+" \U0001F50B "+ str(abs(self.pcbattery)) + "%" + " \U0001F50C"
        else:
            text = " \U0001F4BB "+" \U0001F50B "+ str(abs(self.pcbattery)) + "%"
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + int(4*int(consts.RESOLUTION[0]/consts.NUMBER_OF_ROBOTS)/6), consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 9 *consts.FACTOR,),text, cor)

        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 13 *consts.FACTOR,),"\U0001F30D  " + str(f"{round(self.position[0], 2):^2}") + " " + str(f"{round(self.position[1], 2):^3}") + " " + str(f"{self.position[2]:^3}") + "  \U000026BD " + str(f"{round(self.ball_position_robot[0], 2):^3}") + " " + str(f"{round(self.ball_position_robot[1], 2):^3}") + " " + str(f"{round(self.ball_position_robot[2], 2):^3}") + " " + str(f"{round(self.ball_weight, 2):^3}") + " " + str(self.ball_handler), (255, 255, 255))
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 20 *consts.FACTOR,),"\U0001F4E9  " + consts.SKILLSGUI[self.packet[0]] + " " + str(self.packet[1:]), (255, 255, 255))
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 26 *consts.FACTOR,),"\U0001F4F6  " + str(f"{int(self.commsQuality):^3}") + "% | " + str(f"{self.ID:^3}") + "/128", self.get_text_color(self.commsQuality))
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 40 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 26 *consts.FACTOR,),"\U000023F1  " + str(f"{int(self.dtComms):^3}"), self.get_text_color(self.dtComms))
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 54 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 26 *consts.FACTOR,),"\U000026A1 \U000026BD : " + str(self.Cap) + " %", self.get_text_color(self.Cap))
        consts.SMALLFONT.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 32*consts.FACTOR,),"OMNI-\U000023EB: " + str(f"{self.linear_vel:^3}") + " \U0001F504: " + str(f"{self.angular_vel:^3}") + " \U00002199: " + str(f"{self.direction:^3}"), (255, 255, 255))
        text, rect = consts.SMALLFONT.render("OMNI - \U000023EB:" + str(self.linear_vel) + "\U0001F504:" + str(self.angular_vel) + "\U00002199:" + str(self.direction), (255, 255, 255))
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 4 * consts.FACTOR + rect.width,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 32.5 *consts.FACTOR,),"    \U0001F321:" + str(f"{self.OMNI_temp:^3}") + "ºC", self.get_text_color(self.OMNI_temp))
        consts.SMALLFONT.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 38 *consts.FACTOR,),"\U00002197  " + str(f"{self.disp_db_l:^3}") + "  v-> " + str(f"{self.vel_db_l:^3}") + "  \U0001F94E  " + str(f"{self.vel_db_r:^3}") + " <-v  " + str(f"{self.disp_db_r:^3}") + "  \U00002196", (255, 255, 255))
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 44.5 *consts.FACTOR,),"CPU:" + str(f"{self.cpu:^3}") + "%", self.get_text_color(self.cpu))
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 22 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 44.4 *consts.FACTOR,),"\U0001F321:" + str(f"{self.cpuTemp:^3}") + "ºC", self.get_text_color(self.cpuTemp))
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 39 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 44.5 *consts.FACTOR,),"GPU:" + str(f"{self.gpu:^3}") + "%", self.get_text_color(self.gpu))
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 59 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 44.5 *consts.FACTOR,),"\U0001F321:" + str(f"{self.gpuTemp:^3}") + "ºC", self.get_text_color(self.gpuTemp))
        consts.SMALLFONT2.render_to(consts.SCREEN,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,consts.FIELD_SIZE["wall"][1] + consts.MENUS_SIZE * consts.RESOLUTION[1] + 3 *consts.FACTOR + 49 *consts.FACTOR,),"IP : " + str(f"{self.robotIP:^7}") + " Buttons:" + str(self.buttons), (255, 255, 255))
        
    def get_text_color(self, text):
        match text:
            case self.cpu:
                if self.cpu > 80:
                    # self.audioList.append(self.audios["High CPU Usage"])
                    return consts.COLORS["batRed"]
                elif self.cpu > 50:
                    return consts.COLORS["batYellow"]
                else:
                    return consts.COLORS["white"]
            case self.gpu:
                if self.gpu > 80:
                    # self.audioList.append(self.audios["High GPU Usage"])
                    return consts.COLORS["batRed"]
                elif self.gpu > 50:
                    return consts.COLORS["batYellow"]
                else:
                    return consts.COLORS["white"]
                
            case self.cpuTemp:
                if self.cpuTemp > 75:
                    # self.audioList.append(self.audios["High Temperature"])
                    return consts.COLORS["batRed"]
                elif self.cpuTemp > 50:
                    return consts.COLORS["batYellow"]
                else:
                    return consts.COLORS["white"]
                
            case self.gpuTemp:
                if self.gpuTemp > 75:
                    # self.audioList.append(self.audios["High Temperature"])
                    return consts.COLORS["batRed"]
                elif self.gpuTemp > 50:
                    return consts.COLORS["batYellow"]
                else:
                    return consts.COLORS["white"]
                
            case self.OMNI_temp:
                if self.OMNI_temp > 45:
                    # self.audioList.append(self.audios["High Temperature"])
                    return consts.COLORS["batRed"]
                elif self.OMNI_temp > 30:
                    return consts.COLORS["batYellow"]
                else:
                    return consts.COLORS["white"]
        
            case self.dt:
                if self.dt > 50:
                    return consts.COLORS["batRed"]
                elif self.dt > 34:
                    return consts.COLORS["batYellow"]
                else:
                    return consts.COLORS["white"]
                
            case self.Cap:
                if self.Cap > 75:
                    return consts.COLORS["white"]
                elif self.Cap > 50:
                    return consts.COLORS["batYellow"]
                else:
                    return consts.COLORS["batRed"]
                
            case self.commsQuality:
                if int(self.commsQuality) > 90:
                    return consts.COLORS["white"]
                elif int(self.commsQuality) > 70:
                    return consts.COLORS["batYellow"]
                else:
                    return consts.COLORS["batRed"]
                
            case self.fps:
                if self.fps >= 15:
                    return consts.COLORS["white"]
                elif self.fps > 0:
                    return consts.COLORS["batYellow"]
                else:
                    return consts.COLORS["batRed"]
                
            case self.dtComms:
                if self.dtComms >= 50:
                    return consts.COLORS["white"]
                elif self.dtComms > 34:
                    return consts.COLORS["batYellow"]
                else:
                    # self.audioList.append(self.audios["Slow Loop"])
                    return consts.COLORS["batRed"]
                
            case self.commit:
                if consts.gitHash["playerYolo"] in self.commit:
                    return consts.COLORS["white"]
                else:
                    if consts.SIMULATOR == 0 and self.audioTimes["Incorrect Commit"] == 0:
                        self.audioList.append(self.audios["Incorrect Commit"])
                        self.audioTimes["Incorrect Commit"] = 1
                    
                    return consts.COLORS["batRed"]
                
    
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
                # pygame.draw.polygon(consts.SCREEN, consts.COLORS["yellow"], points, width=1)
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
            
            
    def handleAudio(self):
        # print(gitCheck.t1.is_alive())
        if self.connected == 1 and self.connected != self.prevConnected:
            self.audioList.append(self.audios["Connected"])
            self.audioTimes["Incorrect Commit"] = 0
            # if not gitCheck.t1.is_alive():
            #     gitCheck.t1.start()
        if self.connected == 0 and self.connected != self.prevConnected:
            self.audioList.append(self.audios["Disconnected"])
        
        if len(self.audioList) > 0:
            audio.play_sound(self.audioChannel, self.audioList[0])
            self.audioList.pop(0)
        
        
def getInfo(Robots):
    a = 0
    for robot in Robots:
        try:
            # NOTE: As divisoes por 100 sao pelo facto dos valores chegarem em centimetros e aqui as coisas funcionam em metros
            newMessageBool = 0
            while True:
                try:
                    TempMessage = robot.rfrSocket.recvfrom(1024)
                    robot.message = TempMessage
                    newMessageBool = 1
                    newMessage = robot.message[0].decode("utf8", "strict")
                    # logFile.log_message(str(str(robot.robotID) + ";R;" + str(newMessage)))
                    robot.info = (newMessage.replace(" ", "").split(";"))
                    if len(robot.info[4]) > 0:
                        robot.pcInfo = robot.info[4].replace("[", "").replace("]", "").replace(";", "").split(",")
                        robot.ID = int(robot.pcInfo[7])
                        robot.messagesIDs[int(robot.ID)] = 1
                        # if robot.robotID == 2:
                        # print("########################## ", int(robot.ID), "################################")
                except Exception as e:
                    break
                
            # print(1, robot.robotID, robot.message)
            newMessage = robot.message[0].decode("utf8", "strict")
            # print(robot.robotID, newMessage)
            logFile.log_message(str(str(robot.robotID) + ";R;" + str(newMessage)))
            
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
                robot.orientation = robot.position[3]
                # print(robot.robotID,robot.position, robot.orientation)
            else:
                pass
                # print("NO POSITION????")
                
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
            robot.dist2Ball = round(np.sqrt(np.power((robot.position[0] - robot.ball_position[0]), 2)+ np.power((robot.position[1] - robot.ball_position[1]), 2)),2,)
            robot.ball_position[2] = ball_position[2]
            robot.ball_position.append(ball_position[3])
            robot.ball_position.append(ball_position[4])
            robot.ball_position.append(ball_position[5])
            robot.ball_position.append(100)
            robot.ball_handler = ball_position[5]*100
            if robot.ball_handler >= 3.0:
                robot.ball_handler = 0
            robot.ball_position_robot = list(robot.ball_position)
            
            # if robot.robotID == 1:            
            #     print(robot.ball_position, robot.ball_position_robot, end = " ^ ")
            #     robot.ball_position[0] += 1
            #     print(robot.ball_position, robot.ball_position_robot, end = " ^ ")
            
            otherRobots = robot.info[2].replace("[", "")[:-1].split("],")
            # if len(otherRobots) > 2:
            robot.otherRobots = []
            for i in range(len(otherRobots)):
                if otherRobots[i] != "":
                    tempAray = [float(num) for num in otherRobots[i].split(",")]
                    robot.otherRobots.append(convertRelativeToAbsolute(robot.position[0], robot.position[1], tempAray[0]/100, tempAray[1]/100, robot.orientation))
                    robot.otherRobots[-1][2] = tempAray[2]
                    
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
                robot.buttons = robot.esp32Info[14]
                #! 2 -> relocation
                #! 1 -> Dribbler
                #! 3 -> Jogo
                if robot.buttons > 2:
                    robot.inGame = 0
                else:
                    robot.inGame = 1
                # print(robot.buttons)
                
            if len(robot.info[4]) > 0:
                robot.pcInfo = robot.info[4].replace("[", "").replace("]", "").replace(";", "").split(",")
                # robot.pcInfo = [float(num) for num in robot.pcInfo]
                robot.cpu = float(robot.pcInfo[0])
                robot.cpuTemp = float(robot.pcInfo[1])
                robot.gpu = float(robot.pcInfo[2])
                robot.gpuTemp = float(robot.pcInfo[3])
                robot.pcbattery = round(float(robot.pcInfo[4]))
                robot.dt = int(robot.pcInfo[5])
                robot.commit = str(robot.pcInfo[6].replace("\"", "").replace("'", ""))
                robot.ID = int(robot.pcInfo[7])
                robot.dtComms = int(robot.pcInfo[8])
            
            robot.messagesIDs[int(robot.ID)] = 1
            robot.received_packages = robot.messagesIDs.count(1)
            # print(robot.messagesIDs, robot.received_packages)
                
            if robot.ID > 64 and robot.commsReady == 0:
                robot.commsReady = 1
            if robot.ID < 64 and robot.commsReady == 1:
                robot.commsReady = 0
                robot.received_packages = robot.messagesIDs.count(1)
                for i in range(len(robot.messagesIDs)):
                    robot.messagesIDs[i] = 0
                robot.commsQuality = (robot.received_packages / 128) * 100
                robot.received_packages = 0
                
            if robot.ID != robot.IDprevious:
                robot.IDprevious = robot.ID
                robot.fps = round(1/(time.time()-robot.lastTime))
                robot.lastTime = time.time()
                a = 1
                
            if time.time()-robot.lastTime > 3:
                robot.fps = -1
                robot.prevConnected = robot.connected
                robot.connected = 0
            else:
                robot.prevConnected = robot.connected
                robot.connected = 1
            
        except Exception as e:
            if str(e) != "[WinError 10035] A non-blocking socket operation could not be completed immediately" and str(e) != "string index out of range":
                print(e)
            if time.time()-robot.lastTime > 3:
                robot.fps = -1
                robot.connected = 0
    return a

def getInfoOpo(Oponents):
    for robot in Oponents:
        try:
            while True:
                try:
                    TempMessage = robot.rfrSocket.recvfrom(1024)
                    robot.message = TempMessage
                except Exception as e:
                    break
                
            newMessage = robot.message[0].decode("utf8", "strict")
                        
            robot.info = (newMessage.replace(" ", "").split(";"))
            ball_position = [float(num)/100 for num in robot.info[0].replace("[", "").replace("]","").split(",")]
            myTeamRobots = robot.info[1].replace("[", "")[0:-1].split("],")
            if myTeamRobots[0] != "":
                robot.position = [float(num) for num in myTeamRobots[0].replace("[", "").replace("]","").split(",")]
                robot.position[0] /= 100
                robot.position[1] /= 100
                robot.orientation = robot.position[3]
            
            # print(robot.position)
            
        except Exception as e:
            if str(e) != "[WinError 10035] A non-blocking socket operation could not be completed immediately" and str(e) != "string index out of range":
                print(e)

def sendInfo(Robots, force = False):
    
    for robot in Robots:
        if robot.fps != -1 or force:
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
            #print(robot.robotID, " -- ", packetTemp)

            logFile.log_message(str(str(robot.robotID) + ";S;" + str(list(robot.packet))))
            #print(robot.robotID, len(packetTemp))
            robot.s2rSocket.sendto(str(packetTemp).encode(), robot.s2rRASocket)


def dataFusion(Robots):
    """This gets the recieved data from the robots, and cleans it
       So that you only have 5 opponents but everyone of the robots knows where they are

    Args:
        Robots (list): Robots
    """
    weightss = []
    for robot in Robots:
        dist2Ball = max(robot.dist2Ball, 1)
        #if robot.ball_position[2] < 
        robot.ball_weight = (robot.ball_position[2]*100)/dist2Ball
        robot.ball_weight = min(robot.ball_weight, 1)
        robot.ball_weight = max(0, robot.ball_weight)
        weightss.append(robot.ball_weight)
    
    
    ball_positions = [[robot.ball_position[0], robot.ball_position[1], robot.ball_weight] for robot in Robots if robot.fps != -1]
    total_x = 0
    total_y = 0
    total_weight = 0
    number = 0

    testWeight = 0
    for ball in ball_positions:
        testWeight += ball[2]
    if testWeight < 0.001:
        for ball in ball_positions:
            ball[2] = 1


    for ball in ball_positions:
        if ball[2] > 0:
            x, y, weight = ball
            #print(weight)
            total_x += x * weight
            total_y += y * weight
            total_weight += weight
            number += 1
    
    if total_weight == 0:
        total_weight = 1
    average_x = total_x / total_weight
    average_y = total_y / total_weight
    # print(average_x, average_y)

    for robot in Robots:
        robot.ball_position[0] = average_x
        robot.ball_position[1] = average_y

    
    try:
        robotPositions = [[robot.position[0], robot.position[1]] for robot in Robots]
        for robot in Robots:
            for robotpos in robotPositions:
                for oo in robot.otherRobots:
                    if abs(robotpos[0] - oo[0]) + abs(robotpos[1] - oo[1]) < 0.75:
                        robot.otherRobots.remove(oo)

        otherRobotsPosition = []
        otherRobotsPosition2 = []

        for robot in Robots:
            for otherRobot in robot.otherRobots:
                otherRobotsPosition.append(otherRobot)

        for robot1 in otherRobotsPosition:
            got = 0
            for robot2 in otherRobotsPosition2:
                if abs(robot1[0] - robot2[0]) + abs(robot1[1] - robot2[1]) < 0.75:
                    got = 1
            if got == 0:
                otherRobotsPosition2.append(robot1)
                
        otherRobotsPosition2 = np.array(otherRobotsPosition2)
        # print(otherRobotsPosition2)
        if len(otherRobotsPosition2) > 0:
            otherRobotsPosition2 = otherRobotsPosition2[otherRobotsPosition2[:, 0].argsort()]
            # print(len(otherRobotsPosition2))
            # print(otherRobotsPosition2)
            for robot in Robots:
                robot.otherRobots = list(otherRobotsPosition2)
                #print(robot.robotID, len(robot.otherRobots), end= " | ")
    except Exception as e:
        print(e)
        pass

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

def count_non_zero(arr):
    count = 0
    for value in arr:
        if value != 0:
            count += 1
    return count

def spaceCalculator(string, robotID, spacewidth):
    Swidth, Sheight = consts.SMALLFONT.size(string)
    spacer1 = ""
    for i in range(int(((robotID) * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) - Swidth) / spacewidth)):    spacer1 += " "
    return spacer1

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
    
    
def distance_to_probability(distance, mean, standard_deviation):
    exponent = -((distance - mean) ** 2) / (2 * standard_deviation ** 2)
    return np.exp(exponent) / (np.sqrt(2 * np.pi) * standard_deviation)

class SimOpponent:
    def __init__(self, robotID, myIP, robotIP, Aport, Bport):
        self.robotID = robotID
        self.myIP = myIP
        self.robotIP = robotIP

        self.rfrMASocket = (
            self.myIP,
            30000 + Bport * 1000 + Aport * 100 + self.robotID * 10 + 0,
        )
        self.rfrRASocket = (
            self.robotIP,
            30000 + Bport * 1000 + Aport * 100 + self.robotID * 10 + 1,
        )
        self.s2rMASocket = (
            self.myIP,
            30000 + Aport * 1000 + Bport * 100 + self.robotID * 10 + 1,
        )
        self.s2rRASocket = (
            self.robotIP,
            30000 + Aport * 1000 + Bport * 100 + self.robotID * 10 + 0,
        )

        self.s2rSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.s2rSocket.bind(self.s2rMASocket)
        self.s2rSocket.setblocking(0)
        
        self.rfrSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.rfrSocket.bind(self.rfrMASocket)
        self.rfrSocket.setblocking(0)
        
        self.message = ""
        self.skill = ""
        self.packet = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.info = ""
        self.position = [0, 0, 0]
        self.orientation = 0
        self.lastPacketTime = 0

    def sendInfoOpo(self):
        packetTemp = list(self.packet)
        if self.packet[0] == consts.MOVE:
            if self.packet[1] < 100: packetTemp[1] *= 100
            if self.packet[2] < 100: packetTemp[2] *= 100
            if self.packet[4] < 100: packetTemp[4] *= 100
            if self.packet[5] < 100: packetTemp[5] *= 100
        elif self.packet[0] == consts.ATTACK:
            if self.packet[1] < 100: packetTemp[1] *= 100
            if self.packet[2] < 100: packetTemp[2] *= 100
        elif self.packet[0] == consts.KICK:
            if self.packet[1] < 100: packetTemp[1] *= 100
            if self.packet[2] < 100: packetTemp[2] *= 100
            if self.packet[4] < 100: packetTemp[4] *= 100
            if self.packet[5] < 100: packetTemp[5] *= 100
        elif self.packet[0] == consts.RECIEVE:
            if self.packet[1] < 100: packetTemp[1] *= 100
            if self.packet[2] < 100: packetTemp[2] *= 100
        elif self.packet[0] == consts.COVER:
            if self.packet[1] < 100: packetTemp[1] *= 100
            if self.packet[2] < 100: packetTemp[2] *= 100
            if self.packet[3] < 100: packetTemp[3] *= 100
            if self.packet[4] < 100: packetTemp[4] *= 100
            if self.packet[5] < 100: packetTemp[5] *= 100
            if self.packet[6] < 100: packetTemp[6] *= 100
        elif self.packet[0] == consts.DEFEND:
            if self.packet[1] < 100: packetTemp[1] *= 100
            if self.packet[2] < 100: packetTemp[2] *= 100
        if self.packet[0] == consts.CONTROL:
            if self.packet[1] < 100: packetTemp[1] *= 100
            if self.packet[2] < 100: packetTemp[2] *= 100
        packetTemp = [ int(x) for x in packetTemp ]
        # print(str(packetTemp), self.s2rRASocket)
        if time.time()-self.lastPacketTime >= 0.01:
            self.s2rSocket.sendto(str(packetTemp).encode(), self.s2rRASocket)
            self.lastPacketTime = time.time()


        
    
if __name__ == "__main__":
    a = convertRelativeToAbsolute(5, -5, -8, 3, -45) # tem que dar 0, -6
    print(a)
    b = convertAbsoluteToRelative(5, -5, a[0], a[1], 45)
    print(b)
    
