/*
 * File:        Botnroll_omni.c
 * Date:        May 31, 2013
 * Description: Demo for the Bot'n Roll OMNI (by SAR)
 * Author:      Fernando Ribeiro, University of Minho, Guimarães
 */

#include <webots/robot.h>
#include <webots/servo.h>
#include <webots/distance_sensor.h>
#include <webots/compass.h>
#include <webots/gps.h>
#include <webots/led.h>
#include <webots/light_sensor.h>
#include <stdio.h>
#include <math.h>

#define TIME_STEP 64

WbDeviceTag wheels[3];
WbDeviceTag SonarFrente, SonarTras, SonarEsquerda, SonarDireita;
WbDeviceTag Bussola;
WbDeviceTag gps;
WbDeviceTag led[3]={0,0,0};
WbDeviceTag LuzC, LuzF, LuzT, LuzE, LuzD;
WbDeviceTag SBola[18];

//Variaveis Globais - guardam valores dos sensores
int SF, ST, SE, SD;
int LuzCvalor, LuzFvalor, LuzTvalor, LuzEvalor, LuzDvalor;
double gpsValor[3];
int SBolaValor[18];
int BOLA;       // numero do sensor que vê a bola [1-18]
int BOLAValor;  // Valor lido pelo sensor de bola (para calcular a distancia)
int ANG_BUSSOLA=90;

void le_sonares()
{
  SF = wb_distance_sensor_get_value(SonarFrente);
  ST = wb_distance_sensor_get_value(SonarTras);
  SE = wb_distance_sensor_get_value(SonarEsquerda);
  SD = wb_distance_sensor_get_value(SonarDireita);
}

int le_bussola()
{
const double *BU = wb_compass_get_values(Bussola);
double angle = atan2(BU[0], BU[2]);
int angulo=(int)(angle*180.0/M_PI);

return angulo;
}

void le_gps()
{
const double *gps_values = wb_gps_get_values(gps);
int i;

  for(i=0;i<3;i++)
    gpsValor[i]=gps_values[i];
}

void le_Luz()
{
  LuzCvalor = wb_distance_sensor_get_value(LuzC);
  LuzFvalor = wb_distance_sensor_get_value(LuzF);
  LuzTvalor = wb_distance_sensor_get_value(LuzT);
  LuzEvalor = wb_distance_sensor_get_value(LuzE);
  LuzDvalor = wb_distance_sensor_get_value(LuzD);
}

void le_Bola()
{
int i;
char temp[20];
int final, maximo=0;

  for (i=0;i<18;i++)
  {
    sprintf(temp, "SBola%d",i+1);
    SBolaValor[i] = (int)wb_light_sensor_get_value(SBola[i]);
    if (SBolaValor[i]>maximo)
    {
      maximo=SBolaValor[i];
      final=i+1;
    }
  }
BOLA=final;
BOLAValor=maximo;
}

void andar(int direccao, int vel_linear, int vel_angular)
{
static int motor1, motor2, motor3;

  motor1=vel_angular + (int)(0.5+(double)vel_linear*cos(( 30-direccao)*M_PI/180.0));
	motor2=vel_angular + (int)(0.5+(double)vel_linear*cos((150-direccao)*M_PI/180.0));
	motor3=vel_angular + (int)(0.5+(double)vel_linear*cos((270-direccao)*M_PI/180.0));
  wb_servo_set_velocity(wheels[0], motor1>>1);
  wb_servo_set_velocity(wheels[1], motor2>>1);
  wb_servo_set_velocity(wheels[2], motor3>>1);
}

