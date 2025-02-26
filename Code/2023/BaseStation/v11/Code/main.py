""" This is the main code of the basestation. It is the code that runs the representation and strategy for the MSL LAR MinhoTeam. It was developed by the team, and it can interact either with the real robots or the robots on our simulation environment on Webots.\n
    It has some dependecies:\n
    1. numpy @ 1.23.4 
    2. pygame @ 2.1.3.dev8

    To install the dependencies please run the following line:\n
    ``pip3 install numpy==1.23.4 pygame==2.1.3.dev8``

    To get the simulation running, you need Webots installed, at least the version 2023a. You also need the simulation environemnt files. Those can be found in the following repository.\n
    <https://github.com/MSL-LAR-MinhoTeam/Simulator>
    
    """

import consts
import math
import time
import numpy as np
import sys
import time
import socket
import json
import pygame
from robot import *
from guiFuncs import *
from strategy import *
import pygame_widgets
import fileHandling
from pygame_widgets.button import Button
from pygame_widgets.button import ButtonArray
from pygame_widgets.combobox import ComboBox
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.progressbar import ProgressBar
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.toggle import Toggle
import matplotlib.pyplot as plt
import refBox

runMode = 1
if len(sys.argv) > 1:
    for i in sys.argv:
        if i == '--http':
            runMode = 0

kick = 0
recebe = 0
finalTime = 0
timerAverage = 0
loop = 0
# skillsMarker = FieldCoord2coord(0, 0)
skillsMarker = [[[0, 0, -1], [0, 0, -1]], [[0, 0, -1], [0, 0, -1]], [[0, 0, -1], [0, 0, -1]], [[0, 0, -1], [0, 0, -1]], [[0, 0, -1], [0, 0, -1]]]
mouseGUI = [[coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1]),coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1])], [coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1]),coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1])], [coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1]),coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1])], [coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1]),coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1])], [coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1]),coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1])]]
controlIDSList = []
# skillsMarker = [0, 0, 0]

controlWidgets = [Toggle(consts.SCREEN, 1400, int(consts.YOFFSET + 5*consts.FACTOR), 90, 30), TextBox(consts.SCREEN, 1300, int(consts.YOFFSET+5*consts.FACTOR), 80, 30, colour=consts.COLORS["button"], borderColour = consts.COLORS["button"], textColour = (255, 255, 255))]
controlWidgets[1].disable()
controlWidgets[1].setText("Data Fusion")

GameButtonNames = ["PENALTY", "CORNER", "THROWIN", "GOALKICK", "FREEKICK", "KICKOFF", "DROP_BALL", "  ", "SIDE", "PARK", "STOP", "START", "PENALTY", "CORNER", "THROWIN", "GOALKICK", "FREEKICK", "KICKOFF"]
gameWidgets = []
for i in range(3):
    for j in range(6):
        gameWidgets.append(Button(SCREEN, int(consts.FACTOR + consts.FIELD_SIZE["wall"][0]+(i*(consts.RESOLUTION[0]-int(consts.FIELD_SIZE["wall"][0]))/3)),
                                        int(consts.YOFFSET+consts.FIELD_SIZE["wall"][1]) - (j+1)*(int(0.075*consts.RESOLUTION[1])),
                                        int(consts.RESOLUTION[0]-int(consts.FIELD_SIZE["wall"][0]+2*consts.FACTOR))/3, 
                                        int(0.07*consts.RESOLUTION[1]), 
                                        text=str(GameButtonNames[i*6+j]), 
                                        radius = 20, 
                                        onClick = lambda a: RefBoxCommands(a), 
                                        onClickParams = [GameButtonNames[i*6+j]], 
                                        textColour = (255, 255, 255),
                                        inactiveColour = consts.COLORS["button"],
                                        hoverColour = consts.COLORS["hover"],
                                        pressedColour = consts.COLORS["activated"]))

