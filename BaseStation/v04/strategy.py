from Robot import *
from consts import *
import json

BallHandler = -1
CanShoot = 0
CanGoal = 0
CanPass = 0
knownBall = 0
Refbox = 0
BallPosition = []
args = []
strat = []
oldstrat = []

############ STRATEGY INIT ############
with open('./decisionTree.json', 'r') as f:
  StrategyDT = json.load(f)

def checkLineOfPass(Robots):
    return 0

def strategyTEMP(Robots, kick, recebe):
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
                break
    
    args = []
    args.append("RefBox" if Refbox == 1 else "!RefBox")
    args.append("Ball" if BallHandler > 0 else "!Ball")
    args.append("CanShoot" if CanShoot == 1 else "!CanShoot")
    args.append("CanGoal" if CanGoal == 1 else "!CanGoal")
    args.append("CanPass" if CanPass == 1 else "!CanPass")
    args.append("knownBall" if knownBall == 1 else "!knownBall")

    #print(args)
    oldstrat = strat
    if "KICK" in oldstrat and "RECIEVE" in oldstrat:
        knownBall = 1
    strat = StrategyDT
    for i in range(6):
        if args[i] in strat:
            strat=strat[args[i]]
    print(strat)
    for index, robot in enumerate(Robots):
        robot.temp = strat[index]
    #print(StrategyDT)
    #print(f'{globals()[([0])]}')
    #print(f'{eval(StrategyDT["RefBox"]["Start"][0])}')

    
    if Robots[1].ball_handler == 0 and kick == 0:
        Robots[1].packet = [ATTACK, Robots[1].ball_position[0], Robots[1].ball_position[1], 0, 0, 0, 0, 0]
    else:
        kick = 1
        Robots[1].packet = [KICK, Robots[0].position[0], Robots[0].position[1], 0, 0, 0, 0, 0]
        if Robots[1].ball_handler == 0:
            Robots[1].packet = [STOP, 0, 0, 0, 0, 0, 0, 0]

    if Robots[0].ball_handler == 1:
        if Robots[0].checkPosition(Robots[0].packet[1], Robots[0].packet[2]):
            Robots[0].packet = [KICK, -14, -2, 1, 0, 0, 0, 0]
        else:
            Robots[0].packet = [MOVE, -7, 3, 1, -14, -2, 0, 0]
    else:
        if Robots[0].checkPosition(Robots[0].packet[1], Robots[0].packet[2]) or kick == 1:
            Robots[0].packet = [RECIEVE, Robots[1].ball_position[0], Robots[1].ball_position[1], 0, 0, 0, 0, 0]
        else:
            Robots[0].packet = [MOVE, 2, 0, 0, 0, 0, 0, 0]

    Robots[2].packet = [STOP, 0, 0, 0, 0, 0, 0, 0]
    Robots[3].packet = [STOP, 0, 0, 0, 0, 0, 0, 0]

    Robots[4].packet = [DEFEND, Robots[0].ball_position[0], Robots[0].ball_position[1], 0, 0, 0, 0, 0]
    if Robots[4].ball_handler == 1:
        Robots[4].packet = [KICK, Robots[2].position[0], Robots[2].position[1], 0, 0, 0, 0, 0]
        recebe = 1
    if recebe == 1:
        Robots[2].packet = [RECIEVE, Robots[1].ball_position[0], Robots[1].ball_position[1], 0, 0, 0, 0, 0]
        if Robots[2].ball_handler == 1:
            Robots[2].packet = [KICK, Robots[3].position[0], Robots[3].position[1], 0, 0, 0, 0, 0]
            Robots[3].packet = [RECIEVE, Robots[2].ball_position[0], Robots[2].ball_position[1], 0, 0, 0, 0, 0]
    elif kick == 0:
        Robots[2].packet = [COVER, Robots[0].position[0], Robots[0].position[1], Robots[3].ball_position[0], Robots[3].ball_position[1], 1, 0.5, 0]    
    else:
        Robots[2].packet = [MOVE, -5, -4, 0, 0, 0, 0, 0]
    

    return Robots, kick, recebe
        