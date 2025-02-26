#if !defined( ESP32 )
  #error This code is intended to run on the ESP32 platform! Please check your Tools->Board setting.
#endif

#include <Wire.h>                   // required by Omni3MD.cpp
#include <BnrOmni.h>

#include <SPI.h>
 #include "Arduino.h"
#include <DabbleESP32.h>

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


#define CUSTOM_SETTINGS
#define INCLUDE_GAMEPAD_MODULE
#define REMOTE_CONTROL // Uncomment if you want to control remotly via BT

//odometry parameters
#define SEN60 0.8660254038
#define COS60 0.5
#define To_mm 0.1112 //ticks to mm
#define To_rad 0.017453293 //ticks to mm

//commands for CMPS14 firmware
#define BEARING_Register 2 
#define PITCH_Register 4 
#define ROLL_Register 5

#define MAGNETX_Register  6
#define MAGNETY_Register  8
#define MAGNETZ_Register 10

#define ACCELEROX_Register 12
#define ACCELEROY_Register 14
#define ACCELEROZ_Register 16

#define GYROX_Register 18
#define GYROY_Register 20
#define GYROZ_Register 22

#define CALIB_Register 30

#define ONE_BYTE   1
#define TWO_BYTES  2
#define FOUR_BYTES 4
#define SIX_BYTES  6


//I2C communication address for OLED monitor
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
//OLED monitor resolution
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
 
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
 
//I2C communication pins for CMPS14 sensor 
#define CMPS14_Address 0x60
#define SDA_CMPS14 19
#define SCL_CMPS14 23
 
//I2C communication pins for OMNI driver
#define  SDA_OMNI 21
#define SCL_OMNI 22
#define OMNI3MD_ADDRESS 0x30

#define M1 1
#define M2 2
#define M3 3
//driblers driver control pins
#define IN1 13  
#define IN2 12
#define IN3 14  
#define IN4 27  
#define PWM1 16 // new board version 25
#define PWM2 17// new board version 26
#define ENABLE_DB 5
#define db1_channel 0
#define db2_channel 1

#define KICK 4

#define TIMER0_INTERVAL_MS        1000
#define TIMER0_DURATION_MS        0//5000

#define TIMER1_INTERVAL_MS        30
#define TIMER1_DURATION_MS        0//5000
#define PWM1_Ch 0
#define PWM2_Ch 1

#define LAST_COM_TIMEOUT        500
#define LED 5
//Declaration of object variable to control the Omni3MD
BnrOmni omni; 
//Declaration of object variable to communicate with CPS14 via I2C         
TwoWire CMPS14= TwoWire(1);
// Init ESP32 timer 0 and 1
 
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &CMPS14, OLED_RESET);


int serial_communication_time = 0;
int communication_time = 0;

//Actuation variables for OMNI
int linear_sp= 0;    // 0 to 100
int direction_sp= 0;   // 0 to 360
int rotational_sp=0; // -100 to 100

int omni_Kp = 0;
int omni_Ki = 0;
int omni_Kd = 0;

int last_enc1 = 0;
int last_enc2 = 0;
int last_enc3 = 0;

float omni_temperature = 0.0;
float omni_battery = 0.0;
  

//Actuation speed for dribler motors
int dribler1_vel= 0;   // 0 to 100  speed for motor 1 from dribler
int dribler2_vel= 0;    // 0 to 100

int maxKick = 35;
hw_timer_t *Kick_timer = NULL;
const int wdtTimeout = 3000;  //time in ms to trigger the watchdog

String command;
bool new_command=false;

bool negative=false;
int   count_KICK=0;
uint32_t currTime=0;
uint32_t InterruptTime=0;
bool Kick_end=false;

uint32_t last_communication_time=0;
uint32_t last_time=0;

int angle_reference=0;

bool send_package=false;


 
float accelScale = 9.80592991914f/1000.f; // 1 m/s^2

