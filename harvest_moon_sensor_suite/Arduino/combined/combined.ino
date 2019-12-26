#include "PinChangeInterrupt.h"
#include <dht.h>
#include <OneWire.h>

#define DHT11_PIN 7
#define SSR_PIN 8

dht DHT;
OneWire ds(6);

unsigned int l_hour_pin2; // flow l/h (pin2 - Sensor F1)
unsigned int l_hour_pin3; // flow l/h (pin2 - Sensor F2)
unsigned int l_hour_pin4; // flow l/h (pin2 - Sensor F3)
unsigned int l_hour_pin5; // flow l/h (pin2 - Sensor F4)
float celsius; // WT for water temp
float humidity; // HD for humidity
float amb_temp; // AT for ambient temp

volatile int flow_frequency_pin2; // Measures flow sensor pulses for pin 2
volatile int flow_frequency_pin3; //Measures flows sensor pulses for pin3
volatile int flow_frequency_pin4;
volatile int flow_frequency_pin5;  

unsigned char flowsensor_pin2 = 2;
unsigned char flowsensor_pin3 = 3;
unsigned char flowsensor_pin4 = 4;
unsigned char flowsensor_pin5 = 5;

unsigned long currentTime;
unsigned long cloopTime;

String start_of_header = "\x01";
String end_of_transmission = "\x04";
String end_of_text = "\x03";
String sep = "\x1e";
String temp_n_hum_string;
String flow_string;
String string_wo_checksum;
String string_w_checksum;
String string_to_be_sent; 
int checksum;

//for dht
int chk;

//for controlling lights
String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete

void flow_pin2_irs () // Interrupt function
{
  flow_frequency_pin2++;
}

void flow_pin3_irs ()
{
  flow_frequency_pin3++;
}

void flow_pin4_irs ()
{
  flow_frequency_pin4++;
}

void flow_pin5_irs ()
{
  flow_frequency_pin5++;
}

//super simple custom checksum func
int stringChecksum(String s)
{
    char char_array[100];
    s.toCharArray(char_array, 100);
    int counter;
    int c_sum = 0;
    for (counter = 0; counter<strlen(char_array); counter++){
      c_sum = c_sum + char_array[counter];
    }
    return c_sum; 
}


void setup()
{
   inputString.reserve(200);
   pinMode(LED_BUILTIN, OUTPUT);
   digitalWrite(LED_BUILTIN, LOW);

   pinMode(SSR_PIN, OUTPUT);
   digitalWrite(SSR_PIN, LOW);
   
   pinMode(flowsensor_pin2, INPUT);
   digitalWrite(flowsensor_pin2, HIGH); // Optional Internal Pull-Up
   
   pinMode(flowsensor_pin3, INPUT);
   digitalWrite(flowsensor_pin3, HIGH);

   pinMode(flowsensor_pin4, INPUT);
   digitalWrite(flowsensor_pin3, HIGH);

   pinMode(flowsensor_pin5, INPUT);
   digitalWrite(flowsensor_pin3, HIGH);
   
   Serial.begin(9600);
   
   attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(flowsensor_pin2), flow_pin2_irs, RISING);
   attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(flowsensor_pin3), flow_pin3_irs, RISING);
   attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(flowsensor_pin4), flow_pin4_irs, RISING);
   attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(flowsensor_pin5), flow_pin5_irs, RISING);

   sei(); // Enable interrupts
   
   currentTime = millis();
   cloopTime = currentTime;
}

