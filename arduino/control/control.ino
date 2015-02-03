#include "SDPArduino.h"
#include "SerialCommand.h"
#include <Wire.h>

/* Motors assignment */
#define LEFT_MOTOR 0
#define RIGHT_MOTOR 1
#define BACK_MOTOR 2
#define KICK_MOTOR 3

/* Times assignment */
int FORWARD_10_TIME = 400;
int FORWARD_50_TIME = 1600;
int BACKWARD_20_TIME = 750;
int KICK_TIME = 300;
int PASS_TIME = 200;
int GRAB_TIME = 200;
int SPIN_TIME = 10000;

// command
SerialCommand comm;

void setupCommands() {
  comm.addCommand("BB_MOVE", make_move);
  comm.addCommand("BB_KICK", make_kick);
} 

void setup(){
  SDPsetup();
  setupCommands();
  //Serial.println("SETUP COMPLETE");
}

void make_move() {
  char *left_m;
  char *right_m;
  char *back_m;
  
  int left_speed;
  int right_speed;
  int back_speed;
  
  left_m = comm.next();
  right_m = comm.next();
  back_m = comm.next();
  
  if (left_m != NULL && right_m != NULL && back_m != NULL) {
    left_speed = atoi(left_m);
    right_speed = atoi(right_m);
    back_speed = atoi(back_m);
  }
  
  Serial.println(left_speed < 0);
  Serial.println(right_speed < 0);
  Serial.println(back_speed < 0);
  
  if (left_speed > 0)
    motorForward(LEFT_MOTOR, left_speed);
  
  if (left_speed < 0)
    motorBackward(LEFT_MOTOR, -left_speed);
    
  if (right_speed > 0)
    motorForward(RIGHT_MOTOR, right_speed);
  
  if (right_speed < 0)
    motorBackward(RIGHT_MOTOR, -right_speed);
      
  if (back_speed > 0)
    motorForward(BACK_MOTOR, back_speed);
  
  if (back_speed < 0)  
    motorBackward(BACK_MOTOR, -back_speed);
    
  delay(2000);
  motorAllStop();
}

void make_kick() {

}

void invalid_command(const char* command) { }

void loop() {
  // if command received
  comm.readSerial();
}
