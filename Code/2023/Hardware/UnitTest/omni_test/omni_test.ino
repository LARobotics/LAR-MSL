#include <BnrOmni.h>

/*
 Omni-3MD 3 motor controller from botnroll.com http://www.botnroll.com/en/controllers/84-bot-n-roll-omni-3md-.html
  
 Read data from Omni-3MD:
 - this code assumes you are using 1,2 or 3 DC motors with encoders attached to Omni3MD board;
 - this example was developed using Arduino 1.7.10 open-source Arduino environment
 - this example is compatible with Omni3MD firmware version 1.74 or higher. Visit http://www.botnroll.com/omni3md/ to check if your version is updated.

Purpose:
 This example demonstrates all routines for reading values from Omni3MD.
 You can read a single value in a single I2C request.
 You can read multiple values in a single I2C request.
 Multiple values can be read in one I2C request, for example, to read all three encoders at once. 
 This increases precision and communication is faster than reading values in three I2C requests.
 Values are printed in the serial monitor. Press (ctrl+shift+m) after uploading to open the serial monitor.
 

 Omni3MD board features: 
 - Holonomic movement integrated control for 3 motors with PID control;
 - Diferencial movement (SI units) with PID control;
 - Linear movement of 3 independent motors with or without PID control;
 - Position control of 3 motors using motor encoders.
 - Encoder reading;
 - Battery reading;
 - Temperature reading;
 
 The circuit:
 * Omni3MD board attached to Arduino analog input 4 (SDA) and 5 (SCL), GND and 5V DC.
 
 This example was created by José Cruz (www.botnroll.com)
 on 26 September 2012
 Updated on 17 January 2017

 This code example is in the public domain. 
 http://www.botnroll.com
*/
   
#include <Wire.h>                   //required by BnrOmni.cpp
 
//constants definitions
#define OMNI3MD_ADDRESS 0x30        //default factory address

BnrOmni omni;                       //declaration of object variable to control the Omni3MD

/*** variable declarations ***/
//Variables to read from Omni3MD
int enc1=0;            // encoder1 reading, this is the encoder incremental count for the defined prescaler (positional control)
int enc2=0;            // encoder2 reading, this is the encoder incremental count for the defined prescaler (positional control)
int enc3=0;            // encoder3 reading, this is the encoder incremental count for the defined prescaler (positional control)
float battery=0.0;     // battery reading
float temperature=0.0; // temperature reading
float firmware=0.0;    // the firmware version of your Omni3MD board (visit http://www.botnroll.com/omni3md/ to check if your version is updated)
byte firm_int=0;       // the firmware version of your Omni3MD board (visit http://www.botnroll.com/omni3md/ to check if your version is updated)
byte firm_dec=0;       // the firmware version of your Omni3MD board (visit http://www.botnroll.com/omni3md/ to check if your version is updated)
byte firm_dev=0;       // the firmware version of your Omni3MD board (visit http://www.botnroll.com/omni3md/ to check if your version is updated)
byte ctrl_rate=0;      // the control rate for your motors defined at calibration (in times per second)
int enc1_max;          // maximum count for encoder 1 at calibration, for the defined control rate
int enc2_max;          // maximum count for encoder 2 at calibration, for the defined control rate
int enc3_max;          // maximum count for encoder 3 at calibration, for the defined control rate
int limiar1=0;         // Necessary motor M1 power to start movement. Acquired during motors calibration.
int limiar2=0;         // Necessary motor M2 power to start movement. Acquired during motors calibration.
int limiar3=0;         // Necessary motor M3 power to start movement. Acquired during motors calibration.

void setup()
{
    //setup routines
    delay(1500);                       // wait electronics to stabilize
    Serial.begin(115200);
    Wire.begin(21,22);// set baud rate to 57600bps for printing values on serial monitor. Press (ctrl+shift+m) after uploading
    omni.i2cConnect(OMNI3MD_ADDRESS);  // set i2c connection
    omni.stop();                       // stop all motors
}

