#include "SDPArduino.h"
#include "SerialCommand.h"
#include <Wire.h>

/* Motors assignment */
#define LEFT_MOTOR 0
#define RIGHT_MOTOR 1
#define BACK_MOTOR 4
#define KICK_MOTOR 5

/* State */
int GRABBER_OPEN = 0;

/* Constants */
int KICK_TIME = 1000;
int GRAB_TIME = 240;
int CLOSE_TIME = 400;
int OPEN_TIME = 500;
int RELEASE_DOWN_TIME = 175;
int RELEASE_UP_TIME = 400;

int MAX_SPEED = 100;
int OPEN_SPEED = 25;
int CLOSE_SPEED = 70;

// command
SerialCommand comm;

void setupCommands() {
  comm.addCommand("BB_MOVE", make_move);
  comm.addCommand("BB_KICK", make_kick);
  comm.addCommand("BB_OPEN", open_grabber);
  comm.addCommand("BB_CLOSE", close_grabber);
  comm.addCommand("BB_STOP", make_stop);
  comm.addCommand("BB_PAUSE", make_pause);
  comm.addCommand("BB_STEP", make_incremental_move);
  comm.addCommand("BB_RELEASE", release_grabber);
} 

void setup(){
  SDPsetup();
  setupCommands();
}

void burst_move(int left_speed,int right_speed, int back_speed) {
  
  boolean forward = (back_speed == 0);
  
  if (forward)
    motorStop(BACK_MOTOR);
    
  if (left_speed > 0)
    motorForward(LEFT_MOTOR, left_speed);
  else if (left_speed < 0)
    motorBackward(LEFT_MOTOR, -left_speed);
    
  if (right_speed > 0)
    motorForward(RIGHT_MOTOR, right_speed);
  else if (right_speed < 0)
    motorBackward(RIGHT_MOTOR, -right_speed);
  
  if (forward)
    return;
      
  if (back_speed > 0)
    motorForward(BACK_MOTOR, back_speed);
  else if (back_speed < 0)  
    motorBackward(BACK_MOTOR, -back_speed); 
}
 
void make_incremental_move() {
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
  
  burst_move(left_speed, right_speed, back_speed);
  delay(220);
  make_pause();
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
  
  burst_move(left_speed, right_speed, back_speed);
}

void make_kick() {
  
  if (GRABBER_OPEN)
    return;
  
  motorBackward(KICK_MOTOR, MAX_SPEED);
  delay(KICK_TIME);
  motorStop(KICK_MOTOR);
  
  /* Assign state of the grabber */
  GRABBER_OPEN = 0;
}

void open_grabber() {
  
  if (GRABBER_OPEN)
    return;
  
  motorStop(KICK_MOTOR);
  motorBackward(KICK_MOTOR, MAX_SPEED);
  delay(OPEN_TIME);
  motorBackward(KICK_MOTOR, OPEN_SPEED);
  
  /* Assign state of the grabber */
  GRABBER_OPEN = 1;
}

void close_grabber() {
  motorStop(KICK_MOTOR);
  motorForward(KICK_MOTOR, MAX_SPEED);
  delay(CLOSE_TIME);
  motorForward(KICK_MOTOR, CLOSE_SPEED);
  
  /* Assign state of the grabber */
  GRABBER_OPEN = 0;
}

void make_pause() {
  motorStop(BACK_MOTOR);
  motorStop(LEFT_MOTOR); 
  motorStop(RIGHT_MOTOR);
  delay(210);
}

void make_stop() {
  motorStop(BACK_MOTOR);
  motorStop(LEFT_MOTOR); 
  motorStop(RIGHT_MOTOR);
}

void release_grabber() {
  motorStop(KICK_MOTOR);
  
  if (GRABBER_OPEN) {
    motorForward(KICK_MOTOR, MAX_SPEED);
    delay(RELEASE_DOWN_TIME);
    motorStop(KICK_MOTOR);
  } 
  else {
    motorBackward(KICK_MOTOR, MAX_SPEED);
    delay(RELEASE_UP_TIME);
    motorStop(KICK_MOTOR);
  }
  
  GRABBER_OPEN = 0;
}
    
      
    

void invalid_command(const char* command) { }

void loop() {
  // if command received
  comm.readSerial();
}
