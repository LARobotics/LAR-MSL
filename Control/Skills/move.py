import cv2
import numpy as np
import math
import time
import Skills.PID as PID
import Skills.Atractor as Atractor
import Skills.Repeller as Repeller
#from mpc_controller_obs import MPCControllerFatropOBS

#Constants
#Kp_atack = 0.1
Kp_move = 0.25
#Ki_atack = 0.008
Ki_move = 0.0001
#Kd_atack = 0.000
Kd_move = 0.0001
outputLimit_PID_move = 10.000
Katracao_move = 5
#Kintensidade_atack = 0.422
Kintensidade_move = 0.0125
outputLimit_atractor_move = 40.000

# Move skill
move_atractor = Atractor.Atractor(Katracao_move, Kintensidade_move, outputLimit_atractor_move)
move_orientation = PID.PID(Kp_move, Ki_move, Kd_move, 0.05, outputLimit_PID_move)#, 100)
#MPC_Obs = MPCControllerFatropOBS(N=10, dt=0.05, numObstacles=15)

def convertToDistAng(pos_x,pos_y):
    dist = math.sqrt(pos_x**2+pos_y**2) 
    ang = math.degrees(np.arctan2(pos_y,pos_x))
    return dist, ang

def calculateDist(x,y):
    return math.sqrt(x**2+y**2) 

def calculate_distance(point1,point2=(0,0)):
    distance = math.sqrt((point2[0]-point1[0])*(point2[0]-point1[0]) + (point2[1]-point1[1])*(point2[1]-point1[1]))
    return distance

def calculateAngle(point):
    return math.degrees(math.atan2(point[1],point[0]))

def calculateAngle(point1,point2):
    return math.degrees(math.atan2(point1[1]-point2[1],point1[0]-point2[0]))

