"""This module is responsible for the strategy of the team. It will have multiple files and  ultiple possible strategies, but its based on the decisionTree.json file.
"""
import time
from robot import *
from consts import *
import json
import decisionMaking
import guiFuncs
import plots
import pathFinding
import pathPredicter
from scipy.optimize import linear_sum_assignment
import refBox
from collections import Counter


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
Penalti = 0
time2Kick = 0
FreeBall = 0
Transition = 0
TransitionGoal = 0
TransitionPass = 0
overallProb = 0
overallProbTemp = 0
prevProb = 0
solutionProbsTemp = 0
overAllProbCounter = 0
solutionProbs = []
oldstrat = []
solutionTemp = 0
finalSolution = []
finalSolutionProbs = []
prevSolution = []
refBoxSlow = 0
solutionCounter = 1000
activeDT = []
activeMap = [[], [], [], [], []]

graph1 = plots.plot(0.2, 0.2, 0, 10, -3, 3, 0, 0, 10)

solutionArray = []




state = 0
previous_state = -1
start_state_time = 0

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


def mainStrategy(Robots, kick, recebe, nextStart, ourBall):
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
    global overallProb
    global overallProbTemp
    global prevProb
    global solutionProbsTemp
    global solutionProbs
    global overAllProbCounter
    global solutionCounter
    global solutionTemp
    global prevSolution
    global solutionArray
    global finalSolution
    global refBoxSlow
    global Penalti
    global finalSolutionProbs
    loopTime = time.time()
    # BallHandler, Shoot, Goal, Pass, knownBall, BallPosition, Refbox, StrategyDT, args, strat, oldstrat, lastKnowBall = getGameState(Robots, solution)
    BallHandler = 0
    for index, robot in enumerate(Robots):
        if robot.ball_handler != 0:
            BallHandler = index+1
            break

    dist2Ball = []
    for robot in Robots:
        if robot.fps == -1:# or robot.ball_position[2] < 0.2:
            dist2Ball.append(998)
        elif robot.robotID == 1:
            dist2Ball.append(999)
        else:
            dist2Ball.append(robot.dist2Ball)
    
    dist2BallMin = np.sort(dist2Ball)
    #for i in range(5):
    #    print(dist2Ball.index(dist2BallMin[i]), end=" | ")
    # print()


    if BallHandler > 0:
        playersMap, playersMapProbs = decisionMaking.calculateGraph(Robots, BallHandler, show = 1)
        #print(BallHandler)
        if refBoxSlow and not Penalti:
            playersMap[str(BallHandler)][-1] = ('0', 100)
        # print()
        #print(playersMap)
        graph = pathFinding.Graph(playersMap)
        # if Penalti:
        #     graph[]
        solutionTemp = graph.a_star_algorithm(str(BallHandler), '0')

        solutionTemp = [int(a) for a in solutionTemp]
        solutionProbsTemp = []
        for index in range(len(solutionTemp)-1):
            solID = solutionTemp[index+1]-1
            if solutionTemp[index] <= solID:
                solID -= 1
            solutionProbsTemp.append(playersMapProbs[str(solutionTemp[index])][solID][1])
        
        prevOverallProb = overallProb
        overallProbTemp = 1
        for i in solutionProbsTemp:
            overallProbTemp *= i

        solution = solutionTemp
        solutionProbs = solutionProbsTemp
        overallProb = overallProbTemp
        
        if finalSolution == []:
            finalSolution = solution
            finalSolutionProbs = []
            for index in range(len(finalSolution)-1):
                solID = finalSolution[index+1]-1
                if finalSolution[index] <= solID:
                    solID -= 1
                finalSolutionProbs.append(playersMapProbs[str(finalSolution[index])][solID][1])

        solutionCounter += 1
        #print(solution)

        solutionArray.append(solution)

        if len(solution) > 1:
            if solution[1] == 0:
                playersMap[str(solution[0])][4] = ("0", 100)
            elif (solution[0] > solution[1]):
                playersMap[str(solution[0])][solution[1]-1] = (str(solution[1]-1), 100)
            else:
                playersMap[str(solution[0])][solution[1]-2] = (str(solution[1]-2), 100)
            graph = pathFinding.Graph(playersMap)
            solution2 = graph.a_star_algorithm(str(BallHandler), '0')
            solution2 = [int(a) for a in solution2]
            solutionProbs2 = []
            for index in range(len(solution2)-1):
                solID = solution2[index+1]-1
                if solution2[index] <= solID:
                    solID -= 1
                solutionProbs2.append(playersMapProbs[str(solution2[index])][solID][1])
            
            # for i in range(len(solution2)-2):
            #     guiFuncs.drawLine(Robots[solution2[i]-1].position, Robots[solution2[i+1]-1].position, color=COLORS["batYellow"], width=2, text=str(solutionProbs2[i]))
            # guiFuncs.drawLine(Robots[solution2[-2]-1].position, (consts.FIELD_DIMENSIONS["A"]/20, 0), color=COLORS["batYellow"], width=2, text=str(solutionProbs2[-1]))
            
        # for i in range(len(solution)-2):
        #     guiFuncs.drawLine(Robots[solution[i]-1].position, Robots[solution[i+1]-1].position, color=COLORS["pink"], width=int(10*solutionProbs[i]), text=str(solutionProbs[i]))
        # guiFuncs.drawLine(Robots[solution[-2]-1].position, (consts.FIELD_DIMENSIONS["A"]/20, 0), color=COLORS["pink"], width=int(10*solutionProbs[-1]), text=str(solutionProbs[-1]))
        
        if solutionCounter >= 25:
            solutionArrayTemp = []
            for i in solutionArray:
                b = ""
                for a in i:
                    b += str(a)
                solutionArrayTemp.append(b) 
            #flattened_solutions = [a for a in solutionArrayTemp]
            solution_counts = Counter(solutionArrayTemp)
            tt = []
            try:
                tt = [int(i) for i in solution_counts.most_common(1)[0][0]]
                #print(tt)
            #for a, count in solution_counts.items():
            #    print(f"{a}: {count}")
            #try:
            #    print(max(solution_counts))
            #    print(solution_counts.most_common(1)[0][0])

                finalSolution = tt
                finalSolutionProbs = []
                for index in range(len(finalSolution)-1):
                    solID = finalSolution[index+1]-1
                    if finalSolution[index] <= solID:
                        solID -= 1
                    finalSolutionProbs.append(playersMapProbs[str(finalSolution[index])][solID][1])
            except:
                pass
            ##print("##########################")

            #print(tt)
            #freq = np.array([np.count_nonzero(arr1 == i) for i in ])
            solutionArray = []
            solutionCounter = 0
            #tt = []

            #prevSolution = solution
            #solution = solutionTemp
        
        #! OFF FOR PICTURES LIME GREEN; POSITIONING
        # for i in range(len(finalSolution)-2):
        #     guiFuncs.drawLine(Robots[finalSolution[i]-1].position, Robots[finalSolution[i+1]-1].position, color=COLORS["limeGreen"], width=5)
        # guiFuncs.drawLine(Robots[finalSolution[-2]-1].position, (consts.FIELD_DIMENSIONS["A"]/20, 0), color=COLORS["limeGreen"], width=5)

    elif DEBUG_KEYS_SIMULATION:
        kick = 0 # THIS IS TO STOP AT EACH PASS
        #finalSolution = []
        #finalSolutionProbs = []
        tt = []
        finalSolution = []#solution
        finalSolutionProbs = []
        solutionArray = []
        solutionCounter = 0
        #print("entrei aqui 1")
    else:
        finalSolution = []#solution
        finalSolutionProbs = []
        tt = []
        solutionArray = []
        solutionCounter = 0
        #print("entre aqui 2")
    
    if consts.PRINTTIME:        print(round((time.time()-loopTime)*1000), "ms | ", end=' ')
    #?#################### HUNGARIAN ALGORITHM TO MAKE THEM SWAP POSITIONS ######################
    robotsLocationTemp = np.array([robot.position[0:2] for robot in Robots[0:5]])
    ZonesLocationTemp = (np.array(consts.ZonesPointsLoc[0:5]))
    
    #* This is to give the player with the ball the nearest zone regarding the Hungarian Algorithm
    ball_handler_Zones_Dist = [0, 0, 0, 0, 0]
    if BallHandler:
        for i in range(len(ball_handler_Zones_Dist)):
            ball_handler_Zones_Dist[i] = getDistance(Robots[BallHandler-1].position, ZonesLocationTemp[i])
        # print(ball_handler_Zones_Dist.index(min(ball_handler_Zones_Dist)), ball_handler_Zones_Dist)
        ZonesLocationTemp[ball_handler_Zones_Dist.index(min(ball_handler_Zones_Dist))] = Robots[BallHandler-1].position[0:2]
    
    row, col, distances = decisionMaking.hungarian(robotsLocationTemp, ZonesLocationTemp)
    min_distance = distances[row, col].sum()
    for i in range(len(row)):
        if Robots[row[i]].fps != -1 or not robot.inGame:
            # guiFuncs.drawLine(Robots[row[i]].position, consts.ZonesPointsLoc[col[i]], color=COLORS["skyblue"], width=1)
            Robots[row[i]].probField[3].field = consts.zonesFields[col[i]]
            Robots[row[i]].probField[3].zonePoint = consts.ZonesPointsLoc[col[i]]


    #?#################### HUNGARIAN ALGORITHM TO assign defense ######################
    robotsLocationTemp = np.array([robot.position[0:2] for robot in Robots[1:]])    
    OpponentRobotLocations = []
    for robot in Robots:
        if robot.fps != -1 or not robot.inGame:
            robot.nearestOpponent = [-100, -100]
            for i in robot.otherRobots:
                OpponentRobotLocations.append(i[0:2])
            break
        else:
            continue
    OpponentRobotLocations = np.array(OpponentRobotLocations)
    # print(1, OpponentRobotLocations)
    # print(2, robotsLocationTemp)
    
    # for  robot in Robots:
    #     print(robot.robotID, " -- ", robot.otherRobots)
    
    row1, col1, distances = decisionMaking.hungarian(robotsLocationTemp, OpponentRobotLocations)
    min_distance = distances[row1, col1].sum()
    # print(row1, col1, len(row1), len(col1))
    
    for i in range(len(row1)):
        if Robots[row1[i]].fps != -1 or not robot.inGame:
            try:
                # guiFuncs.drawLine(robotsLocationTemp[row1[i]], OpponentRobotLocations[col1[i]], color=COLORS["black"], width=2)
                # guiFuncs.drawLine(Robots[row[i]+1].position, Robots[row[i]+1].otherRobots[col1[i]], color=COLORS["black"], width=1)
                Robots[row1[i]+1].nearestOpponent = OpponentRobotLocations[col1[i]]
                # print(robotsLocationTemp[row[i]], Robots[row1[i]+1])
                # guiFuncs.drawLine(Robots[row[i]].position, Robots[row[i]].nearestOpponent, color=COLORS["skyblue"], width=1)
            except:
                pass
    
    
    if consts.PRINTTIME:        print(round((time.time()-loopTime)*1000), "ms | ", end=' ')
    #?#################### BALL MOVEMENT PREDICTION ######################
    ballPath.NextMove(Robots[1].ball_position[0], Robots[1].ball_position[1]) #CORRIGIR ISTO | nao pode ser so de um robo
    ballPath.getPrediction(2) # pegar no valor apos 2 loops
    nextBallPosition = [ballPath.nextXUI, ballPath.nextYUI]
    ballPath.NextAngle(np.degrees(np.arctan2(ballPath.nextYUI-ballPath.Y[-1], ballPath.nextXUI-ballPath.X[-1])))
    
    
    if consts.PRINTTIME:        print(round((time.time()-loopTime)*1000), "ms | ", end=' ')
    #?########################## GET GAME STATE VARIBALES #################################
    
    if BallHandler != 0:
        ourBall = 0
        FreeBall = 0
        Transition = 0
        TransitionGoal = 0
        TransitionPass = 0
        Shoot = 1 if Robots[BallHandler-1].position[0] > 0 else 0
        if Shoot and len(finalSolution)>1:
            if finalSolution[1] == 0 and finalSolutionProbs[0] >= MINPROBGOAL + HISTERESEGOAL:
                Goal = 1 
            elif finalSolution[1] == 0 and finalSolutionProbs[0] <= MINPROBGOAL - HISTERESEGOAL:#finalSolutionProbs[0] <= MINPROBPASS - HISTERESEPASS:
                Goal = 0
                
        if finalSolutionProbs[0] >= MINPROBPASS + HISTERESEPASS:
            Pass = 1 
        elif finalSolutionProbs[0] <= MINPROBPASS - HISTERESEPASS:
            Pass = 0
            
        knownBall = 1
        lastKnowBall = time.time()
        freeBalltime = time.time()
        
        
    else:
        Shoot = 0
        Goal = 0
        Pass = 0
        if (abs(round(ballPath.angle[-1]-robotAng)) < ANGLEMARGIN and round(time.time()-freeBalltime) < freeBallTimeout and FreeBall == 0) or time.time() - time2Kick < 0.5:
            guiFuncs.drawLine(Robots[1].ball_position, nextBallPosition, color=COLORS["brightblue"], width=3)
            Transition = 1
            if idRecieve == -1:
                TransitionGoal = 1
            else:
                TransitionPass = 1
        else:
            guiFuncs.drawLine(Robots[1].ball_position, nextBallPosition, color=COLORS["red"], width=3)
            FreeBall = 1
            Transition = 0
    
    args = []
    args.append("Ball" if BallHandler > 0 else "!Ball")
    args.append("Shoot" if Shoot else "!Shoot")
    args.append("Goal" if Goal else "!Goal")
    args.append("Pass" if Pass else "!Pass")
    args.append("knownBall" if knownBall else "!knownBall")
    if ourBall:
        args.append("ourBall")
    else:
        if time.time()-nextStart < 0:
            args.append("opponent")
        else:
            args.append("free" if FreeBall else "!free")
    args.append("transition" if Transition else "!transition")
    args.append("goal" if TransitionGoal else "!goal")
    args.append("pass" if TransitionPass else "!pass")
    
    activeDT = args
    
    OurBall = 1 if BallHandler > 0 or Transition else 0
    for robot in Robots:
        NearBall = 1 if robot.robotID-1 == dist2Ball.index(dist2BallMin[0]) else 0
        activeMap[robot.robotID-1] = []
        activeMap[robot.robotID-1].append("OurBall" if OurBall else "!OurBall")
        InPath = 1 if robot.robotID in finalSolution else 0
        if OurBall:
            if Transition:  activeMap[robot.robotID-1].append("Transition")
            else:
                activeMap[robot.robotID-1].append("InPath" if InPath else "!InPath")
                if not InPath:  activeMap[robot.robotID-1].append("LPass" if Pass else "!LPass")
                else:
                    activeMap[robot.robotID-1].append("MyBall" if robot.ball_handler else "FriendBall")
                    if robot.ball_handler:
                        if not Pass:
                            activeMap[robot.robotID-1].append("!Pass")
                        else:
                            activeMap[robot.robotID-1].append("Goal" if finalSolution[1] == 0 else "Pass")
                    else:
                        activeMap[robot.robotID-1].append("Pass" if Pass else "!Pass")
                         
        else:
            activeMap[robot.robotID-1].append("NearBall" if NearBall else "!NearBall")
            activeMap[robot.robotID-1].append("Timeout" if NearBall else "Defending") #TEMPORARLY
                
            # TODO : FALTA DEFENDING E TIMEOUT
        
        consts.heatMapSituations[robot.robotID-1] = consts.mapConfigJsonPaths.index(activeMap[robot.robotID-1])
            
    if consts.PRINTTIME:        print(round((time.time()-loopTime)*1000), "ms | ", end=' ')
    TimeToPass = 1
    oldstrat = strat
     
    if (time.time() - lastKnowBall > TimeToPass):
        knownBall = 1
    strat = StrategyDT
    for i in range(len(args)):
        if args[i] in strat:
            strat=strat[args[i]]
    ss = [0, 0, 0, 0, 0]
    for i, s in enumerate(strat):
        match s:
            case "KICK":     #?#################### KICK #####################
                Penalti = 0
                refBoxSlow = 0
                idRecieve = finalSolution[1]-1
                maxidRecieve = idRecieve
                Robots[BallHandler-1].packet = [KICK, Robots[idRecieve].position[0], Robots[idRecieve].position[1], 0, Robots[BallHandler-1].moveTo[0], Robots[BallHandler-1].moveTo[1], 0, 0]
                robotAng = np.degrees(np.arctan2(Robots[idRecieve].position[1]-Robots[BallHandler-1].position[1],Robots[idRecieve].position[0]-Robots[BallHandler-1].position[0]))
                if idRecieve == -1:
                    print("GOLO")
                    Robots[BallHandler-1].packet = [KICK, consts.FIELD_DIMENSIONS["A"]/20, -1, 1, Robots[BallHandler-1].moveTo[0], Robots[BallHandler-1].moveTo[1], 0, 0]
                    robotAng = np.degrees(np.arctan2(0-Robots[BallHandler-1].position[1],consts.FIELD_DIMENSIONS["A"]/20-Robots[BallHandler-1].position[0]))
                time2Kick = time.time()                
                Penalti = 0
                ss[BallHandler-1] = 1
                #* ADICIONEI O MOVE NO KICK MAS ELE ASSIM QUE TIOVER ORIENTADO NO SIMULADOR CHUTA E NO REAL È PARA SER IGUAL
                
            case "ATTACK":      #?#################### ATTACK #####################
                # if Robots[dist2Ball.index(dist2BallMin[0])].robotID != 0:
                #    Robots[dist2Ball.index(dist2BallMin[0])].packet = [ATTACK, Robots[dist2Ball.index(dist2BallMin[0])].ball_position[0], Robots[dist2Ball.index(dist2BallMin[0])].ball_position[1], 0, 0, 0, 0, 0]
                # else:
                Robots[dist2Ball.index(dist2BallMin[0])].packet = [ATTACK, Robots[dist2Ball.index(dist2BallMin[0])].ball_position[0], Robots[dist2Ball.index(dist2BallMin[0])].ball_position[1], 0, 0, 0, Penalti, 0]

                # ss[dist2Ball.index(dist2BallMin[0])] = 1
                ss[np.argmin(dist2Ball)] = 1
                
            case "COVER":      #?#################### COVER #####################
                for j in range(5):
                    if ss[j] == 0:
                        if Robots[j].robotID in [5, 1, 2, 3, 4]:
                            if Robots[j].nearestOpponent[0] <= -100 and Robots[j].nearestOpponent[1] < -100:
                                Robots[j].nearestOpponent = Robots[j].zonePoint
                            print(Robots[j].nearestOpponent)
                            guiFuncs.drawLine(Robots[j].position, Robots[j].nearestOpponent, color=COLORS["brown"], width=1)
                            midpoint = ((-consts.FIELD_DIMENSIONS["A"]/20 + Robots[j].nearestOpponent[0]) // 2, (Robots[j].nearestOpponent[1] + 0) // 2)
                            print(midpoint)
                            guiFuncs.drawLine(Robots[j].position, midpoint, color=COLORS["white"], width=1)
                            agress = ((consts.FIELD_DIMENSIONS["A"]/20 + Robots[j].nearestOpponent[0]))/(consts.FIELD_DIMENSIONS["A"]/10)
                            if agress > 0.75:
                                agress = 0.75
                            # Robots[j].packet = [MOVE, -consts.FIELD_DIMENSIONS["A"]/20, 0, Robots[i].nearestOpponent[0], Robots[i].nearestOpponent[1],  0.5, 1-agress, 0, 0]
                            Robots[j].packet = [MOVE, midpoint[0], midpoint[1], 1, Robots[j].ball_position_robot[0], Robots[j].ball_position_robot[1], 0, 0]
                            ss[j] = 1
                            break
                        
            case "RECIEVE":      #?#################### RECIEVE #####################
                if idRecieve == -1:
                    # if "transition" in args:
                    #     Robots[dist2Ball.index(dist2BallMin[0])].packet = [ATTACK, Robots[dist2Ball.index(dist2BallMin[0])].ball_position[0], Robots[dist2Ball.index(dist2BallMin[0])].ball_position[1], 0, 0, 0, 0]
                    #     ss[np.argmin(dist2Ball)] = 1
                    print("to goal")
                elif "transition" in args:
                    Robots[maxidRecieve].packet = [RECIEVE, Robots[maxidRecieve].ball_position[0], Robots[maxidRecieve].ball_position[1], 0, 0, 0, 0, 0]
                    ss[maxidRecieve] = 1
                elif idRecieve != BallHandler-1:
                    Robots[idRecieve].packet = [RECIEVE, Robots[BallHandler-1].ball_position[0], Robots[BallHandler-1].ball_position[1], 0, 0, 0, 0, 0]
                    ss[idRecieve] = 1
                else:
                    print("nao é nada")
                    
            case "DEFEND":      #?#################### DEFEND #####################
                    Robots[0].packet = [DEFEND,  Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
                    ss[0] = 1

            case "MOVE":      #?#################### MOVE #####################
                for i, a in enumerate(ss):
                    if a == 0:
                        # print(i, "MOVE", end="")
                        Robots[i].packet = [MOVE, Robots[i].moveTo[0], Robots[i].moveTo[1], 1, Robots[i].ball_position_robot[0], Robots[i].ball_position_robot[1], 0, 0]

 
    #for robot in Robots:
    #    if robot.inGame and robot.packet[0] == MOVE:
    #        robot.packet[0] = STOP
    

    if BallHandler != 0 and kick == 0 and DEBUG_KEYS_SIMULATION:
        for robot in Robots:
            if robot.packet[0] == KICK:
                robot.packet[0] = STOP
            
    return Robots, kick, recebe, finalSolution, ourBall

def playMaker(Robots, kick, recebe, nextStart, ourBall, arg):
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
    global overallProb
    global overallProbTemp
    global prevProb
    global solutionProbsTemp
    global solutionProbs
    global overAllProbCounter
    global solutionCounter
    global solutionTemp
    global prevSolution
    global solutionArray
    global finalSolution
    global refBoxSlow
    global Penalti
    global finalSolutionProbs
    global state, previous_state, start_state_time
    
    # BallHandler, Shoot, Goal, Pass, knownBall, BallPosition, Refbox, StrategyDT, args, strat, oldstrat, lastKnowBall = getGameState(Robots, solution)
    BallHandler = 0
    for index, robot in enumerate(Robots):
        if robot.ball_handler != 0:
            BallHandler = index+1
            break

    dist2Ball = []
    for robot in Robots:
        if robot.fps == -1:# or robot.ball_position[2] < 0.2:
            dist2Ball.append(998)
        elif robot.robotID == 1:
            dist2Ball.append(999)
        else:
            dist2Ball.append(robot.dist2Ball)
    
    dist2BallMin = np.sort(dist2Ball)
    #for i in range(5):
    #    print(dist2Ball.index(dist2BallMin[i]), end=" | ")
    # print()


    if BallHandler > 0:
        playersMap, playersMapProbs = decisionMaking.calculateGraph(Robots, BallHandler, show = 1)
        #print(BallHandler)
        if refBoxSlow and not Penalti:
            playersMap[str(BallHandler)][-1] = ('0', 100)
        # print()
        #print(playersMap)
        graph = pathFinding.Graph(playersMap)
        # if Penalti:
        #     graph[]
        solutionTemp = graph.a_star_algorithm(str(BallHandler), '0')

        solutionTemp = [int(a) for a in solutionTemp]
        solutionProbsTemp = []
        for index in range(len(solutionTemp)-1):
            solID = solutionTemp[index+1]-1
            if solutionTemp[index] <= solID:
                solID -= 1
            solutionProbsTemp.append(playersMapProbs[str(solutionTemp[index])][solID][1])
        
        prevOverallProb = overallProb
        overallProbTemp = 1
        for i in solutionProbsTemp:
            overallProbTemp *= i

        solution = solutionTemp
        solutionProbs = solutionProbsTemp
        overallProb = overallProbTemp
        
        if finalSolution == []:
            finalSolution = solution
            finalSolutionProbs = []
            for index in range(len(finalSolution)-1):
                solID = finalSolution[index+1]-1
                if finalSolution[index] <= solID:
                    solID -= 1
                finalSolutionProbs.append(playersMapProbs[str(finalSolution[index])][solID][1])

        solutionCounter += 1
        #print(solution)

        solutionArray.append(solution)

        if len(solution) > 1:
            if solution[1] == 0:
                playersMap[str(solution[0])][4] = ("0", 100)
            elif (solution[0] > solution[1]):
                playersMap[str(solution[0])][solution[1]-1] = (str(solution[1]-1), 100)
            else:
                playersMap[str(solution[0])][solution[1]-2] = (str(solution[1]-2), 100)
            graph = pathFinding.Graph(playersMap)
            solution2 = graph.a_star_algorithm(str(BallHandler), '0')
            solution2 = [int(a) for a in solution2]
            solutionProbs2 = []
            for index in range(len(solution2)-1):
                solID = solution2[index+1]-1
                if solution2[index] <= solID:
                    solID -= 1
                solutionProbs2.append(playersMapProbs[str(solution2[index])][solID][1])
            
            # for i in range(len(solution2)-2):
            #     guiFuncs.drawLine(Robots[solution2[i]-1].position, Robots[solution2[i+1]-1].position, color=COLORS["batYellow"], width=2, text=str(solutionProbs2[i]))
            # guiFuncs.drawLine(Robots[solution2[-2]-1].position, (consts.FIELD_DIMENSIONS["A"]/20, 0), color=COLORS["batYellow"], width=2, text=str(solutionProbs2[-1]))
            
        for i in range(len(solution)-2):
            guiFuncs.drawLine(Robots[solution[i]-1].position, Robots[solution[i+1]-1].position, color=COLORS["pink"], width=int(10*solutionProbs[i]), text=str(solutionProbs[i]))
        guiFuncs.drawLine(Robots[solution[-2]-1].position, (consts.FIELD_DIMENSIONS["A"]/20, 0), color=COLORS["pink"], width=int(10*solutionProbs[-1]), text=str(solutionProbs[-1]))
        
        if solutionCounter >= 25:
            solutionArrayTemp = []
            for i in solutionArray:
                b = ""
                for a in i:
                    b += str(a)
                solutionArrayTemp.append(b) 
            #flattened_solutions = [a for a in solutionArrayTemp]
            solution_counts = Counter(solutionArrayTemp)
            tt = []
            try:
                tt = [int(i) for i in solution_counts.most_common(1)[0][0]]
                #print(tt)
            #for a, count in solution_counts.items():
            #    print(f"{a}: {count}")
            #try:
            #    print(max(solution_counts))
            #    print(solution_counts.most_common(1)[0][0])

                finalSolution = tt
                finalSolutionProbs = []
                for index in range(len(finalSolution)-1):
                    solID = finalSolution[index+1]-1
                    if finalSolution[index] <= solID:
                        solID -= 1
                    finalSolutionProbs.append(playersMapProbs[str(finalSolution[index])][solID][1])
            except:
                pass
            ##print("##########################")

            #print(tt)
            #freq = np.array([np.count_nonzero(arr1 == i) for i in ])
            solutionArray = []
            solutionCounter = 0
            #tt = []

            #prevSolution = solution
            #solution = solutionTemp
        
        #! OFF FOR PICTURES LIME GREEN; POSITIONING
        for i in range(len(finalSolution)-2):
            guiFuncs.drawLine(Robots[finalSolution[i]-1].position, Robots[finalSolution[i+1]-1].position, color=COLORS["limeGreen"], width=5)
        guiFuncs.drawLine(Robots[finalSolution[-2]-1].position, (consts.FIELD_DIMENSIONS["A"]/20, 0), color=COLORS["limeGreen"], width=5)

    elif DEBUG_KEYS_SIMULATION:
        kick = 0 # THIS IS TO STOP AT EACH PASS
        #finalSolution = []
        #finalSolutionProbs = []
        tt = []
        finalSolution = []#solution
        finalSolutionProbs = []
        solutionArray = []
        solutionCounter = 0
    else:
        finalSolution = []
        finalSolutionProbs = []
        tt = []
        solutionArray = []
        solutionCounter = 0
    
    if state != previous_state:
        start_state_time = time.time()
    previous_state = state
    
    if time.time()-start_state_time > 0.5:
        state+=1
    
    if arg == 1:
        state = -1
    
    #! JOGADA 1
    # match state:
    #     case 0:
    #         Robots[0].packet = [DEFEND,  Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
    #         Robots[2].packet = [COVER, -10.5, 0, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 0.5, 0.5, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.5, 0.5, 0]
    #         consts.SimOpponents[1].packet = [MOVE, -11, -8, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -7.0, 2, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -7.2, -6.5, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, -6.5, 4, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #     case 2:
    #         Robots[0].packet = [DEFEND, 2, -3, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [COVER, -10.5, 0, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 0.1, 0.1, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.3, 0.3, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -6.4, 2.2, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, -11, -7.5, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #     case 4:
    #         Robots[0].packet = [DEFEND, 2, -4, 0, 0, 0, 0, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.3, 0.3, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -6, 2, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, -11, -7, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -7.3, -5, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #     case 6:
    #         Robots[0].packet = [DEFEND, 2, -3, 0, 0, 0, 0, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.3, 0.3, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -5.7, 1.8, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #         Robots[2].packet = [COVER, -10.5, 0, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 0.1, 0.1, 0]
    #     case 8:
    #         Robots[0].packet = [DEFEND, 2, -4, 0, 0, 0, 0, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.3, 0.3, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -5.6, 1, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #         Robots[2].packet = [COVER, -10.5, 0, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 0.1, 0.1, 0]
    #     case 10:
    #         Robots[0].packet = [DEFEND, 2, -3, 0, 0, 0, 0, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.3, 0.3, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -5.5, 0.3, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]            
    #         Robots[2].packet = [COVER, -10.5, 0, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 0.1, 0.1, 0]
    #     case 12:
    #         Robots[0].packet = [DEFEND, 2, -4, 0, 0, 0, 0, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.3, 0.3, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -5.5, 0, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]            
    #         Robots[2].packet = [COVER, -10.5, 0, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 0.1, 0.1, 0]
    #     case 14:
    #         Robots[0].packet = [DEFEND, 2, -3, 0, 0, 0, 0, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.3, 0.3, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -5.7, 0, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]            
    #         Robots[2].packet = [COVER, -10.5, 0, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 0.1, 0.1, 0]
    #     case 16:
    #         Robots[0].packet = [DEFEND, 2, -4, 0, 0, 0, 0, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.3, 0.3, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -5.9, -0.2, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]            
    #         Robots[2].packet = [COVER, -10.5, 0, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 0.1, 0.1, 0]
    #     case 18:
    #         Robots[0].packet = [DEFEND, 2, -3, 0, 0, 0, 0, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.3, 0.3, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -5.9, -0.5, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]            
    #         Robots[2].packet = [COVER, -10.5, 0, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 0.1, 0.1, 0]
    #     case 20:
    #         Robots[0].packet = [DEFEND, 2, -4, 0, 0, 0, 0, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.3, 0.3, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -6.1, -0.5, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #         Robots[2].packet = [COVER, -10.5, 0, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 0.1, 0.1, 0]
    #     case 22:
    #         Robots[0].packet = [DEFEND, 2, -3, 0, 0, 0, 0, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.3, 0.3, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -6.1, 0.2, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #         consts.SimOpponents[1].packet = [ATTACK,  Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0, 0, 0, 0]
    #         Robots[2].packet = [COVER, -10.5, 0, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 0.12, 0.12, 0]
    #     case 24:
    #         Robots[0].packet = [DEFEND, 2, -4, 0, 0, 0, 0, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.5, 0.5, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -6.4, 0.3, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #         Robots[2].packet = [COVER, -10.5, 0, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 0.1, 0.1, 0]
    #     case 26:
    #         Robots[0].packet = [DEFEND, 2, -3, 0, 0, 0, 0, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.5, 0.5, 0]
    #         consts.SimOpponents[2].packet = [RECIEVE, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0, 0, 0, 0]
    #         Robots[2].packet = [COVER, -10.5, 0, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 0.1, 0.1, 0]
    #     case 27:
    #         Robots[0].packet = [DEFEND, 2, -4, 0, 0, 0, 0, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.5, 0.5, 0]
    #         consts.SimOpponents[1].packet = [KICK, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 6, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 0, 0, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0]
    #         consts.SimOpponents[2].packet = [RECIEVE, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0, 0, 0, 0]
            
    #     case 28:
    #         consts.SimOpponents[2].packet = [RECIEVE, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0, 0, 0, 0]
    #         Robots[0].packet = [DEFEND, 2, -3, 0, 0, 0, 0, 0]
    #         Robots[1].packet = [COVER, -10.5, 0, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.5, 0.5, 0]
    #         Robots[2].packet = [COVER, -10.5, 0, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 0.1, 0.1, 0]
    #     case 29:            
    #         consts.SimOpponents[2].packet = [RECIEVE, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 0, 0, 0, 0, 0]
    #     case 31:
    #         consts.SimOpponents[2].packet = [KICK, -11, -0.3, 1, 0, 0, 0, 0]
    #     case 32:
    #         Robots[0].packet = [DEFEND, 2, -1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -4, -2, 1, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, -3.7, -1.4, 1, 0, 0, 0, 0]
    #     case 35:
    #         consts.SimOpponents[2].packet = [MOVE, -5, 1, 1, 0, 0, 0, 0]
    
    
    #! JOGADA 2
    # match state:
    #     case 0:
    #         Robots[0].packet = [DEFEND,  Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
    #         Robots[1].packet = [MOVE, -0.2, -0.75, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -0.2, 0.85, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -2, 2, 0, 0, 0, 0, 0]
    #         Robots[4].packet = [MOVE, -4, 4, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[0].packet = [MOVE, 11, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 2, 1, 1, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 2, 0, 1, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 5, 0, 1, 0, 0, 0, 0]
    #     case 1:
    #         Robots[0].packet = [DEFEND,  Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
    #         Robots[1].packet = [MOVE, 1, -0.75, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -1, -1, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -1.4, -1, 0, 0, 0, 0, 0]
    #         Robots[4].packet = [MOVE, -4, 4, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 0, 3, 1, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 1, 2, 1, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 4, 0, 1, 0, 0, 0, 0]
    #     case 2:
    #         Robots[1].packet = [MOVE, 1.5, -0.5, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -1, -1.5, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -1.5, -1.1, 0, 0, 0, 0, 0]
    #     case 3:
    #         Robots[1].packet = [MOVE, 1.7, -0.3, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -1, -1.7, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -1.7, -1.2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 1, 3, 1, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 2, 3, 1, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 1, -5, 1, 0, 0, 0, 0]
    #     case 4:
    #         Robots[1].packet = [MOVE, 2, -0.1, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -1, -2, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -2, -1, 0, 0, 0, 0, 0]
    #     case 6:
    #         Robots[1].packet = [MOVE, 2, -0.1, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -2, -2, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -3, -3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 2, 1, 1, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 2, 0, 1, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 2, -1, 1, 0, 0, 0, 0]
    #     case 8:
    #         Robots[1].packet = [MOVE, 1, 1, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -1, -3, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -2, 3, 0, 0, 0, 0, 0]
    #     case 13:
    #         Robots[1].packet = [ATTACK, Robots[1].ball_position[0], Robots[1].ball_position[1], 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, 2, -3, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -2, 3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 1.5, 0.2, 1, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 1, 0, 1, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 4, -1.5, 1, 0, 0, 0, 0]
    #     case 16:
    #         Robots[1].packet = [KICK, 3, -2.5, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [RECIEVE, Robots[1].ball_position[0], Robots[1].ball_position[1], 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -2, 3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 3, -1.5, 1, 0, 0, 0, 0]
            
            
    #! JOGADA 3
    # Robots[0].packet = [DEFEND, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
    # consts.SimOpponents[0].packet = [MOVE, 11, 0, 0, 0, 0, 0, 0]
    # match state:
    #     case 0:
    #         Robots[1].packet = [MOVE, -4, 0.5, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -4.4, 0, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -4.8, 0.5, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 3.5, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 3.5, -2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 6, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 6, -4, 0, 0, 0, 0, 0]
    #     case 1:
    #         Robots[1].packet = [MOVE, -1, -2, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -4, 0.5, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -5, 0.4, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 0.5, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 0.5, -2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 6, -3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 6, -5, 0, 0, 0, 0, 0] 
    #     case 4:
    #         Robots[1].packet = [MOVE, -0.5, -3, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -4.5, -0.5, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -5, -0.4, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 0, -0.5, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -1, -1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 6, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 6, -6, 0, 0, 0, 0, 0] 
    #     case 6:
    #         Robots[1].packet = [MOVE, -0.5, -3, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -5, -0.2, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -6, -0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 0, -0.5, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -1, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 6, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 6, -6, 0, 0, 0, 0, 0] 
    #     case 8:
    #         consts.SimOpponents[1].packet = [MOVE, 0, -0.5, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 0, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 6, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 5, -3, 0, 0, 0, 0, 0] 
    #     case 10:
    #         consts.SimOpponents[1].packet = [MOVE, 0, -0.5, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 0, 2.5, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 6, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 5, 2, 0, 0, 0, 0, 0] 
    #     case 15:
    #         Robots[1].packet = [MOVE, 0.5, -3, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -2, -0.2, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -6, -0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [ATTACK, 0, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 5, -2, 0, 0, 0, 0, 0]
    #     case 18:
    #         Robots[1].packet = [MOVE, 0.5, -2, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -1.5, -0.2, 0, 0, 0, 0, 0]
    #     case 20:
    #         Robots[1].packet = [MOVE, 0.5, -1, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -0.5, 0.2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [KICK, 0, 2.5, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [RECIEVE, 0, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 5, -5, 0, 0, 0, 0, 0]
    #     case 22:
    #         Robots[1].packet = [MOVE, 2, -0, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -1, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 1, 1.75, 0, 0, 0, 0, 0]
    #     case 24:
    #         Robots[1].packet = [MOVE, 2, -0, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -1, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 2, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 3, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 5, -5, 0, 0, 0, 0, 0]
    #     case 26:
    #         Robots[1].packet = [MOVE, 2, 1, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -2, 0.5, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 2, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 0, 1.5, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 0, -6, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 5, 0, 0, 0, 0, 0, 0]
    #     case 28:
    #         Robots[1].packet = [MOVE, 2, 0, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -2, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 2, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 0, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 0, -6, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 5, 0, 0, 0, 0, 0, 0]
    #     case 30:
    #         Robots[1].packet = [MOVE, 2, 0, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -2, 0.5, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 2, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 0, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 5, 0, 0, 0, 0, 0, 0]
    #     case 32:
    #         Robots[1].packet = [MOVE, 2, 0, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -1, 1, 0, 0, 0, 0, 0]
    #     case 34:
    #         Robots[1].packet = [MOVE, 2, 0, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -1, 1, 0, 0, 0, 0, 0]
    #     case 36:
    #         Robots[1].packet = [MOVE, 2, 0.5, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -1.5, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 0, -2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -1, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -1, -4, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 4, -3, 0, 0, 0, 0, 0]
    #     case 38:
    #         Robots[1].packet = [MOVE, 2, 0, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -0.5, 0.5, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, -4, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -3, 3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -3, -2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 4, -3, 0, 0, 0, 0, 0]
    #     case 40:
    #         Robots[1].packet = [MOVE, 1, 2, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -2, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [KICK, -11, 0, 1, 0, 0, 0, 0]
    #     case 42:
    #         consts.SimOpponents[1].packet = [MOVE, -4, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -4, -3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 4, -3, 0, 0, 0, 0, 0]
    #     case 44:
    #         Robots[1].packet = [MOVE, 2, 0, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -2, 0, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -12, 0, 0, 0, 0, 0, 0]
    #     case 46:
    #         consts.SimOpponents[1].packet = [MOVE, -4, 4, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 0, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -5, -4, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 2, 4, 0, 0, 0, 0, 0]
            
    #! JOGADA 4
    
    # Robots[0].packet = [DEFEND, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
    # match state:
    #     case -1:
    #         Robots[1].packet = [MOVE, 1, -0.5, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -2.5, 2, 0, 0, 0, 0, 0]
    #         Robots[3].packet = [MOVE, -5, -4, 0, 0, 0, 0, 0]
    #         Robots[4].packet = [MOVE, -11, -8, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 3, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 3, -1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 3, -3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 4, -3, 0, 0, 0, 0, 0]
    #     case 0:
    #         Robots[1].packet = [MOVE, 0, -1, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -2.5, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 3, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 3, -1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 3, -3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 4, -3, 0, 0, 0, 0, 0]
    #     case 6:
    #         Robots[1].packet = [MOVE, 0.3, 0.2, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -2, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 3, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 3, -1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 3, -3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 4, -3, 0, 0, 0, 0, 0]
    #     case 8:
    #         Robots[1].packet = [MOVE, 0.3, 1, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -1.5, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 4, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 3.5, -1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 3, -3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 4, -3, 0, 0, 0, 0, 0]
    #     case 10:
    #         Robots[1].packet = [MOVE, 0.2, 3.5, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -1.5, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 4, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 3, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 3, -1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 4, -1, 0, 0, 0, 0, 0]
    #     case 12:
    #         Robots[1].packet = [MOVE, 0.2, 2.5, 0, 0, 0, 0, 0]
    #         Robots[2].packet = [MOVE, -2, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [MOVE, 4, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 3, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 3, -1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 4, -1, 0, 0, 0, 0, 0]
    #     case 14:
    #         Robots[1].packet = [MOVE, 0.2, 2.5, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [ATTACK, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 2, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 1, 1, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 7, 1, 0, 0, 0, 0, 0]
    #     case 16:
    #         Robots[1].packet = [MOVE, -1, 2.5, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [ATTACK, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 0.5, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 1, -2.5, 0, 0, 0, 0, 0]
    #     case 18:
    #         Robots[1].packet = [MOVE, -0.5, 2.5, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [ATTACK, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 0.5, 3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, 0, -3, 0, 0, 0, 0, 0]
    #     case 20:
    #         Robots[1].packet = [COVER, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], -11, 0, 0.5, 0.2, 0]
    #         consts.SimOpponents[1].packet = [MOVE, -4, 3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 0.5, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -4, -3, 0, 0, 0, 0, 0]
    #     case 22:
    #         Robots[1].packet = [COVER, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], -11, 0, 0.5, 0.2, 0]
    #         consts.SimOpponents[1].packet = [MOVE, -4.2, 3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 0.5, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -4.5, -2.5, 0, 0, 0, 0, 0]
    #     case 24:
    #         Robots[1].packet = [COVER, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], -11, 0, 0.5, 0.2, 0]
    #         consts.SimOpponents[1].packet = [MOVE, -4.5, 3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -5, -1, 0, 0, 0, 0, 0]
    #     case 26:
    #         Robots[1].packet = [COVER, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], -11, 0, 0.5, 0.2, 0]
    #         consts.SimOpponents[1].packet = [MOVE, -4.5, 3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -5.5, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 0, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 0, 0, 0, 0, 0, 0, 0]
    #     case 28:
    #         Robots[1].packet = [COVER,consts.SimOpponents[3].position[0], consts.SimOpponents[3].position[1], consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.8, 0.7, 0]
    #         consts.SimOpponents[1].packet = [MOVE, -4.5, 3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, 0, 3, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -5.5, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 0, 0, 0, 0, 0, 0, 0]
    #     case 30:
    #         Robots[1].packet = [COVER, consts.SimOpponents[3].position[0], consts.SimOpponents[3].position[1], consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.8, 0.7, 0]
    #         consts.SimOpponents[1].packet = [KICK, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 1, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [RECIEVE, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -5.5, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 0, -1, 0, 0, 0, 0, 0]
    #     case 32:
    #         Robots[1].packet = [COVER, consts.SimOpponents[3].position[0], consts.SimOpponents[3].position[1], consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.8, 0.7, 0]
    #         Robots[2].packet = [MOVE, -2, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [KICK, consts.SimOpponents[2].position[0], consts.SimOpponents[2].position[1], 1, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [RECIEVE, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -5.5, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 0, -3, 0, 0, 0, 0, 0]
    #     #case 33:
    #         #consts.SimOpponents[2].packet = [KICK, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 1, 0, 0, 0, 0]
    #     case 34:
    #         Robots[1].packet = [COVER, consts.SimOpponents[3].position[0], consts.SimOpponents[3].position[1], consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.8, 0.7, 0]
    #         Robots[2].packet = [MOVE, -2, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [RECIEVE, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [KICK, consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 1, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -6, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 0, -1, 0, 0, 0, 0, 0]
    #     case 35:
    #         consts.SimOpponents[1].packet = [KICK, -11, -0.8, 9, 0, 0, 0, 0]
    #     case 36:
    #         Robots[1].packet = [COVER, consts.SimOpponents[3].position[0], consts.SimOpponents[3].position[1], consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.7, 0.7, 0]
    #         Robots[2].packet = [MOVE, -1.5, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [KICK, -11, -0.8, 9, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -1, -2, 1, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -6, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 0, -1, 0, 0, 0, 0, 0]
    #     case 38:
    #         Robots[1].packet = [COVER, consts.SimOpponents[3].position[0], consts.SimOpponents[3].position[1], consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.7, 0.7, 0]
    #         Robots[2].packet = [MOVE, -1, 2, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[1].packet = [KICK, -11, -0.8, 9, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -3, -2, 1, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -5, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 0, -1, 0, 0, 0, 0, 0]
    #     case 40:
    #         Robots[1].packet = [COVER, consts.SimOpponents[3].position[0], consts.SimOpponents[3].position[1], consts.SimOpponents[1].position[0], consts.SimOpponents[1].position[1], 0.6, 0.6, 0]
    #         consts.SimOpponents[1].packet = [KICK, -11, -0.8, 9, 0, 0, 0, 0]
    #         consts.SimOpponents[2].packet = [MOVE, -3, -2, 1, 0, 0, 0, 0]
    #         consts.SimOpponents[3].packet = [MOVE, -3, 0, 0, 0, 0, 0, 0]
    #         consts.SimOpponents[4].packet = [MOVE, 0, -1, 0, 0, 0, 0, 0]
            
        
    Robots[0].packet = [DEFEND, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
    match state:
        case -1:
            pass
    
    return Robots, kick, recebe, finalSolution, ourBall, state


def ControlRobots(keyboard, joystick, Robots, selectedRobot, controlIDSList, opo=0):
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
    if opo == 0:
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
    else:
        if consts.NUMBERofJoySticks == 1:
            if 7 in joystick[0] and consts.TempJoyStickPointer < 4:
                consts.SimOpponents[consts.JoyStickPointer].packet = [CONTROL, 0, 0, 0, 0, 0, 0, 0]
                consts.JoyStickPointer = consts.TempJoyStickPointer+1
            elif 6 in joystick[0] and consts.TempJoyStickPointer > 0:
                consts.SimOpponents[consts.JoyStickPointer].packet = [CONTROL, 0, 0, 0, 0, 0, 0, 0]
                consts.JoyStickPointer = consts.TempJoyStickPointer-1
            else:
                consts.TempJoyStickPointer = consts.JoyStickPointer
                
            consts.SimOpponents[consts.JoyStickPointer].packet[0] = CONTROL
            consts.SimOpponents[consts.JoyStickPointer].packet[1] = int(10*joystick[0][0])
            consts.SimOpponents[consts.JoyStickPointer].packet[2] = int(-10*joystick[0][1])
            if 10 or 12 in joystick[0]:
                consts.SimOpponents[consts.JoyStickPointer].packet[1] = int(20*joystick[0][0])
                consts.SimOpponents[consts.JoyStickPointer].packet[2] = int(-20*joystick[0][1])
            if joystick[0][2] != 0 or joystick[0][3] != 0:      consts.SimOpponents[consts.JoyStickPointer].packet[3] = int(np.degrees(np.arctan2(-joystick[0][3], joystick[0][2])))
            if 2 in joystick[0]:   consts.SimOpponents[consts.JoyStickPointer].packet[4] = 1      
            if 4 in joystick[0]:   consts.SimOpponents[consts.JoyStickPointer].packet[4] = 2
            for i in consts.SimOpponents:
                i.sendInfoOpo()
                
        elif consts.NUMBERofJoySticks > 1:
            for i, opo in enumerate(consts.SimOpponents[1:]):
                # if i in controlIDSList:
                opo.packet = [opo.packet[0], 0, 0, opo.packet[3], 0, 0, 0, 0]
                opo.packet[0] = CONTROL
                opo.packet[1] = int(10*joystick[i][0])
                opo.packet[2] = int(-10*joystick[i][1])
                if 10 or 12 in joystick[i]:
                    opo.packet[1] = int(20*joystick[i][0])
                    opo.packet[2] = int(-20*joystick[i][1])
                if joystick[i][2] != 0 or joystick[i][3] != 0:      opo.packet[3] = int(np.degrees(np.arctan2(-joystick[i][3], joystick[i][2])))
                if 2 in joystick[i]:   opo.packet[4] = 1      
                if 4 in joystick[i]:   opo.packet[4] = 2
                opo.sendInfoOpo()
        
    # print(consts.JoyStickPointer)

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
    # Robots[selectedRobot].probField[-3].field1 = Robots[0].probField[0].calculateOpponents(Robots[selectedRobot].ball_position, Robots[selectedRobot].otherRobots, Robots[selectedRobot].probField[-3])
    loc = []
    for robot in Robots:
        loc.append(robot.position[0:2])
    Robots[selectedRobot].probField[-1].field1 = Robots[0].probField[0].calculateCircles(loc, Robots[selectedRobot].probField[-1])
    Robots[selectedRobot].probField[-3].field1 = Robots[0].probField[0].calculateCircles(Robots[selectedRobot].otherRobots, Robots[selectedRobot].probField[-3])
    for robot in Robots:
        robot.probField[-1].field1 = Robots[selectedRobot].probField[-1].field1
        robot.probField[-2].field1 = Robots[selectedRobot].probField[-2].field1
        robot.probField[-3].field1 = Robots[selectedRobot].probField[-3].field1
        robot.probField[0].calculate(robot.probField[1:], robot, Robots, solution, situation[robot.robotID-1])
        if consts.MainMenus[4][2][2].getValue():
            robot.probField[0].calculate(robot.probField[1:], robot, Robots, solution)
        if len(robot.probField[0].centers):
            if robot.probField[0].centers[0] != (0, 0):
                robot.locationCenterDists = []
                for i in range(len(robot.probField[0].locationCenter)):
                    robot.locationCenterDists.append(round(np.sqrt(np.power((robot.position[0] - robot.probField[0].locationCenter[i][0]), 2)+ np.power((robot.position[1] - robot.probField[0].locationCenter[i][1]), 2)),2,))
            
                dist2moveToMin = np.sort(robot.locationCenterDists)
                # print(robot.probField[0].centers, dist2moveToMin, end=" | ")
                if len(robot.locationCenterDists):
                    robot.moveTo = robot.probField[0].locationCenter[robot.locationCenterDists.index(dist2moveToMin[0])]#robot.probField[0].locationCenter[0]
        # print(robot.robotID, robot.moveTo)
        
    # Robots[0].probField[0].calculate(robot.probField[1:], robot, Robots, solution)
    # print(Robots[selectedRobot].probField[0].meanValue)
    return Robots

def positionRobotsRefBox(command, message, Robots):
    global Penalti
    global refBoxSlow
    print("command:", command)
    print(message)
    
    nextStart = time.time()
    if message in refBox.myIPs:
        OurBall = 1
    else:
        OurBall = 0
        
    match command:
        case "NONE":        pass
        case "PENALTY":     
            if message in refBox.myIPs:    #Nosso Penalty
                # dist2Ball = []
                # for robot in Robots:
                #     if robot.fps == -1 or robot.ball_position[2] == 0.0:
                #         dist2Ball.append(999)
                #     else:
                #         dist2Ball.append(robot.dist2Ball)
                # dist2BallMin = np.sort(dist2Ball)
                # print(min(dist2Ball))
                # if min(dist2Ball) > 10:
                #     Robots[1].packet = [MOVE,  2, 2, 1, Robots[1].ball_position_robot[0],  Robots[1].ball_position_robot[1] ,1, 0]
                #     Robots[2].packet = [MOVE,  2, -2, 1, Robots[2].ball_position_robot[0],  Robots[2].ball_position_robot[1] ,1, 0]
                #     Robots[3].packet = [MOVE,  4, 4, 1, Robots[3].ball_position_robot[0],  Robots[3].ball_position_robot[1] ,1, 0]
                #     Robots[4].packet = [MOVE,  4, -4, 1, Robots[4].ball_position_robot[0],  Robots[4].ball_position_robot[1] ,1, 0]
                # else:
                Robots[1].packet = [MOVE,  2,  0, 1, Robots[1].ball_position_robot[0],  Robots[1].ball_position_robot[1] ,1, 0]
                Penalti = 1
                refBoxSlow = 1
            else:                   #Deles
                Robots[0].packet = [DEFEND, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 1, 0]
                Robots[1].packet = [STOP, 0, 0, 0, 0, 0, 0 ,0]
                Robots[2].packet = [STOP, 0, 0, 0, 0, 0, 0, 0]
                Robots[3].packet = [STOP, 0, 0, 0, 0, 0, 0, 0]
                Robots[4].packet = [STOP, 0, 0, 0, 0, 0, 0, 0]
        case "CORNER":      
            if message in refBox.myIPs:    #Nosso Canto
                dist2Ball = []
                for robot in Robots:
                    if robot.fps == -1 or robot.ball_position[2] == 0.0:
                        dist2Ball.append(999)
                    else:
                        dist2Ball.append(robot.dist2Ball)
                dist2BallMin = np.sort(dist2Ball)
                # print(min(dist2Ball))
                if min(dist2Ball) > 10:
                    Robots[1].packet = [MOVE,  7, 3, 1, Robots[1].ball_position_robot[0],  Robots[1].ball_position_robot[1] ,1, 0]
                    Robots[2].packet = [MOVE,  7, -3, 1, Robots[2].ball_position_robot[0],  Robots[2].ball_position_robot[1] ,1, 0]
                    Robots[3].packet = [MOVE,  5, 3, 1, Robots[3].ball_position_robot[0],  Robots[3].ball_position_robot[1] ,1, 0]
                    Robots[4].packet = [MOVE,  5, -3, 1, Robots[4].ball_position_robot[0],  Robots[4].ball_position_robot[1] ,1, 0]
                    refBoxSlow = 1
                else:
                    Robots[dist2Ball.index(dist2BallMin[0])].packet = [MOVE,  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[0],  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[1] +  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[1]/10, 1, Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[0],  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[1] ,1, 0]
            else:                   #Canto deles
                Robots[0].packet = [DEFEND, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0]
                nextStart = time.time()+3
        case "THROWIN":     
            if message in refBox.myIPs:    #Nosso THROWIN
                refBoxSlow = 1
                dist2Ball = []
                for robot in Robots:
                    if robot.fps == -1 or robot.ball_position[2] == 0.0:
                        dist2Ball.append(999)
                    else:
                        dist2Ball.append(robot.dist2Ball)
                dist2BallMin = np.sort(dist2Ball)
                Robots[dist2Ball.index(dist2BallMin[0])].packet = [MOVE,  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[0],  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[1] +  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[1]/10, 1, Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[0],  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[1], 1, 0]

                # Robots[dist2Ball.index(dist2BallMin[0])].packet = [MOVE, Robots[0].ball_position[0], Robots[0].ball_position[1] + Robots[0].ball_position[1]/10, 0, 0, 0, 0]
                
            else:                   #deles
                nextStart = time.time()+3
        case "GOALKICK":    
            if message in refBox.myIPs:    #Nosso GOALKICK
                refBoxSlow = 1
                dist2Ball = []
                for robot in Robots:
                    if robot.fps == -1 or robot.ball_position[2] == 0.0:
                        dist2Ball.append(999)
                    else:
                        dist2Ball.append(robot.dist2Ball)
                dist2BallMin = np.sort(dist2Ball)
                Robots[dist2Ball.index(dist2BallMin[0])].packet = [MOVE,  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[0],  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[1] +  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[1]/10, 1, Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[0],  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[1], 1, 0]

                # Robots[dist2Ball.index(dist2BallMin[0])].packet = [MOVE, Robots[0].ball_position[0], Robots[0].ball_position[1] + Robots[0].ball_position[1]/10, 0, 0, 0, 0]
                
            else:                   #deles
                nextStart = time.time()+5
        case "FREEKICK":    
            if message in refBox.myIPs:    #Nosso FREEKICK
                refBoxSlow = 1
                dist2Ball = []
                for robot in Robots:
                    if robot.fps == -1 or robot.ball_position[2] == 0.0:
                        dist2Ball.append(999)
                    else:
                        dist2Ball.append(robot.dist2Ball)
                dist2BallMin = np.sort(dist2Ball)
                Robots[dist2Ball.index(dist2BallMin[0])].packet = [MOVE,  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[0],  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[1] +  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[1]/10, 1, Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[0],  Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[1], 1, 0]

                # Robots[dist2Ball.index(dist2BallMin[0])].packet = [MOVE, Robots[0].ball_position[0], Robots[0].ball_position[1] + Robots[0].ball_position[1]/10, 0, 0, 0, 0]
                
            else:                   #deles
                nextStart = time.time()+5
        case "KICKOFF":     
            if message in refBox.myIPs:    #Nosso KICKOFF   #?????????? DONE !!!!!!!!!!!!
                refBoxSlow = 1
                dist2Ball = []
                for robot in Robots:
                    if robot.fps == -1 or robot.ball_position[2] == 0.0:
                        dist2Ball.append(999)
                    else:
                        dist2Ball.append(robot.dist2Ball)
                dist2BallMin = np.sort(dist2Ball)
                Robots[dist2Ball.index(dist2BallMin[0])].packet = [MOVE, FIELD_DIMENSIONS["H"]/40, 0, 1, Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[0], Robots[dist2Ball.index(dist2BallMin[0])].ball_position_robot[1], 1, 0]
                Robots[dist2Ball.index(dist2BallMin[1])].packet = [MOVE, -4, 0, 1, Robots[dist2Ball.index(dist2BallMin[1])].ball_position_robot[0], Robots[dist2Ball.index(dist2BallMin[1])].ball_position_robot[1], 1, 0]
                Robots[dist2Ball.index(dist2BallMin[2])].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/20, 1, Robots[dist2Ball.index(dist2BallMin[2])].ball_position_robot[0], Robots[dist2Ball.index(dist2BallMin[2])].ball_position_robot[1], 1, 0]
                Robots[dist2Ball.index(dist2BallMin[3])].packet = [MOVE, -6, FIELD_DIMENSIONS["C"]/20, 1, Robots[dist2Ball.index(dist2BallMin[3])].ball_position_robot[0], Robots[dist2Ball.index(dist2BallMin[3])].ball_position_robot[1], 1, 0]
                
                Robots[0].packet = [DEFEND, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
                # Robots[1].packet = [MOVE, Robots[1].ball_position[0]+FIELD_DIMENSIONS["H"]/40, Robots[0].ball_position[1], 0, 0, 0, 0]
            
            else:                   #KICKOFF deles
                Robots[1].packet = [MOVE, -3, 1.5, 1, Robots[1].ball_position_robot[0], Robots[1].ball_position_robot[1], 1, 0]
                Robots[2].packet = [MOVE, -3, -1.5, 1, Robots[2].ball_position_robot[0], Robots[2].ball_position_robot[1], 1, 0]
                Robots[3].packet = [MOVE, -5, 3, 1, Robots[3].ball_position_robot[0], Robots[3].ball_position_robot[1], 1, 0]
                Robots[4].packet = [MOVE, -5, -3, 1, Robots[4].ball_position_robot[0], Robots[4].ball_position_robot[1], 1, 0]
                nextStart = time.time()+5
        case "DROPBALL":   
            if message in refBox.myIPs:    #DROPBALL Canto
                Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]
                Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]
                Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]
                Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]
                Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]
            else:                   #DROPBALL deles
                Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]
                Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]
                Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]
                Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]
                Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]
        case "PARK":
            Robots[0].packet = [MOVE, -9, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]
            Robots[1].packet = [MOVE, -8, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]
            Robots[2].packet = [MOVE, -7, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]
            Robots[3].packet = [MOVE, -6, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]
            Robots[4].packet = [MOVE, -5, -FIELD_DIMENSIONS["C"]/10-FIELD_DIMENSIONS["L"]/20, 0, 0, 0, 0, 0]

    for robot in Robots:
        if robot.packet[0] == MOVE:
            robot.packet[6] = 1

    return Robots, nextStart, OurBall

def getDistance(a, b):
    return round(np.sqrt(np.power((a[0] - b[0]), 2)+ np.power((a[1] - b[1]), 2)),2,)