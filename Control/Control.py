from Config import Print, FREQUENCY, STOP, MOVE, ATTACK, KICK, RECEIVE, COVER, DEFEND, CONTROL
import IPCom
import time
import atexit

import math
import Skills.Atractor as Atractor
import Skills.PID as PID
import time
import numpy as np
import Skills.receive as receive
import cv2
import Skills.attack as attack
import Skills.defend as defend
import Skills.kick as kick
import Skills.cover as cover
import Skills.move as move
import Skills.stop as stop
from other_tests.newController import RobotController

# _robotController_ = RobotController(max_acceleration=1, max_angular_velocity=0.1, attenuation_factor_velocity_plus=13, attenuation_factor_velocity_minus=13, attenuation_factor_angular = 13)


P = 1000
I = 500
D = 0
Kl = 900
S = 5
Attenuation_Ang, Attenuation_Vel_minus, Attenuation_Vel_plus, min_value_ang, MAX_VEL = 8, 50, 50, 15, 60
values = [P, I, D, Kl, S, Attenuation_Ang, Attenuation_Vel_minus, Attenuation_Vel_plus, min_value_ang, MAX_VEL]

_robot_ = RobotController(max_acceleration=8, max_angular_velocity=20, attenuation_factor_velocity_minus=Attenuation_Vel_minus, attenuation_factor_velocity_plus=Attenuation_Vel_plus, attenuation_factor_angular = 360)

#Ki_atack = 0.008
#Kd_atack = 0.000
#outputLimit_PID_atack = 15.000
#Katracao_atack = 1.126
#Kintensidade_atack = 0.422
#outputLimit_atractor_atack = 10.000
## Atack skill
#atack_atractor = Atractor.Atractor(Katracao_atack, Kintensidade_atack, outputLimit_atractor_atack)
#atack_orientation = PID.PID(Kp_atack, Ki_atack, Kd_atack, 0.05, outputLimit_PID_atack)#, 100)


Kp_kick = 0.195
Ki_kick = 0.106
Kd_kick = 0.054
outputLimit_PID_kick = 16.300
Katracao_kick = 0.000
Kintensidade_kick = 0.000
outputLimit_atractor_kick = 0.000
# Kick skill
kick_orientation = PID.PID(Kp_kick, Ki_kick, Kd_kick, 0.05, outputLimit_PID_kick)#, 100)


# kp_place_lin = 1
# ki_place_lin = 0.0
# kd_place_lin = 0.0
# outputLimit_PID_place = 1 # m/s ????
# place_lin_vel = Pid.Pid(PID_place.kp_lin, PID_place.ki_lin, PID_place.kd_lin, PID_place.output_limit_lin, outputLimit_PID_place)
# kp_place = 1
# ki_place = 0.0
# kd_place = 0.0
# outputLimit_PID_place = 1 # m/s ????
# place_lin_vel = Pid.Pid(kp_place, ki_place, kd_place, 0.05, outputLimit_PID_place)
# kp_place = 1
# ki_place = 0.0
# kd_place = 0.0
# outputLimit_PID_place = 1 # m/s ????
# place_lin_vel = Pid.Pid(kp_place, ki_place, kd_place, 0.05, outputLimit_PID_place)



current_time = 0.0
old_time=0.0

    
#Defend Skill 
kp_def_angular = 0.1
kp__def_linear = 0.1

#Flags Receive
first_receive = 0

test = 0

img = np.zeros((480,640,3))

white = (255,255,255)
yellow = (0,255,255)
red = (0,0,255)
blue = (255,0,0)


def convertRelativeToAbsolute(xAbs, yAbs, xr, yr, alpha):
    absoluteValues = [0, 0, 0]
    
    # absoluteValues[0] = round(np.cos(np.radians(-alpha-90))*xr-np.sin(np.radians(-alpha-90))*yr+xAbs, 2)
    # absoluteValues[1] = round(-np.sin(np.radians(-alpha-90))*xr-np.cos(np.radians(-alpha-90))*yr+yAbs, 2)
    absoluteValues[0] = round(np.cos(np.radians(-alpha))*xr-np.sin(np.radians(-alpha))*yr+xAbs, 2)
    absoluteValues[1] = round(-np.sin(np.radians(-alpha))*xr-np.cos(np.radians(-alpha))*yr+yAbs, 2)
    return absoluteValues

    
