"""This module is responsible for the strategy of the team. It will have multiple files and  ultiple possible strategies, but its based on the decisionTree.json file.
"""
from robot import *
from consts import *
import json
import time
import decisionMaking
import guiFuncs
import guiElements
import plots
import pathFinding
import pathPredicter
from scipy.optimize import linear_sum_assignment

BallHandler = -1
CanShoot = 0
CanGoal = 0
CanPass = 0
knownBall = 1
Refbox = 0
BallPosition = []
args = []
strat = []
oldstrat = []
idRecieve = 0
lastKnowBall = time.time()
solution = []
ballPath = pathPredicter.movementPrediciton("Ball", 10)
robotAng = 0
maxidRecieve = 0
transition = 0
transitionCounter = 0

# selectedRobot = 0

graph1 = plots.plot(0.2, 0.2, 0, 10, -3, 3, 0, 0, 10)

############ STRATEGY INIT ############
with open('./decisionTree.json', 'r') as f:
  StrategyDT = json.load(f)

def checkLineOfPass(Robots):
    return 0

def getGameState(Robots):
    """This function returns the game state based on the robot variables.
    It checks what robot has the ball, if we can shoot, pass, etc.

    Args:
        Robots (list): List of the robots of our team where all the info is stored.

    Returns:
        list: All the game state variables
    """
    global BallHandler
    global CanShoot
    global CanGoal
    global CanPass
    global knownBall
    global BallPosition
    global Refbox
    global StrategyDT
    global args
    global strat
    global oldstrat
    global idRecieve
    global lastKnowBall

    for index, robot in enumerate(Robots):
        if BallPosition != [-1, -1, -1]:
            BallHandler = 0
            CanShoot = 0
            CanGoal = 0
            CanPass = 0
            if robot.ball_handler != 0:
                BallHandler = index+1
                CanShoot = 1 if robot.position[0] < 0 else 0
                CanGoal = 1 if robot.position[0] < -6 else 0
                CanPass = 1
                knownBall = 1
                lastKnowBall = time.time()
                break
    
    args = []
    args.append("RefBox" if Refbox == 1 else "!RefBox")
    args.append("Ball" if BallHandler > 0 else "!Ball")
    args.append("CanShoot" if CanShoot == 1 else "!CanShoot")
    args.append("CanGoal" if CanGoal == 1 else "!CanGoal")
    args.append("CanPass" if CanPass == 1 else "!CanPass")
    args.append("knownBall" if knownBall == 1 else "!knownBall")
    # args.append("free") # MAde this because i started to alter the decision tree to have over time decisions but got stuck
    # if knownBall == 1:
    #     free
    #     transition
    #     opponents
    # print(args) 

    return BallHandler, CanShoot, CanGoal, CanPass, knownBall, BallPosition, Refbox, StrategyDT, args, strat, oldstrat, lastKnowBall


