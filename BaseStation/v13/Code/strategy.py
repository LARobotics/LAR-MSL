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

# TODO 
# ?
# !
# *




BallHandler = -1
Shoot = 0
Goal = 0
Pass = 0
knownBall = 1
Refbox = 0
BallPosition = []
args = []
strat = []
idRecieve = 0
lastKnowBall = time.time()
solution = []
ballPath = pathPredicter.movementPrediciton("Ball", 10)
robotAng = 0
maxidRecieve = 0
transition = 0
transitionCounter = 0
freeBalltime = time.time()
togoal = 0
FreeBall = 1
time2Kick = 0
FreeBall = 0
Transition = 0
TransitionGoal = 0
TransitionPass = 0
oldstrat = []

activeDT = []
activeMap = [[], [], [], [], []]

graph1 = plots.plot(0.2, 0.2, 0, 10, -3, 3, 0, 0, 10)

#?########### STRATEGY INIT ############
with open('./configs/decisionTree.json', 'r') as f:
  StrategyDT = json.load(f)

#?########### MAP INIT ############
with open('./configs/mapSituation.json', 'r') as f:
  MapSituation = json.load(f)

def checkLineOfPass(Robots):
    return 0

# def getGameState(Robots, solution):
#     """This function returns the game state based on the robot variables.
#     It checks what robot has the ball, if we can shoot, pass, etc.

#     Args:
#         Robots (list): List of the robots of our team where all the info is stored.

#     Returns:
#         list: All the game state variables
#     """
#     global BallHandler
#     global Shoot
#     global Goal
#     global Pass
#     global knownBall
#     global BallPosition
#     global Refbox
#     global StrategyDT
#     global args
#     global strat
#     global oldstrat
#     global idRecieve
#     global lastKnowBall
#     global freeBalltime

#     print(solution)

#     # if BallPosition != [-1, -1, -1]:
#     BallHandler = 0
#     Shoot = 0
#     Goal = 0
#     Pass = 0
#     knownBall = 1
#     for index, robot in enumerate(Robots):
#         if robot.ball_handler != 0:
#             BallHandler = index+1
#             Shoot = 1 if robot.position[0] > 0 else 0
#             if Shoot and len(solution)>1:
#                 Goal = 1 if solution[1] == 0 else 0
#             Pass = 1
#             knownBall = 1
#             lastKnowBall = time.time()
#             break
    
#     args = []
#     args.append("Ball" if BallHandler > 0 else "!Ball")
#     args.append("Shoot" if Shoot == 1 else "!Shoot")
#     args.append("Goal" if Goal == 1 else "!Goal")
#     args.append("Pass" if Pass == 1 else "!Pass")
#     args.append("knownBall" if knownBall == 1 else "!knownBall")
#     # args.append("free") # MAde this because i started to alter the decision tree to have over time decisions but got stuck
#     # if knownBall == 1:
#     #     free
#     #     transition
#     #     opponents

#     return BallHandler, Shoot, Goal, Pass, knownBall, BallPosition, Refbox, StrategyDT, args, strat, oldstrat, lastKnowBall


