#!/usr/bin/env python3
"""! @brief 2Calibration of the colors of the field."""
##
# @mainpage Calibration
#
# @section description_main Description
# To easy calibrate all sensors.
# All the senttings should be save in a .txt file.
# 
# @section notes_main Calibrations
# calib_cam_omni.py -> Calibrates Omni Camera Colour.
#
# calib_cam2.py -> Calibrates Front Camera Colour .
#
# Copyright (c) 2022 MinhoTeam.  All rights reserved.
##
# @file calib_cam_omni.py
#
# @brief Calibrates Omni Camera Colour. 
#
# @section description_doxygen_example Description
# Just move the track bars to right position to see the correct colours (like: field -> green , lines -> white, robots -> black). The wanted result is a 100% of image full of vivid colours.
#
# @section libraries_main Libraries/Modules
# - time standard library (https://docs.python.org/3/library/time.html)
#   - Access to sleep function.
# - openCV standart library (https://docs.python.org/3/library/opencv.html)
#   - Access to Camera and Computer Vision function.
#
# @section notes_doxygen_example Notes
# - Comments are Doxygen compatible.
#
# \todo
# - Make Flycamera capture
# - Make Track-bars
# - Make Filter
# - Read .txt
# - Write .txt
# 
# \test 
# - Capture image from camera
#
# \bug 
# - Flycamera capture

# @section author_doxygen_example Author(s)
# - Created by José Martins on 24/09/2022.
# - Modified by José Martins on 25/09/2022.
#
# Copyright (c) 2022 MinhoTeam.  All rights reserved.


# Imports
import os
#import PySpin
import EasyPySpin
from gc import callbacks
import PySimpleGUI as sg
import cv2 as cv
import numpy as np
from numpy import arange
import math
import sys
import keyboard
from time import time
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
# TODO:
# ADICIONAR Camera Omni

# Global Constants
## The mode of capture; 0 = camera, 1 = video, 2 = image.
capture = 1 
dists_calibration=[15,30,40,50,60,70,80,110,120,150,180,210,240,270,320,370,420,480,540,640,750,900,1000]
dists_calibration = np.array(dists_calibration)+24
label_ball_calibration=[15,30,50,80,100,150,180,240,320,420,540,640,750,900] #TESTAR O NUMEROP DE PONTOS Devem ser muitos
ball_calibration= np.array(label_ball_calibration)+24
code_omni = [["MAX_H_ball_omni",0],
        ["MIN_H_ball_omni",0],
        ["MAX_S_ball_omni",0],
        ["MIN_S_ball_omni",0],
        ["MAX_V_ball_omni",0],
        ["MIN_V_ball_omni",0],
        ["MAX_H_field_omni",0],
        ["MIN_H_field_omni",0],
        ["MAX_S_field_omni",0],
        ["MIN_S_field_omni",0],
        ["MAX_V_field_omni",0],
        ["MIN_V_field_omni",0],
        ["MAX_H_lines_omni",0],
        ["MIN_H_lines_omni",0],
        ["MAX_S_lines_omni",0],
        ["MIN_S_lines_omni",0],
        ["MAX_V_lines_omni",0],
        ["MIN_V_lines_omni",0],
        ["MAX_H_robot_omni",0],
        ["MIN_H_robot_omni",0],
        ["MAX_S_robot_omni",0],
        ["MIN_S_robot_omni",0],
        ["MAX_V_robot_omni",0],
        ["MIN_V_robot_omni",0],
        ["MAX_H_redshirt_omni",0],
        ["MIN_H_redshirt_omni",0],
        ["MAX_S_redshirt_omni",0],
        ["MIN_S_redshirt_omni",0],
        ["MAX_V_redshirt_omni",0],
        ["MIN_V_redshirt_omni",0],
        ["MAX_H_blueshirt_omni",0],
        ["MIN_H_blueshirt_omni",0],
        ["MAX_S_blueshirt_omni",0],
        ["MIN_S_blueshirt_omni",0],
        ["MAX_V_blueshirt_omni",0],
        ["MIN_V_blueshirt_omni",0],
        ["EXPOSURE_omni",0],
        ["GAIN_omni",0],
        ["SATURATION_omni",0],
        ["MAX_AREA_ball_omni",0], #38
        ["MIN_AREA_ball_omni",0], #39
        
        ]
code_front = [["MAX_H_ball_front",0],
        ["MIN_H_ball_front",0],
        ["MAX_S_ball_front",0],
        ["MIN_S_ball_front",0],
        ["MAX_V_ball_front",0],
        ["MIN_V_ball_front",0],
        ["MAX_H_field_front",0],
        ["MIN_H_field_front",0],
        ["MAX_S_field_front",0],
        ["MIN_S_field_front",0],
        ["MAX_V_field_front",0],
        ["MIN_V_field_front",0],
        ["MAX_H_lines_front",0],
        ["MIN_H_lines_front",0],
        ["MAX_S_lines_front",0],
        ["MIN_S_lines_front",0],
        ["MAX_V_lines_front",0],
        ["MIN_V_lines_front",0],
        ["MAX_H_robot_front",0],
        ["MIN_H_robot_front",0],
        ["MAX_S_robot_front",0],
        ["MIN_S_robot_front",0],
        ["MAX_V_robot_front",0],
        ["MIN_V_robot_front",0],
        ["MAX_H_redshirt_front",0],
        ["MIN_H_redshirt_front",0],
        ["MAX_S_redshirt_front",0],
        ["MIN_S_redshirt_front",0],
        ["MAX_V_redshirt_front",0],
        ["MIN_V_redshirt_front",0],
        ["MAX_H_blueshirt_front",0],
        ["MIN_H_blueshirt_front",0],
        ["MAX_S_blueshirt_front",0],
        ["MIN_S_blueshirt_front",0],
        ["MAX_V_blueshirt_front",0],
        ["MIN_V_blueshirt_front",0],
        ]
code_warp = [["WARP_bl",0],["WARP_br",0]]



# Images of Buttons
image_pause = './aux_file/pause.png'
image_restart = './aux_file/refresh.png'
image_save = './aux_file/download.png'
image_play = './aux_file/play.png'
image_rec = './aux_file/rec-button1.png'
image_recording = './aux_file/rec-button.png'

