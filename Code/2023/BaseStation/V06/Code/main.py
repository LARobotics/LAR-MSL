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
#import keyboard
from robot import *
from guiFuncs import *
from strategy import *
from guiElements import *
import consts
# import guiData

runMode = 1
if len(sys.argv) > 1:
    for i in sys.argv:
        if i == '--http':
            runMode = 0

kick = 0
recebe = 0

def Game(): 
    if REPRESENT_GAME:
        Field()
        RobotsGUI(Robots)
        RefBox()
    #if -1 != (a := list1.update(globals()["mouse"])):
    #    list1.main = list1.options[a]
    #list1.draw(screen)

def Control():
    #global keyboardPress
    #global joystickPress
    if REPRESENT_GAME:
        Field()
        selectedRobot = ControlRobots(keyboardPress, joystickPress, Robots)
        RobotsGUI(Robots, selectedRobot)
        RefBox()
    #if clear == 1:
        #screen.fill((30,33,36))
    #for but in buttons:
    #    but.handle_hover(globals()["mouse"])

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
    MenuSelected = a
    MainMenus[1] =[[0]*len(MainMenus[0][0])] * len(MainMenus[0])
    MainMenus[1][a] = 1
    for i in range(len(MainMenus[2])):  
        MainMenus[2][i].setFlag(MainMenus[1][i])
    if(a == len(MainMenus[0])-1):
        MainMenus[3][a]()
    #screen.fill((30,33,36))


######################## INIT ########################

############ ROBOTS AND COMUNICATION  ############
try:
    IPS = ["localhost", "localhost", "localhost", "localhost", "localhost", "localhost", 2]
    # IPS = ["192.168.31.249", "192.168.31.147", "192.168.31.147", "192.168.31.147", "192.168.31.147", "192.168.31.147", 1]
    Robots = [Robot(a+1, IPS[0], IPS[a+1], 0, IPS[-1]) for a in range(5)]
except Exception as e:
    print(e)


############ PYGAME INIT ############
if REPRESENT and runMode:
    pygame.init()
    pygame.joystick.init()
    flags = pygame.HWSURFACE | pygame.DOUBLEBUF
    if FULLSCREEN:
        flags |= pygame.FULLSCREEN
    SCREEN = pygame.display.set_mode(tuple(RESOLUTION), flags, display=0)
    # screen = guiData.screen
    # guiData.setScreen(screen)
    ############ MENU TABS ############
    MainMenus = [["Game + RefBox", "Control", "Skills Test", "Calibration", "Exit"],[1, 0, 0, 0, 0],[],[Game, Control, Skills, Skills, Exit]]
    MenuSelected = 0
    for a in range(len(MainMenus[0])):
        MainMenus[2].append(Button(SCREEN, a*(1/len(MainMenus[0])), 0.0, (1/len(MainMenus[0])), MENUS_SIZE, FUNC, changeMenu, a, text=MainMenus[0][a], flag=MainMenus[1][a]))
    keyboardPress = []
    joystickPress = [[0, 0, 0, 0, -1, -1], [0, 0, 0, 0, -1, -1], [0, 0, 0, 0, -1, -1], [0, 0, 0, 0, -1, -1], [0, 0, 0, 0, -1, -1]]
    buttons = []
    buttons.append(Button(SCREEN, 0.0, 0.0+MENUS_SIZE, 0.1, 0.1, SWITCH, [], [], text="Siga Siga"))
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        print(joystick.get_name())
    ############ MOUSE AND FONTS ############
    mouse = (0, 0, 0)
    list1 = DropDown(
        [COLORS["button"], COLORS["activated"]],
        [COLORS["button"], COLORS["hover"]],
        50, 50, 200, 50, 
        pygame.font.SysFont(None, int(5*FACTOR)), 
        "", ["Playing", "Control", "Stop"])

############ GUI MAIN LOOP ############
def guiMain():
    global mouse
    global keyboardPress, joystickPress
    global joysticks
    SCREEN.fill((30,33,36))
    mouse = list(pygame.mouse.get_pos()); 
    mouse.append(0)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:  Exit()
        if ev.type == pygame.KEYDOWN:
            keyboardPress.append(ev.key)
            if ev.key == pygame.K_F1:           sendInfo(Robots)
            if ev.key == pygame.K_ESCAPE:       Exit()
        if ev.type == pygame.KEYUP:             keyboardPress.remove(ev.key)
        if ev.type == pygame.MOUSEBUTTONDOWN:   mouse[2] = 1
        if ev.type == pygame.JOYBUTTONDOWN:     joystickPress[ev.joy].append(ev.button+2)
        if ev.type == pygame.JOYBUTTONUP:
            if ev.button+2 in joystickPress[ev.joy]:  joystickPress[ev.joy].remove(ev.button+2)
        if ev.type == pygame.JOYAXISMOTION:
            joystickPress[ev.joy][ev.axis] = np.round(ev.value, 2)
        if ev.type == pygame.JOYDEVICEADDED or ev.type == pygame.JOYDEVICEREMOVED:
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    
    #print(keyboardPress, joystickPress, end="|")
    MainMenus[3][MenuSelected]()
    for but in MainMenus[2]:
        but.handle_hover(mouse)


def main():
    global Robots
    global kick
    global recebe
    loopTime = time.time()
    newInfo = getInfo(Robots)
    if newInfo:
        dataFusion(Robots)
    if REPRESENT:
        guiMain()
    if MenuSelected == 0:
        Robots, kick, recebe = strategyTEMP(Robots, kick, recebe)
    if newInfo:
        sendInfo(Robots)
    if PRINTTIME: print((time.time()-loopTime)*1000, "ms", end=" | ")

    if PRINTTIME: print((time.time()-loopTime)*1000, "ms", end=" | ")
    print(round((time.time()-loopTime)*1000, 1), "ms")
    while (time.time()-loopTime)*1000 < TIMEPERLOOP:
        pass
    pygame.display.update()
    if PRINTTIME: print((time.time()-loopTime)*1000, "ms")

if runMode:
    ############ MAIN LOOP ############
    initTime = time.time()
    sendInfo(Robots)
    while RUNNING:
        main()        
    pygame.quit()