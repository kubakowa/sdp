#include "SDPArduino.h"
#include "SerialCommand.h"
#include <Wire.h>

/* Motors assignment */
#define LEFT_MOTOR 0
#define RIGHT_MOTOR 1
#define BACK_MOTOR 2
#define KICK_MOTOR 3

/* Constants */
int KICK_TIME = 300;
int GRAB_TIME = 200;
int CLOSE_TIME = 150;
int MAX_SPEED = 100;
int GRAB_SPEED = 10;


// command
SerialCommand comm;

void setupCommands() {
  comm.addCommand("BB_MOVE", make_move);
  comm.addCommand("BB_KICK", make_kick);
  comm.addCommand("BB_OPEN", open_grabber);
  comm.addCommand("BB_CLOSE", close_grabber);
  comm.addCommand("BB_STOP", make_stop);
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
  
  if (left_speed > 0)
    motorForward(LEFT_MOTOR, left_speed);
  else if (left_speed < 0)
    motorBackward(LEFT_MOTOR, -left_speed);
    
  if (right_speed > 0)
    motorForward(RIGHT_MOTOR, right_speed);
  else if (right_speed < 0)
    motorBackward(RIGHT_MOTOR, -right_speed);
      
  if (back_speed > 0)
    motorForward(BACK_MOTOR, back_speed);
  else if (back_speed < 0)  
    motorBackward(BACK_MOTOR, -back_speed);
}

void make_kick() {
  motorBackward(KICK_MOTOR, MAX_SPEED);
  delay(KICK_TIME);
  motorStop(KICK_MOTOR);
}

void open_grabber() {
  motorBackward(KICK_MOTOR, MAX_SPEED);
  delay(GRAB_TIME);
  motorBackward(KICK_MOTOR, GRAB_SPEED);
}

void close_grabber() {
  motorForward(KICK_MOTOR, MAX_SPEED);
  delay(CLOSE_TIME);
  motorStop(KICK_MOTOR);
}

void make_stop() {
  motorStop(LEFT_MOTOR); 
  motorStop(RIGHT_MOTOR);
  motorStop(BACK_MOTOR);
}

void invalid_command(const char* command) { }

void loop() {
  // if command received
  comm.readSerial();
}
