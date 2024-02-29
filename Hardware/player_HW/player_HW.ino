#if !defined( ESP32 )
  #error This code is intended to run on the ESP32 platform! Please check your Tools->Board setting.
#endif

#include <Wire.h>                   // required by Omni3MD.cpp
#include <BnrOmni.h>
#include <string.h>
#include <SPI.h>
#include "Arduino.h"
#include <DabbleESP32.h>
#include <Timeout.h>

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


#define CUSTOM_SETTINGS
#define INCLUDE_GAMEPAD_MODULE
#define REMOTE_CONTROL // Uncomment if you want to control remotly via BT

//odometry constants
#define SEN60 0.8660254038
#define COS60 0.5
#define To_mm 0.1112 //ticks to mm
#define To_rad 0.017453293 //ticks to mm

//I2C commands for CMPS14 sensor
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

//I2C communication pins for CMPS14 sensor 
#define CMPS14_Address 0x60
#define SDA_CMPS14 19
#define SCL_CMPS14 23


//I2C communication address for display
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels

#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)


//I2C communication pins for OMNI driver
#define  SDA_OMNI 21
#define SCL_OMNI 22
//I2C communication address for OMNI driver
#define OMNI3MD_ADDRESS 0x30
#define OMNI_COM_TIMEOUT 0

//OMNI motors constants
#define M1 1
#define M2 2
#define M3 3


//driblers control pins
#define IN2 12  //direction of rotation control for motor A
#define IN1 14  //direction of rotation control for motor A
#define IN3 16  //direction of rotation control for motor B
#define IN4 13  //direction of rotation control for motor B
#define PWM1 17 //PWM to control speed of motor A
#define PWM2 27 //PWM to control speed of motor B
#define ADC12 37  //ADC 12 V
#define ADC24 36  //ADC 24 V

#define ENABLE_DB 5 //3.3V power for gpio control
#define db1_channel 0
#define db2_channel 1

//Kick pin
#define KICK 4

#define TIMER0_INTERVAL_MS        1000
#define TIMER0_DURATION_MS        0//5000

#define TIMER1_INTERVAL_MS        30
#define TIMER1_DURATION_MS        0//5000
#define PWM1_Ch 0
#define PWM2_Ch 1

#define LAST_COM_TIMEOUT        50
#define LED 5



//Declaration of object variable to control the Omni3MD
BnrOmni omni; 
 
//Declaration of object variable to communicate with CPS14 via I2C         
TwoWire CMPS14= TwoWire(1);
 
//#define SCREEN_WIDTH 128 // OLED display width, in pixels
//#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &CMPS14, OLED_RESET);

#define NUMFLAKES     10 // Number of snowflakes in the animation example

#define LOGO_HEIGHT   16
#define LOGO_WIDTH    16


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
 
bool negative=false;
int   count_KICK=0;
uint32_t currTime=0;
uint32_t InterruptTime=0;
bool Kick_end=false;

uint32_t last_communication_time=0;
uint32_t last_time=0;

int angle_reference=0;

bool send_package=false;
/*
  *
  ball_possession_stage defines the distance between ball and dribblers
  0 -> no distance between ball and rollerback (inside dribblers)
  1 -> ball entering in dribblers
  2 -> ball completely out of dribblers
  *
*/

int ball_possession_stage=0;
 
float accelScale = 9.80592991914f/1000.f; // 1 m/s^2

String up_str ="12,0,34,45,45,0";
String bat_str ="";

String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete

Timeout omni_com_timeout;
bool omni_com_failure=false;

#ifdef REMOTE_CONTROL
  bool START=false;
  int speed_= 0;
  int direction_= 0;
  int rotational_=0;
  #endif
 
void InitOMNI(){
  byte _omniAddress = OMNI3MD_ADDRESS>>1;
  Wire.begin(SDA_OMNI,SCL_OMNI);
  delay(10);                          // pause 10 milliseconds
   omni.i2cConnect(OMNI3MD_ADDRESS);  // set i2c connection
  delay(10);                               
   omni.stop();                 // stops all motors
  delay(30);
   omni.setI2cTimeout(OMNI_COM_TIMEOUT); // safety parameter -> I2C communication must occur every [byte timeout] x 100 miliseconds for motor movement                             
  delay(20);                 // 5ms pause required for Omni3MD eeprom writing
                       // 5ms pause required for Omni3MD eeprom writing
  omni.setMinBat(9.7);
 // Serial.println("aqui4");
  delay(10);
  omni.setPid(1000, 50, 0);
  delay(10);
  omni.setRamp(50, 1000);
  delay(10);
 
}


