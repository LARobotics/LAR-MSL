# Hardware
Baudrate 115200

Timeout 200ms

##Installation

$ sudo chmod 777 /dev/ttyUSB*

$ go run . ttyUSB*

 


 

#Full packet (receive) :

String : bearing_angle,Battery,temperature_OMNI, X_displacement, Y_displacement

| Variable | Range |
| ------------- | ------------- |
| bearing_angle  | -180 -> 180  |
| Battery  | 0 -> max battery voltage  |
| temperature_OMNI  |  |
| X_displacement  | 0 -> 1000  |
| Y_displacement  | 0 -> 1000  |

 
#Commands

Full packet  (send)

String : linear_speed,angular_speed,direction,drib1_vel,drib2_vel, Kick_time #resetenc

| Variable | Range |
| ------------- | ------------- |
| linear_speed  | 0 -> 100  |
| angular_speed  | -100 -> 100  |
| direction  | 0 ->360  |
| drib1_vel  | 0 -> 100  |
| drib2_vel  | 0 -> 100  |
| Kick_time  | 0 -> 15 |

OMNI 3MD PID Components 

String: 'P',Kp, ki, kd 

| Variable | Range |
| ------------- | ------------- |
| Kp  | 0 -> 100  |
| Ki  | 0 -> 100  |
| Kd  | 0 ->360  |

OMNI 3MD angular speed 

String: 'W',rotational_sp 

| Variable | Range |
| ------------- | ------------- | 
| angular_speed  | -100 -> 100  |
 
 
OMNI 3MD linear and rotational speed 
String: 'M',linear_speed,angular_speed,direction, 

| Variable | Range |
| ------------- | ------------- | 
| linear_speed  | 0 -> 100  |
| angular_speed  | -100 -> 100  |
| direction  | 0 ->360  |
 
