
#include <Wire.h>


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

  #define ONE_BYTE   1
  #define TWO_BYTES  2
  #define FOUR_BYTES 4
  #define SIX_BYTES  6

#define _i2cAddress 0x60
#define SDA 21
#define SCL 22
 

byte _byteHigh, _byteLow;
int bearing;
int nReceived;
signed char pitch;
signed char roll;

void setup()
{

  
  Serial.begin(115200);              // Start serial ports
  Wire.begin(21,22);

 
}

void loop()
{
  Serial.println("START");
   // Begin communication with CMPS14
  Wire.beginTransmission(_i2cAddress);

  // Tell register you want some data
  Wire.write(BEARING_Register);

  Serial.println("bhiyuilnm");
  // End the transmission
  int nackCatcher = Wire.endTransmission();

  // Return if we have a connection problem 
  if(nackCatcher != 0){bearing = 0; pitch = 0;  roll = 0; return;}
  
  // Request 4 bytes from CMPS14
  nReceived = Wire.requestFrom(_i2cAddress , FOUR_BYTES);

  // Something has gone wrong
  if (nReceived != FOUR_BYTES) {bearing = 0; pitch = 0;  roll = 0; return;}
    Serial.println("STANBYVYCVUBINRT");

  // Read the values
  _byteHigh = Wire.read(); _byteLow = Wire.read();
  bearing = ((_byteHigh<<8) + _byteLow) / 10;

  // Read the values
  pitch = Wire.read();

  // Read the values
  roll = Wire.read();

  Serial.println("STANBYVYCVUBINRT");
  Serial.print("bearingx  : ");            // Display roll data
  Serial.print(bearing, DEC);
  
  Serial.print("    roll: ");            // Display roll data
  Serial.print(roll, DEC);
  
  Serial.print("    pitch: ");          // Display pitch data
  Serial.println(pitch, DEC);
  
  
  delay(100);                           // Short delay before next loop
  
}