void InitCMPS14(){
 
  CMPS14.begin(SDA_CMPS14, SCL_CMPS14);  
  //CMPS14.setTimeout(10000);
 
  delay(20);

}

void InitDriblers(){

  pinMode(IN1, OUTPUT); 
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(PWM1, OUTPUT);
  pinMode(PWM2, OUTPUT);
  //ledcSetup(db1_channel, 5000, 8);
  //ledcSetup(db2_channel, 5000, 8);

  // Attach the channel 0 on the 3 pins
  //ledcAttachPin(PWM1, db1_channel);
   //ledcAttachPin(PWM2, db2_channel);
 
  
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
// Clear the buffer
  ledcSetup(5, 1500, 8);

  // Attach the channel 0 on the 3 pins
  ledcAttachPin(26, 5);
  ledcWrite(5, 0);
 if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
  

  // Show initial display buffer contents on the screen --
  // the library initializes this with an Adafruit splash screen.
  display.display();
  delay(20); // Pause for 2 seconds

 
}
 
 
 
void setup() {
  //setup routines
  Serial.begin(115200);               // set baud rate to 115200bps for printing values in serial monitor. Press (ctrl+shift+m) after uploading
  Dabble.begin("Robot4_ESP");       //set bluetooth name of your device
  
  inputString.reserve(150);
  pinMode(LED,OUTPUT);
 
  InitDriblers();
  InitOMNI();
  InitCMPS14();
  Initkick();
  InitMonitor();

  getBearingReference();
 Serial.println("End Of Setup");
  #ifdef REMOTE_CONTROL
     Serial.println("Entrou");
  #endif
}

 
String GetLastCommand(String& buffer) {
  // Split the incoming serial data into individual commands using '\n' as the delimiter
  int last_index = buffer.lastIndexOf('\n');
  if (last_index == -1) {
    // No complete commands in the buffer yet
    return "";
  }
  bool char_found=false;
  char caracter;
  int first_index=last_index;
  while (!char_found && first_index>=0){//(caracter) <  65 && (caracter) > 90)
    
    caracter=buffer.charAt(first_index);
    if(isAlpha(caracter)){
      char_found=true;
     
    }
    first_index--;
  }
  first_index++;
  if (!char_found || (last_index-first_index>24)){
    return "";
  }
  //Serial.print("\n\nfirst_index:  ");Serial.print(first_index);
  //Serial.print("  last_index  ");Serial.println(last_index);
  
  String last_command = buffer.substring(first_index,last_index + 1);
 // last_command.remove(last_index + 1);
   //Serial.print("last_command:  ");Serial.println(last_command);
  // Return the last command if it is valid (i.e., starts with a letter and ends with '\n')
  
  if (last_command.length() > 1 && isAlpha(last_command.charAt(0)) && last_command.charAt(last_command.length() - 1) == '\n') {
    //Serial.println("return last_command ");
    return last_command;
  } else {
    //Serial.println("return \"\"  ");Serial.println(int(last_command.charAt(last_command.length() - 1)));
    return "";
  }
 }
