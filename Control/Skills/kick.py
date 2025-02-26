import cv2
import numpy as np
import math
import time
import Skills.PID as PID

kp_kick= 0.12
Ki_kick = 0.035 #0.035#0.03 #0.008
Kd_kick = 0.003 #0.0013#0.003
outputLimit_PID_kick = 15.000#8.000
kick_orientation = PID.PID(kp_kick, Ki_kick, Kd_kick, 0.05, outputLimit_PID_kick)#, 100)

HASBASESTATION = 1

GOAL_LENGTH = 240
THRESHOLDMIN = -3
THRESHOLDMAX = 5

KICK_CAP = 70
KICK_FORCE = 60
PASS_FORCE = 30
DIST_MAX = 600

#Global variables kick
first_kick = 0
theta = 0

def getAngle(point1,point2=(0,0)):
   angle = math.atan2(point1[1]-point2[1],point1[0]-point2[0])
   return angle

def calculate_distance(point1,point2=(0,0)):
   distance = math.sqrt((point2[0]-point1[0])*(point2[0]-point1[0]) + (point2[1]-point1[1])*(point2[1]-point1[1]))
   return distance


def generate_poly(point1,point2):
   x = []
   y = []
   x.append(point1[0])
   y.append(point1[1])
   x.append(point2[0])
   y.append(point2[1])
   coefficients = np.polyfit(x, y, 1)
   poly = np.poly1d(coefficients)   
   return poly


"""
   arg0, arg1 = x e y absoluto
   agr2 = tipo chuto (0 passe, 1 remate)
   agr3, agr4 = x e y favorecido
   arg5, arg6
"""

