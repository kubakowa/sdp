# -*- coding: utf-8 -*-
from math import tan, pi, hypot, log, sin, cos, radians, ceil
from planning.models import Robot
import time
import numpy as np

DISTANCE_MATCH_THRESHOLD = 30
DISTANCE_ALMOST_THERSHOLD = 60

ANGLE_MATCH_THRESHOLD = pi/12

BALL_ANGLE_THRESHOLD = pi/20
MAX_DISPLACEMENT_SPEED = 690
MAX_ANGLE_SPEED = 50

BALL_VELOCITY = 4

ALPHA1 = radians(30)
ALPHA2 = radians(150)
ALPHA3 = radians(270)

SPEED_COEFF_MATRIX = np.matrix

COMPANSATION_FACTOR = 1.3

def is_shot_blocked(world, our_robot, their_robot):
    '''
    Checks if our robot could shoot past their robot
    '''
    predicted_y = predict_y_intersection(
        world, their_robot.x, our_robot, full_width=True, bounce=True)
    if predicted_y is None:
        return True
    return abs(predicted_y - their_robot.y) < their_robot.length


def is_attacker_shot_blocked(world, our_attacker, their_defender):
    '''
    Checks if our attacker would score if it would immediately turn and shoot.
    '''

    # Acceptable distance that the opponent defender can be relative to our
    # shooting position in order for us to have a clear shot.
    distance_threshold = 40

    # Return True if attacker and defender ar close to each other on
    # the y dimension
    return abs(our_attacker.y - their_defender.y) < distance_threshold


def can_score(world, our_robot, their_goal, turn=0):
    # Offset the robot angle if need be
    robot_angle = our_robot.angle + turn
    goal_zone_poly = world.pitch.zones[their_goal.zone][0]

    reverse = True if their_goal.zone == 3 else False
    goal_posts = sorted(goal_zone_poly, key=lambda x: x[0], reverse=reverse)[:2]
    # Makes goal be sorted from smaller to bigger
    goal_posts = sorted(goal_posts, key=lambda x: x[1])

    goal_x = goal_posts[0][0]

    robot = Robot(
        our_robot.zone, our_robot.x, our_robot.y, robot_angle % (pi * 2), our_robot.velocity)

    predicted_y = predict_y_intersection(world, goal_x, robot, full_width=True)

    return goal_posts[0][1] < predicted_y < goal_posts[1][1]

def predict_y_intersection(world, predict_for_x, robot, full_width=False, bounce=False):
        '''
        Predicts the (x, y) coordinates of the ball shot by the robot
        Corrects them if it's out of the bottom_y - top_y range.
        If bounce is set to True, predicts for a bounced shot
        Returns None if the robot is facing the wrong direction.
        '''
        x = robot.x
        y = robot.y
        top_y = world._pitch.height - 60 if full_width else world.our_goal.y + (world.our_goal.width/2) - 30
        bottom_y = 60 if full_width else world.our_goal.y - (world.our_goal.width/2) + 30
        angle = robot.angle
        if (robot.x < predict_for_x and not (pi/2 < angle < 3*pi/2)) or (robot.x > predict_for_x and (3*pi/2 > angle > pi/2)):
            if bounce:
                if not (0 <= (y + tan(angle) * (predict_for_x - x)) <= world._pitch.height):
                    bounce_pos = 'top' if (y + tan(angle) * (predict_for_x - x)) > world._pitch.height else 'bottom'
                    x += (world._pitch.height - y) / tan(angle) if bounce_pos == 'top' else (0 - y) / tan(angle)
                    y = world._pitch.height if bounce_pos == 'top' else 0
                    angle = (-angle) % (2*pi)
            predicted_y = (y + tan(angle) * (predict_for_x - x))
            # Correcting the y coordinate to the closest y coordinate on the goal line:
            if predicted_y > top_y:
                return top_y
            elif predicted_y < bottom_y:
                return bottom_y
            return predicted_y
        else:
            return world.our_goal.y