String get_last_command(String input) {
  int last_newline_index = input.lastIndexOf("\n");
  if (last_newline_index >= 0) {
    return input.substring(last_newline_index + 1);
  } else {
    return "";
  }
}
void loop() {
 
   UpdateTableMonitor();
  if(Kick_end){
    Kick_end=false;
    //Serial.print("kick Time:\t");
    //Serial.println(InterruptTime- currTime);
  }
   
  if(millis()-last_communication_time>LAST_COM_TIMEOUT)
  {
   // Serial.print("Commands TIMEOUT:\t\n");
    //omni.stop_motors();
    //.UpdateDriblerParameters(0,0);
    SendPackage();
    last_communication_time = millis();
 
  } 
  
  if(stringComplete) {
    stringComplete=false;
    communication_time = millis();
    
    command = GetLastCommand(inputString);//GetLastCommand(inputString);
      
    if(command!=""){
      int i=0;
      last_communication_time = millis();
    
      switch(command[0]){
        case 'p':
        case 'P' :{   //case the first byte is P sets the omni control parameters                              
           
          String str_kp = GetValues(command, 1);
          String str_ki = GetValues(command, 2);
          String str_kd = GetValues(command, 3);
          Serial.print("\n  kp: ");Serial.print(str_kp);
          Serial.print("  ki: ");Serial.print(str_ki);
          Serial.print("  kd: ");Serial.println(str_kd);
                  

          SetOmniControl(str_kp.toInt(),str_ki.toInt(),str_kd.toInt());
        }
        break;
        case 'r':
        case 'R' :{   //case the first byte is P sets the omni control parameters                              
           
          String str_time = GetValues(command, 1);
          String str_slope = GetValues(command, 2);
          String str_kl = GetValues(command, 3);
          Serial.print("\n  time: ");Serial.print(str_time);
          Serial.print("  slope: ");Serial.print(str_slope);
          Serial.print("  kl: ");Serial.println(str_kl);
          omni.setRamp(str_slope.toInt(),str_kl.toInt());
        }
        break;
        case 'd':
        case 'D' :{    //case the first byt is W it controls only the rotational speed                              
           
          String db1 = GetValues(command, 1); 
          String db2 = GetValues(command, 2); 
         
          UpdateDriblerParameters(db1.toInt(),db2.toInt());
  
        }
        break;
        case 'm':
        case 'M' :{   //case the first byt is R it controls linear, rotational speed and direction                              
           
          String lin_aux = GetValues(command, 1); 
          String rot_aux = GetValues(command, 2); 
          String dir_aux = GetValues(command, 3); 
          
          UpdateOmniParameters(lin_aux.toInt(),rot_aux.toInt(),dir_aux.toInt());
  
        }
        break;
        case 'c':
        case 'C':{    //by default the esp receives a package with the values for update
          String linear_vel = GetValues(command, 1);
          String rotat_vel = GetValues(command, 2);
          String direcao = GetValues(command, 3);
          
          String dribler1 = GetValues(command, 4);
          String dribler2 = GetValues(command, 5);
          
          String kick_time= GetValues(command, 6);  
              
          UpdateOmniParameters(linear_vel.toInt(),rotat_vel.toInt(),direcao.toInt());
         /* Serial.print("\n  linear_vel: ");Serial.print(linear_vel);
          Serial.print("  rotat_vel: ");Serial.print(rotat_vel);
          Serial.print("  direcao: ");Serial.println(direcao);
          Serial.print("\n  dribler1: ");Serial.print(dribler1);
          Serial.print("  dribler2: ");Serial.print(dribler2);
          Serial.print("  kick_time ");Serial.println(kick_time);*/
          UpdateDriblerParameters(dribler1.toInt(),dribler2.toInt());
          if (kick_time.toInt() > 0)
          {
            UpdateKickParameters(kick_time.toInt());
          }
           
         }
        break;
        default:
        break;
      }
      
    }
  



 
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
      rotational_=5;
    }
    //Serial.println(GamePad.isSquarePressed());
    if (GamePad.isSquarePressed()){ 
      rotational_=-5;
    }
    if (GamePad.isTrianglePressed()){ 
      rotational_=0;
      //Serial.print("isTrianglePressed");
    }
    if (GamePad.isCrossPressed())
    {
      UpdateKickParameters(8);
      UpdateDriblerParameters(0,0);
      //Serial.print("isCrossPressed");
    }
    if (GamePad.isUpPressed())
    {
        angle = 90;
        vel = 100;
    }
    if (GamePad.isDownPressed())
    {
        angle = -90;
        vel = 100;
    }
    if (GamePad.isRightPressed())
    {
        angle = 180;
        vel = 100;
    }
    if (GamePad.isLeftPressed())
    {
        angle = 0;
        vel = 100;
    }
    if (GamePad.isSelectPressed())
    {
      UpdateDriblerParameters(255,255);
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

  //String package = String(speed_) + " "  + String(rotational_) + " " + String(direction_) + "\t";
  //Serial.println(package);
}
 
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      //Serial.print(inputString.length());
      if (inputString.length()>150){
        inputString="";
        Serial.flush();
      }else{
        stringComplete = true;
      }
    }  
  }
}
void odometry(int robot_angle,int* xd, int* yd){
    // Degrees to Radians
    float  rad_y_angle=robot_angle*To_rad;
    float  rad_x_angle=(robot_angle-90)*To_rad;
    // Read Encoders
   // omni_com_timeout.start(30);
     int16_t  enc1=0;                
    int16_t enc2=0;                 
    int16_t enc3=0;                 
    int start = millis(); 
  
    enc1=(int16_t)omni.readEnc1();                // read encoder1 count value for the defined prescaler (positional control)
    //Serial.println(!omni_com_timeout.time_over());
   // Serial.print("read odometry0.5=  ");Serial.println(millis()-start); 
    //if(!omni_com_timeout.time_over()){
     // omni_com_failure=false;
      enc2=(int16_t)omni.readEnc2();                // read encoder1 count value for the defined prescaler (positional control)
    //}else{
    ///  omni_com_failure=true;
    //}
    //Serial.println(!omni_com_timeout.time_over());
    //if(!omni_com_timeout.time_over()){
    //  omni_com_failure=false;
      enc3=(int16_t)omni.readEnc3();                // read encoder1 count value for the defined prescaler (positional control)
    ////}else{
     // omni_com_failure=true;
    //}
   // Serial.print("read odometry=  ");Serial.println(millis()-start); 
    start = millis(); 
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
     
        


      start = millis(); 
    
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
    linear_sp = (lin <= 100 && lin >= 0 ) ? lin : linear_sp;
    //rotational velocity varies between -100 and 100
    rotational_sp = (rot <= 100 && rot >= -100)? rot : rotational_sp ;
    //direction varies between 0 and 360
    direction_sp = (dir < 360 && dir >= 0)? dir : direction_;
    /*Serial.print("\nlin  ");  Serial.print(linear_sp);
    Serial.print("    rot  ");  Serial.print(rotational_sp );
    Serial.print("    dir  ");  Serial.println(direction_sp );*/
    
   
    omni.movOmni(linear_sp ,rotational_sp ,direction_sp );
 
}
void UpdateDriblerParameters(int M1_, int M2_){
  //speed of the driblers can go from -100 to 100
  
  dribler1_vel= M1_;   // 0 to 100  speed for motor 1 from dribler
  dribler2_vel= M2_;  
  if(M1_ > 100){
    dribler1_vel=100;
  }
  else if(M1_ < -100){
    dribler1_vel=-100;    
  }
  if(M2_ > 100){
    dribler2_vel=100;
  }
  else if(M2_ < -100){
    dribler2_vel=-100;
  }
  

  if(M1_ >= 0){
    //digitalWrite(PWM1, HIGH);
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(PWM1, (dribler1_vel*2.5));
    //ledcWrite(db1_channel, dribler1_vel);
  }
   else if(M1_ < 0){
    //digitalWrite(PWM1, HIGH);
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    analogWrite(PWM1, -dribler1_vel*2.5);
    //ledcWrite(db1_channel, -dribler1_vel);
  } 
  
  if(M2_ >= 0){
    //digitalWrite(PWM2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    //Serial.println("OURUOUTOTU  ");
   // ledcWrite(db2_channel, dribler2_vel);
    analogWrite(PWM2, (dribler2_vel));
    //analogWrite(PWM2, 255);
    //delay(10);
  } 
  else if(M2_ < 0){
    //digitalWrite(PWM2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(PWM2, -dribler2_vel);
   // ledcWrite(db2_channel, -dribler2_vel);
    //delay(10);
  } 
  //Serial.print(dribler1_vel);Serial.println("   ");Serial.print(dribler2_vel);  
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
 delay(time_);
   digitalWrite(KICK , LOW);
  
}


