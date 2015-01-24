#include "SDPArduino.h"
#include "MotorsControl.h"
#include <Wire.h>

/* Motors assignment */
#define LEFT_MOTOR 0
#define RIGHT_MOTOR 1
#define BACK_MOTOR 2
#define KICK_MOTOR 3

#define MAX_SPEED 100

/* Define commands */
#define STOP 0          
#define FORWARD_10CM 1  
#define FORWARD_50CM 2  
#define BACKWARD_20CM 3 
#define SPIN_LEFT 4     
#define SPIN_RIGHT 5
#define KICK 6

void setup(){
  SDPsetup();
  Serial.println("SETUP COMPLETE");
}

// the command buffer
byte command;  

void loop() {
  // if command received
  if (Serial.available()>=1)
  {
    command = Serial.read() - '0';
    switch (command) {
      case STOP:
        motorAllStop();
        Serial.println("STOP");
        break;
        
      case FORWARD_10CM:
        Serial.println("FORWARD 10CM");
        Serial.println("L: F, R: F, B: S");
        motorForward(LEFT_MOTOR, MAX_SPEED);
        motorForward(RIGHT_MOTOR, MAX_SPEED);
        delay(800);
        motorAllStop();
        break;
        
      case FORWARD_50CM:
        Serial.println("FORWARD 50CM");
        Serial.println("L: F, R: F, B: S");
        motorForward(LEFT_MOTOR, MAX_SPEED);
        motorForward(RIGHT_MOTOR, MAX_SPEED);
        delay(1500);
        motorAllStop();
        break; 
        
      case BACKWARD_20CM:
        Serial.println("BACKWARD 20CM");
        motorBackward(LEFT_MOTOR, MAX_SPEED);
        motorBackward(RIGHT_MOTOR, MAX_SPEED);
        delay(5000);
        motorAllStop();
        break; 
        
      case SPIN_LEFT:
        Serial.println("SPIN LEFT");
        motorForward(LEFT_MOTOR, 
        MAX_SPEED);
        motorBackward(RIGHT_MOTOR, MAX_SPEED);
        motorBackward(BACK_MOTOR, MAX_SPEED);
        delay(5000);
        motorAllStop();
        break;
        
      case SPIN_RIGHT: 
        Serial.println("SPIN LEFT");
        motorBackward(LEFT_MOTOR, MAX_SPEED);
        motorForward(RIGHT_MOTOR, MAX_SPEED);
        motorForward(BACK_MOTOR, MAX_SPEED);
        delay(5000);
        motorAllStop();
        break;
      
      case KICK:
        Serial.println("KICK");
        motorBackward(KICK_MOTOR, MAX_SPEED);
        delay(500);
        motorAllStop();
        break;
      
      // handle new line
      case (byte) ('\n' - '0'):
        break;
        
      default:
        Serial.println("UNKNOWN COMMAND");
        break;
    } 
  }
}
