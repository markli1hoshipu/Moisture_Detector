#include <LiquidCrystal.h>
#include <EEPROM.h>
#define EEPROM_SIZE 1024  

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2; // initialize the connections to variables from LCD display to arduino to their respective pin numbers 
// connections are:
// d4, d5, d6, d7 ; Data lines
// rs ; Register Select Lines
// en; enable signal

LiquidCrystal lcd(rs, en, d4, d5, d6, d7); //set up LCD display function 
int redPin= 9;
int greenPin = 7;
int bluePin = 6; // define variables with respective pin numvers for RGB LED control 


const int buttonPin1 = 13;
const int buttonPin2 = 10;

// 13, button 1 is outer button for power source
// 10, button 2 is inner button for recording

bool buttonPressed1 = false; 
bool buttonPressed2 = false;
bool lastButtonState1 = LOW; 
bool lastButtonState2 = LOW;

bool powerOn = false; 
// initially the entire system is off
int mode = 0;
// mode 0 is regular mode; mode 1 is for comparison

int moisturebefore = 0;
int moistureafter = 0; 
int address = 0;


void setup() { // commands to setup pin, LED ground voltage (pin 4), LCD and Moisture sensor
  
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT); // LED colour initialization

  pinMode(buttonPin1, INPUT_PULLUP); 
  pinMode(buttonPin2, INPUT_PULLUP); 

  analogWrite(8,255); // Ground voltage 
  Serial.begin(57600); // Sensor initialization 
  lcd.begin(16, 2);

  lcd.print(" Team 0104B");
  
}

void loop() { //Main functional loop that Arduino will run

  int buttonState1 = digitalRead(buttonPin1);
  int buttonState2 = digitalRead(buttonPin2);
  
  Serial.println(powerOn);
  if(mode == 0){ // regular mode
    // first check the first button for state changes
    if (!buttonState1 && lastButtonState1) {
      Serial.println("Button 1 pressed");
      powerOn = !powerOn;
    }
    //main program
    if(powerOn){ //if not powerOn, just don't do anything 
      //main program
      if (!buttonState2 && lastButtonState2) {
        Serial.println("Button 2 pressed");
        if(moisturebefore == 0){
          moisturebefore = analogRead(A0);
          Serial.println("moisturebefore recorded");
        }
        else{
          moistureafter = analogRead(A0);
          Serial.println("moisturebefore recorded");
          mode = 1;
        }
      }
      else{
        Serial.print("Moisture Sensor Value:"); 
        Serial.println(analogRead(A0)); // print moisture sensor values to terminal screen (laptop)

        setColor_frominput(analogRead(A0));  
        lcd.setCursor(0, 1);

        if (setColor_frominput(analogRead(A0)) == 1){ //print state of soil according to each state and corresponding moisture sensor value
          lcd.print("desert      ");
          lcd.print(analogRead(A0));
        }// No colour - driest mode 
        else if (setColor_frominput(analogRead(A0)) == 2){
          lcd.print("too dry     ");
          lcd.print(analogRead(A0));
          delay(150); // set delay after each print command to the LCD for User readability 
          lcd.print("     ");
          //red  - too dry mode 
        }
        else if (setColor_frominput(analogRead(A0)) == 3){
          lcd.print("dry     ");
          lcd.print(analogRead(A0));
          delay(150);
          lcd.print("     ");
        } // pink  - dry mode
        else if (setColor_frominput(analogRead(A0)) == 4){
          lcd.print("Good     ");
          lcd.print(analogRead(A0));
          delay(150);
          lcd.print("     ");
        } // Blue - Optimal moisture
        else if (setColor_frominput(analogRead(A0)) == 5){
          lcd.print("tiny wet    ");
          lcd.print(analogRead(A0));
          delay(150);
          lcd.print("     ");
        } // 
        else if (setColor_frominput(analogRead(A0)) == 6){
          lcd.print("too wet     ");
          lcd.print(analogRead(A0));
          delay(150);
          lcd.print("     ");
        }
        lcd.print(analogRead(A0));
        delay(150);
        lcd.print("     ");
      }
      //main program ends
    }
    else{ //powerOn is false
      if (!buttonState2 && lastButtonState2){ //initialize
        address = 0;
        Serial.println("clear data");
        while (address < EEPROM.length()) {
          EEPROM.write(address,0);
          address++;
        }
        lcd.print("system initialized");
        delay(150);
        lcd.print("     ");
      }
      else{
        lcd.print("     ");
        delay(150);
        lcd.print("     ");
      }
    }
  }
  else if(mode == 1){ // selection mode
    lcd.print("Save data?(N/Y)");
    lcd.print(moisturebefore);
    lcd.print(moistureafter);
    delay(150);
    lcd.print("     ");
    
    if (!buttonState1 && lastButtonState1) {
      Serial.println("Button 1 pressed");

      EEPROM.write(address, moisturebefore);
      address++;
      if (address == EEPROM_SIZE) {
        address = 0;
      }

      EEPROM.write(address, moistureafter);
      address++;
      if (address == EEPROM_SIZE) {
        address = 0;
      }
      Serial.println(moisturebefore);
      Serial.println(moistureafter);
      Serial.println("succ saved");
      moisturebefore = 0;
      moistureafter = 0;
      mode = 0;
      
    }
    if (!buttonState2 && lastButtonState2) {
      Serial.println("Button 2 pressed");
      moisturebefore = 0;
      moistureafter = 0;
      mode = 0;

      Serial.println("false saved");
    }
  }
  lastButtonState1 = buttonState1;
  lastButtonState2 = buttonState2;
  delay(300);  
}


void setColor(int redValue, int greenValue, int blueValue) {
  // function takes in RGB values and outputs values to corresponding physical RGB LED output 
  analogWrite(redPin, 255-redValue);
  analogWrite(greenPin, 255-greenValue);
  analogWrite(bluePin, 255-blueValue);
}

int setColor_frominput(int sensorval){ // function takes in sensor and manipulates RGB colours based on reading, return integer correlating to each state 
  if(sensorval == 0){
    setColor(0,0,0);
    
    return 1;
  }
  else if(sensorval < 150){ //dry
    setColor(255,0,0);
    
    return 2;
  }
  else if(sensorval < 300){ //a bit dry
    setColor(255,180,0);
   
    return 3;
  }
  else if(sensorval < 450){ //good
    setColor(0,255,0);
   
    return  4;
  }
  else if(sensorval < 600){ //a bit wet
    setColor(0,180,255);
   
    return 5;
  }
  else if(sensorval>0){ //too wet
    setColor(0,0,255);
    
    return 6;
  }
}