void SetOmniControl(int Kp,int Ki,int Kd){
  omni_Kp = (Kp <= 1000 && Kp >= 0 )? Kp : omni_Kp;
  omni_Ki = (Ki <= 1000 && Ki >= 0 )? Ki : omni_Ki;
  omni_Kd = (Kd <= 1000 && Kd >= 0 )? Kd : omni_Kd;

  //Serial.print("  kp: ");Serial.print(omni_Kp);
  //Serial.print("  ki: ");Serial.print(omni_Ki);
  //Serial.print("  kd: ");Serial.println(omni_Kd);
   omni.setPid(omni_Kp ,omni_Ki ,omni_Kd);
}

void UpdateTableMonitor(void) {
  display.clearDisplay();
  char buffer [15];
  int16_t i;
  static bool blink;
  uint16_t adc12v = analogRead(ADC12);
  uint16_t adc24v = analogRead(ADC24);
  float voltage12v = (float(adc12v))/10;
  float voltage24v = (float(adc24v))/10;
  //Serial.println(adc12v);
  static int mean12v=26;
  mean12v =mean12v*0.95 +map(voltage12v,100.0,140.0,0.0,100.0)*0.05; 
  static int mean24v=26;
  mean24v =mean24v*0.95 +map(voltage24v,200.0,252.0,0.0,100.0)*0.05; 
  static int soundcount12v =0;
  if((mean12v<=-50 &&  mean24v>20) || (mean24v<=-50 &&  mean12v>20) ||(mean24v<=-50 &&  mean12v<=-50)){
        ledcWrite(5, 0);
    }
  else if(mean12v<=20 || mean24v<=20){ // 
       soundcount12v++;
    if(mean12v<=5 || mean24v<=5){


      if(soundcount12v<5){
        ledcWrite(5, 125);

          } 
      if(soundcount12v>5){
        ledcWrite(5, 0);  
      }
      if(soundcount12v>10){
        soundcount12v=0;}
    }
    else if(mean12v<=10|| mean24v<=10){

      if(soundcount12v<15){
        ledcWrite(5, 125);

          } 
      if(soundcount12v>15){
        ledcWrite(5, 0);  
      }
      if(soundcount12v>30){
        soundcount12v=0;}
      //Serial.println("Entrou");      
    }else{
      if(soundcount12v<30){
        ledcWrite(5, 125);

          } 
      if(soundcount12v>30){
        ledcWrite(5, 0);  
      }
      if(soundcount12v>60){
        soundcount12v=0;}
    }
    
  }else{ ledcWrite(5, 0);  }





  display.clearDisplay();

  display.setTextSize(1);      // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_INVERSE); // Draw white text4
  // Linha 1
  display.setCursor(0, 0);     // Start at top-left corner
  display.cp437(true);         // Use full 256 char 'Code Page 437' font
  //const char* to_print="24V:"+map(voltage,100.0,140.0,0.0,100.0)+"%";
  char buffer24[20];
  sprintf(buffer24, "24V:%d%%", mean24v);
  display.write(buffer24);
  display.setCursor(53, 0);
  char buffer12[20];
  sprintf(buffer12, "12V:%d%%", mean12v);
  display.write(buffer12);
  
  
  if(blink){
    display.fillRect(104, 0, 15, 8, SSD1306_WHITE);
    blink=false; 
  }

  else{
    display.drawRect(104, 0, 15, 8, SSD1306_WHITE);
    blink=true; 
  }
 
  // Linha 2
  display.setCursor(0, 8);     
  display.setTextColor(SSD1306_WHITE);
  display.write("P:-1000");
  display.setCursor(48, 8);     
  display.write("-1000");
  display.setCursor(82, 8);     
  display.write("A:-180");
  
  //Linha 3
  display.setCursor(0, 16);     
  display.setTextColor(SSD1306_WHITE);
  itoa (linear_sp,buffer,10);
  display.write("V:");
  display.write(buffer);

  display.setCursor(42, 16);     
  itoa (direction_sp,buffer,10);
  display.write("D:");  
  display.write(buffer);   
  
  display.setCursor(82, 16);     
  itoa (rotational_sp,buffer,10);
  display.write("R:");
  display.write(buffer);
  //display.write(uint16_t(rotational_sp));
   //Linha 4

  display.setCursor(0, 24);     
  itoa (dribler1_vel,buffer,10);
  display.write("DL:");
  display.write(buffer);
  display.setCursor(46, 24);     
  itoa (dribler2_vel,buffer,10);
  display.write("DR:");
  display.write(buffer);
  display.setCursor(96, 24);
  display.write("Cap:");
  display.write(buffer);
  //Linha Capacitors 
  display.drawRect(121, 0, 7, 32, SSD1306_WHITE);
  display.display();
  
 

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
  int start = millis();
  ReadCMPS(&bearing);//, &accel_x, &accel_y
  //ReadOMNI(&enc1,&enc2,&enc3,&bat,&temp);
   odometry(bearing, &dx, &dy);
   bat=omni.readBattery(); 
   //Serial.print(bat);
  x+=dx;
  y+=dy;
  // Serial.print(" Sum"); Serial.print(x);Serial.print(" ");Serial.println(y);
  omni_temperature=temp;
  omni_battery=bat;

   
  
  String package = String(bearing)+","+ String(int(bat))+","+ String((int)temp)+","+ String(dx)+","+ String(dy);//+","+ String(ball_possession_stage);
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


void getBearingReference(){
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
  // delay(10);
  
}
