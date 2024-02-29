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
#include <webots/touch_sensor.h>
#include <stdio.h>
#include <math.h>

#define TIME_STEP 16

#define SINAL(x) ((x)>0?3:((x)<0?-3:0))
#define RED    0
#define YELLOW 1
#define GREEN  2

WbDeviceTag wheels[3];
WbDeviceTag SonarFrente, SonarTras, SonarEsquerda, SonarDireita;
WbDeviceTag Bussola;
WbDeviceTag gps;
WbDeviceTag led[3]={ 0,0,0};
WbDeviceTag LuzC, LuzF, LuzT, LuzE, LuzD;
WbDeviceTag Kicker;
WbDeviceTag SToque;
WbDeviceTag SBola[18];

//Variaveis Globais - guardam valores dos sensores
int SF, ST, SE, SD;
int LuzCvalor, LuzFvalor, LuzTvalor, LuzEvalor, LuzDvalor;
double gpsValor[3];
int SBolaValor[18];
double BOLAAng;       // numero do sensor que vê a bola [1-18]
int BOLAValor;  // Valor lido pelo sensor de bola (para calcular a distancia)
int ANG_BUSSOLA=90;
int KickerValue=0;

int estado=1;   // esta variavel controla o GrafCet (comportamento do robo)

#define ACERTO_VEL_ANGULAR 5

#define ALVOMEIO     1
#define ALVOESQUERDA 0
#define ALVODIREITA  2
double ALVOZ[3]={-0.23, 0.0, 0.23};
double ALVOX=0.95;
double PosIniGRX=-0.78, PosIniGRZ=0.0;

int direccao=180, vel_linear=0, vel_angular=0;

#include "outros.c"

void orienta(double xf, double zf)
{
double xd, zd;
double angulo;
double temp;

  xd=gpsValor[0] - xf;
  zd=gpsValor[2] - zf;
  angulo = M_PI/2 + atan2(xd, zd);     norm_rad(&angulo);
  temp=((double)(ANG_BUSSOLA-90)-(angulo*180.0/M_PI));
  corrige_vel_angular(-temp);
//  printf("BUSS=%d angulo=%lf temp=%lf\n", ANG_BUSSOLA, angulo*180.0/M_PI, temp);
}

void orientaBussola(int norte)
{
int temp;

  temp=(ANG_BUSSOLA-norte); norm_graus(&temp);
  corrige_vel_angular((double)(-temp));
//  printf("BUSS=%d temp=%d\n", ANG_BUSSOLA, temp);
}

void orientaBola(void)  // ainda não está a ser usado
{
double angulo;

  angulo = BOLAAng;
  norm_graus_double(&angulo);
  corrige_vel_angular(angulo);
//  printf("\nangulo=%.4lf ", angulo);
}

void vai_para(double xf, double zf)
{
double xd, zd;
double angulo;

  xd=gpsValor[0] - xf;
  zd=gpsValor[2] - zf;
  angulo = atan2(xd, zd);
  direccao=(int)(0.5+(angulo-M_PI/2)*180.0/M_PI);
  if (direccao<0) direccao+=360;
//  printf("angulo=%lf direcao=%d\n", angulo*180.0/M_PI, direccao);
}

void orbita(double xf, double zf) // Não está a ser usado
{
double xd, zd;
double angulo;

  xd=gpsValor[0] - xf;
  zd=gpsValor[2] - zf;
  angulo = atan2(xd, zd);
//  printf("\nangulo=%.4lf ", angulo*180.0/M_PI);

  if (angulo>M_PI/2 || angulo<-M_PI/2)
    angulo += M_PI;
  norm_rad(&angulo);
  
  direccao=(int)(0.5 + angulo*180.0/M_PI);
  if (direccao<0) direccao+=360;
//  printf("Nangulo=%.4f direccao=%d\n", angulo*180.0/M_PI, direccao);
}

