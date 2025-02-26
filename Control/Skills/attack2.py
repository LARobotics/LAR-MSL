import numpy as np

def skAttack(data): #! TINO Make it right
        
    scale1 = 0.26 #without distance
    scale2 = 9
    Direction_Scaler = 0.1
    distance_scalar = 0.14

    angle = data.ball_ang
    distance = data.ball_dist
    distance = distance if distance != 0 else 1
    print("measured::   angle:", angle, "  ,distance:", distance)

    if distance < 0:
        linear_vel = 0#max(min((distance+100) * distance_scalar * np.cos(np.deg2rad(angle)), 30), 0)
        angular_vel = max(min((angle+0.1)*100, 10), -10)
        direction = 0
    elif distance < 100:
        #linear_vel = min(int(distance / 2), 15)
        linear_vel = max(min((distance+100) * distance_scalar * np.cos(np.deg2rad(angle)), 20), 0)
        angular_vel = max(min(int(angle * (-scale2/distance)), 25), -25)
        direction = angle * Direction_Scaler * 0.5
    else:
        linear_vel = max(min((distance+100) * distance_scalar * np.cos(np.deg2rad(angle)), 20), 0)
        angular_vel = max(min(int(angle * (-scale1)), 25), -25)
        direction = angle * Direction_Scaler

    return linear_vel, direction, angular_vel

    print("C," + str(linear_vel) + ',' + str(direction) + ',' + str(angular_vel) + ',' + str(distance))# * distance_scalar * np.cos(np.deg2rad(angle))))
    IPCom.Handler.ToSend.linear_vel = int(linear_vel)
    IPCom.Handler.ToSend.angular_vel = int(angular_vel)
    IPCom.Handler.ToSend.direction = int(direction)