String up_str ="12,0,34,45,45";
String middle_str ="";

#ifdef REMOTE_CONTROL
  bool START=false;
  int speed_= 0;
  int direction_= 0;
  int rotational_=0;
  #endif
 
void InitOMNI(){
  byte _omniAddress = OMNI3MD_ADDRESS>>1;
 Wire.begin(21,22);
     delay(10);                          // pause 10 milliseconds

 omni.i2cConnect(OMNI3MD_ADDRESS);  // set i2c connection
    delay(10);                               
  omni.stop();                 // stops all motors
  delay(30);
  
  omni.setI2cTimeout(0); // safety parameter -> I2C communication must occur every [byte timeout] x 100 miliseconds for motor movement                             
  delay(20);                 // 5ms pause required for Omni3MD eeprom writing
                       // 5ms pause required for Omni3MD eeprom writing

  delay(1500);
  //Serial.println("OMNI initialized");

}


void InitCMPS14(){
  //CMPS14.setClock(400000);
  CMPS14.begin(SDA_CMPS14, SCL_CMPS14);  
  delay(20);
  //Serial.println("CMPS14 initialized");
}

void InitDriblers(){

  pinMode(IN1, OUTPUT); 
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  //pinMode(PWM1, OUTPUT);
  //pinMode(PWM2, OUTPUT);
  ledcSetup(db1_channel, 5000, 8);
  ledcSetup(db2_channel, 5000, 8);

  // Attach the channel 0 on the 3 pins
  ledcAttachPin(PWM1, db1_channel);
  ledcAttachPin(PWM2, db2_channel);
 
  
  digitalWrite(IN1, LOW);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(IN2, LOW);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(IN3, LOW);   // turn the LED on (HIGH is the voltage level)  
  digitalWrite(IN4, LOW);   // turn the LED on (HIGH is the voltage level)
 
   pinMode(ENABLE_DB, OUTPUT);
   digitalWrite(ENABLE_DB, HIGH);
  //add PWM pins
}

void Initkick(){
  pinMode(KICK, OUTPUT);
  digitalWrite(KICK, LOW);

    
}

void InitMonitor(){
// SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  // Show initial display buffer contents on the screen --
  // the library initializes this with an Adafruit splash screen.
  display.display();
  delay(2000); // Pause for 2 seconds
 
}
/*
void draw_table(void){

   Heltec.display->clear();
  Heltec.display->drawRect(0, 0, DISPLAY_WIDTH-2*0, 15);
  Heltec.display->drawVerticalLine(60, 0, 15);
  Heltec.display->display();
   
  //Serial.println("In here Cralho");
  Heltec.display->setTextAlignment(TEXT_ALIGN_LEFT);
  Heltec.display->setFont(ArialMT_Plain_10);
  Heltec.display->drawString(0, 0, up_str);
  Heltec.display->drawString(64, 0, middle_str);
  Heltec.display->display();  
  delay(2000);
}
*/
void setup() {
  //setup routines
  Serial.begin(115200);               // set baud rate to 115200bps for printing values in serial monitor. Press (ctrl+shift+m) after uploading
      Dabble.begin("Robot4_ESP");       //set bluetooth name of your device

   pinMode(LED,OUTPUT);
  InitOMNI();
  InitCMPS14();
  InitDriblers();
  Initkick();
  
  

   byte _byteHigh, _byteLow;
   int nReceived;
  int bear=0;
  signed char mrd, rol=0;
 // Begin communication with CMPS14
  CMPS14.beginTransmission(CMPS14_Address);

  // Tell register you want some data
  CMPS14.write(BEARING_Register);

   // End the transmission
  int nackCatcher = CMPS14.endTransmission();

  // Return if we have a connection problem 
  if(nackCatcher != 0){bear = 0; mrd = 0;  rol = 0; return;}
  
  // Request 4 bytes from CMPS14
  nReceived = CMPS14.requestFrom(CMPS14_Address , FOUR_BYTES);

  // Something has gone wrong
  if (nReceived != FOUR_BYTES) {bear = 0; mrd = 0;  rol = 0; return;}
 
  // Read the values
  _byteHigh = CMPS14.read(); 
  _byteLow = CMPS14.read();
  bear = ((_byteHigh<<8) + _byteLow) / 10;
 mrd = CMPS14.read();

  // Read the values
  rol = CMPS14.read();
  angle_reference=bear;
  //Serial.println(bear);
  delay(1000);
  
 // Heltec.begin(true /*DisplayEnable Enable*/, false /*LoRa Disable*/, false /*Serial Enable*/);
  //draw_table();
  InitMonitor();

  #ifdef REMOTE_CONTROL
    //Dabble.begin("Robot4_ESP");       //set bluetooth name of your device
    Serial.println("Entrou");
  #endif
}