SkillButtonNames = ["Stop \U0001F6D1", "Move \U00002B06", "Attack \U00002B06 \U000026BD", "Kick \U0001F9BF \U000026BD", "Recieve \U00002B07", "Cover \U0001F6E1", "Defend \U0001F6E1 \U0001F945", "Control \U0001F3AE"]
skillWidgets = []
for j in range(2):
    for i in range(4):
        skillWidgets.append(Button(SCREEN, int(consts.FACTOR + consts.FIELD_SIZE["wall"][0]+(i*(consts.RESOLUTION[0]-int(consts.FIELD_SIZE["wall"][0]))/4)),
                                        j*(int(0.075*consts.RESOLUTION[1])) + consts.YOFFSET + 2*consts.FACTOR,
                                        int(consts.RESOLUTION[0]-int(consts.FIELD_SIZE["wall"][0]+2*consts.FACTOR))/4, 
                                        int(0.07*consts.RESOLUTION[1]), 
                                        text=str(SkillButtonNames[i*2+j]), 
                                        radius = 20, 
                                        onClick = lambda a: SkillTestButtons(a), 
                                        onClickParams = [SkillButtonNames[i*2+j]], 
                                        textColour = (255, 255, 255),
                                        inactiveColour = consts.COLORS["button"],
                                        hoverColour = consts.COLORS["hover"],
                                        pressedColour = consts.COLORS["activated"]))

# skillWidgets.append(Button(SCREEN, int(consts.FACTOR + consts.FIELD_SIZE["wall"][0]+(consts.RESOLUTION[0]-int(consts.FIELD_SIZE["wall"][0])/4)),
#                             2*(int(0.075*consts.RESOLUTION[1])) + consts.YOFFSET + 2*consts.FACTOR,
#                             int(consts.RESOLUTION[0]-int(consts.FIELD_SIZE["wall"][0]+2*consts.FACTOR)), 
#                             int(0.5*consts.RESOLUTION[1]), 
#                             text=str("STOP ALL"), 
#                             radius = 20, 
#                             onClick = lambda a: SkillTestButtons(a, 1), 
#                             onClickParams = ["STOP ALL"], 
#                             textColour = (255, 255, 255),
#                             inactiveColour = consts.COLORS["red"],
#                             hoverColour = consts.COLORS["red"],
#                             pressedColour = consts.COLORS["red"]))


calibrationWidgets = [] #BUG IS A HERE, nao consigo usar este dropbox
calibrationWidgets.append(Dropdown(SCREEN,
                            0.01*consts.RESOLUTION[0], 
                            0.05*consts.RESOLUTION[1], 
                            0.23*consts.RESOLUTION[0], 
                            0.050*consts.RESOLUTION[1], 
                            name='Select Robot',
                            choices=[
                                'Robot 1',
                                'Robot 2',
                                'Robot 3',
                                'Robot 4',
                                'Robot 5',
                            ],
                            borderRadius=3, 
                            colour=consts.COLORS["button"], 
                            textColour = consts.COLORS["white"],
                            fontSize = 5*consts.FACTOR,
                            values=[1, 2, 3, 4, 5], 
                            direction='down', 
                            textHAlign='centre', 
                        )
                    )
calibrationWidgets.append(Dropdown(SCREEN,
                            0.26*consts.RESOLUTION[0], 
                            0.05*consts.RESOLUTION[1], 
                            0.23*consts.RESOLUTION[0], 
                            0.050*consts.RESOLUTION[1], 
                            name='PID Select',
                            choices=[
                                'PID Attack',
                                'PID Move',
                                'PID Kick',
                                'PID Recieve',
                                'PID Cover',
                            ],
                            borderRadius=3, 
                            colour=consts.COLORS["button"], 
                            textColour = consts.COLORS["white"],
                            fontSize = 5*consts.FACTOR,
                            values=[1, 2, 3, 4, 5], 
                            direction='down', 
                            textHAlign='centre', 
                        )
                    )