def save_map_field2(values):
    MAP_MARGIN_SIZE_H=420
    MAP_MARGIN_SIZE_W=340
    

    A=int(int(values["-F_A-"])/10)
    B=int(int(values["-F_B-"])/10)
    C=int(int(values["-F_C-"])/10)
    D=int(int(values["-F_D-"])/10)
    E=int(int(values["-F_E-"])/10)
    F=int(int(values["-F_F-"])/10)
    G=int(int(values["-F_G-"])/10)
    H=int(int(values["-F_H-"])/10)
    I=int(int(values["-F_I-"])/10)
    J=int(int(values["-F_J-"])/10)
    K=int(int(values["-F_K-"])/10)
    L=int(int(values["-F_L-"])/10)
    M=int(int(values["-F_M-"])/10)
    N=int(int(values["-F_N-"])/10)
    O=int(int(values["-F_O-"])/10)
    P=int(int(values["-F_P-"])/10)
    Q=int(int(values["-F_Q-"])/10)
    MAP_FIELD=np.zeros((MAP_MARGIN_SIZE_H+1,MAP_MARGIN_SIZE_W+1)) 
    
    #====GREY LINES====
    #CENTER CIRCLES
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2),int(MAP_MARGIN_SIZE_H/2)), int(H/2), 150, 2 )
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2),int(MAP_MARGIN_SIZE_H/2)), int(J/2)+1, 150, -1)
    #PENALTY CIRCLES
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2),int(MAP_MARGIN_SIZE_H/2-round(A/2)+I)), int(J/2)+1, 155, -1)
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2),int(MAP_MARGIN_SIZE_H/2+round(A/2)-I)), int(J/2)+1, 155, -1)
    #CORNER ARCS
    ## Why circle+ellipse? Ellipse alone don´t print the 4 corner iqual. So, is used circle to print corner arc and
    ## black ellipse to erease 3/4 of circle. (Fast solution)
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2+round(B/2)),int(MAP_MARGIN_SIZE_H/2+round(A/2))), (G), 150, 2)
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2+round(B/2)),int(MAP_MARGIN_SIZE_H/2-round(A/2))), (G), 150, 2)
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2-round(B/2)),int(MAP_MARGIN_SIZE_H/2-round(A/2))), (G), 150, 2)
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2-round(B/2)),int(MAP_MARGIN_SIZE_H/2+round(A/2))), (G), 150, 2)
 
    
    #HORIZONTAL LINES
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int(MAP_MARGIN_SIZE_H/2)), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int(MAP_MARGIN_SIZE_H/2)), 150, 2)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int(MAP_MARGIN_SIZE_H/2+round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int(MAP_MARGIN_SIZE_H/2+round(A/2))), 150, 2)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int(MAP_MARGIN_SIZE_H/2-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int(MAP_MARGIN_SIZE_H/2-round(A/2))), 150, 2)
 
        
    #HORIZONTAL LINES AREA
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)+(A/2)-E)), (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)+(A/2)-E)), 150, 2)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)-(A/2)+E)), (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)-(A/2)+E)), 150, 2)
    
    #HORIZONTAL LINES SMALL AREA
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)+(A/2)-F)), (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)+(A/2)-F)), 150, 2)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)-(A/2)+F)), (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)-(A/2)+F)), 150, 2)
    #VERTICAL LINES
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 150, 2)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 150, 2)
    #VERTICAL LINES AREA 1
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2)+E)), 150, 2)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2)+E)), 150, 2)
    #VERTICAL LINES AREA 2
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2)-E)), (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 150, 2)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2)-E)), (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 150, 2)
    #VERTICAL LINES SMALL AREA 1
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2)+F)), 150, 2)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2)+F)), 150, 2)
    #VERTICAL LINES SMALL AREA 2
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2)-F)), (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 150, 2)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2)-F)), (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 150, 2)

    #====WHITE LINES====
    #CENTER CIRCLES
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2),int(MAP_MARGIN_SIZE_H/2)), int(H/2), 255, 1)
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2),int(MAP_MARGIN_SIZE_H/2)), int(J/2), 255, -1)
    #PENALTY CIRCLES
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2),int(MAP_MARGIN_SIZE_H/2-round(A/2)+I)), int(J/2), 255, -1)
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2),int(MAP_MARGIN_SIZE_H/2+round(A/2)-I)), int(J/2), 255, -1)
    #CORNER ARCS
    ## Why circle+ellipse? Ellipse alone don´t print the 4 corner iqual. So, is used circle to print corner arc and
    ## black ellipse to erease 3/4 of circle. (Fast solution)
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2+round(B/2)),int(MAP_MARGIN_SIZE_H/2+round(A/2))), (G), 255, 1)
    cv.ellipse(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2+round(B/2)+1),int(MAP_MARGIN_SIZE_H/2+round(A/2)+1)), (20,20),180,90,360, 0, -1 )
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2+round(B/2)),int(MAP_MARGIN_SIZE_H/2-round(A/2))), (G), 255, 1)
    cv.ellipse(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2+round(B/2)+1),int(MAP_MARGIN_SIZE_H/2-round(A/2)-1)), (20,20),90,90,360, 0, -1 )
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2-round(B/2)),int(MAP_MARGIN_SIZE_H/2-round(A/2))), (G), 255, 1)
    cv.ellipse(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2-round(B/2)-1),int(MAP_MARGIN_SIZE_H/2-round(A/2)-1)), (20,20),0,90,360, 0, -1 )
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2-round(B/2)),int(MAP_MARGIN_SIZE_H/2+round(A/2))), (G), 255, 1)
    cv.ellipse(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2-round(B/2)-1),int(MAP_MARGIN_SIZE_H/2+round(A/2)+1)), (20,20),270,90,360, 0, -1 )
    
    #HORIZONTAL LINES
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int(MAP_MARGIN_SIZE_H/2)), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int(MAP_MARGIN_SIZE_H/2)), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int(MAP_MARGIN_SIZE_H/2+round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int(MAP_MARGIN_SIZE_H/2+round(A/2))), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int(MAP_MARGIN_SIZE_H/2-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int(MAP_MARGIN_SIZE_H/2-round(A/2))), 255, 1)
 
        
    #HORIZONTAL LINES AREA
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)+(A/2)-E)), (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)+(A/2)-E)), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)-(A/2)+E)), (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)-(A/2)+E)), 255, 1)
    
    #HORIZONTAL LINES SMALL AREA
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)+(A/2)-F)), (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)+(A/2)-F)), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)-(A/2)+F)), (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)-(A/2)+F)), 255, 1)
    #VERTICAL LINES
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 255, 1)
    #VERTICAL LINES AREA 1
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2)+E)), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2)+E)), 255, 1)
    #VERTICAL LINES AREA 2
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2)-E)), (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2)-E)), (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 255, 1)
    #VERTICAL LINES SMALL AREA 1
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2)+F)), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2)+F)), 255, 1)
    #VERTICAL LINES SMALL AREA 2
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2)-F)), (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2)-F)), (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 255, 1)


    

    #Corrections because elipses
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)-1),int(MAP_MARGIN_SIZE_H/2+round(A/2)+1)), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)+1),int(MAP_MARGIN_SIZE_H/2+round(A/2)+1)), 150, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)-1),int(MAP_MARGIN_SIZE_H/2-round(A/2)-1)), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)+1),int(MAP_MARGIN_SIZE_H/2-round(A/2)-1)), 150, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)-1),int((MAP_MARGIN_SIZE_H/2)-round(A/2))-1), (int((MAP_MARGIN_SIZE_W/2)-round(B/2)-1),int((MAP_MARGIN_SIZE_H/2)+round(A/2))+1), 150, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(B/2)+1),int((MAP_MARGIN_SIZE_H/2)-round(A/2))-1), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)+1),int((MAP_MARGIN_SIZE_H/2)+round(A/2))+1), 150, 1)
    cv.imwrite('FIELD2.png',MAP_FIELD)

def save_map_field(values):
    MAP_MARGIN_SIZE_H=620
    MAP_MARGIN_SIZE_W=540
    

    A=int(int(values["-F_A-"])/10)
    B=int(int(values["-F_B-"])/10)
    C=int(int(values["-F_C-"])/10)
    D=int(int(values["-F_D-"])/10)
    E=int(int(values["-F_E-"])/10)
    F=int(int(values["-F_F-"])/10)
    G=int(int(values["-F_G-"])/10)
    H=int(int(values["-F_H-"])/10)
    I=int(int(values["-F_I-"])/10)
    J=int(int(values["-F_J-"])/10)
    K=int(int(values["-F_K-"])/10)
    L=int(int(values["-F_L-"])/10)
    M=int(int(values["-F_M-"])/10)
    N=int(int(values["-F_N-"])/10)
    O=int(int(values["-F_O-"])/10)
    P=int(int(values["-F_P-"])/10)
    Q=int(int(values["-F_Q-"])/10)
    MAP_FIELD=np.zeros((MAP_MARGIN_SIZE_H+1,MAP_MARGIN_SIZE_W+1)) 
        #CENTER CIRCLES
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2),int(MAP_MARGIN_SIZE_H/2)), int(H/2), 255, 1)
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2),int(MAP_MARGIN_SIZE_H/2)), int(J/2), 255, -1)
    #PENALTY CIRCLES
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2),int(MAP_MARGIN_SIZE_H/2-round(A/2)+I)), int(J/2), 255, -1)
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2),int(MAP_MARGIN_SIZE_H/2+round(A/2)-I)), int(J/2), 255, -1)
    #CORNER ARCS
    ## Why circle+ellipse? Ellipse alone don´t print the 4 corner iqual. So, is used circle to print corner arc and
    ## black ellipse to erease 3/4 of circle. (Fast solution)
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2+round(B/2)),int(MAP_MARGIN_SIZE_H/2+round(A/2))), (G), 255, 1 )
    cv.ellipse(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2+round(B/2)+1),int(MAP_MARGIN_SIZE_H/2+round(A/2)+1)), (20,20),180,90,360, 0, -1 )
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2+round(B/2)),int(MAP_MARGIN_SIZE_H/2-round(A/2))), (G), 255, 1)
    cv.ellipse(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2+round(B/2)+1),int(MAP_MARGIN_SIZE_H/2-round(A/2)-1)), (20,20),90,90,360, 0, -1 )
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2-round(B/2)),int(MAP_MARGIN_SIZE_H/2-round(A/2))), (G), 255, 1)
    cv.ellipse(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2-round(B/2)-1),int(MAP_MARGIN_SIZE_H/2-round(A/2)-1)), (20,20),0,90,360, 0, -1 )
    cv.circle(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2-round(B/2)),int(MAP_MARGIN_SIZE_H/2+round(A/2))), (G), 255, 1)
    cv.ellipse(MAP_FIELD, (int(MAP_MARGIN_SIZE_W/2-round(B/2)-1),int(MAP_MARGIN_SIZE_H/2+round(A/2)+1)), (20,20),270,90,360, 0, -1 )
    
    #HORIZONTAL LINES
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int(MAP_MARGIN_SIZE_H/2)), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int(MAP_MARGIN_SIZE_H/2)), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int(MAP_MARGIN_SIZE_H/2+round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int(MAP_MARGIN_SIZE_H/2+round(A/2))), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int(MAP_MARGIN_SIZE_H/2-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int(MAP_MARGIN_SIZE_H/2-round(A/2))), 255, 1)
 
        
    #HORIZONTAL LINES AREA
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)+(A/2)-E)), (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)+(A/2)-E)), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)-(A/2)+E)), (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)-(A/2)+E)), 255, 1)
    
    #HORIZONTAL LINES SMALL AREA
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)+(A/2)-F)), (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)+(A/2)-F)), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)-(A/2)+F)), (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)-(A/2)+F)), 255, 1)
    #VERTICAL LINES
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)-round(B/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(B/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 255, 1)
    #VERTICAL LINES AREA 1
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2)+E)), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2)+E)), 255, 1)
    #VERTICAL LINES AREA 2
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2)-E)), (int((MAP_MARGIN_SIZE_W/2)-round(C/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2)-E)), (int((MAP_MARGIN_SIZE_W/2)+round(C/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 255, 1)
    #VERTICAL LINES SMALL AREA 1
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2)+F)), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2))), (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)-round(A/2)+F)), 255, 1)
    #VERTICAL LINES SMALL AREA 2
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2)-F)), (int((MAP_MARGIN_SIZE_W/2)-round(D/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 255, 1)
    cv.line(MAP_FIELD, (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2)-F)), (int((MAP_MARGIN_SIZE_W/2)+round(D/2)),int((MAP_MARGIN_SIZE_H/2)+round(A/2))), 255, 1)



    

    cv.imwrite('FIELD.png',MAP_FIELD)
    #cv.imshow("Field",MAP_FIELD)
    #cv.waitKey(20)
