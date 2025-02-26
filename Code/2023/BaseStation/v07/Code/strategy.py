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
# import matplotlib
# matplotlib.use('module://pygame_matplotlib.backend_pygame')
# import matplotlib.pyplot as plt

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
    args.append("free") # MAde this because i started to alter the decision tree to have over time decisions but got stuck
    # if knownBall == 1:
    #     free
    #     transition
    #     opponents
    # print(args) 

    return BallHandler, CanShoot, CanGoal, CanPass, knownBall, BallPosition, Refbox, StrategyDT, args, strat, oldstrat, idRecieve, lastKnowBall


def strategyTEMP(Robots, kick, recebe):
    """Temporarly strategy that is used to implement the game strategy

    Args:
        Robots (list): List of the robots of our team
        kick (bool): Temporarly bool that is a simple flag for an old strategy initial implementation
        recebe (bool): Temporarly bool that is a simple flag for an old strategy initial implementation
    """
    BallHandler, CanShoot, CanGoal, CanPass, knownBall, BallPosition, Refbox, StrategyDT, args, strat, oldstrat, idRecieve, lastKnowBall = getGameState(Robots)

    if BallHandler > 0:
        graph = decisionMaking.calculateGraph(Robots, BallHandler, show = 1)
        solution = graph.a_star_algorithm(str(BallHandler), '0')
        solution = [int(a) for a in solution]
        # graph1.set_plot(solution)
        # graph1.show_plot()
        for i in range(len(solution)-2):
            guiElements.drawLine(Robots[solution[i]-1].position, Robots[solution[i+1]-1].position, color=COLORS["pink"], width=3)
        guiElements.drawLine(Robots[solution[-2]-1].position, (11, 0), color=COLORS["pink"], width=3)
        # print(solution)
    elif DEBUG_KEYS_SIMULATION:
        kick = 0 # TEMP VELU TO DEBUG

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
        s.packet[0] = STOP
        if s.ball_handler == 1:
            print(s.linesOfPass, end=" - ")
            # print(s.linesOfPassCutted, consts.MARGIN2PASS, consts.MARGIN2PASS*consts.MARGIN2CHECKPASS, end = " - ")

    ss = [0, 0, 0, 0, 0]
    for i, s in enumerate(strat):
        if s == "KICK":
            idRecieve = solution[1]-1
            Robots[BallHandler-1].packet = [KICK, Robots[idRecieve].position[0], Robots[idRecieve].position[1], 0, 0, 0, 0]
            if idRecieve == -1:
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

    if BallHandler != 0 and kick == 0 and DEBUG_KEYS_SIMULATION:
        for robot in Robots:
            robot.packet[0] = STOP

    return Robots, kick, recebe


def ControlRobots(keyboard, joystick, Robots):
    """This functions handles the joystick and keyboard events and translates that to packets to send to the robots and control them

    Args:
        keyboard (list): List of all the keys pressed in the keyboard
        joystick (list(list)): List of all the joysitcks and all their events
        Robots (list): List of all the robots

    Returns:
        int: selected robot to be controlled by the keyboard
    """
    global selectedRobot
    
    # print(keyboard, joystick, end="|")
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