calibrationWidgets.append(Dropdown(SCREEN,
                            0.01*consts.RESOLUTION[0], 
                            0.11*consts.RESOLUTION[1], 
                            0.23*consts.RESOLUTION[0], 
                            0.050*consts.RESOLUTION[1], 
                            name='Code 0',
                            choices=[
                                'Code 0',
                                'Code 1',
                                'Code 2',
                                'Code 3',
                                'Code 4',
                            ],
                            borderRadius=3, 
                            colour=consts.COLORS["button"], 
                            textColour = consts.COLORS["white"],
                            fontSize = 5*consts.FACTOR,
                            values=[1, 2, 3, 4, 5], 
                            direction='down', 
                            textHAlign='centre', 
                        )
                    )
calibrationWidgets.append(Dropdown(SCREEN,
                            0.26*consts.RESOLUTION[0], 
                            0.11*consts.RESOLUTION[1], 
                            0.23*consts.RESOLUTION[0], 
                            0.050*consts.RESOLUTION[1], 
                            name='Siga 0',
                            choices=[
                                'Siga 1',
                                'Siga 2',
                                'Siga 3',
                                'Siga 4',
                                'Siga 5',
                            ],
                            borderRadius=3, 
                            colour=consts.COLORS["button"], 
                            textColour = consts.COLORS["white"],
                            fontSize = 5*consts.FACTOR,
                            values=[1, 2, 3, 4, 5], 
                            direction='down', 
                            textHAlign='centre', 
                        )
                    )


calibrationWidgets.append(Button(SCREEN,
                            int(0.01*consts.RESOLUTION[0]), 
                            int(0.18*consts.RESOLUTION[1]),
                            int(0.48*consts.RESOLUTION[0]), 
                            int(0.06*consts.RESOLUTION[1]),
                            fontSize=40,
                            inactiveColour=consts.COLORS["hover"], 
                            #border=consts.COLORS["hover"], 
                            textColour=(255,255,255),
                            radius=5, 
                            borderThickness=2,
                            textHAlign='right',
                        )
                    )
calibrationWidgets[-1].disable()

calibrationWidgets.append(Button(SCREEN,
                            int(0.01*consts.RESOLUTION[0]), 
                            int(0.24*consts.RESOLUTION[1]),
                            int(0.48*consts.RESOLUTION[0]), 
                            int(0.06*consts.RESOLUTION[1]),
                            fontSize=40,
                            inactiveColour=consts.COLORS["hover"], 
                            #border=consts.COLORS["hover"], 
                            textColour=(255,255,255),
                            radius=5, 
                            borderThickness=2,
                            textHAlign='right',
                        )
                    )
calibrationWidgets[-1].disable()

calibrationWidgets.append(Button(SCREEN,
                            int(0.01*consts.RESOLUTION[0]), 
                            int(0.30*consts.RESOLUTION[1]),
                            int(0.48*consts.RESOLUTION[0]), 
                            int(0.06*consts.RESOLUTION[1]),
                            fontSize=40,
                            inactiveColour=consts.COLORS["hover"], 
                            #border=consts.COLORS["hover"], 
                            textColour=(255,255,255),
                            radius=5, 
                            borderThickness=2,
                            textHAlign='right',
                        )
                    )
calibrationWidgets[-1].disable()

calibrationWidgets.append(TextBox(SCREEN,
                            int(0.43*consts.RESOLUTION[0]), 
                            int(0.19*consts.RESOLUTION[1]),
                            int(0.04*consts.RESOLUTION[0]), 
                            int(0.04*consts.RESOLUTION[1]),
                            fontSize=30,
                            colour=consts.COLORS["hover"],
                            borderThickness=0,
                            radius=5,
                            textColour=(255, 255, 255),
                        )
                    )
calibrationWidgets.append(TextBox(SCREEN,
                            int(0.43*consts.RESOLUTION[0]), 
                            int(0.25*consts.RESOLUTION[1]),
                            int(0.04*consts.RESOLUTION[0]), 
                            int(0.04*consts.RESOLUTION[1]),
                            fontSize=30,
                            colour=consts.COLORS["hover"],
                            borderThickness=0,
                            radius=5,
                            textColour=(255, 255, 255),
                        )
                    )
