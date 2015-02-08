# -*- coding: utf-8 -*-
from math import tan, pi, hypot, log
from planning.models import Robot

DISTANCE_MATCH_THRESHOLD = 50
ANGLE_MATCH_THRESHOLD = pi/15
BALL_ANGLE_THRESHOLD = pi/20
MAX_DISPLACEMENT_SPEED = 690
MAX_ANGLE_SPEED = 50
BALL_VELOCITY = 3


def is_shot_blocked(world, our_robot, their_robot):
    '''
    Checks if our robot could shoot past their robot
    '''
    predicted_y = predict_y_intersection(
        world, their_robot.x, our_robot, full_width=True, bounce=True)
    if predicted_y is None:
        return True
    print '##########', predicted_y, their_robot.y, their_robot.length
    print abs(predicted_y - their_robot.y) < their_robot.length
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
            return None


def grab_ball():
    return {'left_motor': 0, 'right_motor': 0, 'kicker': 0, 'catcher': 1, 'speed': 1000}


def kick_ball():
    return {'left_motor': 0, 'right_motor': 0, 'kicker': 1, 'catcher': 0, 'speed': 1000}


def open_catcher():
    return {'left_motor': 0, 'right_motor': 0, 'kicker': 2, 'catcher': 0, 'speed': 1000}


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


def calculate_motor_speed(displacement, angle, backwards_ok=False, careful=False):
    '''
    Simplistic view of calculating the speed: no modes or trying to be careful
    '''
    moving_backwards = False
    general_speed = 95 if careful else 300
    angle_thresh = BALL_ANGLE_THRESHOLD if careful else ANGLE_MATCH_THRESHOLD

    if backwards_ok and abs(angle) > pi/2:
        angle = (-pi + angle) if angle > 0 else (pi + angle)
        moving_backwards = True

    if not (displacement is None):

        if displacement < DISTANCE_MATCH_THRESHOLD:
            print 'Displacement:', displacement
            print 'movement action called while robot is at the ball'
            return {'left_motor': 0, 'right_motor': 0, 'kicker': 0, 'catcher': 0, 'speed': general_speed}

        elif abs(angle) > angle_thresh:
            #BB old 7s code:  speed = (angle/pi) * MAX_ANGLE_SPEED
            print ('angle to ball: ', angle)
            if abs(angle)<0.8:
                print 'angle close to needed'
                bb_speed=0
            else:
                print 'angle still too big for stepping'
                bb_speed=1
            #BB
            if angle<0:
                speed1=70
                speed2=-70
            else:
                speed1=-70
                speed2=70

	    returnDict= {'left_motor': speed1, 'right_motor': speed2, 'kicker': 0, 'catcher': 0, 'speed': bb_speed, 'bb_turn': 1}


            return returnDict

        else:
            print('moving to ball')
            bb_speed = 1
            if displacement<70:
                bb_speed=0
                print 'Carefully. DISP:', displacement
           # if careful:
           #     return {'left_motor': speed, 'right_motor': speed, 'kicker': 0, 'catcher': 0, 'speed': 1000/(1+10**(-0.1*(displacement-85)))}
           # return {'left_motor': speed, 'right_motor': speed, 'kicker': 0, 'catcher': 0, 'speed': 1000/(1+10**(-0.1*(displacement-30)))}
	return  {'left_motor': 70, 'right_motor': 70, 'back_motor': 0, 'kicker':0, 'catcher':0, 'speed': bb_speed}
    else:
        print 'robot is at the ball'
        if abs(angle) > angle_thresh:
            #BB old 7s code:  speed = (angle/pi) * MAX_ANGLE_SPEED
            print('angle to ball', angle)
            if abs(angle)<0.8:
                bb_speed=0
            else:
                bb_speed=1
            #BB
            if angle<0:
                speed1=70;
                speed2=-70;
            else:
                speed1=-70;
                speed2=70;
            return {'left_motor': speed1, 'right_motor': speed2, 'kicker': 0, 'catcher': 0, 'speed': bb_speed, 'back_motor': 0}

        else:
            return {'left_motor': 0, 'right_motor': 0, 'kicker': 0, 'catcher': 0, 'speed': general_speed, 'back_motor': 0}

