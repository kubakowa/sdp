# -*- coding: utf-8 -*-
from vision.vision import Vision, Camera, GUI
from planning.planner import Planner
from postprocessing.postprocessing import Postprocessing
from preprocessing.preprocessing import Preprocessing
import vision.tools as tools
from cv2 import waitKey
import cv2
import serial
import warnings
import time
import threading

warnings.filterwarnings("ignore", category=DeprecationWarning)

class Controller:
    """
    Primary source of robot control. Ties vision and planning together.
    """

    def __init__(self, pitch, color, our_side, video_port=0, comm_port='/dev/ttyACM0', comms=1):
        """
        Entry point for the SDP system.

        Params:
            [int] video_port                port number for the camera
            [string] comm_port              port number for the arduino
            [int] pitch                     0 - main pitch, 1 - secondary pitch
            [string] our_side               the side we're on - 'left' or 'right'
            *[int] port                     The camera port to take the feed from
            *[Robot_Controller] attacker    Robot controller object - Attacker Robot has a RED
                                            power wire
            *[Robot_Controller] defender    Robot controller object - Defender Robot has a YELLOW
                                            power wire
        """
        assert pitch in [0, 1]
        assert color in ['yellow', 'blue']
        assert our_side in ['left', 'right']

        self.pitch = pitch

        # Set up the Arduino communications
        self.arduino = Arduino(comm_port, 115200, 1, comms)
	#self.arduino.write("BB_KICK\n")
	raw_input('Press enter to start')
	

        # Set up camera for frames
        self.camera = Camera(port=video_port, pitch=self.pitch)
        frame = self.camera.get_frame()
        center_point = self.camera.get_adjusted_center(frame)

        # Set up vision
        self.calibration = tools.get_colors(pitch)
        self.vision = Vision(
            pitch=pitch, color=color, our_side=our_side,
            frame_shape=frame.shape, frame_center=center_point,
            calibration=self.calibration)

        # Set up postprocessing for vision
        self.postprocessing = Postprocessing()

        # Set up main planner
        self.planner = Planner(our_side=our_side, pitch_num=self.pitch)

        # Set up GUI
        self.GUI = GUI(calibration=self.calibration, arduino=self.arduino, pitch=self.pitch)

        self.color = color
        self.side = our_side

        self.preprocessing = Preprocessing()

        self.defender = Defender_Controller()

    def wow(self):
        """
        Ready your sword, here be dragons.
        """
        counter = 1L
        timer = time.clock()
        try:
            c = True
	    
            while c != 27:  # the ESC key

                frame = self.camera.get_frame()
                pre_options = self.preprocessing.options
                # Apply preprocessing methods toggled in the UI
                preprocessed = self.preprocessing.run(frame, pre_options)
                frame = preprocessed['frame']
                if 'background_sub' in preprocessed:
                    cv2.imshow('bg sub', preprocessed['background_sub'])
                # Find object positions
                # model_positions have their y coordinate inverted

		#find positions of objects in current preprocessed frame
                model_positions, regular_positions = self.vision.locate(frame)
                model_positions = self.postprocessing.analyze(model_positions)

                # Find appropriate action
                self.planner.update_world(model_positions) #planner now has an up-to-date world model
                defender_actions = self.planner.plan('defender')
		
		# Update attacker action
		attacker_actions = 'unknown'

                if self.defender is not None:
                   self.defender.execute(self.arduino, defender_actions)

                # Information about the grabbers from the world
                grabbers = {
                    'our_defender': self.planner._world.our_defender.catcher_area,
                    'our_attacker': self.planner._world.our_attacker.catcher_area
                }

                # Information about states
                defenderState = (self.planner.defender_state, self.planner.defender_strat_state)
		attackerState = ('unknown', 'unknown')

                # Use 'y', 'b', 'r' to change color.
                c = waitKey(2) & 0xFF
                actions = []
                fps = float(counter) / (time.clock() - timer)
                # Draw vision content and actions

                self.GUI.draw(
                    frame, model_positions, actions, regular_positions, fps, attackerState,
                    defenderState, attacker_actions, defender_actions, grabbers,
                    our_color=self.color, our_side=self.side, key=c, preprocess=pre_options)
                counter += 1

        except:
            if self.defender is not None:
                self.defender.shutdown(self.arduino)
            raise

        finally:
            # Write the new calibrations to a file.
            tools.save_colors(self.pitch, self.calibration)
            if self.defender is not None:
                self.defender.shutdown(self.arduino)


class Robot_Controller(object):
    """
    Robot_Controller superclass for robot control.
    """

    def __init__(self):
        """
        Connect to Brick and setup Motors/Sensors.
        """
        self.current_speed = 0

    def shutdown(self, comm):
        # TO DO
            pass