void loop() {
  
  if(Kick_end){
    Kick_end=false;
    //Serial.print("kick Time:\t");
    //Serial.println(InterruptTime- currTime);
  }
  //send values of OMNI (battery, temperature); bussola(bearing);  
  if(send_package){
    send_package=false;
    
    SendPackage();
    

  }
  if(millis()-last_communication_time>LAST_COM_TIMEOUT)
  {
   // Serial.print("Commands TIMEOUT:\t\n");
    //omni.stop_motors();
    //.UpdateDriblerParameters(0,0);
    last_communication_time = millis();
  } 
  
  if(Serial.available()) {
  
    communication_time = millis();
    
    command = (String)Serial.readStringUntil('\n');
    //Serial.flush()

    new_command=true; 
    if(new_command){
      new_command=false;
      int i=0;
      last_communication_time = millis();

      switch(command[0]){
        case 'P':{   //case the first byte is P sets the omni control parameters                              
           
          String str_kp = GetValues(command, 1);
          String str_ki = GetValues(command, 2);
          String str_kd = GetValues(command, 3);
          Serial.print("\n  kp: ");Serial.print(str_kp);
          Serial.print("  ki: ");Serial.print(str_ki);
          Serial.print("  kd: ");Serial.println(str_kd);
                  

          SetOmniControl(str_kp.toInt(),str_ki.toInt(),str_kd.toInt());
        }
        break;
        case 'R':{   //case the first byte is P sets the omni control parameters                              
           
          String str_time = GetValues(command, 1);
          String str_slope = GetValues(command, 2);
          String str_kl = GetValues(command, 3);
          Serial.print("\n  time: ");Serial.print(str_time);
          Serial.print("  slope: ");Serial.print(str_slope);
          Serial.print("  kl: ");Serial.println(str_kl);
         omni.setRamp(str_slope.toInt(),str_kl.toInt());
        }
        break;
       
        case 'D':{    //case the first byt is W it controls only the rotational speed                              
           
          String db1 = GetValues(command, 1); 
          String db2 = GetValues(command, 2); 
         
          UpdateDriblerParameters(db1.toInt(),db2.toInt());
  
        }
        break;
        case 'M':{   //case the first byt is R it controls linear, rotational speed and direction                              
           
          String lin_aux = GetValues(command, 1); 
          String rot_aux = GetValues(command, 2); 
          String dir_aux = GetValues(command, 3); 
          
          UpdateOmniParameters(lin_aux.toInt(),rot_aux.toInt(),dir_aux.toInt());
  
        }
        break;
        default:    //by default the esp receives a package with the values for update
          String linear_vel = GetValues(command, 0);
          String rotat_vel = GetValues(command, 1);
          String direcao = GetValues(command, 2);
          
          String dribler1 = GetValues(command, 3);
          String dribler2 = GetValues(command, 4);
          
          String kick_time= GetValues(command, 5);       
          up_str =linear_vel+","+rotat_vel+","+direcao+","+dribler1+","+dribler2;
          UpdateOmniParameters(linear_vel.toInt(),rotat_vel.toInt(),direcao.toInt());
  
          UpdateDriblerParameters(dribler1.toInt(),dribler2.toInt());
  
          if (kick_time.toInt() > 0)
          {
            UpdateKickParameters(kick_time.toInt());
          }
        break;
      }
      
    }
   // draw_table();

  }

  #ifdef REMOTE_CONTROL
     Dabble.processInput();             //this function is used to refresh data obtained from smartphone.Hence calling this function is mandatory in order to get data properly from your mobile.
 
 
  bool STARTPRESED=false;
  if (GamePad.isStartPressed())
  {
    while(!STARTPRESED){STARTPRESED=GamePad.isStartPressed();}
    Serial.println("Start");
    START = START ? false:true;
    omni.movOmni(0,0,0);
  }
  if (START)
  { 
    //Serial.println("START");
    int angle = GamePad.getAngle(); 
       
    int vel = GamePad.getRadius();

    if (GamePad.isCirclePressed()){
      if(GamePad.isCirclePressed()==0);
      rotational_=10;
    }
    //Serial.println(GamePad.isSquarePressed());
    if (GamePad.isSquarePressed()){ 
      rotational_=-10;
    }
    if (GamePad.isTrianglePressed()){ 
      rotational_=0;
      //Serial.print("isTrianglePressed");
    }
    if (GamePad.isCrossPressed())
    {
      UpdateKickParameters(8);
      //Serial.print("isCrossPressed");
    }
     angle-=90;
    if (angle<0){
     angle+=360;
     
    }
  
    if (angle>=0 && angle <=360)
      direction_=angle;
   
    speed_=vel*10;
     
    if (speed_ <= 0){
      speed_=0;
    }
    if (speed_ > 90){
      speed_=100;
    }
    
    
    if(rotational_>90){
      rotational_=90;
    }
    
    if(rotational_<-90){
      rotational_=-90;
    }
    
    UpdateOmniParameters(speed_,rotational_,direction_);
    //omni.mov_omni(speed_,rotational_,direction_);
    }
  #endif
    //Serial.print(" time="  );
  //Serial.println(millis()-last_time);
  //last_time=millis();
}

