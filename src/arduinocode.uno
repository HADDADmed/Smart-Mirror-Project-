#include <Arduino.h>
#include <Audio.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <SerialFlash.h>
#include <SoftwareSerial.h>
#include <LiquidCrystal.h>


AudioInputAnalog adc1(A0); // assuming microphone is connected to analog pin A0
SoftwareSerial serial(2, 3); // RX, TX pins for Emic 2 module
// Define the LCD pins
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


#define LED_PIN 2
void setup() {
  Serial.begin(9600); // Initialize serial communication
  AudioMemory(12);
  serial.begin(9600); // Initialize serial communication with Emic 2 module
 // Initialize the LCD
  lcd.begin(16, 2);
  // Clear the LCD screen
  lcd.clear();
    pinMode(LED_PIN, OUTPUT);
 digitalWrite(LED_PIN, HIGH);
  
}

void loop() {
    if (Serial.available() > 0) {
     char marker = Serial.read();
     if (marker == 'T') {
      // Read the text data from Raspberry Pi
      String textData = Serial.readStringUntil('\n');
      // Pass the text data to Emic 2 module for synthesis to display the data as an audio
      serial.println(textData);
    }
     elseif (marker == 'd') {
      // Read the text data from Raspberry Pi
      String textData = Serial.readStringUntil('\n');
      // Display the text on the LCD
      lcd.clear();
      lcd.print(textData);
    }
    else{
  // Read audio data from the microphone
  int16_t audioData = adc1.read();
  // Send the audio data to the Raspberry Pi
  Serial.write((uint8_t*)&audioData, sizeof(audioData));
    }
    }
}



