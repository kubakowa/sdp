# -*- coding: utf-8 -*-
import numpy as np
import serial
from math import sin, cos, radians, ceil
import sys

ALPHA1 = radians(30)
ALPHA2 = radians(150)
ALPHA3 = radians(270)

speed_coeff_matrix = np.matrix


def generate_speed_coeff_matrix():
    global speed_coeff_matrix 
    speed_coeff_matrix = [[-sin(ALPHA1), sin(ALPHA2), sin(ALPHA3)],
                         [cos(ALPHA1), -cos(ALPHA2), -cos(ALPHA3)],
                         [-1, 1, 1]]
    
    speed_coeff_matrix = np.linalg.inv(speed_coeff_matrix)

def calc_motor_speeds(x, y, w):
    coeffs = speed_coeff_matrix * np.matrix([[-x], [y], [w]])
    coeffs = coeffs * 100 / max(abs(coeffs))
    return coeffs

class Arduino:

    def __init__(self, port, rate, timeOut, comms):
        self.serial = None
        self.comms = comms
        self.port = port
        self.rate = rate
        self.timeout = timeOut
        self.setComms(comms)

    def setComms(self, comms):
        if comms > 0:
            self.comms = 1
            if self.serial is None:
                try:
                    self.serial = serial.Serial(self.port, self.rate, timeout=self.timeout)
                except:
                    print "No Arduino detected!"
                    print "Continuing without comms."
                    self.comms = 0
                    #raise
        else:
            self.comms = 0

    def write(self, string):
        if self.comms == 1:
            self.serial.write(string)


if __name__ == "__main__":
    generate_speed_coeff_matrix()
    comms = Arduino('/dev/ttyACM1', 115200, 1, 1)
    while (1):
        command = raw_input('Name your command (w, s, a, d, k, o, c, q, 1, 2)')
        #command = 'BB_MOVE %d %d %d\n' %(speeds[0], speeds[1], speeds[2])
        
        if command == 'w':
            speeds = calc_motor_speeds(0, 1, 0)
            comm = 'BB_MOVE %d %d %d\n' %(speeds[0], speeds[1], speeds[2])
            print(speeds)
        
        elif command == 's': 
            speeds = calc_motor_speeds(0, -1, 0)
            comm = 'BB_MOVE %d %d %d\n' %(speeds[0], speeds[1], speeds[2])
            
        elif command == 'a': 
            speeds = calc_motor_speeds(-1, 0, 0)
            comm = 'BB_MOVE %d %d %d\n' %(speeds[0], speeds[1], speeds[2])
            
        elif command == 'd': 
            speeds = calc_motor_speeds(1, 0, 0)
            comm = 'BB_MOVE %d %d %d\n' %(speeds[0], speeds[1], speeds[2])
            
        elif command == '1':
            speeds = calc_motor_speeds(0, 0, 1)
            comm = 'BB_MOVE %d %d %d\n' %(speeds[0], speeds[1], speeds[2])
            print(speeds)
        elif command == '2':
            speeds = calc_motor_speeds(0, 0, -1)
            comm = 'BB_MOVE %d %d %d\n' %(speeds[0], speeds[1], speeds[2])    
            print(speeds)    
        elif command == 'q':
            comm = 'BB_STOP\n'
            
        elif command == 'k':
            comm = 'BB_KICK\n'
            
        elif command == 'o':
            comm = 'BB_OPEN\n'
        
        elif command == 'c':
            comm = 'BB_CLOSE\n'
            
        else:
            print('You fool, unknown command :/')
         
          
        comms.write(comm)
    
