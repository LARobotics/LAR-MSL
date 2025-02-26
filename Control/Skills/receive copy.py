import cv2
import numpy as np
import math
import time
import Skills.PID as PID
import Skills.Atractor as Atractor


first_receive = 0

#Constants
#ORIENTATION
Kp_receive = 0.20
Ki_receive = 0.0001
Kd_receive = 0.0001
# Kp_receive = 0.25
# Ki_receive = 0.01
# Kd_receive = 0.1
outputLimit_PID_receive = 10.000
Katracao_receive = 5
Kintensidade_receive = 0.25
outputLimit_atractor_receive = 40.000
window_size = 40
Kp_receive_vel = 1#0.30
Ki_receive_vel = 0.05#0.005
Kd_receive_vel = 0.001#0.00
# Kp_receive_vel = 0.25
# Ki_receive_vel = 0.05
# Kd_receive_vel = 0.007
# Kp_receive_vel = 0.75
# Ki_receive_vel = 0.05
# Kd_receive_vel = 0.007

# receive_atractor = Atractor.Atractor(Katracao_receive, Kintensidade_receive, outputLimit_atractor_receive)
receive_atractor = PID.PID(Kp_receive_vel, Ki_receive_vel, Kd_receive_vel, 0.05, 40)
receive_orientation = PID.PID(Kp_receive, Ki_receive, Kd_receive, 0.05, outputLimit_PID_receive)#, 100)

# #Constants
# #Kp_atack = 0.1
# Kp_atack = 0.25
# #Ki_atack = 0.008
# Ki_atack = 0.01
# #Kd_atack = 0.000
# Kd_atack = 0.01
# outputLimit_PID_atack = 10.000
# Katracao_atack = 5
# #Kintensidade_atack = 0.422
# Kintensidade_atack = 0.0125
# outputLimit_atractor_atack = 40.000

# # Atack skill
# atack_atractor = Atractor.Atractor(Katracao_atack, Kintensidade_atack, outputLimit_atractor_atack)
# atack_orientation = PID.PID(Kp_atack, Ki_atack, Kd_atack, 0.05, outputLimit_PID_atack)#, 100)



###---DEBUG---###
img = np.zeros((500,500,3))

white = (255,255,255)
yellow = (0,255,255)
red = (0,0,255)
blue = (255,0,0)

#Robot
#angle = 30
#Other Robot (Robot that kick ball)
other_robot = (200,200)
other_angle = 90

#Tracking ball
ball_tr = (200,300)
#Ball
ball = (400,350)

def convert_to_rad(angle):
    rad_angle = (angle/180)*math.pi
    return rad_angle

def convert_to_angle(rad_angle):
    angle = (rad_angle*180)/math.pi
    return angle

def generate_poly(point1,point2):
    x = []
    y = []
    x.append(point1[0])
    y.append(point1[1])
    x.append(point2[0])
    y.append(point2[1])
    coefficients = np.polyfit(x, y,1)
    #poly = np.poly1d(coefficients)   
    return coefficients

def calculate_with_tracking(ball_x,ball_y, ball_xprev,ball_yprev):
    theta_ball_rad = math.atan2(ball_y- ball_yprev,ball_x-ball_xprev)
    theta_ball = convert_to_angle(theta_ball_rad)

    offset = 100
    robot = (int(ball_xprev-offset*math.cos(theta_ball_rad)), int(ball_yprev-offset*math.sin(theta_ball_rad)))
    #distance = math.sqrt(robot[0]*robot[0]+robot[1]*robot[1])
    theta_robot_rad = math.atan2(robot[1],robot[0])
    theta_robot = convert_to_angle(theta_robot_rad)
    #print("Theta -> " + str(round(theta_ball,2)))
    #print("Pos Robot -> " + str(robot))
    return theta_ball, theta_robot, robot


def calculate_distance(point1,point2=(0,0)):
    distance = math.sqrt((point2[0]-point1[0])*(point2[0]-point1[0]) + (point2[1]-point1[1])*(point2[1]-point1[1]))
    return distance


def calculate_distance_pos(point1,point2,theta):
    offset = 100
    theta_rad = convert_to_rad(theta)
    pos = (int(point2[0]-offset*math.cos(theta_rad)), int(point2[1]-offset*math.sin(theta_rad)))
    distance = calculate_distance(point1,point2)
    return distance


def calculate_with_other_robot(other_robot_x,other_robot_y,other_robot_ang):  
    offset = 50
    theta_ball = other_robot_ang
    theta_ball_rad = convert_to_rad(theta_ball)
    robot = (int(other_robot_x - offset*math.cos(theta_ball_rad)),int(other_robot_y - offset*math.sin(theta_ball_rad)))
    return theta_ball, robot

