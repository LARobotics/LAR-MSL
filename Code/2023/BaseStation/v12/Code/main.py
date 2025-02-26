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
import cameras
import cv2

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

skillsMarker = [[[0, 0, -1], [0, 0, -1]], [[0, 0, -1], [0, 0, -1]], [[0, 0, -1], [0, 0, -1]], [[0, 0, -1], [0, 0, -1]], [[0, 0, -1], [0, 0, -1]]]
mouseGUI = [[coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1]),coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1])], [coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1]),coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1])], [coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1]),coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1])], [coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1]),coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1])], [coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1]),coord2FieldCoord(skillsMarker[0][0][0], skillsMarker[0][0][1])]]
controlIDSList = []

controlWidgets = [Toggle(consts.SCREEN, 1400, int(consts.YOFFSET + 5*consts.FACTOR), 90, 30), TextBox(consts.SCREEN, 1300, int(consts.YOFFSET+5*consts.FACTOR), 80, 30, colour=consts.COLORS["button"], borderColour = consts.COLORS["button"], textColour = (255, 255, 255))]
controlWidgets[1].disable()
controlWidgets[1].setText("Data Fusion")

GameButtonNames = ["PENALTY", "CORNER", "THROWIN", "GOALKICK", "FREEKICK", "KICKOFF", "DROP_BALL", "  ", "SIDE", "PARK", "STOP", "START", "PENALTY", "CORNER", "THROWIN", "GOALKICK", "FREEKICK", "KICKOFF"]

calibrationWidgets = [] #BUG IS A HERE, nao consigo usar este dropbox
numberofBoxes = 5
    
# for i in range(numberofBoxes):
#     calibrationWidgets.append(Button(SCREEN,
#                                 i/numberofBoxes*consts.RESOLUTION[0], 
#                                 0.04*consts.RESOLUTION[1] + consts.YOFFSET,
#                                 1/numberofBoxes*consts.RESOLUTION[0],
#                                 0.30*consts.RESOLUTION[1], 
#                                 fontSize=20,
#                                 inactiveColour=consts.COLORS["button"], 
#                                 textColour=(255,255,255),
#                                 radius=5, 
#                                 borderThickness=3,
#                                 textHAlign='center',
#                                 #text="\U0001F4BE Save PID Values \U0001F4BE"
#                             )
#                         )
#     calibrationWidgets[-1].disable()
    
skillWidgets = []    
for i in range(consts.calibSkillNumberOfBars):
    skillWidgets.append(TextBox(SCREEN,
                            int(consts.FIELD_SIZE["wall"][0]+0.01*consts.RESOLUTION[0]) + int(consts.RESOLUTION[0] - consts.FIELD_SIZE["wall"][0] - 0.13*consts.RESOLUTION[0]), 
                            int((0.193+(0.035*i))*consts.RESOLUTION[1]),
                            consts.RESOLUTION[0] - (int(consts.FIELD_SIZE["wall"][0]+0.01*consts.RESOLUTION[0]) + int(consts.RESOLUTION[0] - consts.FIELD_SIZE["wall"][0] - 0.13*consts.RESOLUTION[0])),
                            0.026*consts.RESOLUTION[1], 
                            fontSize=20,
                            colour=consts.COLORS["hover"],
                            borderThickness=0,
                            radius=5,
                            textColour=(255, 255, 255),
                        )
                    )
    
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
    
for j in range(2):
    for i in range(4):
        skillWidgets.append(Button(SCREEN, int(consts.FACTOR + consts.FIELD_SIZE["wall"][0]+(i*(consts.RESOLUTION[0]-int(consts.FIELD_SIZE["wall"][0]))/4)),
                                        j*(int(0.055*consts.RESOLUTION[1])) + consts.YOFFSET + 2*consts.FACTOR,
                                        int(consts.RESOLUTION[0]-int(consts.FIELD_SIZE["wall"][0]+2*consts.FACTOR))/4, 
                                        int(0.05*consts.RESOLUTION[1]), 
                                        text=str(SkillButtonNames[i*2+j]), 
                                        radius = 20, 
                                        onClick = lambda a: SkillTestButtons(a), 
                                        onClickParams = [SkillButtonNames[i*2+j]], 
                                        textColour = (255, 255, 255),
                                        inactiveColour = consts.COLORS["button"],
                                        hoverColour = consts.COLORS["hover"],
                                        pressedColour = consts.COLORS["activated"]))


        