def strategyTEMP(Robots, kick, recebe):
    """Temporarly strategy that is used to implement the game strategy

    Args:
        Robots (list): List of the robots of our team
        kick (bool): Temporarly bool that is a simple flag for an old strategy initial implementation
        recebe (bool): Temporarly bool that is a simple flag for an old strategy initial implementation
    """
    global solution
    global robotAng
    global idRecieve
    global maxidRecieve
    global transition
    global transitionCounter
    BallHandler, CanShoot, CanGoal, CanPass, knownBall, BallPosition, Refbox, StrategyDT, args, strat, oldstrat, lastKnowBall = getGameState(Robots)

    if BallHandler > 0:
        playersMap, playersMapProbs = decisionMaking.calculateGraph(Robots, BallHandler, show = 1)
        graph = pathFinding.Graph(playersMap)
        solution = graph.a_star_algorithm(str(BallHandler), '0')
        solution = [int(a) for a in solution]
        solutionProbs = []
        # print(solution)
        for index in range(len(solution)-1):
            solID = solution[index+1]-1
            if solution[index] <= solID:
                solID -= 1
            # print(str(solution[index]), playersMapProbs[str(solution[index])][solID])
            solutionProbs.append(playersMapProbs[str(solution[index])][solID][1])
        # print(solutionProbs)

        if len(solution) > 1:
            if solution[1] == 0:
                playersMap[str(solution[0])][4] = ("0", 100)
            elif solution[0] > solution[1]:
                playersMap[str(solution[0])][solution[1]-1] = (str(solution[1]-1), 100)
            else:
                playersMap[str(solution[0])][solution[1]-2] = (str(solution[1]-2), 100)
            graph = pathFinding.Graph(playersMap)
            solution2 = graph.a_star_algorithm(str(BallHandler), '0')
            solution2 = [int(a) for a in solution2]
            for i in range(len(solution2)-2):
                guiElements.drawLine(Robots[solution2[i]-1].position, Robots[solution2[i+1]-1].position, color=COLORS["batYellow"], width=2)
            guiElements.drawLine(Robots[solution2[-2]-1].position, (11, 0), color=COLORS["batYellow"], width=2)
            
        # print(solution, solutionProbs, end=" | ")
        for i in range(len(solution)-2):
            guiElements.drawLine(Robots[solution[i]-1].position, Robots[solution[i+1]-1].position, color=COLORS["pink"], width=int(10*solutionProbs[i]), text=str(solutionProbs[i]))
        guiElements.drawLine(Robots[solution[-2]-1].position, (11, 0), color=COLORS["pink"], width=int(10*solutionProbs[-1]), text=str(solutionProbs[-1]))

    elif DEBUG_KEYS_SIMULATION:
        kick = 0 # TEMP VELU TO DEBUG
    
    ##################### HUNGARIAN ALGORITHM TO MAKE THEM SWAP POSITIONS ######################
    robotsLocationTemp = np.array([robot.position[0:2] for robot in Robots[0:4]])
    ZonesLocationTemp = (np.array(consts.ZonesPointsLoc[0:4]))
    row, col, distances = decisionMaking.hungarian(robotsLocationTemp, ZonesLocationTemp)
    min_distance = distances[row, col].sum()
    for i in range(len(row)):
        guiElements.drawLine(Robots[row[i]].position, consts.ZonesPointsLoc[col[i]], color=COLORS["blue"], width=1)
        Robots[row[i]].probField[3].field = consts.zonesFields[col[i]]

    ##################### HUNGARIAN ALGORITHM TO assign defense ######################
    robotsLocationTemp = np.array([robot.position[0:2] for robot in Robots[0:4]])
    # print(Robots[0].otherRobots)
    # print(max(Robots[0].otherRobots[:][0]))
    OpponentRobotLocations = (np.array(Robots[0].otherRobots))[0:4]
    # OpponentRobotLocations  = OpponentRobotLocations[OpponentRobotLocations[:, 0].argsort()]
    # OpponentRobotLocations = OpponentRobotLocations[0:4]

    # if len(OpponentRobotLocations) > 4:

    #     for i, a in enumerate(OpponentRobotLocations):
    #         if a[0] >= max(Robots[0].otherRobots[:][0]):
    #             OpponentRobotLocations = np.delete(OpponentRobotLocations, i, axis=1)
    # print(OpponentRobotLocations)

    row, col, distances = decisionMaking.hungarian(robotsLocationTemp, OpponentRobotLocations)
    min_distance = distances[row, col].sum()
    for i in range(len(row)):
        guiElements.drawLine(Robots[row[i]].position, Robots[row[i]].otherRobots[col[i]], color=COLORS["pink"], width=1)
        # Robots[row[i]].probField[3].field = consts.zonesFields[col[i]]



    ballPath.NextMove(Robots[1].ball_position[0], Robots[1].ball_position[1]) #CORRIGIR ISTO
    # nao pode ser so de um robo
    ballPath.getPrediction(1)
    nextBallPosition = [ballPath.nextXUI, ballPath.nextYUI]
    ballPath.NextAngle(np.degrees(np.arctan2(ballPath.nextYUI-ballPath.Y[-1], ballPath.nextXUI-ballPath.X[-1])))
    # weights = np.repeat(1.0, 3) / 3
    # anglediffs = np.dot(ballPath.angle, ballPath.angleWeights)/np.sum(ballPath.angleWeights) #np.convolve(ballPath.angle, ballPath.weights, 'valid')
    # print(BallHandler, round(ballPath.angle[-1]-robotAng), idRecieve+1,  end=" | ")
    #BallHandler = 0
    if BallHandler == 0:
        if abs(round(ballPath.angle[-1]-robotAng)) < 15:
            guiElements.drawLine(Robots[1].ball_position, nextBallPosition, color=COLORS["brightblue"], width=3)
            args.append("transition") # MAde this because i started to alter the decision tree to have over time decisions but got stuck
        else:
            guiElements.drawLine(Robots[1].ball_position, nextBallPosition, color=COLORS["red"], width=3)
            args.append("opponent") # MAde this because i started to alter the decision tree to have over time decisions but got stuck
            idRecieve = -1
    
    # if recebe == 2:
    #     for robot in Robots:
    #         robot.packet[0] = STOP
    #     return Robots, kick, recebe, solution
    
    TimeToPass = 1
    oldstrat = strat
    if (time.time() - lastKnowBall > TimeToPass):
        knownBall = 1
    strat = StrategyDT
    for i in range(len(args)):
        if args[i] in strat:
            strat=strat[args[i]]

    dist2Ball = [robot.dist2Ball for robot in Robots]
    dist2BallMin = np.sort(dist2Ball)

    for i, s in enumerate(Robots):
        if i != maxidRecieve:
            s.packet[0] = STOP
        if s.ball_handler == 1:
            pass#print(s.linesOfPass, end=" - ")
    # print(args)

    ss = [0, 0, 0, 0, 0]
    for i, s in enumerate(strat):
        if s == "KICK":
            # print("##################### KICK #####################")
            idRecieve = solution[1]-1
            maxidRecieve = idRecieve
            Robots[BallHandler-1].packet = [KICK, Robots[idRecieve].position[0], Robots[idRecieve].position[1], 0, 0, 0, 0]
            robotAng = np.degrees(np.arctan2(Robots[idRecieve].position[1]-Robots[BallHandler-1].position[1],Robots[idRecieve].position[0]-Robots[BallHandler-1].position[0]))
            if idRecieve == -1:
                idRecieve = -1
                Robots[BallHandler-1].packet = [KICK, 11, 0, 0, 0, 0, 0]
                robotAng = np.degrees(np.arctan2(0-Robots[BallHandler-1].position[1],11-Robots[BallHandler-1].position[0]))
            # print(robotAng, end=" | ")
            ss[BallHandler-1] = 1
            # transition = 1
            # transitionCounter = 0
            # guiElements.drawLine(Robots[BallHandler-1].position, Robots[idRecieve].position, color=COLORS["red"], width=5)
        elif s == "ATTACK":
            Robots[dist2Ball.index(dist2BallMin[0])].packet = [ATTACK, Robots[dist2Ball.index(dist2BallMin[0])].ball_position[0], Robots[dist2Ball.index(dist2BallMin[0])].ball_position[1], 0, 0, 0, 0]
            ss[np.argmin(dist2Ball)] = 1
        elif s == "RECIEVE":
            if "transition" in args:
                # print(maxidRecieve)
                Robots[maxidRecieve].packet = [RECIEVE, Robots[maxidRecieve].ball_position[0], Robots[maxidRecieve].ball_position[1], 0, 0, 0, 0]
            if idRecieve != BallHandler-1:
                Robots[idRecieve].packet = [RECIEVE, Robots[BallHandler-1].ball_position[0], Robots[BallHandler-1].ball_position[1], 0, 0, 0, 0]
                ss[idRecieve] = 1
        elif s == "DEFEND" and BallHandler != 5:
            Robots[4].packet = [DEFEND,  Robots[4].ball_position[0], Robots[4].ball_position[1], 0, 0, 0, 0]
            ss[4] = 1

    if BallHandler != 0 and kick == 0 and DEBUG_KEYS_SIMULATION:# and recebe != 2:
        for robot in Robots:
            robot.packet[0] = STOP

    return Robots, kick, recebe, solution


