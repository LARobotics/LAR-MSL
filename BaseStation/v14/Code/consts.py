"""
Constants for the code, Pygame, Representations, Scale Factors, Colors, Fonts, etc \n
It Requires ***pygame*** and ***screeninfo*** installed
"""
from screeninfo import get_monitors
import probField
import pygame
import sys
import platform
import git
import configs.field


pygame.init()

FULLSCREEN = 1
"""This enables the fullscreen option on the GUI"""
RESOLUTION = [1920, 1080]
"""The Resolution variable defines the resolution of the screen, it the ***FULLSCREEN*** option is not enabled"""
REPRESENT = 1
"""This flag turns on or off the represnetation"""
REPRESENT_GAME = 1

"""This flag turns on or off the represnetation"""
REPRESENT_LINES_OF_PASS = 0
"""This flag turns on or off the represnetation"""
REPRESENT_MAX_VALUE_ON_HEAT_MAP = 1
"""This flag turns on or off the represnetation"""
REPRESENT_EVERY_MAX_PIXEL_ON_HEAT_MAP = 0
"""This flag turns on or off the debug keys for simulation"""
DEBUG_KEYS_SIMULATION = 1
"""This flag turns on or off the Data Fusion for localization debugging"""
DEBUG_DATA_FUSION = 1
"""This flag turns on or off the graphic and plot represnetation"""
REPRESENT_PLOTS = 1
"""This flags turns on or off the game representation"""
RUNNING = 1
"""Flag thaat determins if the code should run or not"""
LOG_FILE = 0

NUMBERofJoySticks = 0
JoyStickPointer = 0
SimOpponents = []

SCORE = [0, 0]
TeamNames = ["LAR@MSL", "TechUnited"]

TIMEPERLOOP = 40
SIMULATOR = 0
if len(sys.argv) > 1:
    for i in sys.argv:
        if i == 'local' or i == 'sim' or i == 'simulator':
            SIMULATOR = 1
            TIMEPERLOOP = 50
        
"""Time per iteration defenition"""
PRINTTIME = 0

PRINT1TIME = 0
"""This flag enables the prints to display all the time stamps"""

if platform.system() == "Windows":
    repo = git.Repo("../../../Player_YOLO")
    repo.remotes.origin.pull()
    sha = repo.head.object.hexsha
else:
    sha = "LINUX_COMMIT"
gitHash = {
    "playerYolo": str(sha[:7])
}
print(gitHash)

if FULLSCREEN:
    """This loop checks all the monitors connected to the computer, and gets the resolution of the main one, to display the code in the right resolution"""
    for m in get_monitors():
        if(m.is_primary == True):
            RESOLUTION[0] = m.width
            RESOLUTION[1] = m.height
            break

flags = pygame.HWSURFACE | pygame.OPENGL | pygame.DOUBLEBUF
if FULLSCREEN:
    flags |= pygame.FULLSCREEN
SCREEN = pygame.display.set_mode(tuple(RESOLUTION), flags, 8, display=0)
"""This flag is the "*screen*" used on pygame window, so it is used to display everything"""

FIELD_DIMENSIONS = configs.field.FIELD_DIMENSIONS


"""This now are the flags for the visual aspect of it, representation flags"""
FACTOR = int(int((RESOLUTION[0])/350))
FIELD_FACTOR = int(FACTOR*(240/FIELD_DIMENSIONS["A"]))
# if RESOLUTION[1] < 1200:
#     FIELD_FACTOR -= 1
FACTOR_INT = int(FACTOR)-1

