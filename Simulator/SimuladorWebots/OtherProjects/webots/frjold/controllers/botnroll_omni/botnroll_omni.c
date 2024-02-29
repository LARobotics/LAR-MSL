/*
 * File:        Botnroll_omni.c
 * Date:        May 25, 2010
 * Description: Demo of a three-omni-wheels robot
 * Author:      Mehdi Ghanavati, Shahid Chamran University
 * Adapted by:  Yvan Bourquin - www.cyberbotics.com
 */

#include <webots/robot.h>
#include <webots/servo.h>
#include <webots/camera.h>
#include <webots/display.h>
#include <webots/display.h>
#include <webots/distance_sensor.h>
#include <stdio.h>
#include <math.h>

#ifndef M_PI
	#define M_PI 3.1415926535897932384626433832795L
#endif

static WbDeviceTag wheels[3];

void andar(int direccao, int vel_linear, int vel_angular)
{
static int motor1, motor2, motor3;

  motor1=vel_angular + (int)((double)vel_linear*cos(( 30-direccao)*M_PI/180.0));
	motor2=vel_angular + (int)((double)vel_linear*cos((150-direccao)*M_PI/180.0));
	motor3=vel_angular + (int)((double)vel_linear*cos((270-direccao)*M_PI/180.0));
  wb_servo_set_velocity(wheels[0], motor1>>2);
  wb_servo_set_velocity(wheels[1], motor2>>2);
  wb_servo_set_velocity(wheels[2], motor3>>2);
  wb_robot_step(8);
}

int main()
{
  int i;
  char name[64];
  double distancia;
  int direccao=0, vel_linear=30, vel_angular=0;
  
  wb_robot_init();  // initialize Webots
  for (i = 0; i < 3; i++) {
    sprintf(name, "wheel%d", i+1);
    wheels[i] = wb_robot_get_device(name);
    wb_servo_set_position(wheels[i], INFINITY);
  }
  WbDeviceTag ds = wb_robot_get_device("my_distance_sensor");
  wb_distance_sensor_enable(ds, 8);
  
  while (1) {
    andar(direccao, vel_linear, vel_angular);
    //direccao+=1;
    
    //for (i = 0; i < 5; i++) {
      distancia = wb_distance_sensor_get_value(ds);
      printf("\n%d %7.2lf ===> ", i, distancia);
      if (distancia<300)
        direccao+=5;
    //}
  }

  return 0;
}