skillWidgets.append(Dropdown(SCREEN,
                            consts.FIELD_SIZE["wall"][0]+0.005*consts.RESOLUTION[0], 
                            0.15*consts.RESOLUTION[1],
                            (consts.RESOLUTION[0] - consts.FIELD_SIZE["wall"][0] - 0.01*consts.RESOLUTION[0])/2,
                            0.030*consts.RESOLUTION[1], 
                            name='PID Select',
                            choices=[
                                'Move',
                                'Attack',
                                'Kick',
                                'Recieve',
                                'Cover',
                                'Defend',
                                'Control',
                            ],
                            borderRadius=3, 
                            colour=consts.COLORS["button"], 
                            textColour = consts.COLORS["white"],
                            fontSize = 5*consts.FACTOR,
                            values=[1, 2, 3, 4, 5, 6, 7,], 
                            direction='down', 
                            textHAlign='centre', 
                        )
                    )
skillWidgets.append(Button(SCREEN,
                            consts.FIELD_SIZE["wall"][0]+0.005*consts.RESOLUTION[0] + (consts.RESOLUTION[0] - consts.FIELD_SIZE["wall"][0] + 0.01*consts.RESOLUTION[0])/2, 
                            0.15*consts.RESOLUTION[1],
                            (consts.RESOLUTION[0] - consts.FIELD_SIZE["wall"][0] - 0.02*consts.RESOLUTION[0])/2,
                            0.030*consts.RESOLUTION[1], 
                            fontSize=20,
                            inactiveColour=consts.COLORS["button"], 
                            textColour=(255,255,255),
                            radius=5, 
                            borderThickness=3,
                            textHAlign='center',
                            text="\U0001F4BE Save PID Values \U0001F4BE"
                        )
                    )
numberofDropDowns = len(skillWidgets)-8

# for i in range(consts.calibSkillNumberOfBars):
#     skillWidgets.append(Button(SCREEN,
#                                 consts.FIELD_SIZE["wall"][0]+0.005*consts.RESOLUTION[0], 
#                                 int((0.19+(0.035*i))*consts.RESOLUTION[1]),
#                                 (consts.RESOLUTION[0] - consts.FIELD_SIZE["wall"][0] - 0.005*consts.RESOLUTION[0]),
#                                 0.032*consts.RESOLUTION[1], 
#                                 fontSize=20,
#                                 inactiveColour=consts.COLORS["hover"], 
#                                 #border=consts.COLORS["hover"], 
#                                 textColour=(255,255,255),
#                                 radius=5, 
#                                 borderThickness=2,
#                                 textHAlign='right',
#                             )
#                         )
#     skillWidgets[-1].disable()
print(len(skillWidgets))
for i in range(consts.calibSkillNumberOfBars):
    skillWidgets.append(Slider(SCREEN,
                                int(consts.FIELD_SIZE["wall"][0]+0.01*consts.RESOLUTION[0]), 
                                int((0.198+(0.035*i))*consts.RESOLUTION[1]),
                                int(consts.RESOLUTION[0] - consts.FIELD_SIZE["wall"][0] - 0.14*consts.RESOLUTION[0]),
                                int(0.016*consts.RESOLUTION[1]), 
                                min=0,
                                max=2500,
                                step=1,
                            )
                        )

for i in range(numberofBoxes):
    calibrationWidgets.append(Dropdown(SCREEN,
                                i/numberofBoxes*consts.RESOLUTION[0] + 0.01*consts.RESOLUTION[0], 
                                0.005*consts.RESOLUTION[1] + consts.YOFFSET,
                                1/numberofBoxes*consts.RESOLUTION[0] - 0.02*consts.RESOLUTION[0],
                                0.03*consts.RESOLUTION[1], 
                                name='Cameras',
                                choices=[
                                    'No Camera',
                                    'Omni Yolo',
                                    'Omni Filtered',
                                    'Omni Rendered',
                                    'Kinect Yolo',
                                    'Kinect Depth',
                                ],
                                borderRadius=3, 
                                colour=consts.COLORS["button"], 
                                textColour = consts.COLORS["white"],
                                fontSize = 5*consts.FACTOR,
                                values=[-1, 0, 1, 2, 3, 4,], 
                                direction='down', 
                                textHAlign='centre', 
                                )
                            )
probFieldUI = []

consts.DefaultWidgets = [gameWidgets, controlWidgets, probFieldUI, skillWidgets, calibrationWidgets, []]

