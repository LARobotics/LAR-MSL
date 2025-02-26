import time
import math
import numpy as np
import Skills.PID as PID
import Skills.Defend.place as place
import Skills.Defend.Block as block
from Skills.Defend import simple_block

from Config import *

# * FIELD CONSTANTS
A = 22 # [m]

# * CONFIG PLACE
ellipse_A = 900 # [m] Ellipse Width X
ellipse_B = 500   # [m] Ellipse Lenght Y

# * CONFIG BLOCK

# * UTILITY
def convertRelativeToAbsolute(xAbs, yAbs, xr, yr, alpha):
    absoluteValues = [0, 0, 0]
    
    # absoluteValues[0] = round(np.cos(np.radians(-alpha-90))*sxr-np.sin(np.radians(-alpha-90))*yr+xAbs, 2)
    # absoluteValues[1] = round(-np.sin(np.radians(-alpha-90))*xr-np.cos(np.radians(-alpha-90))*yr+yAbs, 2)
    absoluteValues0 = round(np.cos(np.radians(-alpha))*xr-np.sin(np.radians(-alpha))*yr+xAbs, 2)
    absoluteValues1 = round(np.sin(np.radians(-alpha))*xr+np.cos(np.radians(-alpha))*yr+yAbs, 2)
    #absoluteValues0 = round(np.cos(np.radians(-alpha-90))*xr-np.sin(np.radians(-alpha-90))*yr+xAbs, 2)
    #absoluteValues1 = round(-np.sin(np.radians(-alpha-90))*xr-np.cos(np.radians(-alpha-90))*yr+yAbs, 2)
    
    return absoluteValues0,absoluteValues1

def object2field(robot_position, robot_angle, relative_object_position):
    """
    Transforms the coordinates of an object from the robot's local frame to the global frame using numpy.

    Parameters:
    - robot_position: (x_r, y_r) representing the robot's global position
    - robot_angle: Robot's orientation in degrees (θ_r)
    - relative_object_position: (x_o', y_o') representing the object's position relative to the robot

    Returns:
    - global_position: (x_o, y_o) representing the object's global position
    """
    # Robot's global position and angle in radians
    x_r, y_r = robot_position
    theta_r = np.radians(robot_angle)

    # Relative object position as a column vector
    relative_position = np.array([[relative_object_position[0]], [relative_object_position[1]]])

    # Rotation matrix for transforming the local frame to the global frame
    rotation_matrix = np.array([[np.cos(theta_r), -np.sin(theta_r)], 
                                [np.sin(theta_r), np.cos(theta_r)]])

    # Perform rotation and then translation
    global_position = rotation_matrix @ relative_position + np.array([[x_r], [y_r]])
    #print(f'Object field Position: {global_position}')
    return global_position[0, 0], global_position[1, 0]

def field2goal(Fx, Fy):
    global A
    Gx = -Fy
    Gy = Fx + A/2
    return Gx, Gy

def goal2field(Gx, Gy):
    global A
    Fx = Gy-A/2
    Fy = -Gx
    return Fx, Fy
    
