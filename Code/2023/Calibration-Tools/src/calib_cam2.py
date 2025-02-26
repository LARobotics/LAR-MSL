#!/usr/bin/env python3
"""! @brief 1Calibration of the colors of the field."""
##
##
# @file calib_cam2.py
#
# @brief Example Python program with Doxygen style comments.
#
# @section description_doxygen_example Description
# Example Python program with Doxygen style comments.
#
# @section libraries_main Libraries/Modules
# - time standard library (https://docs.python.org/3/library/time.html)
#   - Access to sleep function.
# - sensors module (local)
#   - Access to Sensor and TempSensor classes.
#
# @section notes_doxygen_example Notes
# - Comments are Doxygen compatible.
#
# @section todo_doxygen_example TODO
# - None.
#
# @section author_doxygen_example Author(s)
# - Created by John Woolsey on 05/27/2020.
# - Modified by John Woolsey on 06/11/2020.
#
# Copyright (c) 2020 Woolsey Workshop.  All rights reserved.


# Imports
import cv2 as cv
import numpy as np
import math
from time import time
from matplotlib import pyplot as plt

# Global Constants
## The mode of capture; 0 = camera, 1 = video, 2 = image.
capture = 1 



# Functions
def mouse_callback(event, x, y, flags, params):
    """!Print RGB and HSV pixel right clicked."""
    if event == 2:
    	#print(x,y)
        print(f"coords {x, y}, colors Blue- {camera[y, x, 0]} , Green- {camera[y, x, 1]}, Red- {camera[y, x, 2]} ")

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

cv.namedWindow("Cam")
cv.setMouseCallback("Cam", mouse_callback)
while True:
   
    
    
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