def skKick(data,delta_t):
   global first_kick, theta

   linear_vel = 0
   angular_vel = 0
   direction = 0
   pwm_kick = 0

   #Relative
   goals = data.goalPosts
   total_valid_goals = 0
   gl_sel = None
   dist = 99999
   self_angle = data.compass
   stateBall = data.stateBall
   cap = data.kick_cap

   tg_x = data.baseStation.arg0 * 100
   tg_y = data.baseStation.arg1 * 100
   kick_type = data.baseStation.arg2 #if data.baseStation.arg2 else 1
   mv_x = data.baseStation.arg3
   mv_y = data.baseStation.arg4

   list_op = data.robots
   op_glkp = None
   list_fr = data.friends
   fr_rb = None
   angl_final = 0

   # #! REMOVE AFTER ONLY DEBUG
   if (stateBall == 3 or stateBall == 0) and data.ball.dist < 900:
      angular_vel = kick_orientation.Update(data.ball.ang, delta_t)
      direction = data.ball.ang
      linear_vel = 20
      print("Angle:", self_angle, "DIRCT:",angl_final, "ORI:", abs(angl_final - self_angle))
      print(f' LINEAR: {linear_vel} ANGULAR_VEL {angular_vel} DIRECTION {direction}')

      # linear_vel = 0
      # angular_vel = 0
      # direction = 0

      return int(linear_vel), int(direction), int(angular_vel), pwm_kick

   # kick
   if kick_type == 1:
      avg_x, avg_y = 0, 0

      # verify goal post over compass
      for i, gl in enumerate(goals):
         calc = ((gl.ang) - (self_angle)) # if gl.ang > self_angle else abs(self_angle - gl.ang)
         #print(gl.ang, self_angle, calc)
         if 0 < calc <= 90:
            total_valid_goals += 1
         else:
            del goals[i]

      #print("GOALS:", len(goals))

      if total_valid_goals == 0:
         #print("NO GOALPOSTS")
         if HASBASESTATION:
            angl_final = np.rad2deg(np.arctan2(tg_y, tg_x))
         else:
            angl_final = -self_angle
      elif total_valid_goals == 1:
         #print("ONE GOALPOSTS")
         # Get Goalkeeper
         #print("POST")
         for op in list_op:
            dt = math.sqrt((op.y - goals[0].y)**2 + (op.x - goals[0].x)**2)
            if (op_glkp is None or dt < dist) and dt < GOAL_LENGTH:
               op_glkp = op
               dist = dt
         
         if op_glkp is not None:
            #print("GOALKEEPER")
            dx = goals[0].x - op_glkp.x
            dy = goals[0].y - op_glkp.y

            length = math.sqrt(dx**2 + dy**2)
            unit_dx = dx / length
            unit_dy = dy / length

            perp_dx = -unit_dy * GOAL_LENGTH
            perp_dy = unit_dx * GOAL_LENGTH

            if goals[0].ang > op_glkp.ang:
               x_goal = goals[0].x + perp_dx
               y_goal = goals[0].y + perp_dy
            else:
               x_goal = goals[0].x - perp_dx
               y_goal = goals[0].y - perp_dy

            avg_y = (y_goal + goals[0].y) / 2
            
            #angl_final = math.degrees(math.atan2(y_goal, x_goal))
            angl_final = np.rad2deg(np.arctan2(y_goal + (0.2*(avg_y-y_goal)), x_goal))
         else:
            #print("NO GOALKEEPER")
            if HASBASESTATION:
               angl_final = np.rad2deg(np.arctan2(tg_y, tg_x))
            else:
               angl_final = goals[0].ang
      else:
         # get average of goal posts
         for i, gl in enumerate(goals):
            if i == 2: break
            #print("GL: ", "x:", gl.x, "y:",gl.y, "ang:", gl.ang)
            avg_x += gl.x
            avg_y += gl.y
            angl_final += gl.ang

         avg_x /= len(goals) if len(goals) > 0 else 1
         avg_y /= len(goals) if len(goals) > 0 else 1
         angl_final /= len(goals) if len(goals) > 0 else 1
         # print("AVEG:", avg_x, avg_y)

         # calucalte the center of goal to closest goalkeeper
         for op in list_op:
            dt = math.sqrt((op.y - avg_y)**2 + (op.x - avg_x)**2)
            if dt < dist and dt < GOAL_LENGTH:
               op_glkp = op
               dist = dt

         if op_glkp is not None:
            #print("GOALKEEPER")
            #print("GLKP:", "x:", op_glkp.x, "y:", op_glkp.y, "ang:", op_glkp.ang, "dist:", dist)
            dist = 0
            for gl in goals:
               dt = math.sqrt((op_glkp.y - gl.y)**2 + (op_glkp.x - gl.x)**2)
               #print("Calc2:", "xr:", gl.x, "yr:", gl.y, "dist:", dt)

               if gl_sel is None or dt > dist:
                  gl_sel = gl
                  dist = dt

            if gl_sel is not None:
               #print("POST")
               #print("GL:", "x:", gl_sel.x, "y:", gl_sel.y, "ang:", gl_sel.ang)
               angl_final = np.rad2deg(np.arctan2(gl_sel.y + (0.2*(avg_y-gl_sel.y)), gl_sel.x))
            else:
               angl_final = op_glkp.ang
         # else:
         #    print("NOT GOALKEEPER")
      
      #print("Angle:", self_angle, "DIRCT:",angl_final, "ORI:", abs(angl_final - self_angle), "thres:", THRESHOLD, "SHOOT:", abs(angl_final - self_angle) < THRESHOLD)
      #print(f' LINEAR: {linear_vel} ANGULAR_VEL {angl_final} DIRECTION {direction}')

   else:
      #print("FRIEND", len(list_fr))
      if HASBASESTATION:
         for fr in list_fr:
            dt = math.sqrt((fr.y - tg_y)**2 + (fr.x - tg_x)**2)
            if dt < dist:
               fr_rb = fr
               dist = dt

         if fr_rb is not None:
            angl_final = fr_rb.ang
         else:
            angl_final = np.rad2deg(np.arctan2(tg_y, tg_x))
      else:
         for i, fr in enumerate(list_fr):
            if i == 1: break
            fr_rb = fr

         if fr_rb is not None:
            angl_final = fr_rb.ang
         else:
            return 0, 0, 0, 0

      #print("Angle:", self_angle, "DIRCT:",angl_final, "ORI:", abs(angl_final), "thres:", THRESHOLD, "SHOOT:", abs(angl_final) < THRESHOLD)
      #print(f' LINEAR: {linear_vel} ANGULAR_VEL {angl_final} DIRECTION {direction}')

   #! REMOVE AFTER
   #angl_final = np.rad2deg(np.arctan2(tg_y, tg_x)) 
   
   angular_vel = kick_orientation.Update(angl_final, delta_t)
   times = np.clip(abs((90-abs(angl_final))/30), 0, 2.2)
   #print(f"TIMES: {times}")
   angular_vel *= times
   angular_vel = np.clip(angular_vel, -8, 8)

   linear_vel = 10
   direction = np.clip(-angl_final*1.5, -90, 90)

   #print("FL_Ang", angl_final, "MY_Ang", self_angle, "SHOOT:", THRESHOLDMIN <= angl_final <= THRESHOLDMAX)
   if THRESHOLDMIN <= angl_final <= THRESHOLDMAX and stateBall == 1:
      pwm_kick = KICK_FORCE if kick_type else PASS_FORCE
      pwm_kick = pwm_kick if cap >= 70 else 0
      
      if pwm_kick != 0:
         linear_vel, angular_vel, direction = 0, 0, 0

   # if first_kick == 0:   
   #    first_kick = 1
   #    line_goal = generate_poly((goal1_x,goal1_y),(goal2_x,goal2_y))            
   #    random_x = np.random(goal1_x,goal2_x)
   #    random_y = line_goal(random_x)
   #    theta = getAngle((random_x,random_y))

   # error = theta - self_angle
   # angular_vel = kick_orientation.Update(error,delta_t)
   # if angular_vel == 0:
   #    first_kick = 0
      # distance = calculate_distance((random_x,random_y))
      # pwm_kick = 100
      # #define equation to get pwm kick with distance to goal
      # kpwm = 0.1
      # pwm_kick = int(distance * kpwm)
      # if pwm_kick  > 100:
      #   pwm_kick = 100

   #linear_vel = 25
   #direction = 0
   print(f"ang: {self_angle} | has_ball: {stateBall} | linear_vel: {linear_vel} | angular_vel: {angular_vel} | direction: {direction} | pw_kick: {pwm_kick}")
   # print(self_angle, has_ball, test_ang, data.ball_dist)
   
   ####---DEBUG KICK---###
   #pwm_kick = 0
   # theta = getAngle((goal1_x,goal1_y))
   # error = theta - self_angle
   # #! DEBUG ONLY REMOVE AFTER
   # angular_vel = 0
   # linear_vel = 0
   # direction = 0
   # pwm_kick = 0
   # error = -test_ang
   # #angular_vel = kick_orientation.Update(error,delta_t)
   # angular_vel = max(min(int(test_ang * (-0.20 )), 25), -25)
   # #print(angular_vel)

   return int(linear_vel), int(direction), int(angular_vel), pwm_kick

if __name__ == "__main__":
   pass
   
