"""This file is where all the main UI functions are stored.
"""
import pygame
import consts
import guiElements
import strategy
import robot as R
import probField
import numpy as np
import time
import matplotlib.pyplot as plt
import fileHandling
import refBox

selectedRobot = 0

def PField(Robots, selectedRobot):
    """Field function draws the field on the screen1
    """
    
    field = Robots[selectedRobot].probField[0]
    matrix = field.get(selectedRobot)
    surf = pygame.pixelcopy.make_surface(matrix)
    consts.SCREEN.blit(pygame.transform.scale_by(surf, consts.FIELD_FACTOR), (0, consts.YOFFSET))
    Field(1)
    
def Field(bk = 0):
    """Field function draws the field on the screen1
    """
    consts.FIELDGREEN = 1
    if bk == 0:
        pygame.draw.rect(consts.SCREEN,consts.COLORS["fieldGround"],(0, consts.YOFFSET, consts.FIELD_SIZE["wall"][0],consts.FIELD_SIZE["wall"][1]), border_radius = consts.FACTOR)
        consts.FIELDGREEN = 0
    pygame.draw.rect(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["offset"],consts.FIELD_SIZE["offset"]+consts.YOFFSET, consts.FIELD_SIZE["outerLine"][0], consts.FIELD_SIZE["outerLine"][1]), border_radius = consts.FACTOR, width=2*consts.FACTOR)
    pygame.draw.rect(consts.SCREEN,consts.COLORS["yellow"],(consts.FIELD_SIZE["offset"]-consts.FIELD_SIZE["goal"][0], (consts.FIELD_SIZE["wall"][1]/2-consts.FIELD_SIZE["goal"][1]/2)+consts.YOFFSET,consts.FIELD_SIZE["goal"][0]+consts.FACTOR*2, consts.FIELD_SIZE["goal"][1]), border_radius = consts.FACTOR)
    pygame.draw.rect(consts.SCREEN,consts.COLORS["blue"],(consts.FIELD_SIZE["wall"][0]-consts.FIELD_SIZE["offset"]-consts.FACTOR*2, (consts.FIELD_SIZE["wall"][1]/2-consts.FIELD_SIZE["goal"][1]/2)+consts.YOFFSET,consts.FIELD_SIZE["goal"][0]+consts.FACTOR*2, consts.FIELD_SIZE["goal"][1]), border_radius = consts.FACTOR)
    pygame.draw.rect(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["offset"], (consts.FIELD_SIZE["wall"][1]/2-consts.FIELD_SIZE["smallArea"][1]/2)+consts.YOFFSET,consts.FIELD_SIZE["smallArea"][0]+consts.FACTOR*2, consts.FIELD_SIZE["smallArea"][1]), border_radius = consts.FACTOR, width = 2*consts.FACTOR)
    pygame.draw.rect(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["wall"][0]-consts.FIELD_SIZE["offset"]-consts.FIELD_SIZE["smallArea"][0]-consts.FACTOR*2, (consts.FIELD_SIZE["wall"][1]/2-consts.FIELD_SIZE["smallArea"][1]/2)+consts.YOFFSET,consts.FIELD_SIZE["smallArea"][0]+consts.FACTOR*2, consts.FIELD_SIZE["smallArea"][1]), border_radius = consts.FACTOR, width = 2*consts.FACTOR)
    pygame.draw.rect(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["offset"], (consts.FIELD_SIZE["wall"][1]/2-consts.FIELD_SIZE["bigArea"][1]/2)+consts.YOFFSET,consts.FIELD_SIZE["bigArea"][0]+consts.FACTOR*2, consts.FIELD_SIZE["bigArea"][1]), border_radius = consts.FACTOR, width = 2*consts.FACTOR)
    pygame.draw.rect(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["wall"][0]-consts.FIELD_SIZE["offset"]-consts.FIELD_SIZE["bigArea"][0]-consts.FACTOR*2, (consts.FIELD_SIZE["wall"][1]/2-consts.FIELD_SIZE["bigArea"][1]/2)+consts.YOFFSET,consts.FIELD_SIZE["bigArea"][0]+consts.FACTOR*2, consts.FIELD_SIZE["bigArea"][1]), border_radius = consts.FACTOR, width = 2*consts.FACTOR)
    pygame.draw.line(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["wall"][0]/2, consts.YOFFSET+consts.FIELD_SIZE["offset"]), (consts.FIELD_SIZE["wall"][0]/2, consts.YOFFSET+consts.FIELD_SIZE["offset"]+consts.FIELD_SIZE["outerLine"][1]), width=consts.FACTOR*2)
    pygame.draw.circle(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["wall"][0]/2,consts.FIELD_SIZE["wall"][1]/2+consts.YOFFSET), 2*consts.FACTOR, width = 2*consts.FACTOR)
    pygame.draw.circle(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["wall"][0]/2,consts.FIELD_SIZE["wall"][1]/2+consts.YOFFSET), consts.FIELD_SIZE["circle"], width = 2*consts.FACTOR)
    pygame.draw.circle(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["offset"]+consts.FIELD_SIZE["penalty"],consts.FIELD_SIZE["wall"][1]/2+consts.YOFFSET), 2*consts.FACTOR, width = 10*consts.FACTOR)
    pygame.draw.circle(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["wall"][0]-(consts.FIELD_SIZE["offset"]+consts.FIELD_SIZE["penalty"]),consts.FIELD_SIZE["wall"][1]/2+consts.YOFFSET), 2*consts.FACTOR, width = 10*consts.FACTOR)
    pygame.draw.circle(consts.SCREEN,consts.COLORS["black"],(consts.FIELD_SIZE["offset"]+consts.FIELD_SIZE["penalty"],consts.FIELD_SIZE["wall"][1]/2+consts.YOFFSET-consts.FIELD_SIZE["blackdots"]), int(consts.FACTOR/2), width = 10*consts.FACTOR)
    pygame.draw.circle(consts.SCREEN,consts.COLORS["black"],(consts.FIELD_SIZE["offset"]+consts.FIELD_SIZE["penalty"],consts.FIELD_SIZE["wall"][1]/2+consts.YOFFSET+consts.FIELD_SIZE["blackdots"]), int(consts.FACTOR/2), width = 10*consts.FACTOR)
    pygame.draw.circle(consts.SCREEN,consts.COLORS["black"],(consts.FIELD_SIZE["wall"][0]-(consts.FIELD_SIZE["offset"]+consts.FIELD_SIZE["penalty"]),consts.FIELD_SIZE["wall"][1]/2+consts.YOFFSET-consts.FIELD_SIZE["blackdots"]), int(consts.FACTOR/2), width = 10*consts.FACTOR)
    pygame.draw.circle(consts.SCREEN,consts.COLORS["black"],(consts.FIELD_SIZE["wall"][0]-(consts.FIELD_SIZE["offset"]+consts.FIELD_SIZE["penalty"]),consts.FIELD_SIZE["wall"][1]/2+consts.YOFFSET+consts.FIELD_SIZE["blackdots"]), int(consts.FACTOR/2), width = 10*consts.FACTOR)
    
    
