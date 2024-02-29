import socket
import pygame
import consts 
import numpy as np
import strategy
# import guiData
import guiFuncs
import time


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

        self.s2rSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.s2rSocket.bind(self.s2rMASocket)
        self.s2rSocket.setblocking(0)
        self.rfrSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.rfrSocket.bind(self.rfrMASocket)
        self.rfrSocket.setblocking(0)

        self.position = [-100, -100, -100]
        self.orientation = 0
        self.ball_position = [0, 0, 0]
        self.ball_handler = 0
        self.dist2Ball = 0

        self.skill = ""
        self.packet = [-1, -1, -1, -1, -1, -1, -1, -1]
        self.info = ""

        self.otherRobots = []
        self.otherRobotsPoints = []

        self.linesOfPass = []
        self.linesOfPassCutted = []

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
        x = self.position[0] * 10 * consts.FACTOR + consts.FIELD_SIZE["wall"][0] / 2
        y = -self.position[1] * 10 * consts.FACTOR + consts.FIELD_SIZE["wall"][1] / 2 + consts.YOFFSET
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

        pygame.draw.circle(consts.SCREEN,consts.COLORS["yellow"],(self.ball_position[0] * 10 * consts.FACTOR + consts.FIELD_SIZE["wall"][0] / 2,-self.ball_position[1] * 10 *consts.FACTOR+ consts.FIELD_SIZE["wall"][1] / 2+ consts.YOFFSET,),consts.FACTOR,)
        text = consts.SMALLFONT.render(str(self.robotID), True, (255, 255, 255))
        consts.SCREEN.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    def draw_opponents(self):
        for opponent in self.otherRobots:
            pygame.draw.circle(consts.SCREEN,consts.COLORS["red"],guiFuncs.coord2FieldCoord(opponent[0], opponent[1]),consts.ROBOT_SIZE,)

    def draw_robotInfo(self):
        robotID = self.robotID - 1
        pygame.draw.rect(consts.SCREEN,consts.COLORS["button"],(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS),160 * consts.FACTOR + consts.MENUS_SIZE * consts.RESOLUTION[1],int(consts.RESOLUTION[0] /consts.NUMBER_OF_ROBOTS) -consts.FACTOR,consts.RESOLUTION[1] - consts.MENUS_SIZE * consts.RESOLUTION[1] - 160 *consts.FACTOR,),border_radius=5,)
        text = consts.SMALLFONT.render("Robot_" + str(self.robotID), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,160 *consts.FACTOR + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR,),)
        text = consts.SMALLFONT.render("Skill: " + str(consts.SKILLSGUI[self.packet[0]]), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,160 *consts.FACTOR + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 7 *consts.FACTOR,),)
        text = consts.SMALLFONT.render("Args: " + str(self.packet[1:]), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,160 *consts.FACTOR + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 14 *consts.FACTOR,),)
        text = consts.SMALLFONT.render("BallHandler: " + str(strategy.BallHandler), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 30 * consts.FACTOR+ 2 *consts.FACTOR,160 *consts.FACTOR + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 21 *consts.FACTOR,),)
        text = consts.SMALLFONT.render("CanShoot: " + str(strategy.CanShoot), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,160 *consts.FACTOR + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 21 *consts.FACTOR,),)
        text = consts.SMALLFONT.render("CanGoal: " + str(strategy.CanGoal), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS)+ 30 * consts.FACTOR+ 2 *consts.FACTOR,160 *consts.FACTOR + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 28 *consts.FACTOR,),)
        text = consts.SMALLFONT.render("CanPass: " + str(strategy.CanPass), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,160 *consts.FACTOR + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 28 *consts.FACTOR,),)
        text = consts.TINYFONT.render(str(strategy.args[1:]), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,160 *consts.FACTOR + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 35 *consts.FACTOR,),)
        text = consts.TINYFONT.render(str(self.skill), True, (255, 255, 255))
        consts.SCREEN.blit(text,(robotID * int(consts.RESOLUTION[0] / consts.NUMBER_OF_ROBOTS) + 2 * consts.FACTOR,160 *consts.FACTOR + consts.MENUS_SIZE * consts.RESOLUTION[1] + 2 *consts.FACTOR + 42 *consts.FACTOR,),)

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
            if self.ball_handler == 1:
                pygame.draw.polygon(consts.SCREEN, consts.COLORS["yellow"], points, width=1)
                pygame.draw.line(consts.SCREEN,consts.COLORS["yellow"],guiFuncs.coord2FieldCoord(myLocation[0], myLocation[1]),guiFuncs.coord2FieldCoord(buddyLocation[0], buddyLocation[1]),width=1,)

            for opponent in robot.otherRobots:
                positionCollision = insidePolygon(myLocation,buddyLocation,ang2Robots,angOponent,opponent,consts.MARGIN2PASS,self.ball_handler)
                if positionCollision[0] != 0:
                    self.linesOfPassCutted[linesOfPassID].append([round(positionCollision[1], 2), round(positionCollision[2], 2), round(positionCollision[3], 2)])
                    if positionCollision[0] == 1:
                        if self.ball_handler == 1:
                            pygame.draw.polygon(consts.SCREEN, consts.COLORS["red"], points, width=2)
                        if robot.robotID in self.linesOfPass:
                            self.linesOfPass.remove(robot.robotID)
            