"""This is a scale factor, used to adjust to diferent displays"""
FIELD_SIZE = {            ## MANEIRA CORRETA
    "offset": FIELD_FACTOR*FIELD_DIMENSIONS["L"],
    "wall": [FIELD_FACTOR*(FIELD_DIMENSIONS["A"]+2*FIELD_DIMENSIONS["L"]), FIELD_FACTOR*(FIELD_DIMENSIONS["B"]+2*FIELD_DIMENSIONS["L"])],
    "outerLine": [FIELD_FACTOR*FIELD_DIMENSIONS["A"], FIELD_FACTOR*FIELD_DIMENSIONS["B"]],
    "goal": [int(FIELD_FACTOR*FIELD_DIMENSIONS["BALIZA_PROF"]), int(FIELD_FACTOR*FIELD_DIMENSIONS["BALIZA_COMP"])],
    "smallArea": [FIELD_DIMENSIONS["F"]*FIELD_FACTOR, FIELD_DIMENSIONS["D"]*FIELD_FACTOR],
    "bigArea": [FIELD_DIMENSIONS["E"]*FIELD_FACTOR, FIELD_DIMENSIONS["C"]*FIELD_FACTOR],
    "circle": FIELD_FACTOR*FIELD_DIMENSIONS["H"]/2,
    "penalty": FIELD_DIMENSIONS["I"]*FIELD_FACTOR,
    "blackdots": FIELD_DIMENSIONS["Q"]*FIELD_FACTOR
}

"""This is a struct that handles the dimensions to build the field and draw it"""
ROBOT_SIZE = FACTOR*2.5
"""It defines the size of the robot to display it on the field"""
MENUS_SIZE = 0.025
"""This defines the size of the menus on percentage, so basically in this case it is 2.5% of the screen height"""
YOFFSET = 0.025*RESOLUTION[1]
"""This defines the size of the menu in pixels"""

FIELDGREEN = 0
############ ROBOTS/GAME CONSTANTS ############
MARGIN2PASS = 2*ROBOT_SIZE/50
MARGIN2CHECKPASS = 2
"""This is the size of the margin to check for lines of pass"""

############ ROBOTS/
# GUI CONSTANTS ############
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
    "yellowStealth": [180, 180, 120],
    "yellowStealth2": [140, 140, 80],
    "blue": [80, 180, 200],
    "blueStealth": [20, 255, 200],
    "brightblue": [130, 230, 250],
    "orange": [210, 105, 30],
    "tomato": [255, 99, 101],
    "red": [240, 60, 60],
    "pink": [252, 178, 197],
    "background": [30, 33, 36],
    "button": [66, 69, 73],
    "hover": [90, 93, 96],
    "selected": [115, 135, 220],
    "activated": [115, 220, 135],
    "fieldGround2": [0, 100, 0],
    "fieldGround": [26, 120, 0],
    "batRed": [237, 27, 36],
    "batYellow": [252, 176, 64],
    "batGreen": [60, 181, 75],
    "green": [0, 255, 0],
    
    "skyblue": [135, 206, 250],
    "limeGreen": [50, 205, 50],
    "gold": [255, 215, 0],
    "indigo": [75, 0, 130],
    "coral": [255, 127, 80],
    "teal": [0, 128, 128],
    "brown": [165, 42, 42],
    "purple": [128, 0, 128]
}
"""This is a struct with all the color used by the software"""

