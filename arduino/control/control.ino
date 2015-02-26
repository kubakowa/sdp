#include "SDPArduino.h"
#include "SerialCommand.h"
#include <Wire.h>

/* Motors assignment */
#define LEFT_MOTOR 0
#define RIGHT_MOTOR 1
#define BACK_MOTOR 2
#define KICK_MOTOR 3

/* State */
int GRABBER_OPEN = 0;
int ackNo = 0;

/* Constants */
int KICK_TIME = 400;
int GRAB_TIME = 200;
int CLOSE_TIME = 250;
int MAX_SPEED = 100;
int OPEN_SPEED = 45;

// command
SerialCommand comm;

void setupCommands() {
  comm.addCommand("BB_MOVE", make_move);
  comm.addCommand("BB_KICK", make_volatile("BB_KICKED"));
  comm.addCommand("BB_OPEN", make_volatile("BB_OPENED"));
  comm.addCommand("BB_CLOSE", make_volatile("BB_CLOSED"));
  comm.addCommand("BB_STOP", make_volatile("BB_STOPPED"));
  comm.addCommand("BB_PAUSE", make_pause);
  comm.addCommand("BB_STEP", make_incremental_move);
} 

void setup(){
  SDPsetup();
  setupCommands();
}

void burst_move(int left_speed,int right_speed, int back_speed) {
  
  boolean forward = left_speed == right_speed;
  
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

// Volatile Commands
void make_volatile(char* command){
  // Get broadcast acknowledgement number 
  int ack_number_pc;
  ack_number_pc = comm.next();
  
  // Check for duplicates - commands received in the past
  if (ack_number_pc != ackNo){
    // Send the acknowledgement again
    Serial.print(command + " " + ack_number_pc + "\n");
  }
  
  // If fresh, carry out command and send acknowledgement
  else {
    if (command == "BB_KICKED"){
      make_kick();
    }
    if (command == "BB_OPENED"){
      open_grabber();
    }
    if (command == "BB_CLOSED"){
      close_grabber();
    }
    if (command == "BB_STOPPED"){
      make_stop();
    }
  
    // Send acknowledgement
    Serial.print(command + " " + ackNo + "\n");
    ackNo++;
  }
}

void make_kick() { 
  if (GRABBER_OPEN)
    return;
  
  motorBackward(KICK_MOTOR, MAX_SPEED);
  delay(KICK_TIME);
  motorStop(KICK_MOTOR);
}

void open_grabber() {
  
  if (GRABBER_OPEN)
    return;
  
  motorBackward(KICK_MOTOR, MAX_SPEED);
  delay(GRAB_TIME);
  motorBackward(KICK_MOTOR, OPEN_SPEED);
  
  /* Assign state of the grabber */
  GRABBER_OPEN = 1;
  Serial.print("BB_OPENED \n");
}

void close_grabber() {
  motorStop(KICK_MOTOR);
  motorForward(KICK_MOTOR, MAX_SPEED);
  delay(CLOSE_TIME);
  motorStop(KICK_MOTOR);
  
  /* Assign state of the grabber */
  GRABBER_OPEN = 0;
  Serial.print("BB_CLOSED \n");
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
  Serial.print("BB_STOPPED \n");
}

void invalid_command(const char* command) { }

void loop() {
  // if command received
  comm.readSerial();
}