def changeCalibValues(selectedRobot):
    temp = consts.calibSkillPIDCode
    consts.calibSkillPIDCode = consts.DefaultWidgets[3][consts.calibSkillNumberOfBars+8+0].getSelected()-1
    if temp != consts.calibSkillPIDCode or selectedRobot != consts.calibSkillSelectedRobot:
        consts.calibSkillSelectedRobot = selectedRobot
        for i in range(consts.calibSkillNumberOfBars):
            consts.DefaultWidgets[3][len(skillWidgets)-consts.calibSkillNumberOfBars+i].setValue(Robots[selectedRobot].calibSkillValues[consts.calibSkillPIDCode][i]*1000)
            #consts.DefaultWidgets[3][8+numberofDropDowns+(consts.calibSkillNumberOfBars*2)+i].setValue(Robots[selectedRobot].calibSkillValues[consts.calibSkillPIDCode][i]*1000)
        
    valueStrings = consts.calibSkillStrings[consts.calibSkillPIDCode]
    tempValues = Robots[selectedRobot].calibSkillValues[consts.calibSkillPIDCode]
    
    Robots[selectedRobot].calibSkillValues[consts.calibSkillPIDCode] = []
    for i in range(consts.calibSkillNumberOfBars):
        Robots[selectedRobot].calibSkillValues[consts.calibSkillPIDCode].append(float(consts.DefaultWidgets[3][len(skillWidgets)-consts.calibSkillNumberOfBars+i].getValue()/1000))
        #Robots[selectedRobot].calibSkillValues[consts.calibSkillPIDCode].append(float(consts.DefaultWidgets[3][8+numberofDropDowns+(consts.calibSkillNumberOfBars*2)+i].getValue()/1000))
        consts.DefaultWidgets[3][i].setText(str(Robots[selectedRobot].calibSkillValues[consts.calibSkillPIDCode][-1]) + " " + str(Robots[selectedRobot].calibSkillValuesRobot[consts.calibSkillPIDCode][-1]) + " " + str(valueStrings[i]))
        # consts.DefaultWidgets[3][8+numberofDropDowns+i].setText(str(Robots[selectedRobot].calibSkillValues[consts.calibSkillPIDCode][-1]) + " " + str(Robots[selectedRobot].calibSkillValuesRobot[consts.calibSkillPIDCode][-1]) + " " + str(valueStrings[i]))
        #consts.DefaultWidgets[3][8+numberofDropDowns+(consts.calibSkillNumberOfBars)+i].setText(str(Robots[selectedRobot].calibSkillValues[consts.calibSkillPIDCode][-1]) + " " + str(Robots[selectedRobot].calibSkillValuesRobot[consts.calibSkillPIDCode][-1]) + " " + str(valueStrings[i]))
        
    if tempValues != Robots[selectedRobot].calibSkillValues[consts.calibSkillPIDCode]:
        Robots[selectedRobot].debSocket.sendto(str(str(consts.calibSkillPIDCode+1) + str(Robots[selectedRobot].calibSkillValues[consts.calibSkillPIDCode])).encode(), Robots[selectedRobot].RoDebugSocket)
        print(str(str(consts.calibSkillPIDCode+1) + str(Robots[selectedRobot].calibSkillValues[consts.calibSkillPIDCode])))
        #print(selectedRobot, consts.calibSkillPIDCode, Robots[selectedRobot].calibSkillValuesRobot[consts.calibSkillPIDCode])
    
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
        #selectedRobot = ControlRobots(keyboardPress, joystickPress, Robots, getSelectedRobot(keyboardPress), controlIDSList)
        RobotsGUI(Robots, justInfo=1)
        cameras.handleCameras(Robots)

