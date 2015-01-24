#include "SDPArduino.h"
#include "SerialCommand.h"
#include <Wire.h>

/* Motors assignment */
#define LEFT_MOTOR 0
#define RIGHT_MOTOR 1
#define BACK_MOTOR 2
#define KICK_MOTOR 3

#define MAX_SPEED 100

/* Times assignment */
int FORWARD_10_TIME = 300;
int FORWARD_50_TIME = 1200;
int BACKWARD_20_TIME = 400;
int KICK_TIME = 300;
int PASS_TIME = 250;
int GRAB_TIME = 200;
int SPIN_TIME = 500;

// command
SerialCommand comm;

void setupCommands() {
  comm.addCommand("MOVE_FORWARD_10_CM", forward10);
  comm.addCommand("MOVE_FORWARD_50_CM", forward50);
  comm.addCommand("MOVE_BACKWARD_20_CM", backward20);
  comm.addCommand("KICK", kick);
  comm.addCommand("PASS", pass);
  comm.addCommand("GRAB", grab);
  comm.addCommand("STOP", stop);
  comm.addCommand("SPIN_CLOCKWISE", spin_clockwise);
  comm.addCommand("SPIN_ANTICLOCKWISE", spin_anticlockwise);
  comm.setDefaultHandler(invalid_command);
  Serial.println("COMMANDS SETUP");
} 

void setup(){
  SDPsetup();
  setupCommands();
  Serial.println("SETUP COMPLETE");
}

void forward10() {
   Serial.println("FORWARD 10CM");
   Serial.println("L: F, R: F, B: S");
   motorForward(LEFT_MOTOR, MAX_SPEED);
   motorForward(RIGHT_MOTOR, MAX_SPEED);
   delay(FORWARD_10_TIME);
   motorAllStop();
}

void forward50() {
   Serial.println("FORWARD 50CM");
   Serial.println("L: F, R: F, B: S");
   motorForward(LEFT_MOTOR, MAX_SPEED);
   motorForward(RIGHT_MOTOR, MAX_SPEED);
   delay(FORWARD_50_TIME);
   motorAllStop();
}

void backward20() {
   Serial.println("BACKWARD 20CM");
   Serial.println("L: B, R: B, B: S");
   motorBackward(LEFT_MOTOR, MAX_SPEED);
   motorBackward(RIGHT_MOTOR, MAX_SPEED);
   delay(BACKWARD_20_TIME);
   motorAllStop();
}

void spin_clockwise() {
   Serial.println("SPIN CLOCKWISE");
   Serial.println("L: F, R: B, B: B");
   motorForward(LEFT_MOTOR, MAX_SPEED);
   motorBackward(RIGHT_MOTOR, MAX_SPEED);
   motorBackward(BACK_MOTOR, MAX_SPEED);
   delay(SPIN_TIME);
   motorAllStop();
}

void spin_anticlockwise() {
   Serial.println("SPIN ANTICLOCKWISE");
   Serial.println("L: B, R: F, B: F");
   motorBackward(LEFT_MOTOR, MAX_SPEED);
   motorForward(RIGHT_MOTOR, MAX_SPEED);
   motorForward(BACK_MOTOR, MAX_SPEED);
   delay(SPIN_TIME);
   motorAllStop();
}

void kick() {
   Serial.println("KICK");
   motorBackward(KICK_MOTOR, MAX_SPEED);
   delay(KICK_TIME);
   motorAllStop();
}

// define with different time or speed
void pass() {
   Serial.println("PASS");
   motorBackward(KICK_MOTOR, MAX_SPEED);
   delay(PASS_TIME);
   motorAllStop();
}

void grab() {
   Serial.println("GRAB");
   motorForward(KICK_MOTOR, MAX_SPEED);
   delay(GRAB_TIME);
   motorAllStop();
}

void invalid_command(const char* command) {
   Serial.print("UNKNOWN COMMAND: "); 
   Serial.println(command);
}

void stop() {
   Serial.println("STOP");
   motorAllStop();
}

void loop() {
  // if command received
  comm.readSerial();
}