calibrationWidgets.append(TextBox(SCREEN,
                            int(0.43*consts.RESOLUTION[0]), 
                            int(0.31*consts.RESOLUTION[1]),
                            int(0.04*consts.RESOLUTION[0]), 
                            int(0.04*consts.RESOLUTION[1]),
                            fontSize=30,
                            colour=consts.COLORS["hover"],
                            borderThickness=0,
                            radius=5,
                            textColour=(255, 255, 255),
                        )
                    )


calibrationWidgets.append(Slider(SCREEN,
                            int(0.02*consts.RESOLUTION[0]), 
                            int(0.20*consts.RESOLUTION[1]), 
                            int(0.40*consts.RESOLUTION[0]), 
                            int(0.015*consts.RESOLUTION[1]), 
                            min=0,
                            max=5000,
                            step=1,
                        )
                    )

calibrationWidgets.append(Slider(SCREEN,
                            int(0.02*consts.RESOLUTION[0]), 
                            int(0.26*consts.RESOLUTION[1]), 
                            int(0.40*consts.RESOLUTION[0]), 
                            int(0.015*consts.RESOLUTION[1]), 
                            min=0,
                            max=5000,
                            step=1,
                        )
                    )

calibrationWidgets.append(Slider(SCREEN,
                            int(0.02*consts.RESOLUTION[0]), 
                            int(0.32*consts.RESOLUTION[1]),
                            int(0.40*consts.RESOLUTION[0]), 
                            int(0.015*consts.RESOLUTION[1]), 
                            min=0,
                            max=5000,
                            step=1,
                        )
                    )


calibrationWidgets.append(Button(SCREEN,
                            int(0.01*consts.RESOLUTION[0]), 
                            int(0.38*consts.RESOLUTION[1]),
                            int(0.48*consts.RESOLUTION[0]), 
                            int(0.06*consts.RESOLUTION[1]),
                            fontSize=30,
                            inactiveColour=consts.COLORS["button"], 
                            textColour=(255,255,255),
                            radius=5, 
                            borderThickness=3,
                            textHAlign='center',
                            text="Save PID Values"
                        )
                    )

probFieldUI = []

consts.DefaultWidgets = [gameWidgets, controlWidgets, probFieldUI, skillWidgets, calibrationWidgets, []]

PIDCalibCode = -1

def changeCalibValues():
    global PIDCalibCode
    a = consts.DefaultWidgets[4][0].getSelected()
    b = consts.DefaultWidgets[4][1].getSelected()
    c = consts.DefaultWidgets[4][2].getSelected()
    d = consts.DefaultWidgets[4][3].getSelected()
    v1 = float(consts.DefaultWidgets[4][10].getValue()/1000)
    v2 = float(consts.DefaultWidgets[4][11].getValue()/1000)
    v3 = float(consts.DefaultWidgets[4][12].getValue()/1000)
    
    consts.DefaultWidgets[4][7].setText(str("kP: ")+str(v1))
    consts.DefaultWidgets[4][8].setText(str("kI: ")+str(v2))
    consts.DefaultWidgets[4][9].setText(str("kD: ")+str(v3))
    
    temp = 1000*a+100*b+10*c+d
    if temp != PIDCalibCode:
        PIDCalibCode = temp
        print(PIDCalibCode)
    
def Game(): 
    if REPRESENT_GAME:
        Field()
        RobotsGUI(Robots)
        RefBox()

def ProbFields(): 
    if REPRESENT_GAME:
        enableProbUI(Robots, getSelectedRobot(keyboardPress), consts.MainMenus)
        PField(Robots, getSelectedRobot(keyboardPress))
        RobotsGUI(Robots, getSelectedRobot(keyboardPress))
        RefBox()
        if keyboardPress != []:
            selectedRobot = ControlRobots(keyboardPress, joystickPress, Robots, getSelectedRobot(keyboardPress), controlIDSList)