### Actionhttp://www.inf.ed.ac.uk/teaching/courses/ct/coursework.html
# left motor - left motor speed
# right motor - right motor speed
# back motor - back motor speed
# kicker - 1 for kick, 0 otherwise 
# catcher - 1 for open, 2 for close, 0 otherwise
# step - 1 for stepping enable, 0 otherwise
# turn - 1 for turning, 0 otherwise
# stop - 1 for stopping all movements, 0 otherwise

def grab_ball():
    return {'left_motor': 0, 'right_motor': 0, 'back_motor': 0, 'kicker': 0, 'catcher': 2, 'step': 0, 'turn': 0, 'stop': 0}

def kick_ball():
    return {'left_motor': 0, 'right_motor': 0, 'back_motor': 0, 'kicker': 1, 'catcher': 0, 'step': 0, 'turn': 0, 'stop': 0}


def open_catcher():
    return {'left_motor': 0, 'right_motor': 0, 'back_motor': 0, 'kicker': 0, 'catcher': 1, 'step': 0, 'turn': 0, 'stop': 0}

# not using this
def turn_shoot(orientation):
    return {'turn_90': orientation, 'left_motor': 0, 'right_motor': 0, 'kicker': 1, 'catcher': 0, 'speed': 1000}


def has_matched(robot, x=None, y=None, angle=None,
                angle_threshold=ANGLE_MATCH_THRESHOLD, distance_threshold=DISTANCE_MATCH_THRESHOLD):
    dist_matched = True
    angle_matched = True
    if not(x is None and y is None):
        dist_matched = hypot(robot.x - x, robot.y - y) < distance_threshold
    if not(angle is None):
        angle_matched = abs(angle) < angle_threshold
    return dist_matched and angle_matched

def calculate_motor_speed(displacement, angle, backwards_ok=False, sideways_ok=False, full_speed=False, distance_threshold=DISTANCE_MATCH_THRESHOLD): 
    direction = 'forward'

    if backwards_ok and not sideways_ok:
	if abs(angle) > pi/2:
	    if angle < 0:
		angle = pi - abs(angle)
	    else:
		angle = angle - pi
	    direction = 'backward'

    if sideways_ok:
	if abs(angle) < pi/4:
	    direction = 'forward'
	elif angle < -pi/4 and angle > -3 * pi/4:
	    angle = angle + pi/2
	    direction = 'right'
	elif angle > pi/4 and angle < 3 * pi/4:
	    angle = angle - pi/2
	    direction = 'left'
	else:
	    if angle < 0:
		angle = pi - abs(angle)
	    else:
		angle = angle - pi
	    direction = 'backward'
  
    # need to adjust the angle
    if abs(angle) > ANGLE_MATCH_THRESHOLD:
	if abs(angle) > pi:  
	   factor = 0.5
	else:
	   factor = 0.35

	x = 0
	y = 0
	# need to turn clockwise
	if angle < 0:
	    w = -1
	# need to turn anticlockwise
	elif angle > 0:
	    w = 1

	speeds = get_speeds_vector(x, y, w, factor)
	left_motor = COMPANSATION_FACTOR * speeds['left_motor']
	right_motor = speeds['right_motor'] 
	back_motor = speeds['back_motor']

	return {'left_motor': left_motor, 'right_motor': right_motor, 'back_motor': back_motor, 'kicker': 0, 'catcher': 0, 'step': 0, 'turn': 1, 'stop': 0}
    # need to adjust distance

    if (displacement is not None and displacement > distance_threshold):
	if displacement > 4 * distance_threshold:  
	   factor = 0.6
	elif displacement > 3 * distance_threshold:
	   factor = 0.55
	else:
	   factor = 0.45
  
	w = 0

	if direction == 'forward':
	    x = 0
	    y = 1
	elif direction == 'backward':
	    x = 0
	    y = -1
	elif direction == 'left':
	    x = -1
	    y = 0
	    factor = 1
	elif direction == 'right':
	    x = 1
	    y = 0
	    factor = 1
	
	speeds = get_speeds_vector(x, y, w, factor)

	left_motor  =  speeds['left_motor']
	right_motor =  speeds['right_motor'] 
	back_motor  =  speeds['back_motor']

	if direction in ['forward', 'backward']:
	  left_motor = COMPANSATION_FACTOR * left_motor
	  back_motor = 0

	if full_speed and direction in ['forward', 'backward']:
	    if direction == 'forward':
		left_motor = 100
		right_motor = 100
	    else:
		left_motor = -100
		right_motor = -100

	return {'left_motor': left_motor, 'right_motor': right_motor, 'back_motor': back_motor, 'kicker': 0, 'catcher': 0, 'step': 0, 'turn': 0, 'stop': 0}
    else:
	return do_nothing()