def calculate_motor_speed_turn(displacement, angle, backwards_ok=False, careful=False):
    '''
    Simplistic view of calculating the speed: no modes or trying to be careful
    '''
    moving_backwards = False
    general_speed = 95 if careful else 300
    angle_thresh = BALL_ANGLE_THRESHOLD if careful else ANGLE_MATCH_THRESHOLD

    if backwards_ok and abs(angle) > pi/2:
        angle = (-pi + angle) if angle > 0 else (pi + angle)
        moving_backwards = True

    if not (displacement is None):

        if displacement < DISTANCE_MATCH_THRESHOLD:
            return {'left_motor': 0, 'right_motor': 0, 'kicker': 0, 'catcher': 0, 'speed': general_speed}

        elif abs(angle) > angle_thresh:
            speed = (angle/pi) * MAX_ANGLE_SPEED
            return {'left_motor': -speed, 'right_motor': speed, 'kicker': 0, 'catcher': 0, 'speed': general_speed}

        else:
            speed = log(displacement, 10) * MAX_DISPLACEMENT_SPEED
            speed = -speed if moving_backwards else speed
            # print 'DISP:', displacement
            if careful:
                return {'left_motor': speed, 'right_motor': speed, 'kicker': 0, 'catcher': 0, 'speed': 1000/(1+10**(-0.1*(displacement-85)))}
            return {'left_motor': speed, 'right_motor': speed, 'kicker': 0, 'catcher': 0, 'speed': 1000/(1+10**(-0.1*(displacement-30)))}

    else:

        if abs(angle) > angle_thresh:
            speed = (angle/pi) * MAX_ANGLE_SPEED
            return {'left_motor': -speed, 'right_motor': speed, 'kicker': 0, 'catcher': 0, 'speed': general_speed}

        else:
            return {'left_motor': 0, 'right_motor': 0, 'kicker': 0, 'catcher': 0, 'speed': general_speed}


def do_nothing():
    return {'left_motor': 0, 'right_motor': 0, 'back_motor': 0, 'kicker': 0, 'catcher': 0, 'speed': 0, 'stop': 0, 'spin': 0}

def adjust_angle(ang):
    speed = 50
    if ang > 0:
    	return {'left_motor': -speed, 'right_motor': speed, 'back_motor': speed, 'kicker': 0, 'catcher': 0, 'speed': 0, 'stop': 0, 'spin': 1}
    else:
        return {'left_motor': speed, 'right_motor': -speed, 'back_motor': -speed, 'kicker': 0, 'catcher': 0, 'speed': 0, 'stop': 0, 'spin': 1}

def adjust_y_position(robot, target_y, side):
    disp = target_y - robot.y
    
    if side == 'right':
      disp = -disp


    if disp < 0:
        # move left
	return {'left_motor': 60, 'right_motor': -60, 'back_motor': 100, 'kicker': 0, 'catcher': 0, 'speed': 0, 'stop': 0, 'spin': 0}
    else:
       # move right
       return {'left_motor': -60, 'right_motor': 60, 'back_motor': -100, 'kicker': 0, 'catcher': 0, 'speed': 0, 'stop': 0, 'spin': 0}

def adjust_x_position(robot, target_x, side):
    disp = target_x - robot.x

    if side == 'right':
      disp = -disp

    print 'Target: %d, Robot: %d' % (target_x, robot.x)
    if disp > 0:
        # move forward
	return {'left_motor': 100, 'right_motor': 100, 'back_motor': 0, 'kicker': 0, 'catcher': 0, 'speed': 0, 'stop': 0, 'spin': 0}
    else:
       # move backward
       return {'left_motor': -100, 'right_motor': -100, 'back_motor': 0, 'kicker': 0, 'catcher': 0, 'speed': 0, 'stop': 0, 'spin': 0}

def is_aligned(robot_coor, target):
    print 'target %d coor %d abs %d' % (target, robot_coor, abs(target-robot_coor))
    return abs(target - robot_coor) < DISTANCE_MATCH_THRESHOLD    

def is_facing_target(ang):
    return abs(ang) < ANGLE_MATCH_THRESHOLD

def defender_stop():
    return {'left_motor': 0, 'right_motor': 0, 'back_motor': 0, 'kicker': 0, 'catcher': 0, 'speed': 0, 'stop': 1, 'spin': 0}
