"""
Constants for the code, Pygame, Representations, Scale Factors, Colors, Fonts, etc \n
It Requires ***pygame*** and ***screeninfo*** installed
"""
from screeninfo import get_monitors
import pygame
pygame.init()

FULLSCREEN = 1
"""This enables the fullscreen option on the GUI"""
RESOLUTION = [1920, 1080]
"""The Resolution variable defines the resolution of the screen, it the ***FULLSCREEN*** option is not enabled"""
REPRESENT = 1
"""This flag turns on or off the represnetation"""
REPRESENT_GAME = 1
"""This flags turns on or off the game representation"""
RUNNING = 1
"""Flag thaat determins if the code should run or not"""
TIMEPERLOOP = 50
"""Time per iteration defenition"""
PRINTTIME = 0
"""This flag enables the prints to display all the time stamps"""
SCREEN = pygame.display.set_mode(tuple(RESOLUTION), display=0)
"""This flag is the "*screen*" used on pygame window, so it is used to display everything"""

if FULLSCREEN:
    """This loop checks all the monitors connected to the computer, and gets the resolution of the main one, to display the code in the right resolution"""
    for m in get_monitors():
        if(m.is_primary == True):
            RESOLUTION[0] = m.width
            RESOLUTION[1] = m.height
            break
print(RESOLUTION)

"""This now are the flags for the visual aspect of it, representation flags"""
FACTOR = int((RESOLUTION[0])/300)
"""This is a scale factor, used to adjust to diferent displays"""
FIELD_SIZE = {
    "offset": FACTOR*10,
    "wall": [FACTOR*240, FACTOR*160],
    "outerLine": [FACTOR*220, FACTOR*140],
    "goal": [int(FACTOR*5), int(FACTOR*26.5)],
    "smallArea": [7.5*FACTOR, 40*FACTOR],
    "bigArea": [22.5*FACTOR, 69*FACTOR],
    "circle": 20*FACTOR
}
"""This is a struct that handles the dimensions to build the field and draw it"""
ROBOT_SIZE = FACTOR*3
"""It defines the size of the robot to display it on the field"""
MENUS_SIZE = 0.025
"""This defines the size of the menus on percentage, so basically in this case it is 2.5% of the screen height"""
YOFFSET = 0.025*RESOLUTION[1]
"""This defines the size of the menu in pixels"""

############ ROBOTS/GAME CONSTANTS ############
MARGIN2PASS = ROBOT_SIZE/50
"""This is the size of the margin to check for lines of pass"""

############ ROBOTS/GUI CONSTANTS ############
NUMBER_OF_ROBOTS = 5
"""The number of robots playing"""
SKILLSGUI = ["Stop", "Move", "Attack", "Kick", "Recieve", "Cover", "Defend", "Control"]
"""This is the name of the skills in order of their number"""
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
    "blue": [80, 180, 200],
    "brightblue": [130, 230, 250],
    "red": [240, 60, 60],
    "background": [30, 33, 36],
    "button": [66, 69, 73],
    "hover": [90, 93, 96],
    "selected": [115, 135, 220],
    "activated": [115, 220, 135],
    "fieldGround": [26, 140, 20]
}
"""This is a struct with all the color used by the software"""

SMALLFONT = pygame.font.SysFont('comicsansms', int(4*FACTOR))
TINYFONT = pygame.font.SysFont('comicsansms', int(3*FACTOR))
"""These are two fonts to represent text in the screen"""