def Control():
    if REPRESENT_GAME:
        consts.DEBUG_DATA_FUSION = controlWidgets[0].getValue()
        Field()
        selectedRobot = ControlRobots(keyboardPress, joystickPress, Robots, getSelectedRobot(keyboardPress), controlIDSList)
        RobotsGUI(Robots, getSelectedRobot(keyboardPress))
        RefBox()

def Calibration():
    if REPRESENT_GAME:
        changeCalibValues()
        # Field()
        # RobotsGUI(Robots)

def Skills():
    global skillsMarker
    global mouseGUI
    if REPRESENT_GAME:
        Field()
        ControlRobots(keyboardPress, joystickPress, Robots, getSelectedRobot(keyboardPress), controlIDSList)
        skillsMarker, mouseGUI = handleMarkers(mouse, skillsMarker, mouseGUI, Robots, getSelectedRobot(keyboardPress))
        RobotsGUI(Robots, getSelectedRobot(keyboardPress))
        if ord('q') in keyboardPress:   SkillTestButtons(SkillButtonNames[0])
        if ord('a') in keyboardPress:   SkillTestButtons(SkillButtonNames[1])
        if ord('w') in keyboardPress:   SkillTestButtons(SkillButtonNames[2])
        if ord('s') in keyboardPress:   SkillTestButtons(SkillButtonNames[3])
        if ord('e') in keyboardPress:   SkillTestButtons(SkillButtonNames[4])
        if ord('d') in keyboardPress:   SkillTestButtons(SkillButtonNames[5])
        if ord('r') in keyboardPress:   SkillTestButtons(SkillButtonNames[6])
        if ord('f') in keyboardPress:   SkillTestButtons(SkillButtonNames[7])
        handleSkillTest(Robots)
        
def Exit():
    global RUNNING
    RUNNING = 0 


def changeMenu(a):
    global MenuSelected
    global Robots
    global controlIDSList
    MenuSelected = a
    consts.MainMenus[1] =[[0]*len(consts.MainMenus[0][0])] * len(consts.MainMenus[0])
    consts.MainMenus[1][a] = 1 # type: ignore
    for i in range(len(consts.MainMenus[2])): 
        if consts.MainMenus[1][i] == 1:
            consts.MainMenus[2][i].inactiveColour = consts.COLORS["activated"]
            consts.MainMenus[2][i].hoverColour = consts.COLORS["activated"]
        else:
            consts.MainMenus[2][i].inactiveColour = consts.COLORS["button"]
            consts.MainMenus[2][i].hoverColour = consts.COLORS["hover"]

    if MenuSelected == 1:
        controlIDSList = [0, 1, 2, 3, 4]
    else:
        controlIDSList = []
    if MenuSelected == 3:       
        for i in Robots: 
            i.packet[0] = STOP 
    
    for i, a in enumerate(consts.MainMenus[4]):
        if i == MenuSelected:
            for x in a:
                x.enableUI()
        else:
            for x in a:
                x.disableUI()
                                
    if(a == len(consts.MainMenus[0])-1):
        consts.MainMenus[3][a]()


