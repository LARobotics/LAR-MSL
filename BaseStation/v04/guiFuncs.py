import pygame
from consts import *
import guiElements
import strategy

    
############ DRAW FIELD ############
def Field(pygame, screen):
    pygame.draw.rect(screen,COLORS["fieldGround"],(0, YOFFSET, FIELD_SIZE["wall"][0], FIELD_SIZE["wall"][1]), border_radius = FACTOR)
    pygame.draw.rect(screen,COLORS["white"],(FIELD_SIZE["offset"], FIELD_SIZE["offset"]+YOFFSET, FIELD_SIZE["outerLine"][0], FIELD_SIZE["outerLine"][1]), border_radius = FACTOR, width=2*FACTOR)
    pygame.draw.rect(screen,COLORS["yellow"],(FIELD_SIZE["offset"]-FIELD_SIZE["goal"][0], (FIELD_SIZE["wall"][1]/2-FIELD_SIZE["goal"][1]/2)+YOFFSET, FIELD_SIZE["goal"][0]+FACTOR*2, FIELD_SIZE["goal"][1]), border_radius = FACTOR)
    pygame.draw.rect(screen,COLORS["blue"],(FIELD_SIZE["wall"][0]-FIELD_SIZE["offset"]-FACTOR*2, (FIELD_SIZE["wall"][1]/2-FIELD_SIZE["goal"][1]/2)+YOFFSET, FIELD_SIZE["goal"][0]+FACTOR*2, FIELD_SIZE["goal"][1]), border_radius = FACTOR)
    pygame.draw.rect(screen,COLORS["white"],(FIELD_SIZE["offset"], (FIELD_SIZE["wall"][1]/2-FIELD_SIZE["smallArea"][1]/2)+YOFFSET, FIELD_SIZE["smallArea"][0]+FACTOR*2, FIELD_SIZE["smallArea"][1]), border_radius = FACTOR, width = 2*FACTOR)
    pygame.draw.rect(screen,COLORS["white"],(FIELD_SIZE["wall"][0]-FIELD_SIZE["offset"]-FIELD_SIZE["smallArea"][0]-FACTOR*2, (FIELD_SIZE["wall"][1]/2-FIELD_SIZE["smallArea"][1]/2)+YOFFSET, FIELD_SIZE["smallArea"][0]+FACTOR*2, FIELD_SIZE["smallArea"][1]), border_radius = FACTOR, width = 2*FACTOR)
    pygame.draw.rect(screen,COLORS["white"],(FIELD_SIZE["offset"], (FIELD_SIZE["wall"][1]/2-FIELD_SIZE["bigArea"][1]/2)+YOFFSET, FIELD_SIZE["bigArea"][0]+FACTOR*2, FIELD_SIZE["bigArea"][1]), border_radius = FACTOR, width = 2*FACTOR)
    pygame.draw.rect(screen,COLORS["white"],(FIELD_SIZE["wall"][0]-FIELD_SIZE["offset"]-FIELD_SIZE["bigArea"][0]-FACTOR*2, (FIELD_SIZE["wall"][1]/2-FIELD_SIZE["bigArea"][1]/2)+YOFFSET, FIELD_SIZE["bigArea"][0]+FACTOR*2, FIELD_SIZE["bigArea"][1]), border_radius = FACTOR, width = 2*FACTOR)
    pygame.draw.circle(screen,COLORS["white"],(FIELD_SIZE["wall"][0]/2, FIELD_SIZE["wall"][1]/2+YOFFSET), FIELD_SIZE["circle"], width = 2*FACTOR)
    pygame.draw.circle(screen,COLORS["white"],(FIELD_SIZE["wall"][0]/2, FIELD_SIZE["wall"][1]/2+YOFFSET), 2*FACTOR, width = 2*FACTOR)
    pygame.draw.line(screen,COLORS["white"],(FIELD_SIZE["wall"][0]/2, YOFFSET+FIELD_SIZE["offset"]), (FIELD_SIZE["wall"][0]/2, YOFFSET+FIELD_SIZE["offset"]+FIELD_SIZE["outerLine"][1]), width=FACTOR*2)
    
############ DRAW ROBOTS AND INFO ############
def RobotsGUI(screen, Robots):
    for robot in Robots:
        robot.draw_robot(screen)
        robot.draw_robotInfo(screen)
        
def RefBox():
    pass