void odometry(int robot_angle,int* xd, int* yd){
    // Degrees to Radians
    float  rad_y_angle=robot_angle*To_rad;
    float  rad_x_angle=(robot_angle-90)*To_rad;
    // Read Encoders
    int16_t  enc1=(int16_t)omni.readEnc1();                // read encoder1 count value for the defined prescaler (positional control)
    int16_t enc2=(int16_t)omni.readEnc2();                // read encoder1 count value for the defined prescaler (positional control)
    int16_t enc3=(int16_t)omni.readEnc3();                // read encoder1 count value for the defined prescaler (positional control)
       /*Serial.print("enc1:");
     Serial.print(enc1);           // prints encoder 1 positional value
     Serial.print(" enc2:");
     Serial.print(enc2);           // prints encoder 2 positional value
     Serial.print(" enc3:");
     Serial.println(enc3); */ 
    // Reset Encoders    
    omni.setEncValue(M1,0);
    omni.setEncValue(M2,0);
    omni.setEncValue(M3,0);
    // Delta Position Robot
    float  y_r = ((enc3-enc1)/(2*SEN60));
    float  x_r = (((enc2*2)-enc1-enc3)/(2*(COS60+1)));
     /*Serial.print(" X_R:");
     Serial.print(x_r);           // prints encoder 2 positional value
     Serial.print(" Y_R:");
     Serial.println(y_r); */
    // Delta Position Field
    *xd = (y_r*cos(rad_y_angle)+ x_r*cos(rad_x_angle))*To_mm;
    *yd = (y_r*sin(rad_y_angle)+ x_r*sin(rad_x_angle))*To_mm;
}
 