def convertAbsoluteToRelative(xRob, yRob, xa, ya, alpha):
    xa -= xRob
    ya -= yRob
    A = np.array([[np.cos(np.radians(-alpha+180+90)), -np.sin(np.radians(-alpha+180+90))],
                    [np.sin(np.radians(-alpha+180+90)), np.cos(np.radians(-alpha+180+90))]])
    b = np.array([[-ya], [-xa]])
    temp = np.linalg.inv(A) @ b
    xr, yr = round(temp[0,0], 2), round(-temp[1,0], 2)
    return xr, yr
    

Skills = ["STOP", "MOVE", "ATTACK", "KICK", "RECEIVE", "COVER", "DEFEND", "CONTROL"]
            #0      1       2           3       4          5        6          7    
def stateMachine(data):
    global old_time, test
    # print(data.baseStation)
    
    #skill = data.baseStation.s #if data.baseStation.s else 1 #7

    #FOR KICK OFF VIDEO
    # ball_dist = data.ball.dist
    # if ball_dist > 300:
    #     skill = ATTACK
    # else:
    #     skill = RECEIVE
    # print(f" BALL DIST -------- {ball_dist}")
    #
    skill = 1
    linear_vel = 0
    direction = 0
    angular_vel = 0
    current_time = time.time()
    delta_t = current_time - old_time 
    old_time = current_time
    des_x = 0
    des_y = 0
    des_angle = 0    
    pwm_kick = 0
    dribblers = 0

    match Skills[skill]:
        case "STOP":
            print("STOP")
            linear_vel, direction, angular_vel = stop.skStop(data,delta_t)
        case "MOVE":
            print("MOVE")            
            
            new_arg0, new_arg1 = convertAbsoluteToRelative(data.robot.x, data.robot.y, data.baseStation.arg0, data.baseStation.arg1, data.robot.ang)
            new_arg3, new_arg4 = convertAbsoluteToRelative(data.robot.x, data.robot.y, data.baseStation.arg3, data.baseStation.arg4, data.robot.ang)

            data.baseStation.arg0 = new_arg0
            data.baseStation.arg1 = new_arg1
            data.baseStation.arg3 = new_arg3
            data.baseStation.arg4 = new_arg4
            
            linear_vel, direction, angular_vel = move.skMove(data,delta_t)
        case "ATTACK":
            print("ATTACK")   
            new_arg0, new_arg1 = convertAbsoluteToRelative(data.robot.x, data.robot.y, data.baseStation.arg0, data.baseStation.arg1, data.robot.ang)

            data.baseStation.arg0 = new_arg0
            data.baseStation.arg1 = new_arg1 
            
            linear_vel, direction, angular_vel = attack.skAttack(data,delta_t)
        case "KICK":
            print("KICK")
            
            new_arg0, new_arg1 = convertAbsoluteToRelative(data.robot.x, data.robot.y, data.baseStation.arg0, data.baseStation.arg1, data.robot.ang)
            new_arg3, new_arg4 = convertAbsoluteToRelative(data.robot.x, data.robot.y, data.baseStation.arg3, data.baseStation.arg4, data.robot.ang)

            data.baseStation.arg0 = new_arg0
            data.baseStation.arg1 = new_arg1
            data.baseStation.arg3 = new_arg3
            data.baseStation.arg4 = new_arg4
            print(data.baseStation)
            linear_vel, direction, angular_vel, pwm_kick = kick.skKick(data,delta_t)
        case "RECEIVE":
            new_arg0, new_arg1 = convertAbsoluteToRelative(data.robot.x, data.robot.y, data.baseStation.arg0, data.baseStation.arg1, data.robot.ang)

            data.baseStation.arg0 = new_arg0
            data.baseStation.arg1 = new_arg1 
            
            print("RECEIVE")
            linear_vel, direction, angular_vel, dribblers,des_x,des_y = receive.skReceive(data,delta_t)
        case "COVER":
            print("COVER")
            new_arg0, new_arg1 = convertAbsoluteToRelative(data.robot.x, data.robot.y, data.baseStation.arg0, data.baseStation.arg1, data.robot.ang)
            new_arg2, new_arg3 = convertAbsoluteToRelative(data.robot.x, data.robot.y, data.baseStation.arg2, data.baseStation.arg3, data.robot.ang)

            data.baseStation.arg0 = new_arg0
            data.baseStation.arg1 = new_arg1
            data.baseStation.arg2 = new_arg2
            data.baseStation.arg3 = new_arg3
            
            linear_vel, direction, angular_vel, des_x, des_y, des_angle = cover.skCover(data,delta_t)
            #angular_vel = 0
        case "DEFEND":
            print("DEFEND")
            #new_arg0, new_arg1 = convertAbsoluteToRelative(data.robot.x, data.robot.y, data.baseStation.arg0, data.baseStation.arg1, data.robot.ang)
 
            linear_vel, direction, angular_vel, des_x, des_y, des_angle  = defend.skDefend(data, delta_t)
            print(f"linear_vel: {linear_vel}, direction: {direction}, angular_vel: {angular_vel}")
        case "CONTROL":
            print("CONTROL")
            
        case _:
            pass

    #print(abs(data.ball.dist))
    if 0 < (data.ball.dist) < 100:
        dribblers = 1
    #print("Drib-> "+ str(dribblers))
    if linear_vel > 40:
        linear_vel = 40

    return skill, linear_vel, direction, angular_vel, pwm_kick, dribblers, des_x, des_y, des_angle