void loop()
{
  /**reading a single value in a single request**/
    //read and print static values that don't change while program runs
      firmware=omni.readFirmware();      // read Omni-3MD firmware version
      Serial.print("Firmware:");  
      Serial.println(firmware);          // print firmware value
      
      ctrl_rate=omni.readControlRate();  // read the control rate value
      Serial.print("Control_Rate:");
      Serial.println(ctrl_rate);         // print control rate value

      enc1_max=omni.readEnc1Max();       // read encoder1 maximum value at calibration (usefull for detecting a faulty encoder)
      Serial.print("Encoder1_Max:");
      Serial.println(enc1_max);          // print encoder1 maximum calibration value

      enc2_max=omni.readEnc2Max();       // read encoder1 maximum value at calibration (usefull for detecting a faulty encoder)
      Serial.print("Encoder2_max:");
      Serial.println(enc2_max);          // print encoder2 maximum calibration value 

      enc3_max=omni.readEnc3Max();       // read encoder1 maximum value at calibration (usefull for detecting a faulty encoder)
      Serial.print("Encoder3_max:");
      Serial.println(enc3_max);          // print encoder3 maximum calibration value

      limiar1=omni.readLim1();           // read the necessary motor power to start movement, acquired during motors calibration.
      Serial.print("Limiar1:");
      Serial.println(limiar1);           // print motor 1 limiar power for movement 

      limiar2=omni.readLim2();           // read the necessary motor power to start movement, acquired during motors calibration.
      Serial.print("Limiar2:");
      Serial.println(limiar2);           // print motor 2 limiar power for movement 

      limiar3=omni.readLim3();           // read the necessary motor power to start movement, acquired during motors calibration.
      Serial.print("Limiar3:");
      Serial.println(limiar3);           // print motor 3 limiar power for movement 

    //read values that change with movement
      temperature=omni.readTemperature();  // read temperature value
      battery=omni.readBattery();          // read battery value
      enc1=omni.readEnc1();                // read encoder1 count value for the defined prescaler (positional control)
      enc2=omni.readEnc2();                // read encoder1 count value for the defined prescaler (positional control)
      enc3=omni.readEnc3();                // read encoder1 count value for the defined prescaler (positional control)
      print_mov_data_values();             // print movement data values


  /**read multiple values in a single request**/
    //read encoders values all at once
      omni.readEncoders(&enc1,&enc2,&enc3);
      print_enc_values();
      delay(5);
      
    //read movement data values all at once
      omni.readMovData(&enc1,&enc2,&enc3,&battery,&temperature);
      print_mov_data_values();
      delay(5);
      
    //read all data values at once
      omni.readAllData(&enc1,&enc2,&enc3,&battery,&temperature,&firm_int,&firm_dec,&firm_dev,&ctrl_rate,&enc1_max,&enc2_max,&enc3_max,&limiar1,&limiar2,&limiar3);
      print_all_data_values();
      delay(5);
      Serial.println("A pause to read...");
      Serial.println();
      delay(100);  // A pause to read
}
void print_enc_values()
{
     Serial.print("enc1:");
     Serial.print(enc1);           // print encoder 1 positional value
     Serial.print(" enc2:");
     Serial.print(enc2);           // print encoder 2 positional value
     Serial.print(" enc3:");
     Serial.println(enc3);         // print encoder 3 positional value
}
void print_mov_data_values()
{
     Serial.print("enc1:");
     Serial.print(enc1);           // print encoder 1 positional value
     Serial.print(" enc2:");
     Serial.print(enc2);           // print encoder 2 positional value
     Serial.print(" enc3:");
     Serial.print(enc3);           // print encoder 3 positional value
     Serial.print("  Bat:");
     Serial.print(battery);        // print battery value
     Serial.print(" Temp:");
     Serial.println(temperature);  // print temperature value
}
void print_all_data_values()
{
     Serial.print("enc1:");
     Serial.print(enc1);          // print encoder 1 positional value
     Serial.print(" enc2:");
     Serial.print(enc2);          // print encoder 2 positional value
     Serial.print(" enc3:");
     Serial.print(enc3);          // print encoder 3 positional value
     Serial.print("  Bat:");
     Serial.print(battery);       // print battery value
     Serial.print(" Temp:");
     Serial.print(temperature);   // print temperature value
     Serial.print(" Fw:"); 
     Serial.print(firm_int);      // print firmware value
     Serial.print(".");  
     Serial.print(firm_dec);      // print firmware value
     Serial.print(".");  
     Serial.print(firm_dev);      // print firmware value
     Serial.print(" CR:");
     Serial.print(ctrl_rate);     // print control rate value
     Serial.print("  E1max:");
     Serial.print(enc1_max);      // print encoder1 maximum calibration value
     Serial.print(" E2max:");
     Serial.print(enc2_max);      // print encoder2 maximum calibration value 
     Serial.print(" E3max:");  
     Serial.print(enc3_max);      // print encoder3 maximum calibration value
     Serial.print("  lim1:");
     Serial.print(limiar1);       // print limar movement value
     Serial.print(" lim2:");
     Serial.print(limiar2);       // print limar movement value
     Serial.print(" lim3:");
     Serial.println(limiar3);     // print limar movement value
}