def mainStrategy(Robots, kick, recebe):
    """Temporarly strategy that is used to implement the game strategy

    Args:
        Robots (list): List of the robots of our team
        kick (bool): Temporarly bool that is a simple flag for an old strategy initial implementation
        recebe (bool): Temporarly bool that is a simple flag for an old strategy initial implementation
    """
    global solution, robotAng
    global idRecieve
    global maxidRecieve
    global transition
    global transitionCounter
    global activeMap
    global activeDT
    global freeBalltime
    global togoal
    global time2Kick
    global BallHandler
    global Shoot
    global Goal
    global Pass
    global knownBall
    global BallPosition
    global Refbox
    global StrategyDT
    global args
    global strat
    global oldstrat
    global idRecieve
    global lastKnowBall
    global freeBalltime
    global FreeBall
    global FreeBall
    global Transition
    global TransitionGoal
    global TransitionPass
    
    
    # BallHandler, Shoot, Goal, Pass, knownBall, BallPosition, Refbox, StrategyDT, args, strat, oldstrat, lastKnowBall = getGameState(Robots, solution)
    BallHandler = 0
    for index, robot in enumerate(Robots):
        if robot.ball_handler != 0:
            BallHandler = index+1
            break


    dist2Ball = [robot.dist2Ball for robot in Robots]
    dist2BallMin = np.sort(dist2Ball)


    if BallHandler > 0:
        playersMap, playersMapProbs = decisionMaking.calculateGraph(Robots, BallHandler, show = 1)
        graph = pathFinding.Graph(playersMap)
        solution = graph.a_star_algorithm(str(BallHandler), '0')
        solution = [int(a) for a in solution]
        solutionProbs = []
        for index in range(len(solution)-1):
            solID = solution[index+1]-1
            if solution[index] <= solID:
                solID -= 1
            solutionProbs.append(playersMapProbs[str(solution[index])][solID][1])

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
            guiElements.drawLine(Robots[solution2[-2]-1].position, (consts.FIELD_DIMENSIONS["A"]/20, 0), color=COLORS["batYellow"], width=2)
            
        for i in range(len(solution)-2):
            guiElements.drawLine(Robots[solution[i]-1].position, Robots[solution[i+1]-1].position, color=COLORS["pink"], width=int(10*solutionProbs[i]), text=str(solutionProbs[i]))
        guiElements.drawLine(Robots[solution[-2]-1].position, (consts.FIELD_DIMENSIONS["A"]/20, 0), color=COLORS["pink"], width=int(10*solutionProbs[-1]), text=str(solutionProbs[-1]))

    elif DEBUG_KEYS_SIMULATION:
        kick = 0 # THIS IS TO STOP AT EACH PASS
    
    
    #?#################### HUNGARIAN ALGORITHM TO MAKE THEM SWAP POSITIONS ######################
    robotsLocationTemp = np.array([robot.position[0:2] for robot in Robots[0:5]])
    ZonesLocationTemp = (np.array(consts.ZonesPointsLoc[0:5]))
    row, col, distances = decisionMaking.hungarian(robotsLocationTemp, ZonesLocationTemp)
    min_distance = distances[row, col].sum()
    for i in range(len(row)):
        guiElements.drawLine(Robots[row[i]].position, consts.ZonesPointsLoc[col[i]], color=COLORS["skyblue"], width=1)
        Robots[row[i]].probField[3].field = consts.zonesFields[col[i]]


    #?#################### HUNGARIAN ALGORITHM TO assign defense ######################
    robotsLocationTemp = np.array([robot.position[0:2] for robot in Robots[1:5]])    
    OpponentRobotLocations = []
    for robot in Robots:
        for i in robot.otherRobots:
            OpponentRobotLocations.append([i[0:2]])
    OpponentRobotLocations = np.array(OpponentRobotLocations)
    row, col, distances = decisionMaking.hungarian(robotsLocationTemp, OpponentRobotLocations)
    min_distance = distances[row, col].sum()
    
    
    #?#################### BALL MOVEMENT PREDICTION ######################
    ballPath.NextMove(Robots[1].ball_position[0], Robots[1].ball_position[1]) #CORRIGIR ISTO | nao pode ser so de um robo
    ballPath.getPrediction(2) # pegar no valor apos 2 loops
    nextBallPosition = [ballPath.nextXUI, ballPath.nextYUI]
    ballPath.NextAngle(np.degrees(np.arctan2(ballPath.nextYUI-ballPath.Y[-1], ballPath.nextXUI-ballPath.X[-1])))
    
    
    #?########################## GET GAME STATE VARIBALES #################################
    # Shoot = 0
    # Goal = 0
    # Pass = 0
    # knownBall = 1
    
    if BallHandler != 0:
        FreeBall = 0
        Transition = 0
        TransitionGoal = 0
        TransitionPass = 0
        Shoot = 1 if Robots[BallHandler-1].position[0] > 0 else 0
        if Shoot and len(solution)>1:
            Goal = 1 if solution[1] == 0 and solutionProbs[0] >= MINPROBGOAL else 0
        Pass = 1 if solutionProbs[0] >= MINPROBPASS else 0
        knownBall = 1
        lastKnowBall = time.time()
        freeBalltime = time.time()
    else:
        Shoot = 0
        Goal = 0
        Pass = 0
        if (abs(round(ballPath.angle[-1]-robotAng)) < ANGLEMARGIN and round(time.time()-freeBalltime) < freeBallTimeout and FreeBall == 0) or time.time() - time2Kick < 0.5:
            guiElements.drawLine(Robots[1].ball_position, nextBallPosition, color=COLORS["brightblue"], width=3)
            Transition = 1
            if idRecieve == -1:
                TransitionGoal = 1
            else:
                TransitionPass = 1
        else:
            guiElements.drawLine(Robots[1].ball_position, nextBallPosition, color=COLORS["red"], width=3)
            FreeBall = 1
            Transition = 0
    
    args = []
    args.append("Ball" if BallHandler > 0 else "!Ball")
    args.append("Shoot" if Shoot else "!Shoot")
    args.append("Goal" if Goal else "!Goal")
    args.append("Pass" if Pass else "!Pass")
    args.append("knownBall" if knownBall else "!knownBall")
    args.append("free" if FreeBall else "!free")
    args.append("transition" if Transition else "!transition")
    args.append("goal" if TransitionGoal else "!goal")
    args.append("pass" if TransitionPass else "!pass")
    
    activeDT = args
    
    OurBall = 1 if BallHandler > 0 or Transition else 0
    for robot in Robots:
        NearBall = 1 if robot.robotID-1 == dist2Ball.index(dist2BallMin[0]) else 0
        activeMap[robot.robotID-1] = []
        # activeMap[robot.robotID-1].append("knownBall" if knownBall else "!knownBall")
        activeMap[robot.robotID-1].append("OurBall" if OurBall else "!OurBall")
        InPath = 1 if robot.robotID in solution else 0
        if OurBall:
            if Transition:  activeMap[robot.robotID-1].append("Transition")
            else:
                activeMap[robot.robotID-1].append("InPath" if InPath else "!InPath")
                if not InPath:  activeMap[robot.robotID-1].append("LPass" if Pass else "!LPass")
                else:
                    activeMap[robot.robotID-1].append("MyBall" if robot.ball_handler else "FriendBall")
                    if robot.ball_handler:
                        activeMap[robot.robotID-1].append("Goal" if solution[1] == 0 else "Pass")
                        
        else:
            activeMap[robot.robotID-1].append("NearBall" if NearBall else "!NearBall")
            activeMap[robot.robotID-1].append("Timeout" if NearBall else "Defending") #TEMPORARLY
                
            # TODO : FALTA DEFENDING E TIMEOUT
        
        # print(consts.mapConfigJsonPaths)    
        consts.heatMapSituations[robot.robotID-1] = consts.mapConfigJsonPaths.index(activeMap[robot.robotID-1])
    # print(consts.heatMapSituations)
            
    TimeToPass = 1
    oldstrat = strat
     
    if (time.time() - lastKnowBall > TimeToPass):
        knownBall = 1
    strat = StrategyDT
    for i in range(len(args)):
        if args[i] in strat:
            strat=strat[args[i]]

    # for i, s in enumerate(Robots):
    #     if i != maxidRecieve:
    #         s.packet[0] = STOP
    #     if s.ball_handler == 1:
    #         pass

    ss = [0, 0, 0, 0, 0]
    for i, s in enumerate(strat):
        match s:
            case "KICK":     #?#################### KICK #####################
                idRecieve = solution[1]-1
                maxidRecieve = idRecieve
                Robots[BallHandler-1].packet = [KICK, Robots[idRecieve].position[0], Robots[idRecieve].position[1], 0, 0, 0, 0]
                robotAng = np.degrees(np.arctan2(Robots[idRecieve].position[1]-Robots[BallHandler-1].position[1],Robots[idRecieve].position[0]-Robots[BallHandler-1].position[0]))
                if idRecieve == -1:
                    Robots[BallHandler-1].packet = [KICK, consts.FIELD_DIMENSIONS["A"]/20, 0, 1, 0, 0, 0]
                    robotAng = np.degrees(np.arctan2(0-Robots[BallHandler-1].position[1],consts.FIELD_DIMENSIONS["A"]/20-Robots[BallHandler-1].position[0]))
                time2Kick = time.time()
                ss[BallHandler-1] = 1
                
            case "ATTACK":      #?#################### ATTACK #####################
                Robots[dist2Ball.index(dist2BallMin[0])].packet = [ATTACK, Robots[dist2Ball.index(dist2BallMin[0])].ball_position[0], Robots[dist2Ball.index(dist2BallMin[0])].ball_position[1], 0, 0, 0, 0]
                # ss[dist2Ball.index(dist2BallMin[0])] = 1
                ss[np.argmin(dist2Ball)] = 1
                
            case "COVER":      #?#################### COVER #####################
                for j in range(5):
                    if ss[j] == 0:
                        if Robots[j].robotID in [0, 1, 2, 3, 4]:
                            agress = ((consts.FIELD_DIMENSIONS["A"]/20 + Robots[i].nearestOpponent[0]))/(consts.FIELD_DIMENSIONS["A"]/10)
                            if agress > 0.5:
                                agress = 0.5
                            Robots[j].packet = [COVER, -consts.FIELD_DIMENSIONS["A"]/20, 0, Robots[i].nearestOpponent[0], Robots[i].nearestOpponent[1],  0.5, 1-agress, 0, 0]
                            ss[j] = 1
                            break
                        
            case "RECIEVE":      #?#################### RECIEVE #####################
                if idRecieve == -1:
                    # if "transition" in args:
                        # Robots[dist2Ball.index(dist2BallMin[0])].packet = [ATTACK, Robots[dist2Ball.index(dist2BallMin[0])].ball_position[0], Robots[dist2Ball.index(dist2BallMin[0])].ball_position[1], 0, 0, 0, 0]
                        # ss[np.argmin(dist2Ball)] = 1
                    print("to goal")
                elif "transition" in args:
                    Robots[maxidRecieve].packet = [RECIEVE, Robots[maxidRecieve].ball_position[0], Robots[maxidRecieve].ball_position[1], 0, 0, 0, 0]
                    ss[maxidRecieve] = 1
                elif idRecieve != BallHandler-1:
                    Robots[idRecieve].packet = [RECIEVE, Robots[BallHandler-1].ball_position[0], Robots[BallHandler-1].ball_position[1], 0, 0, 0, 0]
                    ss[idRecieve] = 1
                else:
                    print("nao é nada")
                    
            case "DEFEND":      #?#################### DEFEND #####################
                if BallHandler != 1:
                    Robots[0].packet = [DEFEND,  Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0]
                    ss[0] = 1

    if BallHandler != 0 and kick == 0 and DEBUG_KEYS_SIMULATION:
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