def mainLoop():
    # Receive CBD
    IPCom.Handler.getInfo()

    # Main Control
    skill, linear_vel, direction, angular_vel,pwm_kick,dribblers, X_des, Y_des, A_des = stateMachine(IPCom.Handler.ToRecv)

    # Ramp Omni
    _robot_.max_velocity = values[-1]
    current_velocity, current_direction, _, _, _, _, _ = _robot_.update_velocity_and_direction(linear_vel, direction, values[6], values[7], values[5], values[8])
    
    vel_lin = current_velocity
    dir_esp = current_direction
    vel_esp = np.clip(vel_lin, 0, _robot_.max_velocity)

    while dir_esp > 360:
        dir_esp -= 360

    while dir_esp < 0:
        dir_esp += 360

    # Send CDB
    IPCom.Handler.ToSend.linear_vel = int(vel_esp)   # 0:100
    IPCom.Handler.ToSend.angular_vel = int(angular_vel) # -100:100
    IPCom.Handler.ToSend.direction = int(dir_esp)     # -180:180  
    IPCom.Handler.ToSend.pwm_kick = int(pwm_kick)       # 0:100 : Intensity
    IPCom.Handler.ToSend.dribblers = int(dribblers)     # 0/1 : OFF/ON
    IPCom.Handler.ToSend.arms = int(0)
    IPCom.Handler.ToSend.X_desired = round(X_des,2)
    IPCom.Handler.ToSend.Y_desired = round(Y_des,2)
    IPCom.Handler.ToSend.A_desired = round(A_des,2)
    IPCom.Handler.ToSend.skill = skill
    
if __name__ == "__main__":
    while 1:
        start = time.time()
        mainLoop()
        IPCom.Handler.sendInfo()
        timeLoop = (time.time() - start)
        time2Wait = (1/FREQUENCY) - (time.time() - start)
        if time2Wait > 0:  time.sleep(time2Wait)  # noqa: E701
        IPCom.Handler.ToSend.loopTime = int(timeLoop*1000)
        IPCom.Handler.ToSend.loopPrecentage = int(((1/FREQUENCY)-time2Wait)/((1/FREQUENCY))*100)
        Print(f"{(timeLoop):.3f}/{time2Wait:.3f} -> {IPCom.Handler.ToSend.loopPrecentage}%")

def Exit():
    print(f"Exiting -> {__name__} <- ") 
    
atexit.register(Exit)