def Skills():
    global skillsMarker
    global mouseGUI
    if REPRESENT_GAME:
        Field()
        selectedRobot = ControlRobots(keyboardPress, joystickPress, Robots, getSelectedRobot(keyboardPress), controlIDSList)
        skillsMarker, mouseGUI = handleMarkers(mouse, skillsMarker, mouseGUI, Robots, getSelectedRobot(keyboardPress))
        changeCalibValues(getSelectedRobot(keyboardPress))
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
                x.show()#enableUI() # NEW OPTIMIZATION IT SOLVES THE BUTTON PROBLEMS
        else:
            for x in a:
                x.hide()#disableUI() # NEW OPTIMIZATION IT SOLVES THE BUTTON PROBLEMS
                
                
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
    defaultIPS = ["172.16.49.88", "172.16.49.11", "172.16.49.12", "172.16.49.13", "172.16.49.14", "172.16.49.15"]
    IPS = []

    for i in range(len(robots)):
        try:
            ip_address = socket.gethostbyname(robots[i])
            #print(f"Hostname: {robots[i]} - ", end=' ')
            #print(f"IP Address: {ip_address}")
            IPS.append(ip_address)
        except:
            IPS.append(defaultIPS[i])
    
    if IPS[0] == "127.0.0.1":
        IPS[0] = "172.16.49.156"
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
    
    if consts.PRINTTIME:
        print(round((time.time()-loopTime)*1000), "ms", end=' ')
    # if refBox.available:
    #     refBox.CommandID = refBox.handleComms()
        # print(refBox.CommandID)
    
    calculateHeatMaps(Robots, getSelectedRobot(keyboardPress), np.asarray(strategy.solution))
    if consts.PRINTTIME:
        print(round((time.time()-loopTime)*1000), "ms", end=' ')
    if REPRESENT:
        kick = guiMain(kick)
    if consts.PRINTTIME:
        print(round((time.time()-loopTime)*1000), "ms", end=' ')

    if MenuSelected == 0 or MenuSelected == 2:
        Robots, kick, recebe, solution = strategyTEMP(Robots, kick, MenuSelected)
    
    if consts.PRINTTIME:
        print(round((time.time()-loopTime)*1000), "ms", end=' ')
    # if refBox.available:
    #     refBox.handleCommand(refBox.CommandID, Robots)
    
    if newInfo:
        sendInfo(Robots)
    
    if consts.PRINTTIME:
        print(round((time.time()-loopTime)*1000), "ms", end=' ')
    pygame.display.update()
    
    # DISPLAY TIME PER LOOP WITH COLORS
    finalTime = round((time.time()-loopTime)*1000)
    if consts.PRINTTIME or consts.PRINT1TIME:
        if finalTime > TIMEPERLOOP:
            print(f"{consts.bcolors.FAIL}{finalTime:3.0f}ms{consts.bcolors.ENDC}", end=" | ")
        elif finalTime > TIMEPERLOOP*0.80:
            print(f"{consts.bcolors.WARNING}{finalTime:3.0f}ms{consts.bcolors.ENDC}", end=" | ")
        else: 
            print(f"{consts.bcolors.ENDC}{finalTime:3.0f}ms{consts.bcolors.ENDC}", end=" | ")

    timerAverage += finalTime
    while (finalTime := round((time.time()-loopTime)*1000)) < TIMEPERLOOP:
        pass
    if consts.PRINTTIME or consts.PRINT1TIME:
        # print(finalTime, "ms", end=' ')
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
                                consts.FIELD_SIZE["wall"][0] + 0.01*consts.RESOLUTION[0], 
                                consts.YOFFSET + consts.FIELD_SIZE["wall"][1]-(0.007*consts.RESOLUTION[1]*consts.FACTOR) - 0.002*consts.RESOLUTION[0],  
                                consts.RESOLUTION[0] - consts.FIELD_SIZE["wall"][0] - 0.015*consts.RESOLUTION[0], 
                                0.007*consts.RESOLUTION[1]*consts.FACTOR  - 0.001*consts.RESOLUTION[0], 
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
    
    timePerLoop = timerAverage/loop
    if timePerLoop > TIMEPERLOOP:
        print(f"{consts.bcolors.FAIL}{timePerLoop:4.1f}ms{consts.bcolors.ENDC}", end=" | ")
    elif timePerLoop > TIMEPERLOOP*0.75:
        print(f"{consts.bcolors.WARNING}{timePerLoop:4.1f}ms{consts.bcolors.ENDC}", end=" | ")
    else: 
        print(f"{consts.bcolors.ENDC}{timePerLoop:4.1f}ms{consts.bcolors.ENDC}", end=" | ")

    #print(timerAverage/loop) 


######################## INIT ########################
if __name__ == "__main__":
    ############ PYGAME INIT ############
    if REPRESENT and runMode:
        pygame.init()
        # pygame.freetype.init()
        pygame.joystick.init()
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        if FULLSCREEN:
            flags |= pygame.FULLSCREEN
        SCREEN = pygame.display.set_mode(tuple(RESOLUTION), flags, 8, display=0)

        ############ MENU TABS ############
        MenuSelected = 3
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
        IPS = getIPS()
        # IPS = ["172.16.49.88", "172.16.49.67", "172.16.49.129", "172.16.49.247", "172.16.49.224", "172.16.49.115", 1] # BASESTATION MINHA
        # IPS = ["172.16.49.136", "172.16.49.129", "172.16.49.79", "172.16.49.79", "172.16.49.235", "172.16.49.79", 1] # BASESTATION TELVISASO
        
        if len(sys.argv) > 1:
            for i in sys.argv:
                if i == 'local' or i == 'sim' or i == 'simulator':
                    IPS = ["localhost", "localhost", "localhost", "localhost", "localhost", "localhost", 2]
        print(IPS)
        Robots = [Robot(a+1, IPS[0], IPS[a+1], 0, IPS[-1]) for a in range(5)]
    except Exception as e:
        print(e)
        
    SuperMain()
    
    # cameras.cap.release()
    # cv2.destroyAllWindows()
    pygame.quit()