void UpdateOmniParameters(int lin, int rot, int dir){
  //linear velocity varies between 0 and 100
  linear_sp = (lin <= 100 && lin >= 0 )? lin : linear_sp;
  //rotational velocity varies between -100 and 100
  rotational_sp = (rot <= 100 && rot >= -100)? rot : rotational_sp ;
  //direction varies between 0 and 360
  direction_sp = (dir < 360 && dir >= 0)? dir : direction_;
 /* Serial.print("\nlin  ");  Serial.print(linear_sp);
  Serial.print("    rot  ");  Serial.print(rotational_sp );
  Serial.print("    dir  ");  Serial.println(direction_sp );
  */
  omni.movOmni(linear_sp ,rotational_sp ,direction_sp );

}

void UpdateDriblerParameters(int M1_, int M2_){
  //speed of the driblers can go from -100 to 100
  
  dribler1_vel= M1_;   // 0 to 100  speed for motor 1 from dribler
  dribler2_vel= M2_;  
  if(M1_ > 255){
    dribler1_vel=255;
  }
  else if(M1_ < -255){
    dribler1_vel=-255;    
  }
  if(M2_ > 255){
    dribler2_vel=255;
  }
  else if(M2_ < -255){
    dribler2_vel=-255;
  }
  

  if(M1_ >= 0){
    //digitalWrite(PWM1, HIGH);
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    //analogWrite(PWM1, (dribler1_vel));
    ledcWrite(db1_channel, dribler1_vel);
  }
  else if(M1_ < 0){
    //digitalWrite(PWM1, HIGH);
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    //analogWrite(PWM1, -dribler1_vel);
     ledcWrite(db1_channel, -dribler1_vel);
  } 
  
  if(M2_ >= 0){
    //digitalWrite(PWM2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    ledcWrite(db2_channel, dribler2_vel);
    //analogWrite(PWM2, (dribler2_vel));
    //analogWrite(PWM2, 255);
    //delay(10);
  }
  else if(M2_ < 0){
    //digitalWrite(PWM2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    //analogWrite(PWM2, -dribler2_vel);
    ledcWrite(db2_channel, -dribler2_vel);
    //delay(10);
  } 
  // set dribblers rotation direction
  /*digitalWrite(IN1, (M1_ >= 0 ? HIGH : LOW));      
  digitalWrite(IN2, (M1_ >= 0 ? LOW : HIGH));    

  digitalWrite(IN3, (M2_ >= 0 ? HIGH : LOW));    
  digitalWrite(IN4, (M2_ >= 0 ? LOW : HIGH));    
  //update PWM pin of L298N driver
  */

}
 
void UpdateKickParameters(int time_){
  //time_ should be 0 for no kick and 35 for maximum time kick
  if(time_>maxKick)
    time_ = maxKick;
  if(time_ < 0)
    time_ = 0;
 
   digitalWrite(KICK , HIGH);
  currTime = millis();
  //ITimer0.restartTimer();
  
}


void SetOmniControl(int Kp,int Ki,int Kd){
  omni_Kp = (Kp <= 100 && Kp >= 0 )? Kp : omni_Kp;
  omni_Ki = (Ki <= 100 && Ki >= 0 )? Ki : omni_Ki;
  omni_Kd = (Kd <= 100 && Kd >= 0 )? Kd : omni_Kd;

  //Serial.print("  kp: ");Serial.print(omni_Kp);
  //Serial.print("  ki: ");Serial.print(omni_Ki);
  //Serial.print("  kd: ");Serial.println(omni_Kd);
   omni.setPid(omni_Kp ,omni_Ki ,omni_Kd);
}

