import time
import math
import numpy as np
import Skills.PID
import Skills.Defend.place as place

class kinematics:
    def __init__(self, kp_lin:float, ki_lin:float, kd_lin:float,limit_lin:int,kp_ang:float, ki_ang:float, kd_ang:float,limit_ang:int, kp_ori:float, ki_ori:float, kd_ori:float, limit_ori:int):
        self.linVel = Skills.PID.PID(kp_lin, ki_lin, kd_lin, 0.05, limit_lin)
        self.direct = Skills.PID.PID(kp_ori, ki_ori, kd_ori, 0.05, limit_ori)
        self.angVel = Skills.PID.PID(kp_ang, ki_ang, kd_ang, 0.05, limit_ang)

# * UTILITY
def convertRelativeToAbsolute(xAbs, yAbs, xr, yr, alpha):
    absoluteValues = [0, 0, 0]
    
    # absoluteValues[0] = round(np.cos(np.radians(-alpha-90))*sxr-np.sin(np.radians(-alpha-90))*yr+xAbs, 2)
    # absoluteValues[1] = round(-np.sin(np.radians(-alpha-90))*xr-np.cos(np.radians(-alpha-90))*yr+yAbs, 2)
    absoluteValues0 = round(np.cos(np.radians(-alpha))*xr-np.sin(np.radians(-alpha))*yr+xAbs, 2)
    absoluteValues1 = round(np.sin(np.radians(-alpha))*xr+np.cos(np.radians(-alpha))*yr+yAbs, 2)
    return absoluteValues0,absoluteValues1

# * CONFIG PLACE
ellipse_A = 900 # Ellipse Width X
ellipse_B = 500 # Ellipse Lenght Y
# PID   
#place_kin= kinematics(1,0,0,100, #?
#                    0,0,0,360,  #?
#                    0,0,0,100)  #?
kp_place = 0.01  #?
ki_place = 0.003    #?
kd_place = 0.003    #?
outputLimit_place = 10.0
PID_place_angle = Skills.PID.PID(kp_place, ki_place, kd_place, 0.05, outputLimit_place)
#Kp_place, Ki_place, Kd_place, outputLimit_PID_place = 0.25, 0.01, 0.006, 10.0
#place_orientation = Skills.PID.PID(Kp_place, Ki_place, Kd_place, 0.05, outputLimit_PID_place)
kp_place_dist = 10  #? 0.9
ki_place_dist = 0.0    #?
kd_place_dist = 0.00    #?
outputLimit_place_dist = 15.0
PID_place_dist = Skills.PID.PID(kp_place_dist, ki_place_dist, kd_place_dist, 0.05, outputLimit_place_dist)

# * CONFIG DEFEND
kp_def_angular = 0.25
kp__def_linear = 0.25
def defend(point):
    x, y = point
    direction = np.arctan2(y, x)
    linear_velocity = kp__def_linear * np.sqrt(x**2 + y**2)
    ang_velocity = kp_def_angular * direction
    return linear_velocity, ang_velocity, direction 