class Defender_Controller(Robot_Controller):
    """
    Defender implementation.
    """

    acknowledgements={"BB_OPEN\n":"BB_OPENED ",
		      "BB_CLOSE\n":"BB_CLOSED ",
		      "BB_KICK\n":"BB_KICKED ", 
		      "BB_STOP\n":"BB_STOPPED "
		      }

    is_turning = 0
    is_moving = 0

    ackNo=0
    def __init__(self):
        """
        Do the same setup as the Robot class, as well as anything specific to the Defender.
        """
        super(Defender_Controller, self).__init__()

    def execute(self, comm, action):
        """
        Execute robot action.
        """
        print action

	# action details
        left_motor = int(action['left_motor'])
        right_motor = int(action['right_motor'])
	back_motor = int(action['back_motor'])
	kicker = int(action['kicker'])
	catcher = int(action['catcher'])
	turn = int(action['turn'])
	step = int(action['step'])
	stop = int(action['stop'])
	
	# open and close are volatile commands
	volatile = 0
	
	# open is crucial command
	crucial = 0
        
	#if left_motor==-right_motor:
	#  # turning
	#  if 'bb_turn' in action:
	#    back_motor=right_motor
	#  # going sideways
	#  else:
	#    back_motor=-1.4*right_motor
	
	command = 'BB_MOVE %d %d %d\n' % (left_motor, right_motor, back_motor)
       
        if step == 1:
            command = 'BB_STEP %d %d %d\n' % (left_motor, right_motor, back_motor)
        
	# if turning and current action does not involve turning, stop robot before proceeding
	if self.is_turning == 1 and turn == 0:
            comm.write('BB_STOP\n')

	if stop == 1:
	    comm.write('BB_STOP\n')
	    self.is_moving = 0
	
	if turn == 1:
            self.is_turning = 1
        else:
            self.is_turning = 0

        if kicker == 1:
            try:
                command = 'BB_KICK\n'
            except StandardError:
                pass
        elif catcher == 1:
            try:
                volatile = 1
		crucial = 1
                command = 'BB_OPEN\n'
            except StandardError:
                pass
            
        elif catcher == 2:
            try:
                volatile = 1
                command = 'BB_CLOSE\n'
            except StandardError:
                pass

	elif catcher == 3:
            try:
                command = 'BB_RELEASE\n'
            except StandardError:
                pass

	if volatile:
	    comm.write(command)
	    time.sleep(0.2)
	    comm.write(command)
	    time.sleep(0.2)
	    comm.write(command)
	    time.sleep(0.2)
	    comm.write(command)

	if crucial:
	    time.sleep(0.2)
	    comm.write(command)
	    time.sleep(0.2)
	    comm.write(command)
	    time.sleep(0.2)
	    comm.write(command)
	    time.sleep(0.2)
	    comm.write(command)

	
#Commands we need to make sure get executed.
#        if volatile:
#
#	  def sendVolatileCommand(command):
#	      command=command[0:len(command)-1] #remove the \n at the end
#	      #command=command + ' ' + str(self.ackNo) + '\n'
#	      print 'sending', command
#	      while(True):
#		  comm.write(command)
#		  time.sleep(0.1)
#		  print 'resending', command
#
#	  t = threading.Timer(0.1, sendVolatileCommand, [command])
#	  t.start()
#	  while(True):
#	      acknowledgement=comm.readline()
#	      if acknowledgement==self.acknowledgements[command]+str(self.ackNo)+'\n':
#		  self.ackNo+=1
#		  t.cancel()  
#		  break
#	      if acknowledgement=="no comms":
#		  t.cancel()  
#		  break

	# assuming this is only for movement commands
        if not (command=="BB_MOVE 0 0 0\n" or command=="BB_STEP 0 0 0\n"):
            comm.write(command)
            self.is_moving = 1
	    print command
	else:
            print 'Empty command, not sending it'
            if self.is_moving == 1:
                comm.write("BB_STOP\n")
                self.is_moving = 0

    def shutdown(self, comm):
        comm.write('BB_STOP\n')

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
            #self.write('A_RUN_KICK\n')
            #self.write('A_RUN_ENGINE %d %d\n' % (0, 0))
            #self.write('D_RUN_KICK\n')
            #self.write('D_RUN_ENGINE %d %d\n' % (0, 0))
            self.comms = 0

    def write(self, string):
        if self.comms == 1:
            self.serial.write(string)

    def readline(self):
        if self.comms == 1:
	    received=self.serial.readline()
	    print "while waiting for ACK, received", received
            return received
	else:
	    return "no comms"


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pitch", help="[0] Main pitch, [1] Secondary pitch")
    parser.add_argument("side", help="The side of our defender ['left', 'right'] allowed.")
    parser.add_argument("color", help="The color of our team - ['yellow', 'blue'] allowed.")
    parser.add_argument(
        "-n", "--nocomms", help="Disables sending commands to the robot.", action="store_true")

    args = parser.parse_args()
    if args.nocomms:
        c = Controller(
            pitch=int(args.pitch), color=args.color, our_side=args.side, comms=0).wow()
    else:
        c = Controller(
            pitch=int(args.pitch), color=args.color, our_side=args.side).wow()