############ DRAW ROBOTS AND INFO ############
def RobotsGUI(Robots, selectedRobot = -1, justInfo = 0):
    """This function is called to draw all the robots on the field.

    Args:
        Robots (list): List of all the robots and their info
        selectedRobot (int, optional): Defaults to -1.
    """
    for index, robot in enumerate(Robots):
        if index == selectedRobot:
            robot.draw_robotInfo(1)
        else:
            robot.draw_robotInfo()
    
    if justInfo:
        return
    
    for robot in Robots:
        robot.draw_opponents()
        robot.draw_lines_of_pass(Robots)
        
    for index, robot in enumerate(Robots):
        if index == selectedRobot:
            robot.draw_robot(1)
        else:
            robot.draw_robot()
        
def RobotsCommsGui(Robots):
    for robot in Robots:
        robot.draw_robotCommsInfo()
        
def Score():
    scoreString = str(consts.SCORE[0]) + " - " + str(consts.SCORE[1])
    text, rect = consts.SCOREFONT.render(scoreString, (255, 255, 255))
    consts.SCOREFONT.render_to(consts.SCREEN, ((consts.RESOLUTION[0] - consts.FIELD_SIZE["wall"][0])/2 + consts.FIELD_SIZE["wall"][0] - rect.width / 2, consts.YOFFSET + consts.FACTOR*4),str(scoreString), (255, 255, 255))
    scoreString2 = str(f"{consts.TeamNames[0]:^12}" + f"{'VS':^4}" + f"{consts.TeamNames[1]:^12}")
    text, rect2 = consts.SCOREFONT2.render(scoreString2, (255, 255, 255))
    consts.SCOREFONT2.render_to(consts.SCREEN, ((consts.RESOLUTION[0] - consts.FIELD_SIZE["wall"][0])/2 + consts.FIELD_SIZE["wall"][0] - rect2.width / 2, consts.YOFFSET + consts.FACTOR*8 + rect.height),str(scoreString2), (255, 255, 255))
    
def RefBox(Robots):
    if refBox.available:
        refBox.CommandID, refBox.Arg = refBox.handleComms()
    

