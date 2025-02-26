from robot import *
from consts import *
import json
import time
import decisionMaking
import guiFuncs

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

selectedRobot = 0

############ STRATEGY INIT ############
with open('./decisionTree.json', 'r') as f:
  StrategyDT = json.load(f)

def checkLineOfPass(Robots):

    return 0

def getGameState(Robots):
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

    return BallHandler, CanShoot, CanGoal, CanPass, knownBall, BallPosition, Refbox, StrategyDT, args, strat, oldstrat, idRecieve, lastKnowBall


def strategyTEMP(Robots, kick, recebe):
    BallHandler, CanShoot, CanGoal, CanPass, knownBall, BallPosition, Refbox, StrategyDT, args, strat, oldstrat, idRecieve, lastKnowBall = getGameState(Robots)
    
    TimeToPass = 1
    #print(args)
    oldstrat = strat
    if (time.time() - lastKnowBall > TimeToPass):
        knownBall = 1
    strat = StrategyDT
    for i in range(6):
        if args[i] in strat:
            strat=strat[args[i]]
    #print(strat, end=" | ")

    dist2Ball = [robot.dist2Ball for robot in Robots]
    dist2BallMin = np.sort(dist2Ball)
    #print(BallHandler, end=" -- ")
    #print(np.argmin(dist2Ball), end=" -- ")

    for i, s in enumerate(Robots):
        s.packet[0] = STOP
        if s.ball_handler == 1:
            print(s.linesOfPass, end="- ")

    ss = [0, 0, 0, 0, 0]
    for i, s in enumerate(strat):
        if s == "KICK":
            risk_reward = [0, 0, 0, 0, 0]

            success3 = decisionMaking.getSucessProbability("GOAL", [Robots[BallHandler-1].position, (11, 0)])
            guiFuncs.drawProbability(Robots[BallHandler-1].position[0], Robots[BallHandler-1].position[1],round(success3, 2))
            risk_reward[BallHandler-1] = round(success3, 2)
            # print(risk_reward, success3)
            for index, robot in enumerate(Robots):
                if index == BallHandler-1:
                    pass
                success = decisionMaking.getSucessProbability(KICK, [Robots[BallHandler-1].position, robot.position])
                success2 = decisionMaking.getSucessProbability("GOAL", [robot.position, (11, 0)])

                # print(Robots[BallHandler-1].linesOfPass)
                if robot.robotID not in Robots[BallHandler-1].linesOfPass:
                    success = 0#decisionMaking.NoLineOfPassRisk
                if index != BallHandler-1:
                    guiFuncs.drawProbability(robot.position[0], robot.position[1],str(success)+"*"+str(success2)+"="+str(round(success*success2, 2)))
                    risk_reward[index] = round(success*success2, 2)
                guiFuncs.drawLine(robot.position[0], robot.position[1], 11, 0)
                    # guiFuncs.drawProbability(robot.position[0], robot.position[1]+0.5,str(success)+"+"+str(success2)+"="+str(round(success+success2, 2)))
                # guiFuncs.drawProbability(robot.position[0]+1, robot.position[1],success2)
                # print(robot.robotID, success*success2, end=" ! ")#, risk, round(reward-risk, 2), end=" ! ")
            idRecieve = risk_reward.index(max(risk_reward))
            print(risk_reward, end=" | ")
            Robots[BallHandler-1].packet = [KICK, Robots[idRecieve].position[0], Robots[idRecieve].position[1], 0, 0, 0, 0]
            if idRecieve == BallHandler-1:
                idRecieve = -1
                Robots[BallHandler-1].packet = [KICK, 11, 0, 0, 0, 0, 0]
            ss[BallHandler-1] = 1
        elif s == "ATTACK":
            Robots[dist2Ball.index(dist2BallMin[0])].packet = [ATTACK, Robots[dist2Ball.index(dist2BallMin[0])].ball_position[0], Robots[dist2Ball.index(dist2BallMin[0])].ball_position[1], 0, 0, 0, 0]
            ss[np.argmin(dist2Ball)] = 1
        elif s == "RECIEVE":
            if idRecieve != BallHandler-1:
                Robots[idRecieve].packet = [RECIEVE, Robots[BallHandler-1].ball_position[0], Robots[BallHandler-1].ball_position[1], 0, 0, 0, 0]
                ss[idRecieve] = 1
        elif s == "DEFEND" and BallHandler != 5:
            Robots[4].packet = [DEFEND,  Robots[4].ball_position[0], Robots[4].ball_position[1], 0, 0, 0, 0]
            ss[4] = 1


