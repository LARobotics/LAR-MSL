from screeninfo import get_monitors
import pygame
pygame.init()


############ PYGAME CONSTANTS ############
RESOLUTION = [1280, 720]
FULLSCREEN = 1
REPRESENT = 1
REPRESENT_GAME = 1
RUNNING = 1
TIMEPERLOOP = 20
PRINTTIME = 0

if FULLSCREEN:
    for m in get_monitors():
        if(m.is_primary == False): # THIS HAS BEEN CHANGED
            RESOLUTION[0] = m.width
            RESOLUTION[1] = m.height
            break


############ REPRESENTATION CONSTANTS ############
FACTOR = int((RESOLUTION[0])/330)
FIELD_SIZE = {
    "offset": FACTOR*10,
    "wall": [FACTOR*240, FACTOR*160],
    "outerLine": [FACTOR*220, FACTOR*140],
    "goal": [int(FACTOR*5), int(FACTOR*26.5)],
    "smallArea": [7.5*FACTOR, 40*FACTOR],
    "bigArea": [22.5*FACTOR, 69*FACTOR],
    "circle": 20*FACTOR
}
ROBOT_SIZE = FACTOR*5
MENUS_SIZE = 0.025
YOFFSET = 0.025*RESOLUTION[1]


############ ROBOTS/GUI CONSTANTS ############
NUMBER_OF_ROBOTS = 5
SKILLSGUI = ["Stop", "Move", "Attack", "Kick", "Recieve", "Cover", "Defend", "Control"]
STOP = 0
MOVE = 1
ATTACK = 2
KICK = 3
RECIEVE = 4
COVER = 5
DEFEND = 6
CONTROL = 7
SMALLFONT = 0


############ COLORS ############
COLORS = {
    "white": [255, 255, 255],
    "black": [0, 0, 0],
    "yellow": [240, 240, 60],
    "blue": [100, 200, 220],
    "background": [30, 33, 36],
    "button": [66, 69, 73],
    "hover": [90, 93, 96],
    "selected": [115, 135, 220],
    "activated": [115, 220, 135],
    "fieldGround": [26, 140, 20]
}

SMALLFONT = pygame.font.SysFont('comicsansms', int(4*FACTOR))
TINYFONT = pygame.font.SysFont('comicsansms', int(3*FACTOR))