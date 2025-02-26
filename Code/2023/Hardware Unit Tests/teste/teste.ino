
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


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
#define SDA_CMPS14 19
#define SCL_CMPS14 23
 
TwoWire CMPS14= TwoWire(1);

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
// The pins for I2C are defined by the Wire-library. 
// On an arduino UNO:       A4(SDA), A5(SCL)
// On an arduino MEGA 2560: 20(SDA), 21(SCL)
// On an arduino LEONARDO:   2(SDA),  3(SCL), ...
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C ///< See datasheet for Address; 0x3D for 128x64, 0x3C for 128x32
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &CMPS14, OLED_RESET);

#define NUMFLAKES     10 // Number of snowflakes in the animation example

#define LOGO_HEIGHT   16
#define LOGO_WIDTH    16
static const unsigned char PROGMEM logo_bmp[] =
{ 0b00000000, 0b11000000,
  0b00000001, 0b11000000,
  0b00000001, 0b11000000,
  0b00000011, 0b11100000,
  0b11110011, 0b11100000,
  0b11111110, 0b11111000,
  0b01111110, 0b11111111,
  0b00110011, 0b10011111,
  0b00011111, 0b11111100,
  0b00001101, 0b01110000,
  0b00011011, 0b10100000,
  0b00111111, 0b11100000,
  0b00111111, 0b11110000,
  0b01111100, 0b11110000,
  0b01110000, 0b01110000,
  0b00000000, 0b00110000 };

byte _byteHigh, _byteLow;
int bearing;
int nReceived;
signed char pitch;
signed char roll;


// Define two I2C buses with the same pins
 void setup()
{

  
  Serial.begin(115200);              // Start serial ports
  CMPS14.begin(SDA_CMPS14, SCL_CMPS14);
 // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  // Show initial display buffer contents on the screen --
  // the library initializes this with an Adafruit splash screen.
  display.display();
  delay(2000); // Pause for 2 seconds

  // Clear the buffer
  display.clearDisplay();

  // Draw a single pixel in white
  display.drawPixel(10, 10, SSD1306_WHITE);

  // Show the display buffer on the screen. You MUST call display() after
  // drawing commands to make them visible on screen!
  display.display();
  delay(2000);
  // display.display() is NOT necessary after every single drawing command,
  // unless that's what you want...rather, you can batch up a bunch of
  // drawing operations and then update the screen all at once by calling
  // display.display(). These examples demonstrate both approaches...

  

  

 }

void loop()
{
  Serial.println("START");
   // Begin communication with CMPS14
  CMPS14.beginTransmission(_i2cAddress);

  // Tell register you want some data
  CMPS14.write(BEARING_Register);

  Serial.println("bhiyuilnm");
  // End the transmission
  int nackCatcher = CMPS14.endTransmission();

  // Return if we have a connection problem 
  if(nackCatcher != 0){bearing = 0; pitch = 0;  roll = 0; return;}
  
  // Request 4 bytes from CMPS14
  nReceived = CMPS14.requestFrom(_i2cAddress , FOUR_BYTES);

  // Something has gone wrong
  if (nReceived != FOUR_BYTES) {bearing = 0; pitch = 0;  roll = 0; return;}
    Serial.println("STANBYVYCVUBINRT");

  // Read the values
  _byteHigh = CMPS14.read(); _byteLow = CMPS14.read();
  bearing = ((_byteHigh<<8) + _byteLow) / 10;

  // Read the values
  pitch = CMPS14.read();

  // Read the values
  roll = CMPS14.read();

  Serial.println("STANBYVYCVUBINRT");
  Serial.print("bearingx  : ");            // Display roll data
  Serial.print(bearing, DEC);
  
  Serial.print("    roll: ");            // Display roll data
  Serial.print(roll, DEC);
  
  Serial.print("    pitch: ");          // Display pitch data
  Serial.println(pitch, DEC);
  
  
  UpdateTableMonitor();  
  delay(100);                           // Short delay before next loop
  
}
 

void UpdateTableMonitor(void) {
  display.clearDisplay();

   

 }

/*void UpdateTableMonitor(void) {
  display.clearDisplay();

  for(int16_t i=0; i<display.height()/2; i+=2) {
    display.drawRect(i, i, display.width()-2*i, display.height()-2*i, SSD1306_WHITE);
    display.display(); // Update screen with each newly-drawn rectangle
    delay(1);
  }

 }
 */