def handleSkillTest(robotList):
    for i in skillsMarker:
        for j in range(len(i)):
            if i[j][2] > -1:
                i[j][0] = Robots[i[j][2]].position[0]
                i[j][1] = Robots[i[j][2]].position[1]
    for robot in robotList:
        if robot.packet[0] == consts.MOVE:
            robot.packet[1] = skillsMarker[robot.robotID-1][0][0] 
            robot.packet[2] = skillsMarker[robot.robotID-1][0][1] 
            robot.packet[3] = 1#skillsMarker[robot.robotID-1][0][2] 
            robot.packet[4] = skillsMarker[robot.robotID-1][1][0] 
            robot.packet[5] = skillsMarker[robot.robotID-1][1][1] 
        if robot.packet[0] == consts.ATTACK:
            if robot.ball_handler == 1:
                robot.packet[0] = STOP
            robot.packet[1] = robot.ball_position[0]
            robot.packet[2] = robot.ball_position[1]
        if robot.packet[0] == consts.KICK:
            #if robot.ball_handler == 0:
            #    robot.packet[0] = STOP
            robot.packet[1] = skillsMarker[robot.robotID-1][1][0] 
            robot.packet[2] = skillsMarker[robot.robotID-1][1][1] 
            if skillsMarker[robot.robotID-1][1][2] != -1:
                Robots[skillsMarker[robot.robotID-1][1][2]].packet[0] = consts.RECIEVE
        if robot.packet[0] == consts.RECIEVE:
            if robot.ball_handler == 1:
                robot.packet[0] = STOP
            robot.packet[1] = robot.ball_position[0]
            robot.packet[2] = robot.ball_position[1]
        if robot.packet[0] == consts.COVER:
            if robot.ball_handler == 1:
                robot.packet[0] = STOP
            robot.packet[1] = skillsMarker[robot.robotID-1][0][0] 
            robot.packet[2] = skillsMarker[robot.robotID-1][0][1] 
            robot.packet[3] = skillsMarker[robot.robotID-1][1][0] 
            robot.packet[4] = skillsMarker[robot.robotID-1][1][1] 
            robot.packet[5] = 0.5
            robot.packet[6] = 0.5
        if robot.packet[0] == consts.DEFEND:
            if robot.ball_handler == 1:
                robot.packet[0] = STOP
            robot.packet[1] = robot.ball_position[0]
            robot.packet[2] = robot.ball_position[1]


def RefBoxCommands(buttonID):
    message = {"command": buttonID}
    if refBox.available:
        refBox.CommandID = refBox.checkMessage(message)
        refBox.handleCommand(refBox.CommandID, Robots)
        # print(buttonID, "\U0001F61C", end=" | ")
        # print("\U0001F3F3\U0001F308")


def SkillTestButtons(buttonID, all=0):
    global keyboardPress, joystickPress, Robots
    selectedRobot = getSelectedRobot(keyboardPress)
    if all == 1:
        for robot in Robots:
            robot.packet[0] = consts.STOP
        return
    if selectedRobot in controlIDSList:
        controlIDSList.remove(selectedRobot)

    if buttonID == SkillButtonNames[0]:     Robots[selectedRobot].packet[0] = consts.STOP
    if buttonID == SkillButtonNames[1]:     Robots[selectedRobot].packet[0] = consts.MOVE
    if buttonID == SkillButtonNames[2]:     Robots[selectedRobot].packet[0] = consts.ATTACK
    if buttonID == SkillButtonNames[3]:     Robots[selectedRobot].packet[0] = consts.KICK
    if buttonID == SkillButtonNames[4]:     Robots[selectedRobot].packet[0] = consts.RECIEVE
    if buttonID == SkillButtonNames[5]:     Robots[selectedRobot].packet[0] = consts.COVER
    if buttonID == SkillButtonNames[6]:     Robots[selectedRobot].packet[0] = consts.DEFEND
    if buttonID == SkillButtonNames[7]:     controlIDSList.append(selectedRobot)
    handleSkillTest([Robots[selectedRobot]])

def getIPS():
    robots = [socket.gethostname(), "robot1", "robot2", "robot3", "robot4", "robot5"]
    defaultIPS = ["172.16.49.88", "172.16.49.67", "172.16.49.129", "172.16.49.247", "172.16.49.224", "172.16.49.115"]
    IPS = []

    for i in range(len(robots)):
        try:
            ip_address = socket.gethostbyname(robots[i])
            #print(f"Hostname: {robots[i]} - ", end=' ')
            #print(f"IP Address: {ip_address}")
            IPS.append(ip_address)
        except:
            IPS.append(defaultIPS[i])

    IPS.append(1)
    return IPS   