def read_front_consts_file(window):
    global code_omni
    global code_front
    file = open("config_front_consts.go",mode="r+")
    file.readline()
    file.readline()
    save_f=0
   
    for index, code_line in enumerate(code_front):
        
        file_line=file.readline()
        try:
            code_line[1]= [int(i) for i in file_line.split() if i.isdigit()][0]
        except:
            save_f=1
    file_line=file.readline()
    window["-WARP-"].update(value = [int(i) for i in file_line.split() if i.isdigit()][0])
    

    if(save_f):
        save_front_consts_file()
    else:
        file.close()

def read_field_consts_file(window):
    file = open("field_consts.txt",mode="r+")
    window["-F_A-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_B-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_C-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_D-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_E-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_F-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_G-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_H-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_I-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_J-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_K-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_L-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_M-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_N-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_O-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_P-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    window["-F_Q-"].update([int(i) for i in file.readline().split() if i.isdigit()][0])
    

   
    file.close()

def read_omni_consts_file(window):
    global code_omni
    global code_front
    file = open("config_omni_consts.go",mode="r+")
    file.readline()
    file.readline()
    save_f=0
    
    for index, code_line in enumerate(code_omni):
        
        file_line=file.readline()
        try:
            code_line[1]= [int(i) for i in file_line.split() if i.isdigit()][0]
            print("Linha "+ str(index)+"   "+str(code_line[0])+": "+str(code_line[1]))
        except:
            save_f=1
            print("ERRO A LER FILE")

    if(save_f):
        save_file()
    else:
        file.close()

def read_file(window):
    global code_omni
    global code_front
    file = open("config.go",mode="r+")
    file.readline()
    file.readline()
    save_f=0
    
    for index, code_line in enumerate(code_omni):
        
        file_line=file.readline()
        try:
            code_line[1]= [int(i) for i in file_line.split() if i.isdigit()][0]
        except:
            save_f=1
        
        
   
    for index, code_line in enumerate(code_front):
        
        file_line=file.readline()
        try:
            code_line[1]= [int(i) for i in file_line.split() if i.isdigit()][0]
        except:
            save_f=1
    file_line=file.readline()
    window["-WARP-"].update(value = [int(i) for i in file_line.split() if i.isdigit()][0])
    

    if(save_f):
        save_file()
    else:
        file.close()

def save_front_consts_file():
    global code_omni
    global code_front
    global real_dist_front
    
    file=open("config_front_consts.go",mode="w+")
    file.write("package main\n\n")
    
    for code_line in code_front:
        #print(code_line)
        file.write("const "+code_line[0]+" = "+str(int(code_line[1]))+"\n")
    for code_line in code_warp:
        #print(code_line)
        file.write("const "+code_line[0]+" = "+str(int(code_line[1]))+"\n")            
    file.close()
    
    print("File Saved!")
    return file
    
def save_front_tables_file():
    global code_omni
    global code_front
    global real_dist_front
    
    file=open("config_front_tables.go",mode="w+")
    file.write("package main\n\n")

    # Add Lookup Table To Front Camera
    file.write("\nvar real_coordenates_front = [480][480][2]int{\n")
    for x in range(0,480):
        file.write("{")
        for y in range(0,480):
            file.write("{"+str(int(real_dist_front[x][y][0]))+", "+str(int(real_dist_front[x][y][1]))+"}")
            file.write(", ")
        
        file.write("},\n")
        
        
    file.write("}")             
    file.close()
    
    print("File Saved!")
    return file

def save_omni_consts_file():
    global code_omni
    global code_front
    
    file=open("config_omni_consts.go",mode="w+")
    file.write("package main\n\n")
    for code_line in code_omni:
        #print(code_line)
        file.write("const "+code_line[0]+" = "+str(int(code_line[1]))+"\n")            
    file.close()
    
    print("File Saved!")
    return file

def save_omni_tables_file():
    global code_omni
    global code_front
    global real_dist_omni
    
    file=open("config_omni_tables.go",mode="w+")
    file.write("package OmniVision_pkg\n\n")

    # Add Lookup Table To Omni Camera Real Distances
    file.write("\nvar real_coordenates_omni = [480][480][4]int{\n")
    for x in range(0,480):
        file.write("{")
        for y in range(0,480):
            file.write("{"+str(int(real_dist_omni[x][y][0]))+", "+str(int(real_dist_omni[x][y][1]))+", "+str(int(real_polar_omni[x][y][0]))+", "+str(int(real_polar_omni[x][y][1]))+"}")
            file.write(", ")
        
        file.write("},\n")
        
        
    file.write("}")             
    file.close()
    
    print("File Saved!")
    return file  

def save_omni_ball_tables_file():
    global code_omni
    global code_front
    global real_dist_omni
    
    file=open("config_omni_tables_ball.go",mode="w+")
    file.write("package OmniVision_pkg\n\n")
    
    # Add Lookup Table To Omni Camera Real Distances
    file.write("\nvar real_coordenates_omni_ball = [480][480][4]int{\n")
    for x in range(0,480):
        file.write("{")
        for y in range(0,480):
            file.write("{"+str(int(real_dist_omni_ball[x][y][0]))+", "+str(int(real_dist_omni_ball[x][y][1]))+", "+str(int(real_polar_omni_ball[x][y][0]))+", "+str(int(real_polar_omni_ball[x][y][1]))+"}")
            file.write(", ")
        
        file.write("},\n")
        
        
    file.write("}")             
    file.close()
    
    print("File Saved!")
    return file 

def save_field_consts_file(values):

    
    file=open("config_field_consts.go",mode="w+")
    file.write("package main\n\n")
    
   
    file.write("const A = "+values["-F_A-"]+"\n")
    file.write("const B = "+values["-F_B-"]+"\n")
    file.write("const C = "+values["-F_C-"]+"\n")
    file.write("const D = "+values["-F_D-"]+"\n")
    file.write("const E = "+values["-F_E-"]+"\n")
    file.write("const F = "+values["-F_F-"]+"\n")
    file.write("const G = "+values["-F_G-"]+"\n")
    file.write("const H = "+values["-F_H-"]+"\n")
    file.write("const I = "+values["-F_I-"]+"\n")
    file.write("const J = "+values["-F_J-"]+"\n")
    file.write("const K = "+values["-F_K-"]+"\n")
    file.write("const L = "+values["-F_L-"]+"\n")
    file.write("const M = "+values["-F_M-"]+"\n")
    file.write("const N = "+values["-F_N-"]+"\n")
    file.write("const O = "+values["-F_O-"]+"\n")
    file.write("const P = "+values["-F_P-"]+"\n")
    file.write("const Q = "+values["-F_Q-"]+"\n")
           
    file.close()

    file=open("field_consts.txt",mode="w+")
    file.write("A = "+values["-F_A-"]+"\n")
    file.write("B = "+values["-F_B-"]+"\n")
    file.write("C = "+values["-F_C-"]+"\n")
    file.write("D = "+values["-F_D-"]+"\n")
    file.write("E = "+values["-F_E-"]+"\n")
    file.write("F = "+values["-F_F-"]+"\n")
    file.write("G = "+values["-F_G-"]+"\n")
    file.write("H = "+values["-F_H-"]+"\n")
    file.write("I = "+values["-F_I-"]+"\n")
    file.write("J = "+values["-F_J-"]+"\n")
    file.write("K = "+values["-F_K-"]+"\n")
    file.write("L = "+values["-F_L-"]+"\n")
    file.write("M = "+values["-F_M-"]+"\n")
    file.write("N = "+values["-F_N-"]+"\n")
    file.write("O = "+values["-F_O-"]+"\n")
    file.write("P = "+values["-F_P-"]+"\n")
    file.write("Q = "+values["-F_Q-"]+"\n")
           
    file.close()
    
    print("File Saved!")
    return file
 
def save_file():
    global code_omni
    global code_front
    global real_dist
    
    file=open("config.go",mode="w+")
    file.write("package main\n\n")
    for code_line in code_omni:
        #print(code_line)
        file.write("const "+code_line[0]+" = "+str(int(code_line[1]))+"\n")
    for code_line in code_front:
        #print(code_line)
        file.write("const "+code_line[0]+" = "+str(int(code_line[1]))+"\n")
    for code_line in code_warp:
        #print(code_line)
        file.write("const "+code_line[0]+" = "+str(int(code_line[1]))+"\n")
    
    
    file.write("\nvar real_coordenates = [480][480][2]int{\n")
    for x in range(0,240):
        file.write("{")
        for y in range(0,240):
            file.write("{"+str(int(real_dist[x][y][0]))+", "+str(int(real_dist[x][y][1]))+"}")
            file.write(", ")
        
        file.write("},\n")
        
        
    file.write("}")             
    file.close()
    
    print("File Saved!")
    return file
    


selected_object=0

def read_slider(values):
    global selected_object
    global code_omni
    global code_front
    global omnicap
    if(Calibration==0):
        code_omni[selected_object*6][1] = int(values["-MAXH-"])
        code_omni[selected_object*6+1][1] = int(values["-MINH-"])
        code_omni[selected_object*6+2][1] = int(values["-MAXS-"])
        code_omni[selected_object*6+3][1] = int(values["-MINS-"])
        code_omni[selected_object*6+4][1] = int(values["-MAXV-"])
        code_omni[selected_object*6+5][1]= int(values["-MINV-"])
        if( code_omni[36][1] != int(values["-EXP-"]) or code_omni[37][1] != int(values["-GAIN-"]) or code_omni[38][1] != int(values["-SAT-"])):
            code_omni[36][1] = int(values["-EXP-"])
            code_omni[37][1] = int(values["-GAIN-"])
            code_omni[38][1]= int(values["-SAT-"])
            omnicap.cam.ExposureTime.SetValue(float(code_omni[36][1])/10)
            omnicap.cam.Gain.SetValue(float(code_omni[37][1])/10)
            omnicap.cam.Saturation.SetValue(float(code_omni[38][1])/10)
            print("Config saved")
        code_omni[39][1] = int(values["-Max_Area-"])
        code_omni[40][1]= int(values["-Min_Area-"])



    if(Calibration==1):
        code_front[selected_object*6][1] = int(values["-MAXH-"])
        code_front[selected_object*6+1][1] = int(values["-MINH-"])
        code_front[selected_object*6+2][1] = int(values["-MAXS-"])
        code_front[selected_object*6+3][1] = int(values["-MINS-"])
        code_front[selected_object*6+4][1] = int(values["-MAXV-"])
        code_front[selected_object*6+5][1]= int(values["-MINV-"])


def update_sliders(window, values):
    global code_omni
    global code_front
    global selected_object
    if(Calibration==0):
        window["-MAXH-"].update(value = code_omni[selected_object*6][1])
        window["-MINH-"].update(value = code_omni[selected_object*6+1][1])
        window["-MAXS-"].update(value = code_omni[selected_object*6+2][1])
        window["-MINS-"].update(value = code_omni[selected_object*6+3][1])
        window["-MAXV-"].update(value = code_omni[selected_object*6+4][1])
        window["-MINV-"].update(value = code_omni[selected_object*6+5][1])
        window["-EXP-"].update(value = code_omni[36][1])
        window["-GAIN-"].update(value = code_omni[37][1])
        window["-SAT-"].update(value = code_omni[38][1])
        window["-Max_Area-"].update(value = code_omni[39][1])
        window["-Min_Area-"].update(value = code_omni[40][1])
    if(Calibration==1):
        window["-MAXH-"].update(value = code_front[selected_object*6][1])
        window["-MINH-"].update(value = code_front[selected_object*6+1][1])
        window["-MAXS-"].update(value = code_front[selected_object*6+2][1])
        window["-MINS-"].update(value = code_front[selected_object*6+3][1])
        window["-MAXV-"].update(value = code_front[selected_object*6+4][1])
        window["-MINV-"].update(value = code_front[selected_object*6+5][1])
    

Calibration=0
Source=1

def update_menu(window, values):
    global selected_object
    global Calibration
    global Source
    
    if(values=="Calibrate Omni"):
        window["-CALIBRATE-"].update("Omni")
        Calibration=0
    elif(values=="Calibrate Front"):
        window["-CALIBRATE-"].update("Front")
        Calibration=1
    elif(values=="Video"):
        window["-SOURCE-"].update("Video")
        Source=0
    elif(values=="Image"):
        window["-SOURCE-"].update("Image")
        Source=1
    elif(values=="Omni"):
        window["-SOURCE-"].update("Omni")
        Source=2
    elif(values=="Front"):
        window["-SOURCE-"].update("Front")
        Source=3
   
    


def Select_Object(window,event,values):
    global selected_object
    if(event=="-Ball-"):
        selected_object=0
        window.Element('-Ball-').Update("->Ball")
        window.Element('-Field-').Update("Field")
        window.Element('-Lines-').Update("Lines")
        window.Element('-Robot-').Update("Robot")
        window.Element('-Rshirt-').Update("Red Shirt")
        window.Element('-Bshirt-').Update("Blues shirt")

    elif(event=="-Field-"):
        selected_object=1
        window.Element('-Ball-').Update("Ball")
        window.Element('-Field-').Update("->Field")
        window.Element('-Lines-').Update("Lines")
        window.Element('-Robot-').Update("Robot")
        window.Element('-Rshirt-').Update("Red Shirt")
        window.Element('-Bshirt-').Update("Blues shirt")
    elif(event=="-Lines-"):
        selected_object=2
        window.Element('-Ball-').Update("Ball")
        window.Element('-Field-').Update("Field")
        window.Element('-Lines-').Update("->Lines")
        window.Element('-Robot-').Update("Robot")
        window.Element('-Rshirt-').Update("Red Shirt")
        window.Element('-Bshirt-').Update("Blues shirt")
    elif(event=="-Robot-"):
        selected_object=3
        window.Element('-Ball-').Update("Ball")
        window.Element('-Field-').Update("Field")
        window.Element('-Lines-').Update("Lines")
        window.Element('-Robot-').Update("->Robot")
        window.Element('-Rshirt-').Update("Red Shirt")
        window.Element('-Bshirt-').Update("Blues shirt")
    elif(event=="-Rshirt-"):
        selected_object=4
        window.Element('-Ball-').Update("Ball")
        window.Element('-Field-').Update("Field")
        window.Element('-Lines-').Update("Lines")
        window.Element('-Robot-').Update("Robot")
        window.Element('-Rshirt-').Update("->Red Shirt")
        window.Element('-Bshirt-').Update("Blues shirt")
    elif(event=="-Bshirt-"):
        selected_object=5
        window.Element('-Ball-').Update("Ball")
        window.Element('-Field-').Update("Field")
        window.Element('-Lines-').Update("Lines")
        window.Element('-Robot-').Update("Robot")
        window.Element('-Rshirt-').Update("Red Shirt")
        window.Element('-Bshirt-').Update("->Blues shirt")
    update_sliders(window,values)
    
nFrames=0
zeros = np.zeros((480,480,3), dtype=np.uint8)
def open_frame_source():
    global nFrames
    global videocap
    global imgcap
    global omnicap
    try:
    
        videocap = cv.VideoCapture('Video_field2.avi')
        nFrames = videocap.get(cv.CAP_PROP_FRAME_COUNT)
    except:
        videocap=zeros

    try:   
        imgcap = cv.imread(cv.samples.findFile("Robot5_bola_50.png"))
    except:
        imgcap = zeros
       
    omnicap = EasyPySpin.VideoCapture(0)
    
    try:
        omnicap.cam.PixelFormat.SetValue(PySpin.PixelFormat_RGB8Packed)
        print("Omni Camera Opened!")
    except:
        print("Can't Open Omni Camera... Trying Again...")
        try:
            omnicap = EasyPySpin.VideoCapture(0)
            omnicap.cam.PixelFormat.SetValue(PySpin.PixelFormat_RGB8Packed)
            print("Omni Camera Opened!")
        except:
            print("Can't Open Omni Camera... Verify Connection")

    #omnicap.cam.SaturationEnable.SetValue(True)
    #omnicap.set(cv.CAP_PROP_FPS,30)

    
        


now_frame = 0
def get_frame(frame_bckup=1):
    global now_frame
    global nFrames
    global videocap
    global imgcap
    global omnicap
    global Source
    #print(Source)
   
    if(Source==0):
        if(nFrames>=now_frame+3):#Endo of video
            now_frame+=1
            return videocap.read()
        else:
            return 1, frame_bckup
    elif(Source==1):
        return 1, imgcap
    elif(Source==2):
        ret,image_test=omnicap.read()
        #print(image_test)
        if(ret):
            dst = cv.cvtColor(image_test, cv.COLOR_BGR2RGB)
            return 1, dst#.reshape(480, 480, 3)
        else:
            return 1, frame_bckup
    else:
        return 1, frame_bckup
def restart_video():
    global nFrames
    global videocap

    videocap = cv.VideoCapture('Video_field2.avi')
    nFrames = videocap.get(cv.CAP_PROP_FRAME_COUNT)

# define the true objective function
def objective(x, a, b, c, d, e,f,g):
	return (a * x) + (b * x**2) + (c * x**3) + (d * x**4)  +(e * x**5)+(f * x**6)+ g
def calc_dist_omni(a,b,c,d,e,f,g):
    global real_dist_omni
    global real_polar_omni
    for x in range(0,480):
        for y in range(0,480):
            #print(x,y,"####################")
            angle = math.atan2(240-y, x-240)
            print(angle)
            dist = math.sqrt(((240-y) ** 2) +((x-240) ** 2))
            d_real=objective(dist, a, b, c, d, e,f,g)
            #print(dist,d_real)
            real_y = math.sin(angle) * d_real
            real_x = math.cos(angle) * d_real
            #print(real_x,real_y)
            real_polar_omni[x][y][0]=d_real
            real_polar_omni[x][y][1]=angle*(180/math.pi)
            real_dist_omni[x][y][0]=real_x
            real_dist_omni[x][y][1]=real_y
    #print(a,b,c,e,f,g)
real_dist_omni=np.zeros((480,480,2)) 
real_polar_omni=np.zeros((480,480,2)) 
a, b, c, d, e, f,g =0,0,0,0,0,0,0


def calc_dist_omni_ball(a_,b_,c_,d_,e_,f_,g_):
    global real_dist_omni_ball
    global real_polar_omni_ball
    for x in range(0,480):
        for y in range(0,480):
            #print(x,y,"####################")
            angle = math.atan2(239-y, x-239)
            #print(angle)
            dist = math.sqrt(((239-y) ** 2) +((x-239) ** 2))
            d_real=objective(dist, a_, b_, c_, d_, e_,f_,g_)
            #print(dist,d_real)
            real_y = math.sin(angle) * d_real
            real_x = math.cos(angle) * d_real
            #print(real_x,real_y)
            real_polar_omni_ball[x][y][0]=d_real
            real_polar_omni_ball[x][y][1]=angle*(180/math.pi)
            real_dist_omni_ball[x][y][0]=real_x
            real_dist_omni_ball[x][y][1]=real_y
    #print(a,b,c,e,f,g)
real_dist_omni_ball=np.zeros((480,480,2)) 
real_polar_omni_ball=np.zeros((480,480,2)) 
a_ball, b_ball, c_ball, d_ball, e_ball, f_ball,g_ball =0,0,0,0,0,0,0

menu_def = [
            ['File', [ 'Save', 'Exit']],
            ['Camera to calibrate', ['Calibrate Front', 'Calibrate Omni']],
            ['Source', ['Camera', ['Front', 'Omni'], 'File',['Image','Video']]],
            ['Help', 'About...']]
var_to_config=[
    [sg.Button("->Ball", size=(10, 1),button_color=('black', 'yellow'), key="-Ball-"),],
    [sg.Button("Field", size=(10, 1),button_color=('black', 'green'), key="-Field-"),],[sg.Button("Lines", size=(10, 1),button_color=('black',"white"), key="-Lines-"),],
    [sg.Button("Robot", size=(10, 1),button_color=('white', 'black'), key="-Robot-"),],[sg.Button("Red Shirt", size=(10, 1),button_color=('white', 'red'), key="-Rshirt-"),],
    [sg.Button("Blue Shirt", size=(10, 1),button_color=('white', 'blue'), key="-Bshirt-"),]]
hsv_config=[
        [sg.Text("Max. H",background_color="white",text_color="black"),
        sg.Slider(
            (0, 255),
            code_omni[selected_object*6][1],
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black" ,
            #color="black",
            key="-MAXH-",
        ),],
        [sg.Text("Min. H",background_color="white",text_color="black"),
        sg.Slider(
            (0, 255),
            code_omni[selected_object*6+1][1],
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-MINH-",
        ),],
        [sg.Text("Max. S",background_color="white",text_color="black"),
        sg.Slider(
            (0, 255),
            code_omni[selected_object*6+2][1],
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-MAXS-",
        ),],
        [sg.Text("Min. S",background_color="white",text_color="black"),
        sg.Slider(
            (0, 255),
            code_omni[selected_object*6+3][1],
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-MINS-",
        ),],
        [sg.Text("Max. V",background_color="white",text_color="black"),
        sg.Slider(
            (0, 255),
            code_omni[selected_object*6+4][1],
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-MAXV-",
        ),],
        [sg.Text("Min. V",background_color="white",text_color="black"),
        sg.Slider(
            (0, 255),
            code_omni[selected_object*6+5][1],
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-MINV-",
        ),],
        [sg.Text("Expo",background_color="white",text_color="black"),
        sg.Slider(
            (456, 327540),#Min 45.6 Max 32754.0
            460,
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-EXP-",
        ),],
        [sg.Text("Gain",background_color="white",text_color="black"),
        sg.Slider(
            (0, 239), # Min 0 Max 23.9 
            200,
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-GAIN-",
        ),],
        [sg.Text("Satur",background_color="white",text_color="black"),
        sg.Slider(
            (0, 3999), #Min 0 Max 399.9
            200,
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-SAT-",
        ),],
        ]
hsv_config2=[
        [sg.Text("Max. H",background_color="white",text_color="black"),
        sg.Slider(
            (0, 255),
            code_omni[selected_object*6][1],
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-MAXH2-",
        ),],
        [sg.Text("Min. H",background_color="white",text_color="black"),
        sg.Slider(
            (0, 255),
            code_omni[selected_object*6+1][1],
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-MINH2-",
        ),],
        [sg.Text("Max. S",background_color="white",text_color="black"),
        sg.Slider(
            (0, 255),
            code_omni[selected_object*6+2][1],
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-MAXS2-",
        ),],
        [sg.Text("Min. S",background_color="white",text_color="black"),
        sg.Slider(
            (0, 255),
            code_omni[selected_object*6+3][1],
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-MINS2-",
        ),],
        [sg.Text("Max. V",background_color="white",text_color="black"),
        sg.Slider(
            (0, 255),
            code_omni[selected_object*6+4][1],
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-MAXV2-",
        ),],
        [sg.Text("Min. V",background_color="white",text_color="black"),
        sg.Slider(
            (0, 255),
            code_omni[selected_object*6+5][1],
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-MINV2-",
        ),],
        [sg.Text("Offset X",background_color="white",text_color="black"),
        sg.Slider(
            (0, 480),
            code_omni[selected_object*6+5][1],
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-OFF2-",
        ),],]
warp_config=[
    [sg.Text("Warp",background_color="white",text_color="black"),
        sg.Slider(
            (0, 240),
            code_omni[selected_object*6+5][1],
            1,
            orientation="h",
            size=(110, 15),
            background_color="white",
            text_color="black",
            key="-WARP-",
        ),],]
field_config=[
    [sg.Text("A = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_A-"),sg.Text("B = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_B-"),sg.Text("C = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_C-")],
    [sg.Text("D = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_D-"),sg.Text("E = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_E-"),sg.Text("F = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_F-")],
    [sg.Text("G = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_G-"),sg.Text("H = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_H-"),sg.Text("I = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_I-")],
    [sg.Text("J = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_J-"),sg.Text("K = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_K-"),sg.Text("L = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_L-")],
    [sg.Text("M = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_M-"),sg.Text("N = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_N-"),sg.Text("O = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_O-")],
    [sg.Text("P = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_P-"),sg.Text("Q = ", size=(4, 1),text_color="black",background_color="white"),sg.InputText(size=(15,1),key="-F_Q-")],
    
    ]
#layout1 = [[, sg.Column(col2, element_justification='c')
#      , sg.Column(col3, element_justification='c'), sg.Column(col4, element_justification='c')]]
# Define the window layout
layout1 = [
    [sg.Text("Original", size=(68, 1), justification="center"),sg.Text("Filtred", size=(68, 1), justification="center")],
    [sg.Image(filename="", key="-IMAGE_ORI-"),sg.Image(filename="", key="-IMAGE-")],
    [sg.Column(var_to_config, element_justification='c' ),sg.Column(hsv_config, element_justification='c',background_color='white')],
    [sg.Button("Save Constants", size=(30, 1),button_color=('black', 'white'),key="-SAVE_CONST-")]]
layout2 = [
    [sg.Text("Original", size=(68, 1), justification="center"),sg.Text("Map", size=(68, 1), justification="center")],
    [sg.Image(filename="", key="-IMAGE_ORI2-"),sg.Image(filename="", key="-IMAGE2-")],
    [sg.Column(hsv_config2, element_justification='c',background_color='white' ),sg.Image(filename="", key="-IMAGE_PLOT-")],
    [ sg.Text("Equation: y = ax⁶ + bx⁵ + cx⁴ + dx³ + ex² + fx + g",size=(200,1),text_color="white",key="-Equation-"),],
    [sg.Button("Save Distances", size=(30, 1),button_color=('black', 'white'),key="-SAVE_DIST-")]]   
layout3 = [
    [sg.Text("Original", size=(68, 1), justification="center"),sg.Text("Warp", size=(68, 1), justification="center")],
    [sg.Image(filename="", key="-IMAGE_ORI3-"),sg.Image(filename="", key="-IMAGE3-")],
    [sg.Column(warp_config, element_justification='c',background_color='white' )],
    ]
layout4 = [
    [sg.Text("Field", size=(68, 1), justification="center")],
    [sg.Image(filename="./aux_file/Field_Original.png")],
    [sg.Column(field_config, element_justification='c',background_color='white' )],
    [sg.Button("Save Field Distances", size=(30, 1),button_color=('black', 'white'),key="-SAVE_FIELD-")],
    ]
layout5 = [
    [sg.Text("Original", size=(68, 1), justification="center")],
    [sg.Image(filename="", key="-IMAGE_CENTER-")],
    ]
layout6 = [
    [sg.Text("Original", size=(68, 1), justification="center"),sg.Text("Map", size=(68, 1), justification="center")],
    [sg.Image(filename="", key="-IMAGE_ORI4-"),sg.Image(filename="", key="-IMAGE4-"),sg.Image(filename="", key="-IMAGE_PLOT2-")],
     [sg.Text("Max. Area",background_color="white",text_color="black"),
        sg.Slider(
            (0, 4000),
            2000,
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-Max_Area-",
        ),],
        [sg.Text("Min. Area",background_color="white",text_color="black"),
        sg.Slider(
            (0, 4000),
            0,
            1,
            orientation="h",
            size=(90, 15),
            background_color="white",
            text_color="black",
            key="-Min_Area-",
        ),],
    [ sg.Text("Equation: y = ax⁶ + bx⁵ + cx⁴ + dx³ + ex² + fx + g",size=(200,1),text_color="white",key="-Equation_Ball-"),],
    [ sg.Text("Put Ball at "+ str(label_ball_calibration[0]/100)+" Meters to the center of the robot",size=(200,5),text_color="white",key="-Put_ball-"),],
    [sg.Button("Check", size=(30, 1),button_color=('black', 'white'),key="-SAVE_BALL-")],
    [sg.Button("Save Distances", size=(30, 1),button_color=('black', 'white'),key="-SAVE_DIST_BALL-")],
    [ sg.Text("X= 0 Y= 0 D= 0 A= 0",size=(200,1),text_color="white",key="-Coordenates_Ball-")],] 
      
tabgrp = [
    [sg.Menu(menu_def,text_color='black', font="SYSTEM_DEFAULT", pad=(10,10))],
        [sg.Text("Calibrate: ",text_color="black",background_color='firebrick4',font=('Any 15')),sg.Text("Omni",text_color="black",background_color='firebrick4',font=('Any 15'),key="-CALIBRATE-"),
        sg.Text("     Source: ",text_color="black",background_color='firebrick4',font=('Any 15')),sg.Text("Image",text_color="black",background_color='firebrick4',font=('Any 15'),key="-SOURCE-"),
        sg.Text("                    ",background_color='firebrick4'),
        sg.Button("    ", image_size=(30, 30), button_color=("firebrick4","firebrick4"),image_filename=image_pause, image_subsample=4, border_width=0,key="Pause"),
        sg.Button("    ", image_size=(40, 40), button_color=("firebrick4","firebrick4"),image_filename=image_play, image_subsample=4, border_width=0,key="Continue"),
        sg.Button("    ", image_size=(30, 30), button_color=("firebrick4","firebrick4"),image_filename=image_restart, image_subsample=4, border_width=0,key="Restart"),
        sg.Button("    ", image_size=(30, 30), button_color=("firebrick4","firebrick4"),image_filename=image_rec, image_subsample=4, border_width=0,key="-Record-"),
        sg.Button("    ", image_size=(30, 30), button_color=("firebrick4","firebrick4"),image_filename=image_save, image_subsample=4, border_width=0,key="Save Record"),
        sg.Text("  Name of video file to save: ",text_color="black",background_color='firebrick4'),
        sg.InputText("My_new.avi",size=(15,1),key="-SAVE_V-"),
        sg.Image(filename="./aux_file/logo_LAR.png",background_color="firebrick4", size=(300,50))],
        [sg.TabGroup([[
            sg.Tab('Center Calibration', layout5, title_color=('Black'), border_width =100,tooltip='Center Calibration', element_justification= 'center',key="-TAB_CENTER-"),
            sg.Tab('HSV Calibration', layout1, title_color=('Black'), border_width =100,tooltip='HSV Calibration', element_justification= 'center',key="-TAB_HSV-"),
            sg.Tab('Map Calibration', layout2,title_color='Blue', element_justification= 'center',key="-TAB_MAP-"),
            sg.Tab('Ball Calibration', layout6,title_color='Blue', element_justification= 'center',key="-TAB_BALL-"),
            sg.Tab('Warp', layout3,title_color='Black',tooltip='Warp', element_justification= 'center',key="-TAB_WARP-"),
            sg.Tab('Field Calibration', layout4, title_color=('Black'), border_width =100,tooltip='Field Calibration', element_justification= 'center',key="-TAB_FIELD-")
            
            ]],key='_TAB_GROUP_', enable_events=True,tab_location='centertop',title_color='white',background_color='firebrick4', tab_background_color='black',selected_title_color='black',selected_background_color='white', border_width=5)],
        ]  

def main():
    sg.theme("LightGreen")
    
   
    #print(code)
    
    print("code")

    
    # Create the window and show 
    window = sg.Window("LAR Calibration", tabgrp,background_color='firebrick4', location=(800, 400))
    
    event, values = window.read(timeout=20)
    #read_file(window)
    #read_front_consts_file(window)
    read_omni_consts_file(window)
    read_field_consts_file(window)
    
    open_frame_source()
    
   
    ret, frame_bckup = get_frame()
    update_sliders(window,values)
    
    now_frame=0
    Pause= False
    Record= False
    #FAZER RESET
    ball_index = 0
    x_array_ball = []
    x_array_ball.append(0)
    y_array_ball = []
    y_array_ball.append(0)
    global out
    #window["-MAXH2-"].update(value = 255)
    #window["-MINH2-"].update(value = 0)
    #window["-MAXS2-"].update(value = 255)
    #window["-MINS2-"].update(value = 0)
    #window["-MAXV2-"].update(value = 255)
    #window["-MINV2-"].update(value = 0)
    #window["-OFF2-"].update(value = 240)
   
    while True:
        
        if(not Pause):    
            ret,frame_ori=get_frame(frame_bckup)
        

        #height, width, number of channels in image
        #print(frame_ori)
        height = frame_ori.shape[0]
        width = frame_ori.shape[1]
        channels = frame_ori.shape[2]
        event, values = window.read(timeout=20)
        read_slider(values)
        Select_Object(window,event,values)
        update_menu(window, event)
        #update_sliders(window, values)
        
        
        if (event == "Exit" or event == sg.WIN_CLOSED) and  sg.popup_yes_no('Do you save?') == 'Yes':
            break
        elif event == "Save":
           file_w=save_file()
        elif event == "Calibrate Front" or event == "Calibrate Omni":
            update_sliders(window,values)
        elif event == "Pause":
            Pause= True
        elif event == "Continue":
            Pause= False
            #print(type(frame_ori))
        elif event == "Restart":
            restart_video()
        elif event == "-Record-":
            if(not Record):
                Record= True
                window["-Record-"].update(image_filename=image_recording,image_subsample=4)
                # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
                out = cv.VideoWriter(values["-SAVE_V-"],cv.VideoWriter_fourcc('M','J','P','G'), 10, (width,height))
        elif event == "Save Record":
            if Record:
                Record= False
                window["-Record-"].update(image_filename=image_rec,image_subsample=4)
                out.release()
        elif event == "-SAVE_DIST-":
            window["-SAVE_DIST-"].update("Saving....")
            if Calibration==0:
                calc_dist_omni(a,b,c,d,e,f,g)
                save_omni_tables_file()
            else:
                save_front_tables_file()
            window["-SAVE_DIST-"].update("Distances Saved!")
        elif event == "-SAVE_DIST_BALL-":
            window["-SAVE_DIST_BALL-"].update("Saving....")
            if Calibration==0:
                calc_dist_omni_ball(a_ball,b_ball,c_ball,d_ball,e_ball,f_ball,g_ball)
                save_omni_ball_tables_file()
            else:
                save_omni_ball_tables_file() 
            window["-SAVE_DIST_BALL-"].update("Distances Saved!")
        elif event == "-SAVE_CONST-":
            window["-SAVE_CONST-"].update("Saving....")
            #calc_dist(a,b,c,d,e,f,g)
            if Calibration==0:
                save_omni_consts_file()
            else:
                save_front_consts_file()
            window["-SAVE_CONST-"].update("Constants Saved!")
        elif event== "-SAVE_FIELD-":
            save_field_consts_file(values)
            save_map_field(values)
            save_map_field2(values)
        
        if(Record):
            out.write(frame_ori)

        frame = cv.cvtColor(frame_ori, cv.COLOR_BGR2HSV)
        #Process the selected TAB
        if values['_TAB_GROUP_'] == "-TAB_CENTER-":
            #  === Center  ===
            # Pixel values in original image
            frame_center=frame_ori.copy()
            cv.line(frame_center, (int(width/2),0), (int(width/2),height), (0,0,255), 1)
            cv.line(frame_center, (0,int(height/2)), (width,int(height/2)), (0,0,255), 1)
            cv.circle(frame_center, (int(width/2),int(height/2)), 5, (0,0,255), -1)
            centerbytes = cv.imencode(".png", frame_center)[1].tobytes()
            window["-IMAGE_CENTER-"].update(data=centerbytes)
        elif values['_TAB_GROUP_'] == "-TAB_MAP-":
            plot_func=np.zeros((300,240,3))
            frame_ori_dist=frame_ori.copy()
            x_array = []
            x_array.append(0)
            y_array = []
            y_array.append(0)
            x_array.append(13)
            y_array.append(8)
            x_array.append(19)
            y_array.append(12)
            x_array.append(25)
            y_array.append(15)
            frame_dist=cv.inRange(frame_ori, (values["-MINH2-"], values["-MINS2-"], values["-MINV2-"]), (values["-MAXH2-"], values["-MAXS2-"], values["-MAXV2-"])) #Tresh
            last=frame_dist[240][int(values["-OFF2-"])]
            count=0
            for y in range(240):
                if(frame_dist[240+y][int(values["-OFF2-"])]!=last and count<len(dists_calibration)):
                    cv.circle(frame_ori_dist, (int(values["-OFF2-"]),240+y), 3, (0,0,255), -1)
                    last=frame_dist[240+y][int(values["-OFF2-"])]
                    x_array.append(y)
                    y_array.append(dists_calibration[count])
                    cv.circle(plot_func,(y,int(299-(dists_calibration[count]*0.3))), 5, (255,0,0), -1)
                    #print(y,dists_calibration[count])
                    count+=1
                
                    
                  
            if(count>6):
            
                # curve fit
                #print(x_array)
                #print(y_array)
                popt, _ = curve_fit(objective, x_array, y_array)
                # summarize the parameter values
                a, b, c, d, e, f,g = popt
                print(min(x_array))
                x_line = arange(min(x_array), max(x_array), 1)
                y_line = objective(x_line, a, b, c, d, e, f,g)
                #print(x_line[5])
                #print(y_line[5])
                #print(objective(100, a, b, c, d, e, f,g))
                equation= "Equation: y = "+str(a)+"x⁶ + "+str(b)+"x⁵ + "+str(c)+"x⁴ + "+str(d)+"x³ + "+str(e)+"x² + "+str(f)+"x + "+str(g)
                window["-Equation-"].update(equation)
                
                for index,x in enumerate(x_line):
                    print(index)
                    if(0<=index<300 and 0<=x<300  ):
                        if 0>int(300-(y_line[index]*0.3)):
                            plot_func[299][x][2]=255
                        elif int(300-(y_line[index]*0.3))>=300:
                            plot_func[0][x][2]=255
                        else:
                            plot_func[int(299-(y_line[index]*0.3))][x][2]=255

                        plot_func[0][x][0]=255
                        plot_func[50][x][0]=255
                        plot_func[100][x][0]=255
                        plot_func[150][x][0]=255
                        plot_func[200][x][0]=255
                        plot_func[250][x][0]=255
                        plot_func[299][x][0]=255
            imgoribytes2=cv.imencode(".png",frame_ori_dist)[1].tobytes()
            imgbytes2 = cv.imencode(".png", frame_dist)[1].tobytes()
            plotbytes = cv.imencode(".png", plot_func)[1].tobytes()
            window["-IMAGE_ORI2-"].update(data=imgoribytes2)
            window["-IMAGE2-"].update(data=imgbytes2)
            window["-IMAGE_PLOT-"].update(data=plotbytes)
        #when ball calibration tab is open
        elif values['_TAB_GROUP_'] == "-TAB_BALL-":
            plot_func=np.zeros((300,240,3))
            frame_ori_dist=frame_ori.copy()
            

            #x_array.append(13)
            #y_array.append(8)
            #x_array.append(19)
            #y_array.append(12)
            #x_array.append(25)
            #y_array.append(15)
            #print(int(code_omni[0][1]))
            #print("S:"+str(code_omni[3][1])+"  "+ str(code_omni[2][1]))
            #print("V:"+str(code_omni[5][1])+"  "+ str(code_omni[4][1]))
            frame_dist=cv.inRange(frame, (code_omni[1][1],code_omni[3][1],code_omni[5][1]), (code_omni[0][1], code_omni[2][1], code_omni[4][1]))
            contours, _ = cv.findContours(frame_dist, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            try:
                best_contour=contours[0]
                best_dist=10000
                best_x=0
                #ellipse = cv.fitEllipse(contours[0])
                #print(ellipse)
                for i, contour in enumerate(contours):
                    #print(code_omni[39][1])
                    #print(code_omni[40][1])
                    if code_omni[40][1]<cv.contourArea(contour)<code_omni[39][1]:
                        
                            ellipse = cv.fitEllipse(contour)
                        #print(ellipse)
                    
                            frame_ori_dist = cv.circle(frame_ori_dist, (round(ellipse[0][0]),round(ellipse[0][1])), 4, (0,0,255), -1)
                            if abs(ellipse[0][0]-239) < best_dist :
                                best_contour = contours[i]
                                best_dist = abs(ellipse[0][0]-239)
                                best_y=239-ellipse[0][1]
            
                            
                #TODO:
                #RECALIBRAR BOLA
                #VERIFICAR DISTANCIAS
                #VERIFICAR O GO
                #OTIMIZAR O GO
                #OBSTACULOS
                #FAZER RESET
                        
                cv.drawContours(frame_ori_dist, [best_contour], 0, (0, 0, 0), 3)
                print(real_dist_omni_ball[round(ellipse[0][0])][round(ellipse[0][1])][0])
                coordenates_ball_str = "X= "+str(real_dist_omni_ball[round(ellipse[0][0])][round(ellipse[0][1])][0]) + "Y= "+str(real_dist_omni_ball[round(ellipse[0][0])][round(ellipse[0][1])][1]) + "D= "+str(real_polar_omni_ball[round(ellipse[0][0])][round(ellipse[0][1])][0]) + "A= "+str(real_polar_omni_ball[round(ellipse[0][0])][round(ellipse[0][1])][1])
                window["-Coordenates_Ball-"].update(coordenates_ball_str)
                #print(real_dist_omni_ball[ellipse[0][0]][ellipse[0][1]],real_polar_omni_ball[ellipse[0][0]][ellipse[0][1]])
                
            except:
                print("Sem Bola")
            
            
            if event == "-SAVE_BALL-":
                ball_index+=1
                if ball_index >= len(ball_calibration):
                    text="Ball Calibration is ready!"
                    window["-Put_ball-"].update(text)
                    print("X1", x_array_ball)
                    print("Y1",y_array_ball)
                    popt, _ = curve_fit(objective, x_array_ball, y_array_ball)
                    
                    # summarize the parameter values
                    a_ball, b_ball, c_ball, d_ball, e_ball, f_ball,g_ball = popt
                    #print(min(x_array))
                    window["-SAVE_DIST_BALL-"].update("Saving....")
                    if Calibration==0:
                        calc_dist_omni_ball(a_ball,b_ball,c_ball,d_ball,e_ball,f_ball,g_ball)
                        save_omni_ball_tables_file()
                    else:
                        save_omni_ball_tables_file() 
                    window["-SAVE_DIST_BALL-"].update("Distances Saved!")
                    x_line = arange(min(x_array_ball), max(x_array_ball), 1)
                    y_line = objective(x_line, a_ball, b_ball, c_ball, d_ball, e_ball, f_ball,g_ball)
                    #print(x_line)
                    #print(y_line)
                    #print(objective(100, a, b, c, d, e, f,g))
                    #Plot
                    equation= "Equation: y = "+str(a_ball)+"x⁶ + "+str(b_ball)+"x⁵ + "+str(c_ball)+"x⁴ + "+str(d_ball)+"x³ + "+str(e_ball)+"x² + "+str(f_ball)+"x + "+str(g_ball)
                    window["-Equation_Ball-"].update(equation)
                    '''for index,x in enumerate(x_line):
            
                        if(0<=index<300 and 0<=x<300  ):
                            if 0>int(300-(y_line[index]*0.3)):
                                plot_func[299][x][2]=255
                            elif int(300-(y_line[index]*0.3))>=300:
                                plot_func[0][x][2]=255
                            else:
                                plot_func[int(299-(y_line[index]*0.3))][x][2]=255

                            plot_func[0][x][0]=255
                            plot_func[50][x][0]=255
                            plot_func[100][x][0]=255
                            plot_func[150][x][0]=255
                            plot_func[200][x][0]=255
                            plot_func[250][x][0]=255
                            plot_func[299][x][0]=255'''

                else:
                    text="Put Ball at "+ str(label_ball_calibration[ball_index]/100)+" Meters to the center of the robot"
                    window["-Put_ball-"].update(text)
                    x_array_ball.append(-best_y) #Center of the ball
                    y_array_ball.append(ball_calibration[ball_index-1])
                    print("Best Y",-best_y,ball_calibration[ball_index-1])
                    
                    
            
                
            imgoribytes3=cv.imencode(".png",frame_ori_dist)[1].tobytes()
            imgbytes3 = cv.imencode(".png", frame_dist)[1].tobytes()
            plotbytes1 = cv.imencode(".png", plot_func)[1].tobytes()
            window["-IMAGE_ORI4-"].update(data=imgoribytes3)
            window["-IMAGE4-"].update(data=imgbytes3)
            window["-IMAGE_PLOT2-"].update(data=plotbytes1)
        
        elif values['_TAB_GROUP_'] == "-TAB_HSV-":        
            # === HSV Treshold ===
            frame=cv.inRange(frame, (values["-MINH-"], values["-MINS-"], values["-MINV-"]), (values["-MAXH-"], values["-MAXS-"], values["-MAXV-"])) #Tresh
            contours, hierarchy = cv.findContours(frame, cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE)
            #print("The Total Number of Contours in the Image = ")
            #command len used to calculate the number of contours in the image
            #try:
            #cv.drawContours(frame_ori, contours, -1,(0,255,0),3)
            #cv.drawContours(frame_ori, contours, -1,(0,255,0),3,hierarchy=0)
            imgbytes = cv.imencode(".png", frame)[1].tobytes()
            window["-IMAGE-"].update(data=imgbytes)
            #except:
            #    imgbytes = cv.imencode(".png", frame)[1].tobytes()
            #    window["-IMAGE-"].update(data=imgbytes)
            
            
        elif values['_TAB_GROUP_'] == "-TAB_WARP-":  
            #  === Warp  ===
            # Pixel values in original image
            frame_warped=frame_ori.copy()
            tl_point = [0,0]
            tr_point = [width,0]
            bl_point = [0,height]
            br_point = [width,height]
            original_points = np.float32([tl_point,tr_point,bl_point,br_point])
            tl_point_f = [0,0]
            tr_point_f = [width,0]
            bl_point_f = [0+values["-WARP-"],height]
            br_point_f = [width-values["-WARP-"],height]
            final_points = np.float32([tl_point_f,tr_point_f,bl_point_f,br_point_f])

            # perspective transform
            perspective_transform = cv.getPerspectiveTransform(original_points,final_points)
            frame_warped = cv.warpPerspective(frame_warped,perspective_transform,(width,height))
            code_warp[0][1]= bl_point_f[0]
            code_warp[1][1]= br_point_f[0] 
            imgbytes3 = cv.imencode(".png", frame_warped)[1].tobytes()
            window["-IMAGE3-"].update(data=imgbytes3)
        
        
        


        

       

        imgoribytes = cv.imencode(".png",frame_ori)[1].tobytes()
        window["-IMAGE_ORI-"].update(data=imgoribytes)
        window["-IMAGE_ORI3-"].update(data=imgoribytes)
      
    
    window.close()

main()
'''
terms = [
     1.3658494555919110e-001,
    -1.1393547368910101e-002,
     2.2561542336866879e-003,
    -2.0540857948124562e-005,
     6.8657323735489783e-008
]



# Functions
def get_camera(capture):
    """!Get device/file of capture.

    @param capture   Type of device. (Global Constants)

    @return  Capture device/file
    """
    if(capture==0):
        cap = cv.imread('14340982-2022-09-19-094032.png',1)
    elif(capture==1):
        cap = cv.VideoCapture('Video_field2.avi')
    elif(capture==2):
        cap = cv.imread('14340982-2022-09-19-094032.png',1)
    return cap
    

def get_frame(capture, cap):
    """!Get frame.

    @param cap   Type of device. (Global Constants)
    @param capture   Device/File.

    @return  Frame
    """
    if(capture==0):
        frame = cap
    elif(capture==1):
        ret, frame = cap.read()
    elif(capture==2):
        frame = cap
    return frame

def mouse_callback(event, x, y, flags, params):
    """!Print RGB and HSV pixel right clicked."""
    if event == 2:
    	#print(x,y)
        print(f"coords {x, y}, colors Blue- {camera[y, x, 0]} , Green- {camera[y, x, 1]}, Red- {camera[y, x, 2]} ")



def regress(x):
  t = 1
  r = 0
  for c in terms:
    r += c * t
    t *= x
  return r



def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
  return result
cap= get_camera(capture)
def main():
    first_time = 1
    """!Main Loop"""
    cv.namedWindow("Cam")
    cv.setMouseCallback("Cam", mouse_callback)
    while True:
        camera=get_frame(capture, cap) 
        
        
        #
        
        cv.imshow("Cam",camera)
        
        camera = cv.cvtColor(camera, cv.COLOR_BGR2HSV)
        #print("Feito7")
        
        size = 480, 480
        size_c = (363, 322 ,3)
        m = np.zeros(size, dtype=np.uint8)
        n = np.zeros(size, dtype=np.uint8)
        m_color = np.zeros(shape=size_c, dtype=np.uint8)
        
        #print(m_color.shape)
        size_robot_view = 80, 80
        real = np.zeros(size_robot_view, dtype=np.uint8)
        #print("Feito8")
        #for x in range(480):
        #    for y in range(1):
        #        if(camera[x][y][1]<120 and camera[x][y][2]>120 ):
        #            m[x][y]=255
        m = cv.inRange(camera, (0, 0, 90), (255, 100, 255)) #Linhas Brancas
        v = cv.inRange(camera, (70, 140, 0), (90, 255, 255)) #Campo Verde
        R = cv.inRange(camera, (0, 0, 0), (255, 200, 100)) #Robots
        contours, hierarchy = cv.findContours(R, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        circularity=0
        for cnt in contours:
            hull = cv.convexHull(cnt)
            
            area = cv.contourArea(hull)
            perimeter = cv.arcLength(hull,True)
            if(perimeter>50):
                circularity=(4*3.14*area)/(perimeter**2)
                print(circularity)
                if(circularity>0.50):
                    cv.drawContours(R, [hull], 0, (150,150,150), 3)
                    (x,y),radius = cv.minEnclosingCircle(cnt)
                    center = (int(x),int(y))
                    radius = int(radius)
                #cv.circle(R,center,radius,(155,155,155),2)
            #print(area)
            #if(area>300):
                #cv.drawContours(R, [cnt], 0, (150,150,150), 3)
        #cv.drawContours(R, contours, -1, (150,150,150), 3)
        cv.imshow("Robos",R)
        cv.imshow("Verde",v)
        mask = cv.bitwise_or(m, v)
        cv.imshow("Mask",mask)
        #ret, m = cv.threshold(camera[:][:][2], 170 , 255, cv.THRESH_BINARY)
        
        #cv.waitKey(0)
        #print(camera[0])
        white_point=False
        green_point=False
        real_x=0
        real_y=0
        #print("Feito11")
        m2=m.copy()
        milliseconds = int(time() * 1000)
        for x in range(0,480,5):
            for y in range(480):
                if(v[x][y]==255 and not green_point ):
                    green_point=True
                elif(not white_point and m[x][y]==255):
                    white_point=True
                    cordX=x
                    cordY=y
                elif(white_point and green_point and v[x][y]==255):
                    #print("Entrou")
                    white_point = False
                    green_point = False
                    ypoint = cordY + int((y - cordY) / 2)
                    n[x][ypoint] = 255
                    cv.circle(m2,(ypoint,x),3, 155, -1)
                    m[x][ypoint] = 155
                    angle = math.atan2(ypoint-240, x-240)
                    d = math.sqrt((ypoint-240)**2+(x-240)**2)
                    if(d>80):
                        real_d = regress(d)
                        real_y = math.sin(angle) * real_d + 40
                        real_x = math.cos(angle) * real_d + 40
                        #print(angle)

                        if(0<real_y<80 and 0<real_x<80):
                            #print(real_x)
                            #print(real_y)
                            real[int(real_x)][int(real_y)]=255
                #else:
                #    white_point=False
                #    green_point=True
            white_point=False
            green_point=False

        milliseconds = int(time() * 1000) -milliseconds

        #print("Feito9",milliseconds)
        
        for y in range(0,480,5):
            for x in range(480):
                
                if(v[x][y]==255 and not green_point ):
                    green_point=True
                elif(not white_point and m[x][y]==255):
                    white_point=True
                    cordX=x
                    cordY=y
                elif(white_point and green_point and v[x][y]==255):
                    green_point = False
                    white_point = False
                    xpoint = cordX + int((x-cordX)/2)
                    n[xpoint][y] = 255
                    cv.circle(m2,(y,xpoint),3, 155, -1)
                    angle = math.atan2(y-240, xpoint-240)
                    d = math.sqrt((y-240) ** 2 + (xpoint-240) ** 2)
                    if(d>80):
                        #print(d)
                        real_d = regress(d)
                        real_y = math.sin(angle) * real_d +40
                        real_x = math.cos(angle) * real_d +40
                        #print(angle)
                        #print(real_d)
                        #print(real_x)
                        #print(real_y)
                        if (0 < real_y < 80 and 0 < real_x < 80):

                            real[int(real_x)][int(real_y)] = 255
            white_point=False
            green_point=False    
        
        #print("Feito10")
        cv.imshow("Campo",m2)
        cv.imshow("Campo2",n)
        cv.imshow("Campo_real",real)

        template=real
        #cv.imshow("Cam",camera)

        img = cv.imread('Campo.png',0)
        img = rotate_image(img,0)
        img2 = img.copy()
        #template = cv.imread('Campo_temp3.png',0)
        #template = rotate_image(template,5)


        w, h = template.shape[::-1]
        # All the 6 methods for comparison in a list
        methods = ['cv.TM_CCOEFF']#['cv.TM_CCOEFF', 'cv.TM_CCORR','cv.TM_CCORR_NORMED']


        # Get coordenates
        for meth in methods:
            img = img2.copy()
            method = eval(meth)
            # Apply template Matching
            #print("Espera")
            res = cv.matchTemplate(img,template,method)
            #print("Feito")
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            #print("Feito2")
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            #print("Min:",min_loc)
            #print("Min:", max_loc)
            if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                top_left = (min_loc[0]+40), (min_loc[1]+40)
            else:
                top_left = (max_loc[0]+40), (max_loc[1]+40)
            #print("Top:",top_left)
            bottom_right = (top_left[0] , top_left[1])
            m_color = cv.merge([img, img, img])
            #print(m_color.shape)
            if(first_time):
                prev_statex=top_left[0]
                prev_statey=top_left[1]
                cv.circle(m_color,(prev_statex,prev_statey),3, (0,0,250), -1)
                first_time=False
            elif(abs(prev_statex-top_left[0])<10 and  abs(prev_statey-top_left[1])<10 ):
                prev_statex=int(prev_statex*0.5+top_left[0]*0.5)
                prev_statey=int(prev_statey*0.5+top_left[1]*0.5)
                cv.circle(m_color,(prev_statex,prev_statey),3, (0,0,250), -1)
            else:
                cv.circle(m_color,(prev_statex,prev_statey),3, (0,0,250), -1)

            #("Feito3")
            #print((top_left[0]+bottom_right[0])/2,(top_left[1]+bottom_right[1])/2)
            cv.imshow("Position",m_color)
            #plt.subplot(121),plt.imshow(res,cmap = 'gray')
            #plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            #plt.subplot(122),plt.imshow(img,cmap = 'gray',)
            #plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            #plt.suptitle(meth)
            #plt.pause(0.01)
            #print("Feito4")
            cv.waitKey(2)
            #print("Feito5")
    #plt.show(block=False)

main()




'''