def skMove(data,delta_t):
    #global counter, ball_dist_prev, ball_ang_prev 
    linear_vel = 0
    angular_vel = 0
    direction =  0
  
    #BASESTATION
    target_x = data.baseStation.arg0*100
    target_y = data.baseStation.arg1*100
    or_ball = data.baseStation.arg2
    ball_x_bs = data.baseStation.arg3*100
    ball_y_bs = data.baseStation.arg4*100
    avoid_ball = data.baseStation.arg5 
    robotX = data.robot.x*100
    robotY = data.robot.y*100

    t_ang = 0

    #CDB
    ball_ang = data.ball.ang
    ball_dist = data.ball.dist
    opponents = data.opponents
    humans = data.humans
    friends = data.friends

    print("HUMANS -> ", len(humans))

    if ball_ang == 0 and data.ball.dist < 0 and or_ball == 0:
        _,ball_ang = convertToDistAng(ball_x_bs,ball_y_bs)

    compass = data.compass
    #ball_dist = data.ball.dist
  

    # if ball_ang == 0 and ball_dist < 0:       
    #     ball_dist, ball_ang = convertToDistAng(ball_x_bs-data.robot.x,ball_y_bs-data.robot.y)
    #target_dist, target_ang = convertToDistAng(target_x-robotX,target_y-robotY)
    target_dist = ball_dist
    target_ang = ball_ang
    #print("target dist-> "+str(target_dist))

    print("target ang " + str(target_ang))
    print("target dist " + str(target_dist))

    # if or_ball == 1:
    #     t_ang = target_ang
    #     target_ang =  target_ang - data.robot.ang

    #TESTE##
    #robot_ang = -60
    if or_ball == 1:
        t_ang = target_ang
        target_ang =  target_ang - data.robot.ang

    #print("target ang-> "+str(target_ang))
        #error_ang = data.robot.ang - target_ang#bussola - target_ang
    # print("error ang-> "+str(error_ang))
    # #target_ang = data.robot.ang

    while target_ang < -180:
        target_ang += 360
    while target_ang > 180:
        target_ang -= 360

    #print(f' X: {data.robot.x} Y: {data.robot.y} A: {data.robot.ang} tx {target_x} ty {target_y} td {target_dist} ta {target_ang}')
    print(f' X: {robotX} Y: {robotY} A: {data.robot.ang} tx {target_x} ty {target_y} td {target_dist} ta {target_ang}')


    #DEBUG#
    #target_dist = ball_dist
    #target_ang = ball_angl
    #print("target dist-> " + str(target_dist))
    #print("target ang-> " + str(target_ang)) 
    ##

    error_dist = target_dist
    if error_dist > 1000:
        error_dist = 1000
    linear_vel = move_atractor.Update(error_dist)
    if linear_vel > 40:
        linear_vel = 40
    if avoid_ball == 1:
        linear_vel = linear_vel/2


    if or_ball == 0:
        direction = target_ang
        error_ang = ball_ang
        angular_vel  = move_orientation.Update(error_ang,delta_t)
    else:
        direction = -target_ang
        error_ang = target_ang
        angular_vel = move_orientation.Update(error_ang,delta_t)
        if angular_vel > 5:
            linear_vel = 5

    print("or_ball-> " + str(or_ball))
    print("direction-> " + str(direction))
    print("error_ang-> " + str(error_ang))
    print("angular_vel->" + str(angular_vel))

    #linear_vel = 10

    # #DEBUG#
    #angular_vel  = 0#move_orientation.Update(error_ang,delta_t)
    # #angular_vel  = move_orientation.Update(error_ang,delta_t)
    # direction = target_ang
    offset = 25
    if len(data.humans) != 0:
        human_dist = data.humans[0].dist
        human_ang = data.humans[0].ang
        print("Human dist-> " + str(human_dist))
        print("Human ang-> " + str(human_ang)) 
        if human_dist +  offset < target_dist:
            desvio = t_ang - human_ang
            print("Desvio-> " + str(desvio))
            #desvio = 45  
            if desvio > 20:
                 desvio = 20
            if desvio < -20:
                 desvio = -20
            if or_ball == 1:
                    angular_vel = move_orientation.Update(target_ang,delta_t)
            # #angular_vel  = move_orientation.Update(desvio,delta_t)
            #print("Desvio-> " + str(desvio))
            direction = desvio
            linear_vel = 30
    
    
    # #if len(data.goalPosts) != 0 
    # if len(data.robots) != 0 or len(data.friends) != 0 or len(data.opponents) != 0 or avoid_ball == 1: #or len(data.humans):4
    #     if len(data.robots) != 0:
    #         robot_dist = data.robots[0].dist
    #         robot_ang = data.robots[0].ang
    #         print("robot dist-> " + str(robot_dist))
    #         print("robot ang-> " + str(robot_ang)) 
    #         if robot_dist +  offset < target_dist:
    #             desvio = t_ang - robot_ang
    #             # if desvio > 75:
    #             #     desvio = 75
    #             # if desvio < -75:
    #             #     desvio = -75
    #             if or_ball == 1:
    #                   angular_vel = move_orientation.Update(target_ang,delta_t)
    #             # #angular_vel  = move_orientation.Update(desvio,delta_t)
    #             #print("Desvio-> " + str(desvio))
    #             direction = desvio
    #             linear_vel = 5#25
    #     elif len(data.friends) != 0:
    #         friend_dist = data.friends[0].dist
    #         friend_ang = data.friends[0].ang
    #         #print("friend dist-> " + str(friend_dist))
    #         #print("friend ang-> " + str(friend_ang))
    #         if friend_dist +  offset < target_dist:
    #             desvio = t_ang - friend_ang
    #             if or_ball == 1:
    #                   angular_vel = move_orientation.Update(target_ang,delta_t)
    #             # if desvio > 75:
    #             #     desvio = 75
    #             # if desvio < -75:
    #             #     desvio = -75
    #             # #angular_vel  = move_orientation.Update(desvio,delta_t)
    #             #print("Desvio-> " + str(desvio))
    #             direction = desvio
    #             linear_vel = 25
        # if len(data.opponents) != 0:
        #     opponent_dist = data.opponents[0].dist
        #     opponent_ang = data.opponents[0].ang
        #     print("opponent dist-> " + str(opponent_dist))
        #     print("opponent ang-> " + str(opponent_ang))
        #     if opponent_dist +  offset < target_dist:
        #         desvio = t_ang - opponent_ang
        #         if or_ball == 1:
        #               angular_vel = move_orientation.Update(target_ang,delta_t)
        #         # if desvio > 75:
        #         #     desvio = 75
        #         # if desvio < -75:
        #         #     desvio = -75
        #         # #angular_vel  = move_orientation.Update(desvio,delta_t)
        #         #print("Desvio-> " + str(desvio))
        #         direction = desvio
        #         linear_vel = 25
        #if ball_dist > 0 and avoid_ball == 1:
        #     if ball_dist +  offset < target_dist:
        #         desvio = t_ang - ball_ang
        #         # if desvio > 75:
        #         #     desvio = 75
        #         # if desvio < -75:
        #         #     desvio = -75
        #         # #angular_vel  = move_orientation.Update(desvio,delta_t)
        #         #print("Desvio-> " + str(desvio))
        #         direction = desvio
        #         linear_vel = 25

    
    #linear_vel = 5  
    #angular_vel  = move_orientation.Update(ball_angl,delta_t) 
    #angular_vel = 0
    #direction = 0

    # print("Ang-> " +str(error_angl))
    # print("Dist->" +str(error_dist))
    # print("Ang vel-> " + str(angular_vel))
    # print("Lin vel-> " + str(linear_vel))
    # print("Dir vel-> " + str(direction))

    #direction = target_ang
    return linear_vel, direction, angular_vel