int x,y;
void SendPackage(){
  //send values of OMNI (battery, temperature); bussola(bearing); dribler(ON/OFF)
  int bearing;
  int nReceived;  
  float accel_x, accel_y;
  
  //Variables to read from Omni3MD
  int enc1=0;            // encoder1 reading, this is the encoder incremental count for the defined prescaler (positional control)
  int enc2=0;            // encoder2 reading, this is the encoder incremental count for the defined prescaler (positional control)
  int enc3=0;            // encoder3 reading, this is the encoder incremental count for the defined prescaler (positional control)
  float bat=0;       // battery reading
  float temp=0;   // temperature reading
  int dx, dy=0;

  ReadCMPS(&bearing);//, &accel_x, &accel_y
  //ReadOMNI(&enc1,&enc2,&enc3,&bat,&temp);
  odometry(bearing, &dx, &dy);
  bat=omni.readBattery(); 
  x+=dx;
  y+=dy;
  // Serial.print(" Sum"); Serial.print(x);Serial.print(" ");Serial.println(y);
  omni_temperature=temp;
  omni_battery=int(bat);

  middle_str="Bat:"+String(bat);
  
  
  String package = String(bearing)+","+ String((int)bat)+","+ String((int)temp)+","+ String(dx)+","+ String(dy);
  //Serial.println(String(bearing)+","+ String(pitch) +","+ String(roll));
  //Serial.println(sizeof(package));
  Serial.println(package);
}

String GetValues(String str, int index){
  int found = 0;
  int strIndex[] = {0, -1};
 
  for(int i=0; i<=(str.length()-1) && found<=index; i++){
    if(str.charAt(i)==',' || i==(str.length()-1)){
        found++;
        
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == (str.length()-1)) ? i+1 : i;
        //Serial.print(strIndex[0]);
        //Serial.print('\t');
        //Serial.println(strIndex[1]);
    }
  }
  
  return found>index ? str.substring(strIndex[0], strIndex[1]) : "";
}

void ReadAccelerator(float *accel_X, float *accel_Y)
{
  byte _byteHigh;
  byte _byteLow;
  float accelX = 0;
  float accelY = 0;
  float accelZ = 0;
  // Begin communication with CMPS14
  CMPS14.beginTransmission(CMPS14_Address);

  // Tell register you want some data
  CMPS14.write(ACCELEROX_Register);

  // End the transmission
  int nackCatcher = CMPS14.endTransmission();

  // Return if we have a connection problem 
  if(nackCatcher != 0){accelX = 0; accelY = 0; accelZ = 0; return;}
  
  // Request 6 bytes from CMPS14
  int nReceived = CMPS14.requestFrom(CMPS14_Address , SIX_BYTES);

  // Something has gone wrong
  if (nReceived != SIX_BYTES) {accelX = 0; accelY = 0; accelZ = 0; return;}
  
  // Read the values
  _byteHigh = CMPS14.read(); _byteLow = CMPS14.read();
  accelX = (((int16_t)_byteHigh <<8) + (int16_t)_byteLow) * accelScale;

  // Read the values
  _byteHigh = CMPS14.read(); _byteLow = CMPS14.read();
  accelY = (((int16_t)_byteHigh <<8) + (int16_t)_byteLow) * accelScale;

  // Read the values
  _byteHigh = CMPS14.read(); _byteLow = CMPS14.read();
  accelZ = (((int16_t)_byteHigh <<8) + (int16_t)_byteLow) * accelScale;
  *accel_X=accelX;
  *accel_Y=accelY;
  // Serial.print("accelX    ");   Serial.println(accelX);    
  // Serial.print("                         accelY     ");Serial.println(accelY);
}

