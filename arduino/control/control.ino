#include "SDPArduino.h"
#include "SerialCommand.h"
#include <Wire.h>

/* Motors assignment */
#define LEFT_MOTOR 0
#define RIGHT_MOTOR 1
#define BACK_MOTOR 2
#define KICK_MOTOR 3

#define MAX_SPEED 100
#define COUNTER_SPEED 98 /* To counter-act the difference in motors */
#define PASS_SPEED 80

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
  comm.addCommand("BB_MOVE10", forward10);
  comm.addCommand("BB_FORWARD50", forward50);  
  comm.addCommand("BB_BACK20", backward20);
  comm.addCommand("BB_KICK", kick);
  comm.addCommand("BB_PASS", pass);
  comm.addCommand("BB_GRAB", grab);
  comm.addCommand("BB_STOP", stop);
  comm.addCommand("BB_SPINC", spin_clockwise);
  comm.addCommand("BB_SPINA", spin_anticlockwise);
  comm.addCommand("BB_GM", go_mad);
  /* For testing purposes */
  comm.addCommand("BB_MOTOR_ONE", move_motor_one); 
  comm.addCommand("BB_MOTOR_TWO", move_motor_two);
  comm.addCommand("BB_MOTOR_THREE", move_motor_three);
  comm.setDefaultHandler(invalid_command);
  Serial.println("COMMANDS SETUP");
} 

void setup(){
  SDPsetup();
  setupCommands();
  Serial.println("SETUP COMPLETE");
}

void move_motor_one() {
  Serial.println("MOTOR ONE MOVING");
  motorForward(LEFT_MOTOR, MAX_SPEED);
  delay(1000);
  motorAllStop();
}

void move_motor_two() {
  Serial.println("MOTOR TWO MOVING");
  motorForward(RIGHT_MOTOR, MAX_SPEED);
  delay(1000);
  motorAllStop();
}

void move_motor_three() {
  Serial.println("MOTOR THREE MOVING");
  motorForward(BACK_MOTOR, MAX_SPEED);
  delay(1000);
  motorAllStop();
}

void forward10() {
   Serial.println("FORWARD 10CM");
   Serial.println("L: F, R: F, B: S");
   motorForward(LEFT_MOTOR, MAX_SPEED);
   motorForward(RIGHT_MOTOR, COUNTER_SPEED);
   delay(FORWARD_10_TIME);
   motorAllStop();
}

void forward50() {
   Serial.println("FORWARD 50CM");
   Serial.println("L: F, R: F, B: S");
   motorForward(LEFT_MOTOR, MAX_SPEED);
   motorForward(RIGHT_MOTOR, COUNTER_SPEED);
   delay(FORWARD_50_TIME);
   motorAllStop();
}

void backward20() {
   Serial.println("BACKWARD 20CM");
   Serial.println("L: B, R: B, B: S");
   motorBackward(LEFT_MOTOR, MAX_SPEED);
   motorBackward(RIGHT_MOTOR, COUNTER_SPEED);
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

void go_mad() {
   Serial.println("GO MAD!");
   spin_clockwise();
   delay(500);
   spin_anticlockwise();
}

void kick() {
   Serial.println("KICK");
   motorBackward(KICK_MOTOR, MAX_SPEED);
   delay(KICK_TIME);
   motorAllStop();
}

void pass() {
   Serial.println("PASS");
   motorBackward(KICK_MOTOR, PASS_SPEED);
   delay(PASS_TIME);
   motorAllStop();
}

void grab() {
   Serial.println("GRAB");
   motorBackward(KICK_MOTOR, MAX_SPEED);
   delay(GRAB_TIME);
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