void loop ()
{
   if (stringComplete) {
      if (inputString == "00*01\r"){
        digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(1000);                       // wait for a second
        digitalWrite(SSR_PIN, HIGH);
        delay(1000);
      }
      else if (inputString == "00*01\n"){
        digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(1000);                       // wait for a second
        digitalWrite(SSR_PIN, HIGH);
        delay(1000);
      }
      else if (inputString == "00*01"){
        digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
        delay(1000);                       // wait for a second
        digitalWrite(SSR_PIN, HIGH);
        delay(1000);
      }
      else if (inputString == "00*00\r"){
        digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
        delay(1000);
        digitalWrite(SSR_PIN, LOW);
        delay(1000);
      }
      else if (inputString == "00*00\n"){
        digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
        delay(1000);
        digitalWrite(SSR_PIN, LOW);
        delay(1000);

      }
      else if (inputString == "00*00"){
        digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
        delay(1000);
        digitalWrite(SSR_PIN, LOW);
        delay(1000);
      }
      // clear the string:
      inputString = "";
      stringComplete = false;
  }
    byte i;
    byte present = 0;
    byte type_s;
    byte data[12];
    byte addr[8];
    
    if ( !ds.search(addr)) {
      celsius = -1;
      ds.reset_search();
      delay(250);
      return;
    }
  
  
    if (OneWire::crc8(addr, 7) != addr[7]) {
      celsius = -1;
      return;
    }
  
  
    // the first ROM byte indicates which chip
    switch (addr[0]) {
      case 0x10:
        type_s = 1;
        break;
      case 0x28:
        type_s = 0;
        break;
      case 0x22:
        type_s = 0;
        break;
      default:
        return;
    }
  
    ds.reset();
    ds.select(addr);
    ds.write(0x44);        // start conversion, use ds.write(0x44,1) with parasite power on at the end
  
    delay(1000);     // maybe 750ms is enough, maybe not
    // we might do a ds.depower() here, but the reset will take care of it.
  
    present = ds.reset();
    ds.select(addr);    
    ds.write(0xBE);         // Read Scratchpad
  
    for ( i = 0; i < 9; i++) {           // we need 9 bytes
      data[i] = ds.read();
    }
  
    // Convert the data to actual temperature
    // because the result is a 16 bit signed integer, it should
    // be stored to an "int16_t" type, which is always 16 bits
    // even when compiled on a 32 bit processor.
    int16_t raw = (data[1] << 8) | data[0];
    if (type_s) {
      raw = raw << 3; // 9 bit resolution default
      if (data[7] == 0x10) {
        // "count remain" gives full 12 bit resolution
        raw = (raw & 0xFFF0) + 12 - data[6];
      }
    } else {
      byte cfg = (data[4] & 0x60);
      // at lower res, the low bits are undefined, so let's zero them
      if (cfg == 0x00) raw = raw & ~7;  // 9 bit resolution, 93.75 ms
      else if (cfg == 0x20) raw = raw & ~3; // 10 bit res, 187.5 ms
      else if (cfg == 0x40) raw = raw & ~1; // 11 bit res, 375 ms
      //// default is 12 bit resolution, 750 ms conversion time
    }
    celsius = (float)raw / 16.0;
    


   //FLOW
   currentTime = millis();
   // Every second, calculate and print litres/hour
   if(currentTime >= (cloopTime + 1000))
   {
      cloopTime = currentTime; // Updates cloopTime
      // Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
      l_hour_pin2 = (flow_frequency_pin2 * 60 / 7.5); // (Pulse frequency x 60 min) / 7.5Q = flowrate in L/hour
      l_hour_pin3 = (flow_frequency_pin3 * 60 / 7.5);
      l_hour_pin4 = (flow_frequency_pin4 * 60 / 7.5);
      l_hour_pin5 = (flow_frequency_pin5 * 60 / 7.5);
      
      flow_frequency_pin2 = 0; // Reset Counter
      flow_frequency_pin3 = 0;
      flow_frequency_pin4 = 0;
      flow_frequency_pin5 = 0;
      
      //Water temperature
      //Serial.print("WT");
      //Serial.print(celsius);
      
      //humidity and temperature
      chk = DHT.read11(DHT11_PIN);
      //Serial.print("AT");
      //Serial.print(DHT.temperature);
      //Serial.print("HD");
      //Serial.print(DHT.humidity);
      //flow
      //Serial.print("FOE");
      //Serial.print(",");
      //Serial.print(l_hour_pin2, DEC); // Print litres/hour
      //Serial.print("FTO");
      //Serial.print(l_hour_pin3, DEC);
      //Serial.print("FTE");
      //Serial.print(l_hour_pin4, DEC);
      //Serial.print("FFR");
      //Serial.println(l_hour_pin5, DEC);

      temp_n_hum_string="WT,"+String(celsius)+sep+"AT,"+String(DHT.temperature)+sep+"HD,"+String(DHT.humidity+sep);
      flow_string = "F1,"+String(l_hour_pin2)+sep+"F2,"+String(l_hour_pin3)+sep+"F3,"+String(l_hour_pin4)+sep+"F4,"+String(l_hour_pin5);
      string_wo_checksum = temp_n_hum_string+flow_string;
      checksum = stringChecksum(string_wo_checksum);
      string_w_checksum = string_wo_checksum + end_of_text + checksum;
      string_to_be_sent = start_of_header + string_w_checksum + end_of_transmission;
      Serial.print(string_to_be_sent);
      checksum = 0;

   }
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == 'c') {
      stringComplete = true;
    }
    else{
      inputString += inChar;
    }
  }
}
