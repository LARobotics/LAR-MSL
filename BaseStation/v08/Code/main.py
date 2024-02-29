""" This is the main code of the basestation. It is the code that runs the representation and strategy for the MSL LAR MinhoTeam. It was developed by the team, and it can interact either with the real robots or the robots on our simulation environment on Webots.\n
    It has some dependecies:\n
    1. numpy @ 1.23.4 
    2. pygame @ 2.1.3.dev8

    To install the dependencies please run the following line:\n
    ``pip3 install numpy==1.23.4 pygame==2.1.3.dev8``

    To get the simulation running, you need Webots installed, at least the version 2023a. You also need the simulation environemnt files. Those can be found in the following repository.\n
    <https://github.com/MSL-LAR-MinhoTeam/Simulator>
    
    """

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
import consts
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.button import ButtonArray
from pygame_widgets.combobox import ComboBox
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.progressbar import ProgressBar
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.toggle import Toggle

runMode = 1
if len(sys.argv) > 1:
    for i in sys.argv:
        if i == '--http':
            runMode = 0

kick = 0
recebe = 0
finalTime = 0

controlWidgets = [Toggle(consts.SCREEN, 1400, int(consts.YOFFSET + 5*consts.FACTOR), 90, 30), TextBox(consts.SCREEN, 1300, int(consts.YOFFSET+5*consts.FACTOR), 80, 30, colour=consts.COLORS["button"], borderColour = consts.COLORS["button"], textColour = (255, 255, 255))]
controlWidgets[1].disable()
controlWidgets[1].setText("Data Fusion")

def Game(): 
    if REPRESENT_GAME:
        Field()
        RobotsGUI(Robots)
        RefBox()

def ProbFields(): 
    if REPRESENT_GAME:
        enableProbUI(Robots, getSelectedRobot(keyboardPress), MainMenus)
        PField(Robots, getSelectedRobot(keyboardPress))
        RobotsGUI(Robots, getSelectedRobot(keyboardPress))
        RefBox()
        selectedRobot = ControlRobots(keyboardPress, joystickPress, Robots, getSelectedRobot(keyboardPress))

def Control():
    if REPRESENT_GAME:
        consts.DEBUG_DATA_FUSION = controlWidgets[0].getValue()
        Field()
        selectedRobot = ControlRobots(keyboardPress, joystickPress, Robots, getSelectedRobot(keyboardPress))
        RobotsGUI(Robots, getSelectedRobot(keyboardPress))
        RefBox()

def Skills():
    if REPRESENT_GAME:
        Field()
        RobotsGUI(Robots)
        RefBox()

def Exit():
    global RUNNING
    RUNNING = 0 

def changeMenu(a):
    global MenuSelected
    global Robots
    MenuSelected = a
    MainMenus[1] =[[0]*len(MainMenus[0][0])] * len(MainMenus[0])
    MainMenus[1][a] = 1
    for i in range(len(MainMenus[2])):  
        if MainMenus[1][i] == 1:
            MainMenus[2][i].inactiveColour = consts.COLORS["activated"]
            MainMenus[2][i].hoverColour = consts.COLORS["activated"]
        else:
            MainMenus[2][i].inactiveColour = consts.COLORS["button"]
            MainMenus[2][i].hoverColour = consts.COLORS["hover"]
    

    for i, a in enumerate(MainMenus[4]):
        if i == MenuSelected:
            for x in a:
                x.enableUI()
        else:
            for x in a:
                x.disableUI()

    # if MenuSelected == 2:
    #     enableProbUI(Robots, getSelectedRobot(keyboardPress), MainMenus)

    if(a == len(MainMenus[0])-1):
        MainMenus[3][a]()
    


######################## INIT ########################

############ PYGAME INIT ############
if REPRESENT and runMode:
    pygame.init()
    pygame.joystick.init()
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    if FULLSCREEN:
        flags |= pygame.FULLSCREEN
    SCREEN = pygame.display.set_mode(tuple(RESOLUTION), flags, display=0)

    ############ MENU TABS ############
    MenuSelected = 2
    MainMenus = [["Game + RefBox", "Control", "Prob Fields", "Skills Test", "Calibration", "Exit"],[0, 0, 0, 0, 0, 0],[],[Game, Control, ProbFields, Skills, Skills, Exit], [[], controlWidgets, [], [], [], []]]
    MainMenus[1][MenuSelected] = 1
    for a in range(len(MainMenus[0])):
        MainMenus[2].append(Button(SCREEN, a*(1/len(MainMenus[0]))*consts.RESOLUTION[0], 0, (1/len(MainMenus[0]))*consts.RESOLUTION[0], MENUS_SIZE*consts.RESOLUTION[1], text=MainMenus[0][a], radius = 20, onClick = lambda a: changeMenu(a), onClickParams = [a], textColour = (255, 255, 255)))
    # for robot in Robots:
    #     for a in robot.probField:
    #         MainMenus[4][2].append(a.UI)
    changeMenu(MenuSelected)

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
    # IPS = ["192.168.31.249", "192.168.31.58", "192.168.31.79", "192.168.31.79", "192.168.31.79", "192.168.31.79", 1]
    Robots = [Robot(a+1, IPS[0], IPS[a+1], 0, IPS[-1]) for a in range(5)]