void getBearing(int *bearing_)
{
  byte _byteHigh;
  byte _byteLow;
  int bearing , bearing_aux; 
  // Begin communication with CMPS14
  CMPS14.beginTransmission(CMPS14_Address);

  // Tell register you want some data
  CMPS14.write(BEARING_Register);
  

  // End the transmission
  int nackCatcher = CMPS14.endTransmission();

  // Return if we have a connection problem 
  if(nackCatcher != 0){return  ;}
 
  // Request 2 bytes from CMPS14
  int nReceived = CMPS14.requestFrom(CMPS14_Address , TWO_BYTES);

  // Something has gone wrong
  if (nReceived != TWO_BYTES) return ;

  // Read the values
  _byteHigh = CMPS14.read(); 
  _byteLow = CMPS14.read();

  // Calculate full bearing
  bearing = ((_byteHigh<<8) + _byteLow) / 10;
   
  
  if(bearing-angle_reference<0){
      bearing_aux = 360+(bearing-angle_reference);
  }
  else{
    bearing_aux =  bearing-angle_reference;
  }
  
  if (bearing_aux > 180){
    *bearing_ = -(bearing_aux -360);
  }
  else{
    *bearing_ = -bearing_aux; 
  }
}
void ReadCMPS(int *bearing_){//, float *accel_X, float *accel_Y
  //getBearing(bearing_);
  //ReadAccelerator(accel_X, accel_Y);
byte _byteHigh;
  byte _byteLow;
  int bearing , bearing_aux; 
  // Begin communication with CMPS14
  CMPS14.beginTransmission(CMPS14_Address);

  // Tell register you want some data
  CMPS14.write(BEARING_Register);
  

  // End the transmission
  int nackCatcher = CMPS14.endTransmission();

  // Return if we have a connection problem 
  if(nackCatcher != 0){return  ;}
 
  // Request 2 bytes from CMPS14
  int nReceived = CMPS14.requestFrom(CMPS14_Address , TWO_BYTES);

  // Something has gone wrong
  if (nReceived != TWO_BYTES) return ;

  // Read the values
  _byteHigh = CMPS14.read(); 
  _byteLow = CMPS14.read();

  // Calculate full bearing
  bearing = ((_byteHigh<<8) + _byteLow) / 10;
   
  
  if(bearing-angle_reference<0){
      bearing_aux = 360+(bearing-angle_reference);
  }
  else{
    bearing_aux =  bearing-angle_reference;
  }
  
  if (bearing_aux > 180){
    *bearing_ = -(bearing_aux -360);
  }
  else{
    *bearing_ = -bearing_aux; 
  }
}


void ReadOMNI(int *enc1,int *enc2,int *enc3,float *bat,float *temp){
 
  omni.readMovData(enc1,enc2,enc3,bat,temp);
  
}



/*void ReadCMPS(int *bearing_, signed char *pitch_, signed char *roll_){
  byte _byteHigh, _byteLow;
  int bearing, bearing_aux;
  int nReceived;
  signed char pitch;
  signed char roll;

  // Begin communication with CMPS14
  CMPS14.beginTransmission(CMPS14_Address);

  // Tell register you want some data
  CMPS14.write(BEARING_Register);

   // End the transmission
  int nackCatcher = CMPS14.endTransmission();

  // Return if we have a connection problem 
  if(nackCatcher != 0){bearing = 0; pitch = 0;  roll = 0; return;}
  
  // Request 4 bytes from CMPS14
  nReceived = CMPS14.requestFrom(CMPS14_Address , FOUR_BYTES);

  // Something has gone wrong
  if (nReceived != FOUR_BYTES) {bearing = 0; pitch = 0;  roll = 0; return;}
 
  // Read the values
  _byteHigh = CMPS14.read(); 
  _byteLow = CMPS14.read();
  bearing = ((_byteHigh<<8) + _byteLow) / 10;

  // Read the values
  pitch = CMPS14.read();

  // Read the values
  roll = CMPS14.read();

   if(bearing-angle_reference<0){
      bearing_aux = 360+(bearing-angle_reference);
    }
   else
 {
  bearing_aux =  bearing-angle_reference;
 }

 if (bearing_aux > 180){
  *bearing_ = -(bearing_aux -360);
  }
  else{*bearing_ = -bearing_aux; }
   //*bearing_ = bearing;
  *pitch_ = pitch;

  
  *roll_ = roll;
  
 /* Serial.print(bearing);
  Serial.print('\t');
  Serial.print( roll);
    Serial.print('\t');
  Serial.println(pitch);
  
}*/