# def drawAllLines(myrobot, Robots):
#     # NOT BEING USED
#     for robot in Robots:
#         myLocation = [myrobot.position[0], myrobot.position[1]]
#         buddyLocation = [robot.position[0], robot.position[1]]
#         pygame.draw.line(consts.SCREEN,consts.COLORS["blue"],coord2FieldCoord(myLocation[0], myLocation[1]),coord2FieldCoord(buddyLocation[0], buddyLocation[1]),width=1,)
#     pygame.draw.line(consts.SCREEN,consts.COLORS["blue"],coord2FieldCoord(myLocation[0], myLocation[1]),coord2FieldCoord(11, 0),width=1,)

def getInfo(Robots):
    a = 0
    for robot in Robots:
        try:
            message = robot.rfrSocket.recvfrom(1024)
            # print(message[0].decode("utf8", "strict"))
            robot.info = (message[0].decode("utf8", "strict").replace("]", "").replace("[", "").replace(" ", "").split(";"))
            robot.position = [float(num) for num in robot.info[0].split(",")]
            robot.orientation = int(robot.info[1])
            robot.ball_position = [float(num) for num in robot.info[2].split(",")]
            robot.ball_handler = int(robot.info[3])
            robot.dist2Ball = round(np.sqrt(np.power((robot.position[0] - robot.ball_position[0]), 2)+ np.power((robot.position[1] - robot.ball_position[1]), 2)),2,)
            if robot.info[4] != "":
                robot.otherRobots = [float(num) for num in robot.info[4].split(",")]
                robot.otherRobots = [
                    [float(robot.otherRobots[i]), float(robot.otherRobots[i + 1])]
                    for i in range(0, len(robot.otherRobots), 2)
                ]
            else:
                robot.otherRobots = []
            a = 1
        except:
            pass
    return a


def sendInfo(Robots):
    for robot in Robots:
        robot.s2rSocket.sendto(str(robot.packet).encode(), robot.s2rRASocket)


def dataFusion(Robots):
    """This gets the recieved data from the robots, and cleans it
       So that you only have 5 opponents but everyone of the robots knows where they are

    Args:
        Robots (list): Robots
    """
    robotPositions = [[robot.position[0], robot.position[1]] for robot in Robots]
    for robot in Robots:
        for robotpos in robotPositions:
            for oo in robot.otherRobots:
                if abs(robotpos[0] - oo[0]) + abs(robotpos[1] - oo[1]) < 0.25:
                    robot.otherRobots.remove(oo)

    otherRobotsPosition = []
    otherRobotsPosition2 = []

    for robot in Robots:
        for otherRobot in robot.otherRobots:
            otherRobotsPosition.append(otherRobot)

    for robot1 in otherRobotsPosition:
        got = 0
        for robot2 in otherRobotsPosition2:
            if abs(robot1[0] - robot2[0]) + abs(robot1[1] - robot2[1]) < 0.25:
                got = 1
        if got == 0:
            otherRobotsPosition2.append(robot1)
            
    for robot in Robots:
        robot.otherRobots = otherRobotsPosition2

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
            if ball_handler == 1:
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

# def get_intersect(a1, a2, b1, b2):
#     """get_intersect function gets the intersection of two lines based on two points from each line

#     Args:
#         a1 (tuple): Point 1 of line 1
#         a2 (tuple): Point 2 of line 1
#         b1 (tuple): Point 1 of line 2
#         b2 (tuple): Point 2 of line 2

#     Returns:
#         tuple: point of intersection of the two lines
#     """
#     s = np.vstack([a1, a2, b1, b2])  # s for stacked
#     h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
#     l1 = np.cross(h[0], h[1])  # get first line
#     l2 = np.cross(h[2], h[3])  # get second line
#     x, y, z = np.cross(l1, l2)  # point of intersection
#     if z == 0:  # lines are parallel
#         return (float("inf"), float("inf"))
#     return (x / z, y / z)