############ GUI MAIN LOOP ############
def guiMain(kick):
    global mouse
    global keyboardPress, joystickPress
    global joysticks
    global MenuSelected
    
    SCREEN.fill(consts.COLORS["background"])
    mouse = list(pygame.mouse.get_pos()); 
    mouse.append(0)
    mouse.append(0)

    events = pygame.event.get()
    # print(events)
    for ev in events:
        if ev.type == pygame.QUIT:  Exit()
        if ev.type == pygame.KEYDOWN:
            keyboardPress.append(ev.key)
            if ev.key == pygame.K_F12:           sendInfo(Robots)
            if ev.key == pygame.K_F1:       MenuSelected = 0; changeMenu(MenuSelected)
            if ev.key == pygame.K_F2:       MenuSelected = 1; changeMenu(MenuSelected)
            if ev.key == pygame.K_F3:       MenuSelected = 2; changeMenu(MenuSelected)
            if ev.key == pygame.K_F4:       MenuSelected = 3; changeMenu(MenuSelected)
            if ev.key == pygame.K_F5:       MenuSelected = 4; changeMenu(MenuSelected)
            if ev.key == pygame.K_F6:       MenuSelected = 5; changeMenu(MenuSelected)
            if ev.key == pygame.K_ESCAPE:       Exit()
            if ev.key == pygame.K_SPACE:        kick = 1
        if ev.type == pygame.KEYUP:             keyboardPress.remove(ev.key)
        if ev.type == pygame.MOUSEBUTTONDOWN:   mouse[2] = ev.button
        if ev.type == pygame.JOYBUTTONDOWN:     joystickPress[ev.joy].append(ev.button+2)
        if ev.type == pygame.JOYBUTTONUP:
            if ev.button+2 in joystickPress[ev.joy]:  joystickPress[ev.joy].remove(ev.button+2)
        if ev.type == pygame.JOYAXISMOTION:
            joystickPress[ev.joy][ev.axis] = np.round(ev.value, 2)
        if ev.type == pygame.JOYDEVICEADDED or ev.type == pygame.JOYDEVICEREMOVED:
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    
    consts.MainMenus[3][MenuSelected]()
    # print(mouse)
    pygame_widgets.update(events)
    return kick


def main():
    global Robots
    global kick
    global recebe
    global finalTime
    global loop
    global timerAverage
    loop += 1
    loopTime = time.time()
    
    newInfo = getInfo(Robots)
    if newInfo and DEBUG_DATA_FUSION:
        dataFusion(Robots)
    
    # if refBox.available:
    #     refBox.CommandID = refBox.handleComms()
        # print(refBox.CommandID)
    
    # calculateHeatMaps(Robots, getSelectedRobot(keyboardPress), np.asarray(strategy.solution))
    if REPRESENT:
        kick = guiMain(kick)

    # if MenuSelected == 0 or MenuSelected == 2:
        # Robots, kick, recebe, solution = strategyTEMP(Robots, kick, MenuSelected)
    
    # if refBox.available:
    #     refBox.handleCommand(refBox.CommandID, Robots)
    
    if newInfo:
        sendInfo(Robots)
    
    pygame.display.update()
   
    # DISPLAY TIME PER LOOP WITH COLORS
    finalTime = round((time.time()-loopTime)*1000, 2)
    if consts.PRINTTIME:
        if finalTime > TIMEPERLOOP:
            print(f"{consts.bcolors.FAIL}{finalTime:4.1f}ms{consts.bcolors.ENDC}", end=" | ")
        elif finalTime > TIMEPERLOOP*0.75:
            print(f"{consts.bcolors.WARNING}{finalTime:4.1f}ms{consts.bcolors.ENDC}", end=" | ")
        else: 
            print(f"{consts.bcolors.ENDC}{finalTime:4.1f}ms{consts.bcolors.ENDC}", end=" | ")

    timerAverage += finalTime
    while (finalTime := round((time.time()-loopTime)*1000, 2)) < TIMEPERLOOP:
        pass
    if consts.PRINTTIME:
        print(finalTime, "ms", end=' ')
        print()