def calculateHeatMaps(Robots, selectedRobot, solution, situation):
    Robots[selectedRobot].probField[-2].field1 = Robots[0].probField[0].calculateOpponents(Robots[selectedRobot].ball_position, Robots[selectedRobot].otherRobots, Robots[selectedRobot].probField[-2])
    loc = []
    for robot in Robots:
        loc.append(robot.position[0:2])
    Robots[selectedRobot].probField[-1].field1 = Robots[0].probField[0].calculateFriends(loc, Robots[selectedRobot].probField[-1])
    for robot in Robots:
        robot.probField[-1].field1 = Robots[selectedRobot].probField[-1].field1
        robot.probField[-2].field1 = Robots[selectedRobot].probField[-2].field1
        if consts.MainMenus[4][2][2].getValue():
            robot.probField[0].calculate(robot.probField[1:], robot, Robots, solution)
        else:
            robot.probField[0].calculate(robot.probField[1:], robot, Robots, solution, situation[robot.robotID-1])
    # Robots[0].probField[0].calculate(robot.probField[1:], robot, Robots, solution)
    # print(Robots[selectedRobot].probField[0].meanValue)
    return Robots

def positionRobotsRefBox(command, message, Robots):
    
    match command:
        case "NONE":        pass
        case "PENALTY":     
            if message in myIPs:    #Nosso Penalty
                Robots[0].packet = [DEFEND, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0]
                Robots[1].packet = [MOVE, Robots[1].ball_position[0]-2, Robots[1].ball_position[1], 0, 0, 0, 0]
                Robots[2].packet = [STOP, 0, 0, 0, 0, 0, 0]
                Robots[3].packet = [STOP, 0, 0, 0, 0, 0, 0]
                Robots[4].packet = [STOP, 0, 0, 0, 0, 0, 0]
            else:                   #Deles
                Robots[0].packet = [DEFEND, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0]
                Robots[1].packet = [STOP, 0, 0, 0, 0, 0, 0]
                Robots[2].packet = [STOP, 0, 0, 0, 0, 0, 0]
                Robots[3].packet = [STOP, 0, 0, 0, 0, 0, 0]
                Robots[4].packet = [STOP, 0, 0, 0, 0, 0, 0]
        case "CORNER":      
            if message in myIPs:    #Nosso Canto
                Robots[0].packet = [DEFEND, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0]
                Robots[1].packet = [STOP, 0, 0, 0, 0, 0, 0]
                Robots[2].packet = [STOP, 0, 0, 0, 0, 0, 0]
                Robots[3].packet = [STOP, 0, 0, 0, 0, 0, 0]
                Robots[4].packet = [STOP, 0, 0, 0, 0, 0, 0]
            else:                   #Canto deles
                Robots[0].packet = [DEFEND, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0]
                Robots[1].packet = [STOP, 0, 0, 0, 0, 0, 0]
                Robots[2].packet = [STOP, 0, 0, 0, 0, 0, 0]
                Robots[3].packet = [STOP, 0, 0, 0, 0, 0, 0]
                Robots[4].packet = [STOP, 0, 0, 0, 0, 0, 0]
        case "THROWIN":     
            if message in myIPs:    #Nosso THROWIN
                Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
            else:                   #deles
                Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
        case "GOALKICK":    
            if message in myIPs:    #Nosso GOALKICK
                Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
            else:                   #deles
                Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
        case "FREEKICK":    
            if message in myIPs:    #Nosso FREEKICK
                Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
            else:                   #deles
                Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
        case "KICKOFF":     
            if message in myIPs:    #Nosso KICKOFF
                Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
            else:                   #KICKOFF deles
                Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
        case "DROPBALL":   
            if message in myIPs:    #DROPBALL Canto
                Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
            else:                   #DROPBALL deles
                Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
                Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
        case "PARK":
            Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
            Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
            Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
            Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]
            Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0]

    return Robots