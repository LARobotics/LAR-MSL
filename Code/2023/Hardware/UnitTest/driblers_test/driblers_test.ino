#define IN1 13  
#define IN2 12
#define IN3 14  
#define IN4 27  
#define PWM1 16 // new board version 25
#define PWM2 17// new board version 26


void InitDriblers(){

  pinMode(IN1, OUTPUT); 
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(PWM1, OUTPUT);
  pinMode(PWM2, OUTPUT);

  digitalWrite(IN1, LOW);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(IN2, LOW);   // turn the LED on (HIGH is the voltage level)
  digitalWrite(IN3, LOW);   // turn the LED on (HIGH is the voltage level)  
  digitalWrite(IN4, LOW);   // turn the LED on (HIGH is the voltage level)
  //digitalWrite(PWM1, HIGH);   // turn the LED on (HIGH is the voltage level)  
  //digitalWrite(PWM2, HIGH);   // turn the LED on (HIGH is the voltage level)
 
  //Serial.println("Dribblers initialized");
pinMode(5, OUTPUT);

  digitalWrite(5, HIGH);   // turn the LED on (HIGH is the voltage level)
  
  //add PWM pins
}


void UpdateDriblerParameters(int M1_, int M2_){
  //speed of the driblers can go from -100 to 100
  
  int dribler1_vel= M1_;   // 0 to 100  speed for motor 1 from dribler
  int dribler2_vel= M2_;  
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
      
  }
  else if(M1_ < 0){
    //digitalWrite(PWM1, HIGH);
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
   // analogWrite(PWM1, -dribler1_vel);
     
  } 
  
  if(M2_ >= 0){
    //digitalWrite(PWM2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    //analogWrite(PWM2, (dribler2_vel));
    //analogWrite(PWM2, 255);
    //delay(10);
  }
  else if(M2_ < 0){
    //digitalWrite(PWM2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    //analogWrite(PWM2, -dribler2_vel);

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
 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);               // set baud rate to 115200bps for printing values in serial monitor. Press (ctrl+shift+m) after uploading
  
  InitDriblers();

}

void loop() {
  // put your main code here, to run repeatedly:
UpdateDriblerParameters(100,100);
delay(20);
}