void orbitaBola(int lado)
{
double angulo;

  angulo = (BOLAAng-90.0)*M_PI/180.0;
//  printf("\nangulo=%.4lf ", angulo*180.0/M_PI);

  switch (lado)
  {
    case 0: // na zona central do campo (lado mais perto)
            if (angulo>M_PI/2 || angulo<-M_PI/2)
              angulo += M_PI;
            break;
    case 1: // lado direito
            angulo += M_PI;
            break;
    case -1: // lado esquerdo
            break;
  }
  norm_rad(&angulo);
  direccao=(int)(0.5 + angulo*180.0/M_PI);
  if (direccao<0) direccao+=360;
//  printf("lado=%d Nangulo=%.4f direccao=%d\n", lado, angulo*180.0/M_PI, direccao);
}

int valida_dentro_campo(void)
{
int flag=0;
    if (gpsValor[2]> 0.65) direccao=270, flag= 1;
    if (gpsValor[2]<-0.65) direccao= 90, flag=-1;
    if (gpsValor[0]> 0.95) direccao=  0;
    if (gpsValor[0]<-0.95) direccao=180;
return flag;
}

char estados[12][25]={"(nulo)",
                      "Vai posicao inicial",
                      "Vai à bola em recta",
                      "Orbita",
                      "Ataca",
                      "",
                      "",
                      "",
                      "",
                      "",
                      "Guarda-Redes"};

#define RaioRobo 0.105
#define DIST_LIMITE_IR_BOLA      1.5
#define DIST_LIMITE_ATACAR_BOLA  0.22
#define DIST_LIMITE_GUARDA_REDES 0.4


int decide_orbita(double x1, double z1, double x2, double z2, double x3, double z3)
{
double mr, mt;
double x, z, r;
int result=0;

  if(x2!=x1 && x2!=x3)  // evita divisões por 0
  {
    mr=(z2-z1)/(x2-x1);
    mt=(z3-z2)/(x3-x2);
    if(mr!=mt && mr!=0)  // evita divisões por 0
    {
      x=(mr*mt*(z3-z1)+mr*(x2+x3)-mt*(x1+x2))/(2*(mr-mt));
      z=-(1/mr)*(x-(x1+x2)/2)+((z1+z2)/2);
      r=sqrt((x-x1)*(x-x1)+(z-z1)*(z-z1));
      printf("O(%lf,%lf) R=%lf\n", x, z, r);
    }
    if(z+r> 0.65)    result= 1; // atingirá linha lateral direita
    if(z-r<-0.65)    result=-1; // atingirá linha lateral esquerda
  }
return result;
}