# still need to refactor and simplify this function
def calculate_motor_speed_old(displacement, angle, backwards_ok=False, careful=False):
    '''
    Simplistic view of calculating the speed: no modes or trying to be careful
    '''
    angle_thresh = 0.25
    angleIncrThresh=0.9
    angleTurnPower=52
    movePower=65

    if not (displacement is None):

        if (displacement < DISTANCE_MATCH_THRESHOLD) and (abs(angle) < angle_thresh):
	    # forward, no turning
	    motor_speeds = get_speeds_vector(0, 1, 0)
	    speed_factor = 0.5

	    left_motor = motor_speeds['left_motor'] * speed_factor
	    right_motor = motor_speed['right_motor'] * speed_factor

	    return {'left_motor': left_motor, 'right_motor': right_motor, 'back_motor': 0, 'kicker': 0, 'catcher': 0, 'step': 1, 'turn': 0, 'stop': 0}
        
        distThreshFast=70

        if abs(angle) > angle_thresh:
            #BB old 7s code:  speed = (angle/pi) * MAX_ANGLE_SPEED
            angleThreshIncr=1.7

            if abs(angle)<angleIncrThresh:
                angleTurnPower=55
                bb_speed=0
            else:
                bb_speed=1
                if displacement==-1:
                    bb_speed=0 # this is if we are turning for a scoring shot
            #BB
            if angle<0:
                speed1=angleTurnPower
                speed2=-angleTurnPower
            else:
                speed1=-angleTurnPower
                speed2=angleTurnPower

	    #return {'left_motor': speed1, 'right_motor': speed2, 'back_motor':speed2, 'kicker': 0, 'catcher': 0, 'speed': bb_speed, 'bb_turn': 1}
	    return {'left_motor': speed1, 'right_motor': speed2, 'back_motor': speed2, 'kicker': 0, 'catcher': 0, 'step': 1, 'turn': 1, 'stop': 0}

        else:
            bb_speed = 1
            if displacement<80:
                movePower=72
                bb_speed=0
		return {'left_motor': movePower, 'right_motor': movePower, 'back_motor': 0, 'kicker': 0, 'catcher': 0, 'step': 0, 'turn': 0, 'stop': 0}
            #move forward
	    return {'left_motor': movePower, 'right_motor': movePower, 'back_motor': 0, 'kicker': 0, 'catcher': 0, 'step': 0, 'turn': 0, 'stop': 0}
    else:	
        if abs(angle) > angle_thresh:
            if abs(angle)<angleIncrThresh:
                bb_speed=0
            else:
                bb_speed=1
            #BB
            if angle<0:
                speed1=angleTurnPower;
                speed2=-angleTurnPower;
            else:
                speed1=-angleTurnPower;
                speed2=angleTurnPower;
	    return {'left_motor': speed1, 'right_motor': speed2, 'back_motor': speed2, 'kicker': 0, 'catcher': 0, 'step': 0, 'turn': 1, 'stop': 0}
        else:
	    return {'left_motor': 0, 'right_motor': 0, 'back_motor': 0, 'kicker': 0, 'catcher': 0, 'step': 0, 'turn': 0, 'stop': 0}


