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

#define TIME_STEP 16

#define SINAL(x) ((x)>0?3:((x)<0?-3:0))
#define RED    0
#define YELLOW 1
#define GREEN  2

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
double BOLAAng;       // numero do sensor que vê a bola [1-18]
int BOLAValor;  // Valor lido pelo sensor de bola (para calcular a distancia)
int ANG_BUSSOLA=90;

int estado=1;   // esta variavel controla o GrafCet (comportamento do robo)

#define ALVOMEIO     1
#define ALVOESQUERDA 0
#define ALVODIREITA  2
double ALVO[3]={-0.23, 0.0, 0.23};

double PosIniGRX=-0.78, PosIniGRZ=0.0;
#define ACERTO_VEL_ANGULAR 5

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
                      "Nao ve bola ou LONGE",
                      "Vai à bola em recta",
                      "Vai posicao inicial",
                      "Orbita",
                      "Ataca",
                      "",
                      "",
                      "",
                      "",
                      "GR - vai para baliza",
                      "GR - Protege baliza"};

#define RaioRobo 0.105
int main()
{
int estado_old=0;
int flag_dentro_campo=0;
double distancia;
double BolaX, BolaZ;
double distancia_GR, tempX, tempZ;
double temp;

  wb_robot_init();  // initialize Webots
  declara_sensores();
  
  estado=1;
  vel_linear=20;
  
  while (1) {
    le_tecla_decide_comportamento();  // Não está a funcionar
    
    le_sensores();
    
    distancia=RaioRobo + (0.000895*(BOLAValor*BOLAValor) -0.71255726*BOLAValor+162.98)/100;
    BolaX = gpsValor[0]+distancia*sin(M_PI/2 + BOLAAng*M_PI/180.0);
    BolaZ = gpsValor[2]+distancia*cos(M_PI/2 + BOLAAng*M_PI/180.0);
printf("distancia=%lf", distancia);
    switch(estado)
    {
      case 1: // nao ve a bola (ou muito longe)
              if (distancia>1.0)  estado=3;
              else estado=2;
              break;
      case 2: // Vai para a bola em linha recta
              flag_dentro_campo = 0;
              if (distancia>1.1)  estado=3;
              if (distancia-RaioRobo<0.22) estado=4; // Problema no calculo da distancia
              if (estado==2)
              {
                vai_para(BolaX-0.2, BolaZ);
                orienta(0.95, gpsValor[2]);
              }
              break;
      case 3: // vai para posicao inicial do jogo (proteje a baliza)
              if (distancia<0.9) estado=2;
              if (estado==3)
              {
                vai_para(-0.3, 0.0);
                orienta(0.95, gpsValor[2]);
              }
              break;
      case 4: // orbita
              if (distancia>0.9)             estado=3;
              if (distancia-RaioRobo>0.25)   estado=2;
              if (BOLAAng<5 || BOLAAng>355)  estado=5;
              if(estado==4) // se não é para sair deste estado
              {
                if(valida_dentro_campo()!=0)
                  flag_dentro_campo = valida_dentro_campo();
                orbitaBola(flag_dentro_campo);
                orienta(0.95, gpsValor[2]); // é para tirar
              }
              break;
      case 5: // ataca a bola
              flag_dentro_campo = 0;
              if (distancia-RaioRobo>0.25)   estado=2;  // NAO CORRIGE QUANDO BOLA MEXE
              if (estado==5)
              {
                vai_para(BolaX, BolaZ);
                if (gpsValor[2]>0)
                  orienta(0.95, ALVO[ALVODIREITA]);
                else
                  orienta(0.95, ALVO[ALVOESQUERDA]);
                orienta(0.95, ALVO[ALVOMEIO]);  // estou a ignorar o if anterior
              }
              break;
      case 10: // GR - vai para posicao inicial do jogo (proteje a baliza)
              tempX = gpsValor[0]-PosIniGRX;
              tempZ = gpsValor[2]-PosIniGRZ;
              distancia_GR = sqrt(tempX*tempX + tempZ*tempZ);
              if (distancia_GR<=0.4) estado=11;
              if(estado==10)
              {
                vai_para(-0.78, 0.0);
//                orienta(0.95, gpsValor[2]);
                orientaBussola(90);   // Este modo de orientação deve ser mais fiável
              }
              break;
      case 11: // Guarda-redes // ESTE ESTADO BASTAVA PARA O GR
              tempX = gpsValor[0]-PosIniGRX;
              tempZ = gpsValor[2]-PosIniGRZ;
              distancia_GR = sqrt(tempX*tempX + tempZ*tempZ); 
//              if (distancia_GR>0.4) estado=10;
              if(estado==11)
              {
                if(BOLAValor>100)   // VALOR A CONFIGURAR... VE_BOLA ?
                {
                  temp=BOLAAng; norm_graus_double(&temp);
                  if (temp> 20.0) temp= 20.0;
                  if (temp<-20.0) temp=-20.0;
                  temp=-temp/100.0;
                }
                else
                  temp=0.0;
                vai_para(-0.78, temp);
                orientaBussola(90);
              }
              break;
      case 12: // NOVO GUARDA-REDES
              if(BOLAValor>100)   // VALOR A CONFIGURAR... VE_BOLA ?
              {
                temp=BOLAAng; norm_graus_double(&temp);
                if (temp> 20.0) temp= 20.0;
                if (temp<-20.0) temp=-20.0;
                temp=-temp/100.0;
              }
              else
                temp=0.0;
              vai_para(-0.78, temp);
              orientaBussola(90);
              break;
    }
    (void)valida_dentro_campo();
    if (estado!=estado_old)
    {
      printf("\nEstado=%d - %s", estado, estados[estado]);
      estado_old = estado;
    }
//    printf("dir(%3d) vlin(%3d) vang(%3d)\n", direccao, vel_linear, vel_angular);
//    printf("Estado=%d BOLAAng=%.3lf distancia=%.3lf  L(%.4lf,%.4lf) BOLAX=%.3lf BOLAZ=%.3lf\n",
//            estado, BOLAAng, distancia, gpsValor[0], gpsValor[2], BolaX, BolaZ);

    andar(direccao, vel_linear, vel_angular);
    wb_robot_step(TIME_STEP);
  }
  andar(0, 0, 0);

  wb_robot_cleanup();
  return 0;
}
