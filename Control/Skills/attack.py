import cv2
import numpy as np
import math
import time
import Skills.PID as PID
import Skills.Atractor as Atractor

#Constants
Kp_atack = 0.150
Ki_atack = 0.001
Kd_atack = 0.001
# Kp_atack = 0.250
# Ki_atack = 0.01
# Kd_atack = 0.006
outputLimit_PID_atack = 10.000
Kp_atack_vel = 1
Ki_atack_vel = 0.000
Kd_atack_vel = 0.200
outputLimit_PID_atack_vel = 40.000
#Kp_atack = 0.25

# Katracao_atack = 5
# Kintensidade_atack = 0.025
Katracao_atack = 5
Kintensidade_atack = 0.0125
outputLimit_atractor_atack = 40.000

# Atack skill
atack_atractor = Atractor.Atractor(Katracao_atack, Kintensidade_atack, outputLimit_atractor_atack)
atack_orientation = PID.PID(Kp_atack, Ki_atack, Kd_atack, 0.05, outputLimit_PID_atack)#, 100)
atack_vel = PID.PID(Kp_atack_vel, Ki_atack_vel, Kd_atack_vel, 0.05, outputLimit_PID_atack_vel)#, 100)

#Counter time not see ball
counter = 0

ball_dist_prev = 0
ball_angle_prev = 0

def convertToDistAng(pos_x,pos_y):
    dist = math.sqrt(pos_x**2+pos_y**2) 
    ang = math.degrees(np.arctan2(pos_y,pos_x))
    return dist, ang

def skAttack(data,delta_t):
    #global counter, ball_dist_prev, ball_angle_prev 
    linear_vel = 0
    angular_vel = 0
    direction =  0

    ball_mov = 1 #data.baseStation.arg5

    if data.ball.ang == 0 and data.ball.dist < 0:
        ball_angle, ball_dist = convertToDistAng(data.baseStation.arg0, data.baseStation.arg1)
    else:
        ball_angle = data.ball.ang
        ball_dist = data.ball.dist

    error_dist = ball_dist
    error_angle = ball_angle
    
    # ball_x_bs = data.baseStation.arg0
    # ball_y_bs = data.baseStation.arg1
    # ball_mov = data.baseStation.arg5

    # ball_angle = data.ball.ang
    # ball_dist = data.ball.dist
    
    # error_dist = ball_dist
    # error_angle = ball_angle
    
    # if ball_angle == 0 and ball_dist < 0:
    #     ball_bs_dist, ball_bs_ang = convertToDistAng(ball_x_bs,ball_y_bs)
    #     error_dist = ball_bs_dist
    #     error_angle = ball_bs_ang

    if error_dist > 1000:
        error_dist = 1000
    linear_vel = atack_atractor.Update(error_dist*1.25) #+ 10
    if ball_mov == 1 and linear_vel > 15:
        linear_vel = 15
    # if ball_mov == 1 and ball_dist < 150:
    #     linear_vel = linear_vel + 10
    #linear_vel = atack_vel.Update(error_dist,delta_t) 
    #if slow == 1:
    #    if ball_dist < 100 and linear_vel > 5:
    #        linear_vel = 5
    if data.stateBall == 2:# and ball_mov == 0:
        linear_vel = 0
    
    
    angular_vel  = atack_orientation.Update(error_angle,delta_t)
    
    if data.stateBall == 1:
        linear_vel = 0
        angular_vel = 0


    #direction = error_angle

    #if ball_dist < 100:
    #    direction = error_angle

    #if abs(ball_dist) < 5:e
    #    angular_vel = 0

    # if ball_angle == 0 and ball_dist < 0:
    #     counter = counter + 1
    # elif ball_angle == 0 and ball_dist < 0 and counter == 20:
    #     counter = 0
    #     linear_vel = 0
    #     angular_vel = 0


    # if ball_dist > 0:
    #     ball_dist_prev = ball_dist
    #     ball_angle_prev =  ball_angle

    #linear_vel = 0
    #angular_vel = 0
    print("Ang-> " +str(error_angle))
    print("Dist->" +str(error_dist))
    print("Ang vel-> " + str(angular_vel))
    print("Lin vel-> " + str(linear_vel))

    return linear_vel, direction, angular_vel

#    print("C," + str(linear_vel) + ',' + str(direction) + ',' + str(angular_vel) + ',' + str(distance))# * distance_scalar * np.cos(np.deg2rad(angle))))