def convertToCoordinates(angle,distance):
    angle_rad = convert_to_rad(angle)
    x = distance*math.cos(angle_rad)
    y = distance*math.sin(angle_rad)
    return x,y

def convertToDistAng(pos_x,pos_y):
    dist = calculate_distance((pos_x,pos_y))
    ang = math.degrees(math.atan2(pos_y,pos_x))
    return dist, ang

def calculateIntersection(ball_x,ball_y,ball_x_pred,ball_y_pred):
    x0 = 0
    y0 = 0
    if ball_x == 0 and ball_y == 0 and ball_x_pred == 0 and ball_y_pred == 0:
        pass
    else: 
        #if (ball_x < ball_x_pred -1 or ball_x > ball_x_pred + 1) and (ball_y < ball_y_pred -1 or ball_y > ball_y_pred +1):
        #    x0 = 0
       #     y0 = 0
        #else: #if ball_x < ball_x_pred -1 or ball_x > ball_x_pred + 1 or ball_y < ball_y_pred -1 and ball_y > ball_y_pred +1 :
        coef_ball = generate_poly((ball_x,ball_y),(ball_x_pred,ball_y_pred))
        a1 = -coef_ball[0]
        b1 = 1
        c1 = -coef_ball[1]
        a2 = 1/coef_ball[0]
        b2 = 1
        c2 = 0
        x0 = (b1*c2 - b2*c1)/(a1*b2 - a2*b1)
        y0 = (c1*a2 - c2*a1)/(a1*b2 - a2*b1)
        # else:
        #     x0 = 0
        #     y0 = 0
    if np.isnan(y0) == True:
        y0 = 0
    return x0,y0

# def calculateTracking(ball_angle,ball_dist,ball_angle_pred,ball_dist_pred):
#     ball_x,ball_y = convertToCoordinates(ball_angle,ball_dist)
#     ball_x_pred,ball_y_pred = convertToCoordinates(ball_angle_pred,ball_dist_pred)
#     theta_ball_rad = math.atan2(ball_y- ball_y_pred,ball_x-ball_x_pred)
#     theta_ball = convert_to_angle(theta_ball_rad)
#     coef_ball = generate_poly((ball_x,ball_y),(ball_x_pred,ball_y_pred))
#     a1 = -coef_ball[0]
#     b1 = 1
#     c1 = -coef_ball[1]
#     a2 = 1/coef_ball[0]
#     b2 = 1
#     c2 = 0
#     x0 = (b1*c2 - b2*c1)/(a1*b2 - a2*b1)
#     y0 = (c1*a2 - c2*a1)/(a1*b2 - a2*b1)
#     return theta_ball,x0,y0

first_window=True
def sliding_window_state(window_size): #TO receive
    global first_window
    if window_size <= 0:
        raise ValueError("Window size must be greater than 0.")

    window = []
    current_state = None

    def update_window(new_value):
        nonlocal current_state
        if first_window==True:  
            if(new_value>0):
                window = []
                for i in range(window_size):
                    window.append(1)  # Add the new value
            else:
                window = []
                for i in range(window_size):
                    
                    window.append(-1)  # Add the new value    
        else:
            if len(window) == window_size:
                window.pop(0)  # Remove the oldest value
            if(new_value>0):
                window.append(1)  # Add the new value
            else:
                window.append(-1)  # Add the new value

        if len(window) == window_size:
            # Determine the state only when the window is full
            if all(v == 1 for v in window):
                current_state = 1
            elif all(v == -1 for v in window):
                current_state = -1

        return current_state, window

    return update_window

# Example usage

