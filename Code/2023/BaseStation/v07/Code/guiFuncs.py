"""This file is where all the main UI functions are stored.
"""
import pygame
import consts
import guiElements
import strategy
import robot as R

def Field():
    """Field function draws the field on the screen1
    """
    pygame.draw.rect(consts.SCREEN,consts.COLORS["fieldGround"],(0, consts.YOFFSET, consts.FIELD_SIZE["wall"][0],consts.FIELD_SIZE["wall"][1]), border_radius = consts.FACTOR)
    pygame.draw.rect(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["offset"],consts.FIELD_SIZE["offset"]+consts.YOFFSET, consts.FIELD_SIZE["outerLine"][0], consts.FIELD_SIZE["outerLine"][1]), border_radius = consts.FACTOR, width=2*consts.FACTOR)
    pygame.draw.rect(consts.SCREEN,consts.COLORS["yellow"],(consts.FIELD_SIZE["offset"]-consts.FIELD_SIZE["goal"][0], (consts.FIELD_SIZE["wall"][1]/2-consts.FIELD_SIZE["goal"][1]/2)+consts.YOFFSET,consts.FIELD_SIZE["goal"][0]+consts.FACTOR*2, consts.FIELD_SIZE["goal"][1]), border_radius = consts.FACTOR)
    pygame.draw.rect(consts.SCREEN,consts.COLORS["blue"],(consts.FIELD_SIZE["wall"][0]-consts.FIELD_SIZE["offset"]-consts.FACTOR*2, (consts.FIELD_SIZE["wall"][1]/2-consts.FIELD_SIZE["goal"][1]/2)+consts.YOFFSET,consts.FIELD_SIZE["goal"][0]+consts.FACTOR*2, consts.FIELD_SIZE["goal"][1]), border_radius = consts.FACTOR)
    pygame.draw.rect(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["offset"], (consts.FIELD_SIZE["wall"][1]/2-consts.FIELD_SIZE["smallArea"][1]/2)+consts.YOFFSET,consts.FIELD_SIZE["smallArea"][0]+consts.FACTOR*2, consts.FIELD_SIZE["smallArea"][1]), border_radius = consts.FACTOR, width = 2*consts.FACTOR)
    pygame.draw.rect(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["wall"][0]-consts.FIELD_SIZE["offset"]-consts.FIELD_SIZE["smallArea"][0]-consts.FACTOR*2, (consts.FIELD_SIZE["wall"][1]/2-consts.FIELD_SIZE["smallArea"][1]/2)+consts.YOFFSET,consts.FIELD_SIZE["smallArea"][0]+consts.FACTOR*2, consts.FIELD_SIZE["smallArea"][1]), border_radius = consts.FACTOR, width = 2*consts.FACTOR)
    pygame.draw.rect(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["offset"], (consts.FIELD_SIZE["wall"][1]/2-consts.FIELD_SIZE["bigArea"][1]/2)+consts.YOFFSET,consts.FIELD_SIZE["bigArea"][0]+consts.FACTOR*2, consts.FIELD_SIZE["bigArea"][1]), border_radius = consts.FACTOR, width = 2*consts.FACTOR)
    pygame.draw.rect(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["wall"][0]-consts.FIELD_SIZE["offset"]-consts.FIELD_SIZE["bigArea"][0]-consts.FACTOR*2, (consts.FIELD_SIZE["wall"][1]/2-consts.FIELD_SIZE["bigArea"][1]/2)+consts.YOFFSET,consts.FIELD_SIZE["bigArea"][0]+consts.FACTOR*2, consts.FIELD_SIZE["bigArea"][1]), border_radius = consts.FACTOR, width = 2*consts.FACTOR)
    pygame.draw.circle(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["wall"][0]/2,consts.FIELD_SIZE["wall"][1]/2+consts.YOFFSET), consts.FIELD_SIZE["circle"], width = 2*consts.FACTOR)
    pygame.draw.circle(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["wall"][0]/2,consts.FIELD_SIZE["wall"][1]/2+consts.YOFFSET), 2*consts.FACTOR, width = 2*consts.FACTOR)
    pygame.draw.line(consts.SCREEN,consts.COLORS["white"],(consts.FIELD_SIZE["wall"][0]/2, consts.YOFFSET+consts.FIELD_SIZE["offset"]), (consts.FIELD_SIZE["wall"][0]/2, consts.YOFFSET+consts.FIELD_SIZE["offset"]+consts.FIELD_SIZE["outerLine"][1]), width=consts.FACTOR*2)
    
############ DRAW ROBOTS AND INFO ############
def RobotsGUI(Robots, selectedRobot = -1):
    """This function is called to draw all the robots on the field.

    Args:
        Robots (list): List of all the robots and their info
        selectedRobot (int, optional): Defaults to -1.
    """
    for index, robot in enumerate(Robots):
        if index == selectedRobot:
            robot.draw_robot(1)
        else:
            robot.draw_robot()
        robot.draw_opponents()
        robot.draw_robotInfo()
    for robot in Robots:
        robot.draw_lines_of_pass(Robots)
        # for r in Robots:
        #     guiElements.drawLine(robot.position, r.position)
        
def RefBox():
    pass

# def drawLine(x1, y1, x2, y2):
#     pygame.draw.line(consts.SCREEN,consts.COLORS["yellow"],coord2FieldCoord(x1, y1), (coord2FieldCoord(x2, y2)), width=2)
#     # print("hello", prob, end=" - ")
#     # screen = guiData.screen
#     # text = consts.SMALLFONT.render(str(prob), True, (255, 0,0))
#     # consts.SCREEN.blit(text,coord2FieldCoord(x, y))

# def drawProbability(x, y, prob):
#     # print("hello", prob, end=" - ")
#     # screen = guiData.screen
#     text = consts.SMALLFONT.render(str(prob), True, (255, 0,0))
#     consts.SCREEN.blit(text,coord2FieldCoord(x, y))



def coord2FieldCoord(X0, X1):
    """This function converts the X and Y to pixels no the screen.

    Args:
        X0 (int): X position on the real map
        X1 (int): Y position on the real map

    Returns:
        list: The new position on pixels
    """
    Y1 = X0 * 10 * consts.FACTOR + consts.FIELD_SIZE["wall"][0] / 2
    Y2 = -X1 * 10 * consts.FACTOR + consts.FIELD_SIZE["wall"][1] / 2 + consts.YOFFSET
    return Y1, Y2
# def coord2FieldCoord(X0, X1):
#     Y1 = X0 * 10 * consts.FACTOR + consts.FIELD_SIZE["wall"][0] / 2
#     Y2 = -X1 * 10 * consts.FACTOR + consts.FIELD_SIZE["wall"][1] / 2 + consts.YOFFSET
#     return Y1, Y2