int main()
{
int estado_old=0;
int flag_dentro_campo=0;
double distancia;
double BolaX, BolaZ;
double temp;
double kickertemp;

  wb_robot_init();  // initialize Webots
  declara_sensores();

  vel_linear=20;
  vel_angular=0;

//  decide_orbita(0.098668, 0.035912, 0.080435, 0.067493, 0.052500, 0.090933);
//  estado_old=decide_orbita(-0.235092, 0.147683, -0.229991, 0.146199, -0.229171, 0.141379);

/*
  estado_old=decide_orbita(-0.205403 , 0.256382 , -0.209377 , 0.25177 , -0.213772 , 0.247578);
  estado_old=decide_orbita(-0.205403 , 0.256382 , -0.213772 , 0.247578 , -0.223041 , 0.241462);
  estado_old=decide_orbita(-0.205403 , 0.256382 , -0.218597 , 0.244531 , -0.231251 , 0.234757);
  estado_old=decide_orbita(-0.205403 , 0.256382 , -0.223041 , 0.241462 , -0.238184 , 0.228004);
*/
//  estado_old=decide_orbita(-0.259557, 0.192796, -0.272164, 0.181684, -0.277897, 0.167236);

//  wb_servo_set_position(Kicker, 0.02);
//  wb_robot_step(TIME_STEP);
        
  while (1) {
    le_tecla_decide_comportamento();
    
    le_sensores();
    
    if (KickerValue==1)
    {
      wb_servo_set_position(Kicker, 0.0);
      KickerValue=0;
printf("(nada)\n");
    }
    else
    {
      kickertemp=wb_touch_sensor_get_value(SToque);
      if (kickertemp > 0)
      {
printf("T=%lf\n", kickertemp);
        wb_servo_set_position(Kicker, 0.10);
        KickerValue=1;
      }
    }
    
    distancia=RaioRobo + (0.000895*(BOLAValor*BOLAValor) -0.71255726*BOLAValor+162.98)/100;
    BolaX = gpsValor[0]+distancia*sin(M_PI/2 + BOLAAng*M_PI/180.0);
    BolaZ = gpsValor[2]+distancia*cos(M_PI/2 + BOLAAng*M_PI/180.0);
    
//    wb_servo_set_position(Kicker, 0);
    
    switch(estado)
    {
      case 1: // vai para posicao inicial do jogo (proteje a baliza)
              if (distancia<DIST_LIMITE_IR_BOLA) estado=2;
              if (estado==1)
              {
                vai_para(-0.3, 0.0);
                orienta(ALVOX, gpsValor[2]);
              }
              break;
      case 2: // Vai para a bola em linha recta
              flag_dentro_campo = 0;
              if (distancia>DIST_LIMITE_IR_BOLA)  estado=1;
              if (distancia-RaioRobo<DIST_LIMITE_ATACAR_BOLA) estado=3; // Problema no calculo da distancia
              if (estado==2)
              {
                vai_para(BolaX-0.2, BolaZ);
                orienta(ALVOX, gpsValor[2]);
              }
              break;
      case 3: // orbita
              if (distancia>DIST_LIMITE_IR_BOLA)             estado=1;
              if (distancia-RaioRobo>DIST_LIMITE_ATACAR_BOLA)   estado=2;
              if (BOLAAng<5 || BOLAAng>355)  estado=4;
              if (BOLAAng>5 && BOLAAng<355)  estado=2;  // TESTAR
              if(estado==3) // se não é para sair deste estado
              {
              printf("\t%lf\t%lf\n", gpsValor[0], gpsValor[2]);
                if(valida_dentro_campo()!=0)
                  flag_dentro_campo = valida_dentro_campo();
                orbitaBola(flag_dentro_campo);
                orienta(ALVOX, gpsValor[2]); // é para tirar
              }
              break;
      case 4: // ataca a bola
              flag_dentro_campo = 0;
              if (distancia-RaioRobo>DIST_LIMITE_ATACAR_BOLA)   estado=2;  // NAO CORRIGE QUANDO BOLA MEXE
              if (estado==4)
              {
                vai_para(BolaX, BolaZ);
                if (gpsValor[2]>0)
                  orienta(ALVOX, ALVOZ[ALVODIREITA]);
                else
                  orienta(ALVOX, ALVOZ[ALVOESQUERDA]);
                orienta(ALVOX, ALVOZ[ALVOMEIO]);  // estou a ignorar o if anterior
              }
              break;
      case 10: // GUARDA-REDES
              if(BOLAValor>100)   // VALOR A CONFIGURAR... VE_BOLA ?
              {
                temp=BOLAAng; norm_graus_double(&temp);
                if (temp> 20.0) temp= 20.0;
                if (temp<-20.0) temp=-20.0;
                temp=-temp/100.0;
              }
              else
                temp=0.0;
              vai_para(PosIniGRX, PosIniGRZ + temp);
              orientaBussola(90);
              break;
    }
    
    (void)valida_dentro_campo();
    if (estado!=estado_old)
    {
      printf("\nEstado=%d - %s", estado, estados[estado]);
      estado_old = estado;
    }
    
//    printf("Estado=%d BOLAAng=%.3lf L(%.4lf,%.4lf) BOLAX=%.3lf BOLAZ=%.3lf\n",
//            estado, BOLAAng, gpsValor[0], gpsValor[2], BolaX, BolaZ);

//    printf("dir(%3d) vlin(%3d) vang(%3d)\n", direccao, vel_linear, vel_angular);
    andar(direccao, vel_linear, vel_angular);
    wb_robot_step(TIME_STEP);
  }
  andar(0, 0, 0);

  wb_robot_cleanup();
  return 0;
}