update_window = sliding_window_state(window_size)
def skReceive(data,delta_t):
    global first_window
    linear_vel= 0
    angular_vel = 0
    direction = 0
    dribblers = 1

    error_angle = 0
    error_dist = 0
    #theta_ball = 0
    des_x = 0 
    des_y = 0

    ball_angle_pred = data.ball.ang_pred
    ball_dist_pred = data.ball.dist_pred
    ball_x = data.ball.x
    ball_y = data.ball.y
    ball_x_pred = round(data.ball.x_pred,2)
    ball_y_pred = round(data.ball.y_pred,2)
    ball_angle = data.ball.ang
    ball_dist = data.ball.dist
    #self_angle = data.compass
    ball_x_bs = data.baseStation.arg0
    ball_y_bs = data.baseStation.arg1
    robot_x_bs = data.baseStation.arg2
    robot_y_bs = data.baseStation.arg3

    #if ball_angle_pred != 0 and ball_dist_pred !=0:
    #theta_ball,x0,y0 =  calculateTracking(ball_angle,ball_dist,ball_angle_pred,ball_dist_pred)
    des_x,des_y =  calculateIntersection(ball_x,ball_y,ball_x_pred,ball_y_pred)
    #print(theta_ball)
    #if ball_dist > 50:
    #x0, y0 = ball_x, ball_y

    #difference = ball_y - ball_y_pred

    distance = abs(ball_dist_pred * np.sin(np.deg2rad(ball_angle_pred)))#calculate_distance((x0,y0))
    #dist1  = calculate_distance((des_x,des_y))
    #print(" --d1-- ", distance)
    #print(" --d29-- ",dist1)

    #distance = dist1

    if ball_dist > ball_dist_pred + 10:

        #theta_ball,x0,y0 =  calculateTracking(ball_angle,ball_dist,ball_angle_pred,ball_dist_pred)
        # Example usage
        state, window = update_window(des_y)
        ##print("WINDOW     ", window)
        
        if (des_y>3 or des_y<-3) and state is not None:
            direction = 1.5*state*abs(des_y)#direction = 90# + theta_ball# + self_angle
            if direction >90:
                direction=90
            if direction <-90:
                direction=-90
            error_dist = distance
            linear_vel = receive_atractor.Update(error_dist, delta_t)
        else:
            print("FORWARD")
            direction = 0
            linear_vel = 40#eceive_atractor.Update(error_dist, delta_t)
    else:
        first_window=True
    # elif ball_dist < 100:
    #     error_dist = ball_dist
    #     if error_dist > 1000:
    #         error_dist = 1000
    #     linear_vel = atack_atractor.Update(error_dist) + 20
    #     if ball_dist < 50:
    #         linear_vel = atack_atractor.Update(error_dist)
    #else:
    #    linear_vel= 0
    #    angular_vel = 0
    #if ball_dist < 150:
    #    error_dist = ball_dist
    #    linear_vel = receive_atractor.Update(error_dist, delta_t)
    #if ball_dist < 45:
    #    ##error_dist = ball_dist
    #    linear_vel = 0

    #error_dist = ball_dist
    #linear_vel = receive_atractor.Update(error_dist, delta_t)

    error_angle = ball_angle
    angular_vel  = receive_orientation.Update(error_angle,delta_t)

    if data.stateBall == 1:
        linear_vel = 0
        angular_vel = 0

    #linear_vel= 0
    # direction = 0
    # angular_vel = 0

    # print("Ang-> " +str(ball_angle))
    # print("Dist->" +str(ball_dist))
    # print("Ang Pred-> " +str(round(ball_angle_pred,2)))
    # print("Dist Pred-> " +str(round(ball_dist_pred,2)))
    # print("Ball x-> " +str(ball_x))
    # print("Ball y->" +str(ball_y))
    # print("Ball x Pred-> " +str(round(ball_x_pred,2)))
    # print("Ball y Pred-> " +str(round(ball_y_pred,2)))
    #print("Comp-> " +str(self_angle))
    #print("X0> " +str(des_x))
    #print("Y0->" +str(des_y))
    #print("State Ball->" +str(data.stateBall))
    print("Ang vel-> " + str(angular_vel))
    print("Lin vel-> " + str(linear_vel))
    print("Direction-> " + str(direction))

    return linear_vel, direction, angular_vel, dribblers, des_x*10, des_y*10

if __name__ == "__main__":

    ball_x = 100
    ball_y = 0
    ball_x_pred = 50
    ball_y_pred = 0

    x0,y0 =  calculateIntersection(ball_x,ball_y,ball_x_pred,ball_y_pred)

    print("Ball x-> " +str(ball_x))
    print("Ball y->" +str(ball_y))
    print("Ball x Pred-> " +str(round(ball_x_pred,2)))
    print("Ball y Pred-> " +str(round(ball_y_pred,2)))
    #print("Comp-> " +str(self_angle))
    print("X0> " +str(x0))
    print("Y0->" +str(y0))


    #cv2.circle(img,robot,20,blue,-1)
    #cv2.circle(img,other_robot,20,blue,-1)
    #Point robot should be move
    #cv2.circle(img,robot,20,white,-1)
    #Ball
    cv2.circle(img,(ball_x,ball_y),20,yellow,-1)
    #Tracking ball
    cv2.circle(img,(ball_x_pred,ball_y_pred),20,red,-1)    
    #Intersection
    cv2.circle(img,(int(x0),int(y0)),20,blue,-1)


    cv2.imshow("Receive",img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