# if platform.system() == "Windows":
SCOREFONT = pygame.freetype.Font('fonts/ocraextended.ttf', int(30*(FACTOR_INT)))
SCOREFONT2 = pygame.freetype.Font('fonts/ocraextended.ttf', int(10*(FACTOR_INT)))
SMALLFONT = pygame.freetype.Font('fonts/segoeuiemoji.ttf', int(5*(FACTOR_INT)))
SMALLFONT2 = pygame.freetype.Font('fonts/segoeuisymbol.ttf', int(5*(FACTOR_INT)))
SSMALLFONT = pygame.freetype.Font('fonts/segoeuiemoji.ttf', int(4*(FACTOR_INT)))
TINYFONT = pygame.freetype.Font('fonts/segoeuiemoji.ttf', int(3*(FACTOR_INT)))
SUPERTINYFONT = pygame.freetype.Font('fonts/segoeuiemoji.ttf', int(2*(FACTOR_INT)))
# else:
#     SCOREFONT = pygame.freetype.Font('fonts/ocraextended.ttf', int(30*(FACTOR_INT)))
#     SCOREFONT2 = pygame.freetype.Font('fonts/ocraextended.ttf', int(10*(FACTOR_INT)))
#     SMALLFONT = pygame.freetype.Font('fonts/segoeuisymbol.ttf', int(5*(FACTOR_INT)))
#     SMALLFONT2 = pygame.freetype.Font('fonts/segoeuisymbol.ttf', int(5*(FACTOR_INT)))
#     SSMALLFONT = pygame.freetype.Font('fonts/segoeuisymbol.ttf', int(4*(FACTOR_INT)))
#     TINYFONT = pygame.freetype.Font('fonts/segoeuisymbol.ttf', int(3*(FACTOR_INT)))
#     SUPERTINYFONT = pygame.freetype.Font('fonts/segoeuisymbol.ttf', int(2*(FACTOR_INT)))
"""These are two fonts to represent text in the screen"""


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

MainMenus = []

############ PROBABILITY ############
bestDistanceToPass = 5
bestDistanceToGoal = 5
deviation = 8
deviationPower = 20

freeBallTimeout = 5

ANGLEMARGIN = 10
MINPROBPASS = 0.225
MINPROBGOAL = 0

HISTERESEGOAL = 0.04
HISTERESEPASS = 0.04
HISTERESPROB = 0.03

############ WIDGETS ############
DefaultWidgets = []

############ POSITIONS AND ZONES ############
mapConfigJson = {}
mapConfigJsonPaths = []
mapNames = []
probFieldUIpointer = 0
probFieldUIprevPointer = -1

heatMaps = []
zonesDefault = []#probField.makeZones(2)
ZonesPoints = [[int((probField.x*4)/6), int(probField.y/2)], [int(probField.x/2), int((probField.y/3))], [int(probField.x/2), int((probField.y*2)/3)], [int((probField.x)/4), int(probField.y/2)], [int(probField.x/10), int(probField.y/2)]]
ZonesPointsLoc = [[p[0]/10-12, p[1]/10-8] for p in ZonesPoints]
zonesFields = []
heatMapSituations = [0, 0, 0, 0, 0]

opponentsFields = []

############ CALIBRATION SKILLS ################
calibSkillNumberOfBars = 11
calibSkillStrings = [
                     ["Kp_move","Ki_move","Kd_move","outputLimit_PID_move","Katracao_move","Kintensidade_move","outputLimit_atractor_move"],
                     ["Kp_atack", "Ki_atack", "Kd_atack", "outputLimit_PID_atack", "Katracao_atack", "Kintensidade_atack", "outputLimit_atractor_atack"],
                     ["Kp_kick","Ki_kick","Kd_kick","outputLimit_PID_kick","Katracao_kick","Kintensidade_kick","outputLimit_atractor_kick",],
                     ["Kp_receive_rot","Ki_receive_rot","Kd_receive_rot","outputLimit_PID_receive_rot","Kp_receive_vel","Ki_receive_vel","Kd_receive_vel","outputLimit_PID_receive_vel","Katracao_receive","Kintensidade_receive","outputLimit_atractor_receive"],
                     ["Kp_cover","Ki_cover","Kd_cover","outputLimit_PID_cover","Katracao_cover","Kintensidade_cover","outputLimit_atractor_cover",],
                     ["Kp_defend","Ki_defend","Kd_defend","outputLimit_PID_defend","Katracao_defend","Kintensidade_defend","outputLimit_atractor_defend",],
                     ["Kp_remoteControl","Ki_remoteControl","Kd_remoteControl","utputLimit_PID_remoteControl","Katracao_remoteControl","Kintensidade_remoteControl","outputLimit_atractor_remoteControl",],]

calibSkillPIDCode = -1
calibSkillSelectedRobot = -1
for i in calibSkillStrings:
    for a in range(calibSkillNumberOfBars):
        i.append("")
        