except Exception as e:
    print(e)



############ GUI MAIN LOOP ############
def guiMain(kick):
    global mouse
    global keyboardPress, joystickPress
    global joysticks
    global MenuSelected
    
    SCREEN.fill(consts.COLORS["background"])
    mouse = list(pygame.mouse.get_pos()); 
    mouse.append(0)

    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:  Exit()
        if ev.type == pygame.KEYDOWN:
            keyboardPress.append(ev.key)
            if ev.key == pygame.K_F12:           sendInfo(Robots)
            if ev.key == pygame.K_F1:       MenuSelected = 0; changeMenu(MenuSelected)
            if ev.key == pygame.K_F2:       MenuSelected = 1;changeMenu(MenuSelected)
            if ev.key == pygame.K_F3:       MenuSelected = 2;changeMenu(MenuSelected)
            if ev.key == pygame.K_F4:       MenuSelected = 3;changeMenu(MenuSelected)
            if ev.key == pygame.K_F5:       MenuSelected = 4;changeMenu(MenuSelected)
            if ev.key == pygame.K_F6:       MenuSelected = 5;changeMenu(MenuSelected)
            if ev.key == pygame.K_ESCAPE:       Exit()
            if ev.key == pygame.K_SPACE:        kick = 1
        if ev.type == pygame.KEYUP:             keyboardPress.remove(ev.key)
        if ev.type == pygame.MOUSEBUTTONDOWN:   mouse[2] = 1
        if ev.type == pygame.JOYBUTTONDOWN:     joystickPress[ev.joy].append(ev.button+2)
        if ev.type == pygame.JOYBUTTONUP:
            if ev.button+2 in joystickPress[ev.joy]:  joystickPress[ev.joy].remove(ev.button+2)
        if ev.type == pygame.JOYAXISMOTION:
            joystickPress[ev.joy][ev.axis] = np.round(ev.value, 2)
        if ev.type == pygame.JOYDEVICEADDED or ev.type == pygame.JOYDEVICEREMOVED:
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    
    MainMenus[3][MenuSelected]()
    pygame_widgets.update(events)
    
    return kick

def main():
    global Robots
    global kick
    global recebe
    global finalTime
   
    loopTime = time.time()
    newInfo = getInfo(Robots)
    if newInfo and DEBUG_DATA_FUSION:
        dataFusion(Robots)
    if REPRESENT:
        kick = guiMain(kick)
    
    # print(Robots[0].position)
    ################### TEMPORARY ####################
    # for robot in Robots:
    #     for probField in robot.probField:
    #         probField.test(robot.robotID)

    if MenuSelected == 0 or MenuSelected == 0:
        Robots, kick, recebe = strategyTEMP(Robots, kick, recebe)
    if newInfo:
        sendInfo(Robots)
    
    pygame.display.update()
   
    # DISPLAY TIME PER LOOP WITH COLORS
    finalTime = round((time.time()-loopTime)*1000, 2)
    if finalTime > TIMEPERLOOP:
        print(f"{consts.bcolors.FAIL}{finalTime:4.1f}ms{consts.bcolors.ENDC}", end=" | ")
    elif finalTime > TIMEPERLOOP*0.5:
        print(f"{consts.bcolors.WARNING}{finalTime:4.1f}ms{consts.bcolors.ENDC}", end=" | ")
    else:
        print(f"{consts.bcolors.ENDC}{finalTime:4.1f}ms{consts.bcolors.ENDC}", end=" | ")

    while (finalTime := round((time.time()-loopTime)*1000, 2)) < TIMEPERLOOP:
        pass
    # print(finalTime, "ms")
    print()

if runMode:
    ############ MAIN LOOP ############
    initTime = time.time()
    sendInfo(Robots)
    while RUNNING:
        main()        
    pygame.quit()