# not using this function for now    
def calculate_motor_speed_turn(displacement, angle, backwards_ok=False, careful=False):
    '''
    Simplistic view of calculating the speed: no modes or trying to be careful
    '''
    moving_backwards = False
    general_speed = 95 if careful else 45
    angle_thresh = ANGLE_MATCH_THRESHOLD
    angleIncrThresh=0.9

    if not (displacement is None):
      return do_nothing()

    else:

	if abs(angle) > angle_thresh:
            #BB old 7s code:  speed = (angle/pi) * MAX_ANGLE_SPEED
            angleThreshIncr=1.5

            #print ('angle to ball: ', angle)
            if abs(angle)<angleIncrThresh:
                #print 'angle close to needed'
                bb_speed=0
            else:
                #print 'angle still too big for stepping'
                bb_speed=1
            #BB
            if angle<0:
                speed1=60
                speed2=-60
            else:
                speed1=-60
                speed2=60

	    return {'left_motor': speed1, 'right_motor': speed2, 'back_motor':speed2, 'kicker': 0, 'catcher': 0, 'speed': bb_speed, 'bb_turn': 1}
       
	else:

           #print 'turning to ball while next to it'
            #print('angle to ball', angle)

            if abs(angle)<angleIncrThresh:
                bb_speed=0
            else:
                bb_speed=1
            #BB
            if angle<0:
                speed1=60;
                speed2=-60;
            else:
                speed1=-60;
                speed2=60;
            #turning when robot is at the ball
            return {'left_motor': speed1, 'right_motor': speed2, 'kicker': 0, 'catcher': 0, 'speed': bb_speed, 'back_motor': speed2, 'bb_turn':1}
     
    return do_nothing()

def do_nothing():
    return {'left_motor': 0, 'right_motor': 0, 'back_motor': 0, 'kicker': 0, 'catcher': 0, 'step': 0, 'turn': 0, 'stop': 0} 

def adjust_y_position(angle):
    if (abs(angle) < pi/2):
	speed = 100
	#factor = 1.4
    else:
	speed = -100
	#factor = 1.2


    return {'left_motor': speed, 'right_motor': speed, 'back_motor': 0, 'kicker': 0, 'catcher': 0, 'step': 0, 'stop': 0, 'turn': 0}

def is_aligned(robot_coor, target):
    return abs(target - robot_coor) < DISTANCE_MATCH_THRESHOLD/2    

def is_aligned_almost(robot_coor, target):
    return abs(target - robot_coor) < DISTANCE_ALMOST_THERSHOLD

def is_facing_target(ang):
    return abs(ang) < ANGLE_MATCH_THRESHOLD

def defender_stop():
    return {'left_motor': 0, 'right_motor': 0, 'back_motor': 0, 'kicker': 0, 'catcher': 0, 'step': 0, 'stop': 1, 'turn': 0}

def generate_speed_coeff_matrix():
    global SPEED_COEFF_MATRIX
    SPEED_COEFF_MATRIX = [[-sin(ALPHA1), sin(ALPHA2), sin(ALPHA3)],
                         [cos(ALPHA1), -cos(ALPHA2), -cos(ALPHA3)],
                         [-1, 1, 1]]
    
    SPEED_COEFF_MATRIX = np.linalg.inv(SPEED_COEFF_MATRIX)

def get_speeds_vector(x, y, w, factor):
    coeffs = SPEED_COEFF_MATRIX * np.matrix([[-x], [y], [w]])
    coeffs = coeffs * 100 / max(abs(coeffs))
    coeffs = coeffs * factor
    return {'left_motor': round(coeffs.item(0)), 'right_motor': round(coeffs.item(1)), 'back_motor': round(coeffs.item(2))}