def skDefend(data,dt):
    ball_x_rel = data.ball.x * 10   # [cm] to [mm]
    ball_y_rel = data.ball.y * 10   # [cm] to [mm]
    ball_d = data.ball.dist * 10    # [cm] to [mm]
    ball_a = data.ball.ang          # [deg]
    angle  = data.robot.ang           # [deg]
    #errI = 0
    # Robot Absolute Position
    cur_x_field = data.robot.x * 1000 # [m] to [mm]
    cur_y_field = data.robot.y * 1000 # [m] to [mm]
    print(f"RobotField: {cur_x_field} {cur_y_field} {angle}")
    # Robot Relative Position to the Goal. Field 2 Goal
    cur_x = -cur_y_field
    cur_y = cur_x_field + 22000/2 #[mm] #! FIX Get Field_Lenght/2
    #print(f"RobotGoal: {cur_x} {cur_y}")

    # Ball Absolute Position. Robot 2 Field
    #def convertRelativeToAbsolute(xAbs, yAbs, xr, yr, alpha):
    ball_x_field = round(np.cos(np.radians(-angle))*ball_x_rel-np.sin(np.radians(-angle))*ball_y_rel+cur_x_field, 2)
    ball_y_field = round(np.sin(np.radians(-angle))*ball_x_rel+np.cos(np.radians(-angle))*ball_y_rel+cur_y_field, 2)
    # print(f"BallField: {ball_x_field} {ball_y_field}")
    # Ball Relative Position to the Goal. Field 2 Goal
    ball_x = -ball_y_field              #[m]
    #ball_y = ball_x_field + 18000/2    #[m] #! FIX Get Field_Lenght/2
    ball_y = ball_x_field + 22000/2     #[m]
    #print(f"BallGoal: {ball_x} {ball_y}")
    # TODO Kick Detection # Remate Enquadrado
    #remate = data.intersection_point
    remate = 0 #! Replace with kick_Detection
    overwrite = 1
    if (overwrite):
        print(f"<<Overwrite>>")
    # Konst
        FIELD_LENGHT = 22    # [m]
        FIELD_WIDTH = 14     # [m] #TODO GET Real Value
        GOAL_WIDTH = 0.8*2     # [m] #something small than the goal
        ball_y = data.ball.y/100     # [cm] 2 [m]
        ball_x = data.ball.x/100
        ball_a = data.ball.ang      # [deg]
        ball_d = data.ball.dist     # [cm] 2 [m]
        robot_x = data.robot.x
        robot_y = data.robot.y
        robot_a = data.robot.ang
        
    # Desired
    # TODO BALL from DET Tra - Relative 2 Abs
        #print(f"ball_d:{ball_d}")
        if ball_d <= 0:
            ball_x = data.baseStation.arg0  # [m]
            ball_y = data.baseStation.arg1  # [m]
            print(f"Ball BS: {ball_x} {ball_y}")
        else:
            #print(f"Before BallField: {ball_x} {ball_y}")
            ball_x, ball_y = convertRelativeToAbsolute(robot_x,robot_y,ball_x,ball_y, robot_a) #robot_x, robot_y
            print(f"After BallField: {ball_x} {ball_y}")
            
        #//convertRelativeToAbsolute(robot_x, robot_y, ball_x, ball_y, robot_a)
        print((ball_y / (FIELD_WIDTH/2))*GOAL_WIDTH/2)
        #// print(f"%{(ball_y / (FIELD_WIDTH/2/1000))}")
        #des_k_y = (ball_y / (FIELD_WIDTH/2/1000))*GOAL_WIDTH/2
        des_k_y = (ball_y / (FIELD_WIDTH/2))*GOAL_WIDTH/2
        des_k_x = 0.2 - FIELD_LENGHT/2

    # Error
        da = np.rad2deg(math.atan2(ball_y-des_k_y, ball_x-des_k_x))

        dx = des_k_x - data.robot.x
        dy = des_k_y - data.robot.y
        dxy = math.sqrt(dx**2 + dy**2)
    # Control
        angular_vel = PID_place_angle.Update(da,dt) 
        # direction = np.rad2deg(math.atan2(robot_y-des_k_y, robot_x-des_k_x))+robot_a
        direction = np.rad2deg(math.atan2(des_k_y-robot_y, des_k_x-robot_x))-robot_a
        while direction > 180:
            direction -= 360
        while direction < -180:
            direction += 360
        print(f"SIN:{math.sin(np.deg2rad(direction+robot_a))}")
        linear_vel = np.clip(abs(math.sin(np.deg2rad(direction+robot_a))*PID_place_dist.Update(dxy,dt)), 0, 15)
        
         #// place_kin.direct.Update(da,dt)
    # Feedback
        des_x_field = des_k_x
        des_y_field = des_k_y
        #if ball_d <= 0:
        #da = math.atan2(ball_y-des_y_field/1000,ball_x-des_x_field/1000)
            #print(f"Ball BS: {ball_x};{ball_y}")
        des_angle = da
        print(f"CURRENT: {data.robot.x};{data.robot.y}")
        print(f"DESIRED: {des_x_field};{des_y_field};{da} ")
    else:

        if(remate):
            print("Remate!")
            # Ball Trajectory Intersection with Goal Plane
            linear_vel, direction, angular_vel = defend(remate)
        else:
            print("🚧 Just Place.")
            if ball_d <= 0:
                ball_x = data.baseStation.arg0
                ball_y = data.baseStation.arg1
            # Desired Pose: Place()
            #//des_x, des_y, des_angle = Skills.place.gk_place(ellipse_A,ellipse_B, ball_x, ball_y)
            des_x, des_y, des_angle = place.gk_place(ellipse_A,ellipse_B, ball_x, ball_y)
            des_angle = np.rad2deg(des_angle)
            print(f"DESIRED GOAL: des_x {round(des_x,2)}; des_y {round(des_y,2)}; des_a {round(des_angle,2)}")
        #! OVERWRITE - TRY to use absolute location for error
            des_x_field = -22000/2 + des_y #! FIX Get Field_Lenght/2
            des_y_field = -des_x 
            print(f"DESIRED FIELD: des_x {des_x_field}; des_y {des_y_field}; des_a {des_angle}")

            # Delta Pose
            dx = des_x-cur_x
            dy = des_y-cur_y
            dxy = math.sqrt(math.pow(dx,2) + math.pow(dy,2))
        #! OVERWRITE - TRY to use absolute location for error
            dx = des_x_field-cur_x_field
            dy = des_y_field-cur_y_field
            dxy = math.sqrt(math.pow(dx,2) + math.pow(dy,2))
            
            # ! DEBUG
            #des_angle = ball_a
            da = des_angle - angle
            
            print(f"DELTA: dx {dx}; dy {dy}; da {da}")
            #? Use the dt from FSM
            # Delta Time
            #//cur_time = time.time()
            #//dt = old_time - cur_time 
            #//old_time = cur_time
            #print(f"CUR_POS: {cur_x}; {cur_y}; {angle}")
            # PID
            angular_vel = PID_place_angle.Update(da,dt) 
            linear_vel = PID_place_dist.Update(dxy,dt)
            direction = np.rad2deg(math.atan2(des_y,-des_x)) #// place_kin.direct.Update(da,dt)
            if direction <= -180:
                direction = -180
            # Desired Robot Absolute Position. Goal 2 Field 
            des_x_field = -22000/2 + des_y #! FIX Get Field_Lenght/2
            des_y_field = -des_x 
            #direction = np.rad2deg(math.atan2(des_y_field,des_x_field)) #/
            #angular_vel = -(da * 10 + errI * 0.5)
    #        print(f"da:{da}")

            #//direction = Skills.PID.PID.Update(da,dt)
            print(f"DESIRED: {des_x_field/1000};{des_y_field/1000}")
                    
    print(f"Kinematics: {linear_vel}; {direction}; {angular_vel}")
    return linear_vel, direction, angular_vel, des_x_field, des_y_field, des_angle # desired XYA only for representation in basestation

# IPCom.Handler.ToSend.linear_vel = int(linear_vel)   # 0:100
# IPCom.Handler.ToSend.angular_vel = int(angular_vel) # -100:100
# IPCom.Handler.ToSend.direction = int(da)     # -360:360

#linear_vel = place_kin.linVel.Update(dxy,dt)
#angular_vel = place_kin.angVel.Update(da,dt)
       