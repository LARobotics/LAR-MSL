import cv2
import numpy as np
import math
import time
import Skills.PID as PID
import Skills.Atractor as Atractor

def skStop(data,delta_t): 
    linear_vel = 0
    angular_vel = 0
    direction =  0
  
    return linear_vel, direction, angular_vel