def handleMarkers(mouse, skillsMarker, mouseGUI, Robots, selectedRobot):
    done = 0
    mouse[1] = mouse[1]-consts.YOFFSET
    if mouse[2] > 0 and mouse[0]<consts.FIELD_SIZE["wall"][0] and mouse[1]<consts.FIELD_SIZE["wall"][1] and mouse[1]>0:
        if mouse[2] == 1:     id = 0
        else:                 id = 1
        skillsMarker1 = FieldCoord2coord(mouse[0], mouse[1])
        for robot in Robots:
            if abs(robot.position[0] - skillsMarker1[0]) + abs(robot.position[1] - skillsMarker1[1]) < 0.3:
                skillsMarker[selectedRobot][id] = [robot.position[0], robot.position[1], robot.robotID-1]#FieldCoord2coord(-1000, robot.robotID-1)
                done = 1
        if done == 0:
            skillsMarker[selectedRobot][id][0:2] = FieldCoord2coord(mouse[0], mouse[1])
            skillsMarker[selectedRobot][id][2] = -1
            mouseGUI[selectedRobot][id] = coord2FieldCoord(skillsMarker[selectedRobot][id][0], skillsMarker[selectedRobot][id][1])
    for i in range(len(skillsMarker[selectedRobot])):
        if skillsMarker[selectedRobot][i][2] >= 0:
            skillsMarker[selectedRobot][i] = [Robots[skillsMarker[selectedRobot][i][2]].position[0], Robots[skillsMarker[selectedRobot][i][2]].position[1], Robots[skillsMarker[selectedRobot][i][2]].robotID-1]
        mouseGUI[selectedRobot][i] = coord2FieldCoord(skillsMarker[selectedRobot][i][0], skillsMarker[selectedRobot][i][1])
    
    pygame.draw.circle(consts.SCREEN,consts.COLORS["orange"],(mouseGUI[selectedRobot][1][0], mouseGUI[selectedRobot][1][1]),consts.FACTOR*3.5,)
    text, rect = consts.TINYFONT.render("T2", (255, 255, 255))
    consts.TINYFONT.render_to(consts.SCREEN, (mouseGUI[selectedRobot][1][0] - text.get_width() / 2, mouseGUI[selectedRobot][1][1] - text.get_height() / 2), str("T2"), (255, 255, 255))
    
    pygame.draw.circle(consts.SCREEN,consts.COLORS["tomato"],(mouseGUI[selectedRobot][0][0], mouseGUI[selectedRobot][0][1]),consts.FACTOR*3.5,)
    text, rect = consts.TINYFONT.render("T2", (255, 255, 255))
    consts.TINYFONT.render_to(consts.SCREEN, (mouseGUI[selectedRobot][0][0] - text.get_width() / 2, mouseGUI[selectedRobot][0][1] - text.get_height() / 2), str("T1"), (255, 255, 255))
    
    return skillsMarker, mouseGUI

def FieldCoord2coord(X0, X1):
    # Y1 = X0 * 10 * consts.FACTOR + consts.FIELD_SIZE["wall"][0] / 2
    Y1 = round((X0-consts.FIELD_SIZE["wall"][0]/2)/(10*consts.FIELD_FACTOR), 2)
    # Y2 = -X1 * 10 * consts.FACTOR + consts.FIELD_SIZE["wall"][1] / 2 + consts.YOFFSET
    Y2 = round(-(X1-consts.FIELD_SIZE["wall"][1]/2)/(10*consts.FIELD_FACTOR), 2)
    return [Y1, Y2]

def coord2FieldCoord(X0, X1):
    """This function converts the X and Y to pixels no the screen.

    Args:
        X0 (int): X position on the real map
        X1 (int): Y position on the real map

    Returns:
        list: The new position on pixels
    """
    Y1 = X0 * 10 * consts.FIELD_FACTOR + consts.FIELD_SIZE["wall"][0] / 2
    Y2 = -X1 * 10 * consts.FIELD_FACTOR + consts.FIELD_SIZE["wall"][1] / 2 + consts.YOFFSET
    return [Y1, Y2]


def getSelectedRobot(keyboardPress):
    global selectedRobot
    if ord('1') in keyboardPress: selectedRobot = 0
    if ord('2') in keyboardPress: selectedRobot = 1
    if ord('3') in keyboardPress: selectedRobot = 2
    if ord('4') in keyboardPress: selectedRobot = 3
    if ord('5') in keyboardPress: selectedRobot = 4
    return selectedRobot

def enableProbUI(Robots, selectedRobot, MainMenus):
    if consts.MainMenus[4][2][2].getValue():
        consts.probFieldUIpointer = consts.MainMenus[4][2][0].getSelected()
    else:
        consts.probFieldUIpointer = consts.heatMapSituations[selectedRobot]
        consts.MainMenus[4][2][0].choose(consts.probFieldUIpointer)
    # print(consts.probFieldUIpointer)
        
    a = fileHandling.getPointer(consts.mapConfigJsonPaths[consts.probFieldUIpointer])
    if consts.probFieldUIpointer != consts.probFieldUIprevPointer:
        for i in range(3, len(a)+3):
            consts.MainMenus[4][2][i].slider.setValue(a[i-3])
    consts.probFieldUIprevPointer = consts.probFieldUIpointer
    
    for i in range(3, len(MainMenus[4][2])):
        # print(type(MainMenus[4][2][i]))
        a[i-3] = MainMenus[4][2][i].slider.getValue()
        MainMenus[4][2][i].text.setText(consts.mapNames[i-3] + " -> " + str(int(a[i-3]*100)))
        

def enableSkillsUI(Robots, selectedRobot, MainMenus):
    pass
    # for robot in Robots:
    #     if robot.robotID-1 == selectedRobot:
    #         pass
    #     else:
    #         for a in robot.probField:
    #             a.UI.disableUI()
    # MainMenus[4][3] = []
    # for a in Robots[selectedRobot].probField:
    #     a.UI.enableUI()
    #     MainMenus[4][3].append(a.UI)