void declara_sensores()
{
int i;
char temp[20];

  // declara sensores
  wheels[0]     = wb_robot_get_device("wheel1");
  wheels[1]     = wb_robot_get_device("wheel2");
  wheels[2]     = wb_robot_get_device("wheel3");
  SonarFrente   = wb_robot_get_device("SonarFrente");
  SonarTras     = wb_robot_get_device("SonarTras");
  SonarEsquerda = wb_robot_get_device("SonarEsquerda");
  SonarDireita  = wb_robot_get_device("SonarDireita");
  Bussola       = wb_robot_get_device("Bussola");
  gps           = wb_robot_get_device("gps");
  led[0]        = wb_robot_get_device("led0");
  led[1]        = wb_robot_get_device("led1");
  led[2]        = wb_robot_get_device("led2");
  LuzC          = wb_robot_get_device("LuzC");
  LuzF          = wb_robot_get_device("LuzF");
  LuzT          = wb_robot_get_device("LuzT");
  LuzE          = wb_robot_get_device("LuzE");
  LuzD          = wb_robot_get_device("LuzD");
//  SBola[0]      = wb_robot_get_device("SBola1");

  for (i=0;i<18;i++)
  {
    sprintf(temp, "SBola%d",i+1);
    SBola[i] = wb_robot_get_device(temp);
  }

  // enable sensores/actuators
  wb_servo_set_position(wheels[0], INFINITY);
  wb_servo_set_position(wheels[1], INFINITY);
  wb_servo_set_position(wheels[2], INFINITY);

  wb_distance_sensor_enable(SonarFrente  , TIME_STEP);
  wb_distance_sensor_enable(SonarTras    , TIME_STEP);
  wb_distance_sensor_enable(SonarEsquerda, TIME_STEP);
  wb_distance_sensor_enable(SonarDireita , TIME_STEP);
  wb_compass_enable(Bussola, TIME_STEP);
  wb_gps_enable(gps, TIME_STEP);
  wb_distance_sensor_enable(LuzC, TIME_STEP);
  wb_distance_sensor_enable(LuzF, TIME_STEP);
  wb_distance_sensor_enable(LuzT, TIME_STEP);
  wb_distance_sensor_enable(LuzE, TIME_STEP);
  wb_distance_sensor_enable(LuzD, TIME_STEP);
  wb_led_set(led[0],1);
  wb_led_set(led[1],1);
  wb_led_set(led[2],1);
  for (i=0;i<18;i++)
    wb_light_sensor_enable(SBola[i], TIME_STEP);

  wb_robot_keyboard_enable(TIME_STEP);
}

void le_sensores()
{
  le_sonares();
  ANG_BUSSOLA=le_bussola();
  le_gps();
  le_Luz();
  le_Bola();
}

/*
void DEBUG()
{
int i;

  printf("\nF=%4d T=%4d E=%4d D=%4d (B=%3d)", SF, ST, SE, SD, angulo);
  printf("\nC=%3d F=%3d T=%3d E=%3d D=%3d", LuzCvalor, LuzFvalor, LuzTvalor, LuzEvalor, LuzDvalor);
  printf("GPS: %.3f %.3f %.3f\n", gpsValor[0], gpsValor[1], gpsValor[2]);
  printf("\n [%3d] ", BOLA);
  for (i=0;i<18;i++)
    printf("%3d ", SBolaValor[i]);

  switch (wb_robot_keyboard_get_key())
  {
    case '4': vel_angular+=10; break;
    case '6': vel_angular-=10; break;
    case 'R': {wb_led_set(led[0],1);printf("R"); break;}
    case 'T': {wb_led_set(led[0],0);printf("T"); break;}
    case 'Y': {wb_led_set(led[1],1);printf("Y"); break;}
    case 'U': {wb_led_set(led[1],0);printf("U"); break;}
    case 'G': {wb_led_set(led[2],1);printf("G"); break;}
    case 'H': {wb_led_set(led[2],0);printf("H"); break;}
  }
}
*/

int main()
{
int direccao=180, vel_linear=10, vel_angular=0;
int ang_bola;
double distancia;

  wb_robot_init();  // initialize Webots

  declara_sensores();
  printf("\n================================\n");
  le_sensores();
  while (1) {
  //direccao=0;vel_linear=0;vel_angular=0;
    andar(direccao, vel_linear, vel_angular);
    le_sensores();
    
    ang_bola=10+(BOLA-1)*20;
    distancia=(BOLAValor-469.63)/-475.59;
    printf("\nBUS=%d Dist=%lf ABola=%d BolaVal=%d Dir=%d Vel=%d VAng=%d",
    ANG_BUSSOLA, distancia, ang_bola, BOLAValor, direccao, vel_linear, vel_angular);
    if(BOLA==1 && distancia<0.2)
      vel_linear=0;
    else
    {
      vel_linear=10;
      direccao+=(ang_bola);
    }
    vel_angular=-((direccao-180)+(ANG_BUSSOLA-90));
//    if (vel_angular>10 || vel_angular<-10)
//      vel_angular=0;
/*
    if (SE<500)
      vel_angular+=2;
    if (SF<500)
      vel_angular+=2;
    if (SD<500)
      vel_angular-=2;
    if ((SE>500) & (SD>500))
      vel_angular=0;
*/    
    wb_robot_step(TIME_STEP);
  }

  wb_robot_cleanup();
  return 0;
}