# * PID   
#linVel = PID.PID(20.0,0.00,0.00,0.05,10) # MAX: 70
#angVel = PID.PID(0.10,0.001,0.0003,0.05,15) # MAX 15
cur_x_acc = 0
cur_y_acc = 0
# * MAIN
def skDefend(data, dt):
    robot_y = data.robot.y
    robot_angle = data.robot.ang
    ball_angle = data.ball.ang
    ball_distance = data.ball.dist

    return simple_block.simple_block(robot_y, robot_angle, ball_angle, ball_distance)

    global cur_x_acc, cur_y_acc
    blockk = True
    a = 0.01
    ball_x_rel = data.ball.x / 100   # [cm] to [m]
    ball_y_rel = data.ball.y / 100   # [cm] to [m]
    ball_d = data.ball.dist / 100    # [cm] to [m]
    ball_a = data.ball.ang          # [deg]
    angle  = data.robot.ang         # [deg]
    # Robot Absolute Position
    cur_x_field = data.robot.x # [m]
    cur_y_field = data.robot.y # [m]
    Print(f"RobotField: {cur_x_field:.2f} {cur_y_field:.2f} {angle:.1f}")
    # Robot Relative Position to the Goal. Field 2 Goal
    cur_x, cur_y = field2goal(cur_x_field,cur_y_field)
    cur_x_acc = cur_x * a + (1-a)*cur_x_acc
    cur_y_acc = cur_y * a + (1-a)*cur_y_acc
    Print(f"RobotGoal: {cur_x_acc:.2f} {cur_y_acc:.2f}")
    
    # If no Ball detected use BaseStation Estimationi
    #Print(f'BallRelative: {ball_x_rel} {ball_y_rel}')
    if ball_d <= 0:
        ball_x_field = data.baseStation.arg0
        ball_y_field = data.baseStation.arg1
    else:
        # Ball Absolute Position. Robot 2 Field
        #ball_x_field, ball_y_field = convertRelativeToAbsolute(cur_x_field, cur_y_field, ball_x_rel, ball_y_rel, angle)
        ball_x_field, ball_y_field = object2field((cur_x_field,cur_y_field),angle,(ball_x_rel,ball_y_rel))
    #ball_x_field = -9
    #ball_y_field = 1.5

    #Print(f"BallField CALC: {ball_x_field} {ball_y_field}")    
    #ball_x_field = -9#round(np.cos(np.radians(-angle))*ball_x_rel-np.sin(np.radians(-angle))*ball_y_rel+cur_x_field, 2)
    #ball_y_field = -1.5#round(np.sin(np.radians(-angle))*ball_x_rel+np.cos(np.radians(-angle))*ball_y_rel+cur_y_field, 2)
    Print(f"BallField: {ball_x_field:.2f} {ball_y_field:.2f}")
    # Ball Relative Position to the Goal. Field 2 Goal
    ball_x, ball_y = field2goal(ball_x_field, ball_y_field)
    ball_x = ball_x *1000   # [m] 2 [mm] for place algorithm
    ball_y = ball_y *1000   # [m] 2 [mm]
    ball_d_goal = math.sqrt(math.pow(ball_x,2)+math.pow(ball_y,2))
    ball_a_goal = np.rad2deg(math.atan2(ball_x,ball_y))
    Print(f"BallGoal: {ball_x:.2f} {ball_y:.2f} | {ball_d_goal:.0f} {ball_a_goal:.1f}")

    ### * Desired Pose: Place()
    ##Print("🚧 Place.")
    ###//des_x, des_y, des_angle = Skills.place.gk_place(ellipse_A,ellipse_B, ball_x, ball_y)
    ##des_x, des_y, des_angle = place.gk_place(ellipse_A,ellipse_B, ball_x, ball_y)
    ##des_angle = -np.rad2deg(des_angle)
    ##Print(f"DESIRED GOAL: des_x {round(des_x,3)}; des_y {round(des_y,3)}; des_a {round(des_angle,2)}")
    ### * Goal 2 Field Reference
    ##des_x_field, des_y_field = goal2field(des_x/1000, des_y/1000)
    ##Print(f"DESIRED FIELD: des_x {round(des_x_field,3)}; des_y {round(des_y_field,3)}; des_a {round(des_angle,3)}")
    # * Desired Pose: Block()
    Print("🚧 Block.")
    des_x, des_y = block.skill_block(ballAngle=ball_a_goal,ballDist=ball_d_goal)
    des_angle = ball_a
    Print(f"DESIRED GOAL: des_x {round(des_x,3)}; des_y {round(des_y,3)}; des_a {round(des_angle,2)}")
    # * Goal 2 Field Reference
    des_x_field, des_y_field = goal2field(des_x/1000, des_y/1000)
    if des_y_field < -A/2:
        des_y_field = -A/2
    Print(f"DESIRED FIELD: des_x {round(des_x_field,3)}; des_y {round(des_y_field,3)}; des_a {round(des_angle,3)}")

    # * Delta Pose
    dx = des_x_field-cur_x_field
    dy = des_y_field-cur_y_field
    dxy = math.sqrt(math.pow(dx,2) + math.pow(dy,2))
    da = des_angle - angle
    if blockk == True:
        da = des_angle
    Print(f"DELTA: dx {round(dx,3)}; dy {round(dy,3)}; da {round(da,3)}")
    
    # Delta Time
    #? Use the dt from FSM

    # * Control PLACE
    #linear_vel = 0.1 * dxy
    direction = np.rad2deg(math.atan2(dy,dx))-angle
    linear_vel = 20*dxy #linVel.Update(dxy,dt)  
    angular_vel = 0.11*da#angVel.Update(da,dt)
    #angular_vel = 0.15*da

    # * Control BLOCK
    if blockk:
        direction = np.rad2deg(math.atan2(dy,dx))-angle
        linear_vel = 30*dxy #linVel.Update(dxy,dt)  
        angular_vel = 0.20*da#angVel.Update(da,dt)

    # * Show
    Print(f"Kinematics: l {round(linear_vel,3)}; o {round(direction,3)}; w {round(angular_vel,3)}")
    return linear_vel, direction, angular_vel, des_x_field, des_y_field, des_angle # desired XYA only for representation in basestation