def SuperMain():
    ############ MAIN LOOP ############
    initTime = time.time()
    try:
        # fil = fileHandling.load4File("./configs/IPS")
        consts.mapConfigJson = fileHandling.load4File("./configs/mapSituation.json")
        consts.mapConfigJsonPaths = [s.split('-') for s in fileHandling.get_paths(consts.mapConfigJson)]
        consts.mapNames = fileHandling.load4File("./configs/mapNames.json")["Names"]
    except:
        pass
    
    consts.MainMenus[4][2].append(Dropdown(SCREEN,
                                0.63*consts.RESOLUTION[0], 
                                0.735*consts.RESOLUTION[1], 
                                0.035*consts.RESOLUTION[0]*consts.FACTOR, 
                                0.010*consts.RESOLUTION[1]*consts.FACTOR, 
                                name='Select Robot',
                                choices= [s.replace("-", " ") for s in fileHandling.get_paths(consts.mapConfigJson)],
                                borderRadius=3, 
                                colour=consts.COLORS["button"],
                                textColour = consts.COLORS["white"],
                                fontSize = 5*consts.FACTOR,
                                values=range(len(consts.mapConfigJsonPaths)), 
                                direction='up', 
                                textHAlign='centre', 
                            )
                        )
    
    for i, a in enumerate(consts.mapNames):
        consts.MainMenus[4][2].append(probField.heatMapUI(a, True, i))

    changeMenu(0)

    sendInfo(Robots)
    while RUNNING:
        main()

    fileHandling.save2FileJSON(consts.mapConfigJson, "./configs/mapSituation.json")
    print(timerAverage/loop) 


######################## INIT ########################
if __name__ == "__main__":
    ############ PYGAME INIT ############
    if REPRESENT and runMode:
        pygame.init()
        pygame.joystick.init()
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        if FULLSCREEN:
            flags |= pygame.FULLSCREEN
        SCREEN = pygame.display.set_mode(tuple(RESOLUTION), flags, display=0)

        ############ MENU TABS ############
        MenuSelected = 0
        consts.MainMenus = [["Game + RefBox", "Control", "Prob Fields", "Skills", "Calibration", "Exit"],[0, 0, 0, 0, 0, 0],[],[Game, Control, ProbFields, Skills, Calibration, Exit], [gameWidgets, controlWidgets, [], skillWidgets, calibrationWidgets, []]]
        consts.MainMenus[1][MenuSelected] = 1
        for a in range(len(consts.MainMenus [0])):
            consts.MainMenus[2].append(Button(SCREEN, a*(1/len(consts.MainMenus[0]))*consts.RESOLUTION[0], 0, (1/len(consts.MainMenus[0]))*consts.RESOLUTION[0], MENUS_SIZE*consts.RESOLUTION[1], text=consts.MainMenus[0][a], radius = 20, onClick = lambda a: changeMenu(a), onClickParams = [a], textColour = (255, 255, 255)))
        # for robot in Robots:
        #     for a in robot.probField:
        #         consts.MainMenus[4][2].append(a.UI)
        # changeMenu(MenuSelected)

        keyboardPress = []
        joystickPress = [[0, 0, 0, 0, -1, -1], [0, 0, 0, 0, -1, -1], [0, 0, 0, 0, -1, -1], [0, 0, 0, 0, -1, -1], [0, 0, 0, 0, -1, -1]]
        
        joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for joystick in joysticks:
            print(joystick.get_name())

        ############ MOUSE AND FONTS ############
        mouse = (0, 0, 0)

    
    ############ ROBOTS AND COMUNICATION  ############
    try:
        IPS = ["localhost", "localhost", "localhost", "localhost", "localhost", "localhost", 2]
        # IPS = ["172.16.49.88", "172.16.49.67", "172.16.49.129", "172.16.49.247", "172.16.49.224", "172.16.49.115", 1] # BASESTATION MINHA
        # IPS = ["172.16.49.136", "172.16.49.129", "172.16.49.79", "172.16.49.79", "172.16.49.235", "172.16.49.79", 1] # BASESTATION TELVISASO
        # IPS = getIPS()
        Robots = [Robot(a+1, IPS[0], IPS[a+1], 0, IPS[-1]) for a in range(5)]
    except Exception as e:
        print(e)
        
    SuperMain()
    pygame.quit()