
// ALVO  (0.9 y  0.00)
// ALVOA (0.9 y -0.23)
// ALVOB (0.9 y  0.23)

void norm_rad(double *radianos)
{
  while (*radianos> M_PI)  *radianos-=2*M_PI;
  while (*radianos<-M_PI)  *radianos+=2*M_PI;
}

void norm_graus(int *graus)
{
  while (*graus> 180)  *graus-=2*180;
  while (*graus<-180)  *graus+=2*180;
}

void norm_graus_double(double *graus)
{
  while (*graus> 180.0)  *graus-=2*180.0;
  while (*graus<-180.0)  *graus+=2*180.0;
}
void ler_sonares()
{
  SF = wb_distance_sensor_get_value(SonarFrente);
  ST = wb_distance_sensor_get_value(SonarTras);
  SE = wb_distance_sensor_get_value(SonarEsquerda);
  SD = wb_distance_sensor_get_value(SonarDireita);
}

int ler_bussola()
{
const double *BU = wb_compass_get_values(Bussola);
double angle = atan2(BU[0], BU[2]);
int angulo=(int)((M_PI-angle)*180.0/M_PI);

return angulo;
}

void ler_gps()
{
const double *gps_values = wb_gps_get_values(gps);
int i;

  for(i=0;i<3;i++)
    gpsValor[i]=gps_values[i];
}

void ler_Luz()
{
  LuzCvalor = wb_distance_sensor_get_value(LuzC);
  LuzFvalor = wb_distance_sensor_get_value(LuzF);
  LuzTvalor = wb_distance_sensor_get_value(LuzT);
  LuzEvalor = wb_distance_sensor_get_value(LuzE);
  LuzDvalor = wb_distance_sensor_get_value(LuzD);
}

void ler_Bola()
{
int i;
char temp[20];
int maximo=0;
int indice;
double final=1.0;

//printf("\n");
  for (i=0;i<18;i++)
  {
    sprintf(temp, "SBola%d",i+1);
    SBolaValor[i] = (int)wb_light_sensor_get_value(SBola[i]);
//    printf("%3d ", SBolaValor[i]);

    if (SBolaValor[i]>maximo)
    {
      maximo=SBolaValor[i];
      indice=i+1;
    }
  }

  int temp1=SBolaValor[(18+indice-1-1)%18], temp2=SBolaValor[(18+indice-1+0)%18], temp3=SBolaValor[(18+indice-1+1)%18];
  if (temp1<temp3)
    final = (double)indice + ((double)(temp3-temp1)/(double)(temp2-temp1))/2.0;
  else
    if (temp1>temp3)
      final = (double)indice - ((double)(temp1-temp3)/(double)(temp2-temp3))/2.0;
  if(final>18.0)
    final-=18.0;
    

//printf("==Ind=%3d Final=%lf", indice, final);

  BOLAAng=10.0+(final-1.0)*20.0;
  while (BOLAAng> 360.0) BOLAAng-=360.0;    // não gosto, devia chamar a normaliza
  BOLAValor=maximo;
//printf("==BOLAAng=%lf", BOLAAng);
}

void andar(int direccao, int vel_linear, int vel_angular)
{
static int motor1, motor2, motor3;

  motor1=-vel_angular + (int)(0.5+(double)vel_linear*cos(( 30-direccao)*M_PI/180.0));
	motor2=-vel_angular + (int)(0.5+(double)vel_linear*cos((270-direccao)*M_PI/180.0));
	motor3=-vel_angular + (int)(0.5+(double)vel_linear*cos((150-direccao)*M_PI/180.0));
  wb_servo_set_velocity(wheels[0], (motor1>>1));
  wb_servo_set_velocity(wheels[1], (motor2>>1));
  wb_servo_set_velocity(wheels[2], (motor3>>1));
//  printf(" Mot[%3d, %3d, %3d] ",motor1>>1, motor2>>1, motor3>>1);
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
  Kicker        = wb_robot_get_device("kicker");
  SToque        = wb_robot_get_device("SToque");
  
  for (i=0;i<18;i++)
  {
    sprintf(temp, "SBola%d",i+1);
    SBola[i] = wb_robot_get_device(temp);
  }

  // enable sensores/actuators
  wb_servo_set_position(wheels[0], INFINITY);
  wb_servo_set_position(wheels[1], INFINITY);
  wb_servo_set_position(wheels[2], INFINITY);
  wb_servo_set_position(Kicker,    INFINITY);

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
//  wb_servo_enable_position(Kicker, TIME_STEP);
  wb_touch_sensor_enable(SToque, TIME_STEP);

  for (i=0;i<18;i++)
    wb_light_sensor_enable(SBola[i], TIME_STEP);

  wb_robot_keyboard_enable(TIME_STEP);
}

void le_sensores()
{
//  ler_sonares();
  ANG_BUSSOLA=ler_bussola();
  ler_gps(); // Isto é o equivalente à Localizacao
//  ler_Luz(); // Ainda não temos os 5 IV por baixo
  ler_Bola();
}

void corrige_vel_angular(double temp)
{
    if (temp>0)
    vel_angular=ACERTO_VEL_ANGULAR;
  else
    if (temp<0)
      vel_angular=-ACERTO_VEL_ANGULAR;
    else
      vel_angular=0;

}

void le_tecla_decide_comportamento(void)
{
    switch (wb_robot_keyboard_get_key())
    {
      case 'K': // Keeper - guarda-redes
                estado=10;
                wb_led_set(led[0],1);
                wb_led_set(led[1],0);
                wb_led_set(led[2],0);
              break;      
      case 'F': // Forward - Atacante
                estado= 1;
                wb_led_set(led[0],0);
                wb_led_set(led[1],1);
                wb_led_set(led[2],0);
              break;
      case 'C': //wb_servo_set_velocity(Kicker, 1);
                wb_servo_set_position(Kicker, 0.025);
                break;
      case ' ': //wb_servo_set_velocity(Kicker, 1);
                wb_servo_set_position(Kicker, 0);
              break;
    }
}