def ControlRobots(keyboard, joystick, Robots, selectedRobot, controlIDSList):
    """This functions handles the joystick and keyboard events and translates that to packets to send to the robots and control them

    Args:
        keyboard (list): List of all the keys pressed in the keyboard
        joystick (list(list)): List of all the joysitcks and all their events
        Robots (list): List of all the robots

    Returns:
        int: selected robot to be controlled by the keyboard
    """
    # global selectedRobot
    for joy in joystick:
        for i in range(6):
            if -0.25 < joy[i] < 0.25: joy[i] = 0

    for i, robot in enumerate(Robots):
        if i in controlIDSList:
            # robot.packet = [CONTROL, 0, 0, robot.packet[3], 0, 0, 0, 0]
            robot.packet[0] = CONTROL
            robot.packet[1] = int(10*joystick[i][0])
            robot.packet[2] = int(-10*joystick[i][1])
            if 10 or 12 in joystick[i]:
                robot.packet[1] = int(20*joystick[i][0])
                robot.packet[2] = int(-20*joystick[i][1])
            if joystick[i][2] != 0 or joystick[i][3] != 0:      robot.packet[3] = int(np.degrees(np.arctan2(-joystick[i][3], joystick[i][2])))
            if 2 in joystick[i]:   robot.packet[4] = 1      
            if 4 in joystick[i]:   robot.packet[4] = 2

    if selectedRobot in controlIDSList:
        if ord('d') in keyboard: Robots[selectedRobot].packet[1] = 10
        if ord('a') in keyboard: Robots[selectedRobot].packet[1] = -10
        if ord('w') in keyboard: Robots[selectedRobot].packet[2] = 10
        if ord('s') in keyboard: Robots[selectedRobot].packet[2] = -10
        if ord('q') in keyboard: Robots[selectedRobot].packet[3] += 5
        if ord('e') in keyboard: Robots[selectedRobot].packet[3] -= 5
        if ord('f') in keyboard: Robots[selectedRobot].packet[4] = 1
        if ord(' ') in keyboard: Robots[selectedRobot].packet[4] = 2



def calculateHeatMaps(Robots, selectedRobot, solution):
    Robots[selectedRobot].probField[-2].field1 = Robots[0].probField[0].calculateOpponents(Robots[selectedRobot].ball_position, Robots[selectedRobot].otherRobots, Robots[selectedRobot].probField[-2])
    loc = []
    for robot in Robots:
        loc.append(robot.position[0:2])
    Robots[selectedRobot].probField[-1].field1 = Robots[0].probField[0].calculateFriends(loc, Robots[selectedRobot].probField[-1])
    for robot in Robots:
        robot.probField[-1].field1 = Robots[selectedRobot].probField[-1].field1
        robot.probField[-2].field1 = Robots[selectedRobot].probField[-2].field1
        robot.probField[0].calculate(robot.probField[1:], robot, Robots, solution)
    # print(Robots[selectedRobot].probField[0].meanValue)
    return Robots
