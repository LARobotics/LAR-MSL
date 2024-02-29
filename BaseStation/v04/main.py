import math
import time
import numpy as np
import sys
import time
import socket
import json
import pygame
#import keyboard
from Robot import *
from guiFuncs import *
from strategy import *
from guiElements import *
from consts import *


kick = 0
recebe = 0

def Game():
    if REPRESENT_GAME:
        Field(pygame, screen)
        RobotsGUI(screen, Robots)
        RefBox()
    if -1 != (a := list1.update(globals()["mouse"])):
        list1.main = list1.options[a]
    list1.draw(screen)

def Control():
    if REPRESENT_GAME:
        Field(pygame, screen)
        RobotsGUI(screen, Robots)
        RefBox()
    #if clear == 1:
        #screen.fill((30,33,36))
    for but in buttons:
        but.handle_hover(globals()["mouse"])

def Skills():
    if REPRESENT_GAME:
        Field(pygame, screen)
        RobotsGUI(screen, Robots)
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
IPS = ["localhost", "localhost", "localhost", "localhost", "localhost", "localhost", 2]
Robots = [Robot(a+1, IPS[0], IPS[a+1], 0, IPS[-1]) for a in range(5)]


############ PYGAME INIT ############
if REPRESENT:
    pygame.init()
    flags = pygame.DOUBLEBUF
    if FULLSCREEN:
        flags |= pygame.FULLSCREEN
    screen = pygame.display.set_mode(tuple(RESOLUTION), flags, display=1)
    ############ MENU TABS ############
    MainMenus = [["Game + RefBox", "Control", "Skills Test", "Calibration", "Exit"],[1, 0, 0, 0, 0],[],[Game, Control, Skills, Skills, Exit]]
    MenuSelected = 0
    for a in range(len(MainMenus[0])):
        MainMenus[2].append(Button(screen, a*(1/len(MainMenus[0])), 0.0, (1/len(MainMenus[0])), MENUS_SIZE, FUNC, changeMenu, a, text=MainMenus[0][a], flag=MainMenus[1][a]))

    buttons = []
    buttons.append(Button(screen, 0.0, 0.0+MENUS_SIZE, 0.1, 0.1, SWITCH, [], [], text="Siga Siga"))

    ############ MOUSE AND FONTS ############
    mouse = (0, 0, 0)
    list1 = DropDown(
        [COLORS["button"], COLORS["activated"]],
        [COLORS["button"], COLORS["hover"]],
        50, 50, 200, 50, 
        pygame.font.SysFont(None, int(5*FACTOR)), 
        "", ["Playing", "Control", "Stop"])

############ GUI MAIN LOOP ############
def mainGui():
    global mouse
    screen.fill((30,33,36))
    mouse = list(pygame.mouse.get_pos()); 
    mouse.append(0)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:  Exit()
        if ev.type == pygame.KEYDOWN:   
            if ev.key == pygame.K_ESCAPE:   Exit()
        if ev.type == pygame.MOUSEBUTTONDOWN:   mouse[2] = 1
    
    MainMenus[3][MenuSelected]()
    for but in MainMenus[2]:
        but.handle_hover(mouse)

    pygame.display.update()


############ MAIN LOOP ############
initTime = time.time()
sendInfo(Robots)
while RUNNING:
    loopTime = time.time()
    newInfo = getInfo(Robots)
    Robots, kick, recebe = strategyTEMP(Robots, kick, recebe)
    if(newInfo):
        sendInfo(Robots)
    if PRINTTIME: print((time.time()-loopTime)*1000, "ms", end=" | ")
    if REPRESENT:
        mainGui()

    if PRINTTIME: print((time.time()-loopTime)*1000, "ms", end=" | ")
    while (time.time()-loopTime)*1000 < TIMEPERLOOP:
        pass
    if PRINTTIME: print((time.time()-loopTime)*1000, "ms")
    
pygame.quit()