#    for i, s in enumerate(Robots):
#        print(s.robotID,SKILLSGUI[s.packet[0]], end="|")


    '''
    for index, robot in enumerate(Robots):
        robot.skill = strat[index]
        if robot.skill == "MOVE":
            robot.packet = [MOVE, robot.position[0], robot.position[1], 0, 0, 0, 0, 0]
        if robot.skill == "ATTACK":
            robot.packet = [ATTACK, robot.ball_position[0], robot.ball_position[1], 0, 0, 0, 0, 0]
        if robot.skill == "KICK":
            robot.packet = [KICK, Robots[index+1].position[0], Robots[index+1].position[1], 0, 0, 0, 0, 0]
        if robot.skill == "RECIEVE":
            robot.packet = [RECIEVE, robot.ball_position[0], robot.ball_position[1], 0, 0, 0, 0, 0]
        if robot.skill == "COVER":
            robot.packet = [COVER, 0, 0, 0, 0, 0, 0, 0]
        if robot.skill == "DEFEND":
            robot.packet = [DEFEND, robot.ball_position[0], robot.ball_position[1], 0, 0, 0, 0, 0]
    '''

    #print(knownBall)
    
    #print(StrategyDT)
    #print(f'{globals()[([0])]}')
    #print(f'{eval(StrategyDT["RefBox"]["Start"][0])}')

    '''
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
    '''
    #if BallHandler != 0:
    # for robot in Robots:
    #     print(str(robot.packet[0]), end=", ")
    #     #robot.packet[0] = STOP
    # print() 

    return Robots, kick, recebe


def ControlRobots(keyboard, joystick, Robots):
    global selectedRobot
    
    print(keyboard, joystick, end="|")
    for joy in joystick:
        for i in range(6):
            if -0.25 < joy[i] < 0.25: joy[i] = 0

    for i, robot in enumerate(Robots):
        robot.packet = [CONTROL, 0, 0, robot.packet[3], 0, 0, 0, 0]
        robot.packet[0] = CONTROL
        robot.packet[1] = int(10*joystick[i][0])
        robot.packet[2] = int(-10*joystick[i][1])
        if 10 or 12 in joystick[i]:
            robot.packet[1] = int(20*joystick[i][0])
            robot.packet[2] = int(-20*joystick[i][1])
        if joystick[i][2] != 0 or joystick[i][3] != 0:      robot.packet[3] = int(np.degrees(np.arctan2(-joystick[i][3], joystick[i][2])))
        if 2 in joystick[i]:   robot.packet[4] = 1      
        if 4 in joystick[i]:   robot.packet[4] = 2
    
    if ord('1') in keyboard: selectedRobot = 0
    if ord('2') in keyboard: selectedRobot = 1
    if ord('3') in keyboard: selectedRobot = 2
    if ord('4') in keyboard: selectedRobot = 3
    if ord('5') in keyboard: selectedRobot = 4
    if ord('d') in keyboard: Robots[selectedRobot].packet[1] = 10
    if ord('a') in keyboard: Robots[selectedRobot].packet[1] = -10
    if ord('w') in keyboard: Robots[selectedRobot].packet[2] = 10
    if ord('s') in keyboard: Robots[selectedRobot].packet[2] = -10
    if ord('q') in keyboard: Robots[selectedRobot].packet[3] += 5
    if ord('e') in keyboard: Robots[selectedRobot].packet[3] -= 5
    if ord('f') in keyboard: Robots[selectedRobot].packet[4] = 1
    if ord(' ') in keyboard: Robots[selectedRobot].packet[4] = 2
    return selectedRobot



