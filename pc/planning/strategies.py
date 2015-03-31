# -*- coding: utf-8 -*-
from utilities import *
import math
from random import randint
from glob import BallState

class Strategy(object):

    GOAL_ALIGN_OFFSET = 60
    PRECISE_BALL_ANGLE_THRESHOLD = math.pi / 15.0
    UP, DOWN = 'UP', 'DOWN'

    def __init__(self, world, states):
        self.world = world
        self.states = states
        self._current_state = states[0]

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, new_state):
        assert new_state in self.states
        self._current_state = new_state

    def reset_current_state(self):
        self.current_state = self.states[0]

    def is_last_state(self):
        return self._current_state == self.states[-1]

    def generate(self):
        return self.NEXT_ACTION_MAP[self.current_state]()

class DefenderDefend(Strategy):

    PREPARE, TRACK_BALL, ALIGN, UP, DOWN  = 'PREPARE', 'TRACK_BALL' ,'ALIGN', 'UP', 'DOWN' 
    STATES = [PREPARE, TRACK_BALL, ALIGN, UP, DOWN]

    LEFT, RIGHT = 'left', 'right'
    SIDES = [LEFT, RIGHT]
    
    def __init__(self, world):
        super(DefenderDefend, self).__init__(world, self.STATES)
 
        self.NEXT_ACTION_MAP = {
	    self.PREPARE: self.prepare,
            self.TRACK_BALL: self.track_ball,
	    self.ALIGN: self.align,
	    self.UP: self.up,
	    self.DOWN: self.down
        }

        self.ball = self.world.ball
	self.our_defender = self.world.our_defender
	self.their_attacker = self.world.their_attacker
	
	def_zone = self.world._pitch._zones[self.world.our_defender.zone]
	min_x, max_x, self.min_y, self.max_y  = def_zone.boundingBox()
	self.center_y = (self.min_y + self.max_y)/2

	self.top_post = self.center_y + 50
	self.bottom_post = self.center_y - 50

	self.goal_front_x = self._get_alignment_x(self.world._our_side, 0)
	self.counter = 0
	self.threshold = 10
	self.distance = 10

    def prepare(self):
	front_x = self._get_alignment_x(self.world._our_side, 20)

        disp, angle = self.our_defender.get_direction_to_point(front_x, self.center_y)

	if self.our_defender.catcher == 'closed':
	    self.our_defender.catcher = 'released'
	    return kick_ball()
	elif self.our_defender.catcher == 'open':
	    self.our_defender.catcher = 'released'
	    return release_catcher()

        if has_matched(self.our_defender, x=front_x, y=self.center_y):
	    if self._confuse():
		self.current_state = self.ALIGN
	    else:
		self.current_state = self.TRACK_BALL
            return defender_stop()
        else:
            return calculate_motor_speed(disp, angle, backwards_ok=True, sideways_ok=True)

    def track_ball(self):
	if BallState.lost:
	    track_y = self.their_attacker.y
	else:
	    track_y = self.ball.y

	if self._confuse():
	    self.current_state = self.ALIGN
	    
	# ball not within the goal range, at the top
	if (track_y > self.top_post+10):
	    disp, angle = self.our_defender.get_direction_to_point(self.goal_front_x, self.top_post)
	    if has_matched(self.our_defender, x=self.goal_front_x, y=self.top_post):
		return defender_stop()
	    else:
		return calculate_motor_speed(disp, angle, backwards_ok=True, full_speed=True, sideways_ok=True)
	
	# ball not within the goal range, at the bottom
	elif (track_y < self.bottom_post-10):
	    disp, angle = self.our_defender.get_direction_to_point(self.goal_front_x, self.bottom_post)
	    if has_matched(self.our_defender, x=self.goal_front_x, y=self.bottom_post):
		return defender_stop()
	    else:
		return calculate_motor_speed(disp, angle, backwards_ok=True, full_speed=True, sideways_ok=True)
	
	# ball within the goal range
	elif has_matched(self.our_defender, x=self.goal_front_x, y=track_y, distance_threshold=20):
	    return defender_stop()
	else:
	    disp, angle = self.our_defender.get_direction_to_point(self.goal_front_x, track_y)
	    return calculate_motor_speed(disp, angle, backwards_ok=True, full_speed=True, sideways_ok=True)

    def align(self):
	self.counter = self.counter + 1

	if not self._confuse():
	    self.current_state = self.TRACK_BALL

	    track_y = self._get_y_within_goal_range(self.ball.y, offset=0)

	    disp, angle = self.our_defender.get_direction_to_point(self.goal_front_x, track_y)
	    return calculate_motor_speed(disp, angle, backwards_ok=True, full_speed=True, sideways_ok=True, distance_threshold=20)
	    
	track_y = self._get_y_within_goal_range(self.their_attacker.y, offset=self.threshold)

	if has_matched(self.our_defender, x=self.goal_front_x, y=track_y, distance_threshold=self.threshold):
	    if self.counter % 2 == 0:
		self.current_state = self.DOWN
	    else:
		self.current_state = self.UP
	    return defender_stop()
	else:
	    disp, angle = self.our_defender.get_direction_to_point(self.goal_front_x, track_y)
	    return calculate_motor_speed(disp, angle, backwards_ok=True, full_speed=True, sideways_ok=True, distance_threshold=self.threshold)

    def up(self):
	if not self._confuse():
	    self.current_state = self.TRACK_BALL

	    track_y = self._get_y_within_goal_range(self.ball.y, offset=0)

	    disp, angle = self.our_defender.get_direction_to_point(self.goal_front_x, track_y)
	    return calculate_motor_speed(disp, angle, backwards_ok=True, full_speed=True, sideways_ok=True, distance_threshold=20)


	track_y = self._get_y_within_goal_range(self.their_attacker.y + self.distance)

	if has_matched(self.our_defender, x=self.goal_front_x, y=track_y, distance_threshold=self.threshold):
	    self.current_state = self.ALIGN
	    return defender_stop()
	else:
	    disp, angle = self.our_defender.get_direction_to_point(self.goal_front_x, track_y)
	    return calculate_motor_speed(disp, angle, backwards_ok=True, full_speed=True, sideways_ok=True, distance_threshold=self.threshold)
    
    def down(self):
	if not self._confuse():
	    self.current_state = self.TRACK_BALL

	    track_y = self._get_y_within_goal_range(self.ball.y, offset=0)

	    disp, angle = self.our_defender.get_direction_to_point(self.goal_front_x, track_y)
	    return calculate_motor_speed(disp, angle, backwards_ok=True, full_speed=True, sideways_ok=True, distance_threshold=20)

	track_y = self._get_y_within_goal_range(self.their_attacker.y - self.distance)
	
	if has_matched(self.our_defender, x=self.goal_front_x, y=track_y, distance_threshold=self.threshold):
	    self.current_state = self.ALIGN
	    return defender_stop()
	else:
	    disp, angle = self.our_defender.get_direction_to_point(self.goal_front_x, track_y)
	    return calculate_motor_speed(disp, angle, backwards_ok=True, full_speed=True, sideways_ok=True, distance_threshold=self.threshold)

    def _get_y_within_goal_range(self, y, offset=0):
	if y > self.top_post - offset:
	    return self.top_post - offset 
	elif y < self.bottom_post + offset:
	    return self.bottom_post + offset
	else:
	    return y

    def _get_alignment_x(self, side, offset):
        assert side in self.SIDES
        if side == self.LEFT:
            return self.world.our_goal.x + self.GOAL_ALIGN_OFFSET + offset
        else:
            return self.world.our_goal.x - self.GOAL_ALIGN_OFFSET - offset

    def _confuse(self):
	return BallState.lost or has_matched(self.their_attacker, x=self.ball.x, y=self.ball.y, distance_threshold=40)

class DefenderGrab(Strategy):

    PREPARE, GO_TO_BALL, GRAB_BALL, GRABBED = 'PREPARE', 'GO_TO_BALL', 'GRAB_BALL', 'GRABBED'
    STATES = [PREPARE, GO_TO_BALL, GRAB_BALL, GRABBED]
    def __init__(self, world):
        super(DefenderGrab, self).__init__(world, self.STATES)

        self.NEXT_ACTION_MAP = {
            self.PREPARE: self.prepare,
            self.GO_TO_BALL: self.position,
            self.GRAB_BALL: self.grab,
	    self.GRABBED: do_nothing
        }

        self.our_defender = self.world.our_defender
        self.ball = self.world.ball

    def prepare(self):
        self.current_state = self.GO_TO_BALL
        self.our_defender.catcher = 'open'
        return open_catcher()

    def position(self):
        displacement, angle = self.our_defender.get_direction_to_point(self.ball.x, self.ball.y)
        if self.our_defender.can_catch_ball(self.ball):
            self.current_state = self.GRAB_BALL
            return defender_stop()
        else:
            return calculate_motor_speed(displacement, angle)

    def grab(self):
        if self.our_defender.can_catch_ball(self.ball):
	    self.our_defender.catcher = 'closed'
	    self.current_state = self.GRABBED
	    return grab_ball()
	else:
	    self.current_state = self.GO_TO_BALL
	    return defender_stop()
            #if self.our_defender.can_catch_ball(self.ball):
            #    self.our_defender.catcher = 'closed'
            #    return grab_ball()
            #else:
            #	self.current_state = self.PREPARE
            #   return defender_stop()


class DefenderPass(Strategy):

    ROTATE, POSITION, CHECK, SHOOT, FINISHED = 'ROTATE', 'POSITION', 'CHECK', 'SHOOT', 'FINISHED'
    STATES = [ROTATE, POSITION, CHECK, SHOOT, FINISHED]

    LEFT, RIGHT = 'left', 'right'
    SIDES = [LEFT, RIGHT]

    UP, DOWN = 'UP', 'DOWN'

    def __init__(self, world):
        super(DefenderPass, self).__init__(world, self.STATES)

        # Map states into functions
        self.NEXT_ACTION_MAP = {
	    self.ROTATE: self.rotate,
	    self.POSITION: self.position,
	    self.CHECK: self.check,
            self.SHOOT: self.shoot,
            self.FINISHED: do_nothing
        }

        self.our_defender = self.world.our_defender
	self.our_attacker = self.world.our_attacker
	self.their_attacker = self.world.their_attacker

	def_zone = self.world._pitch._zones[self.world.our_defender.zone]
	self.att_zone = self.world._pitch._zones[self.world.our_attacker.zone]

	min_x, max_x, min_y, max_y  = def_zone.boundingBox()
	self.def_center_x = (min_x + max_x)/2
	self.center_y = (min_y + max_y)/2

	min_x, max_x, min_y, max_y  = self.att_zone.boundingBox()
	self.att_center_x = (min_x + max_x)/2

	self.pass_y_position = self._get_y_position()
	self.pass_x_position = self.def_center_x

    def rotate(self):
	angle = self.our_defender.get_rotation_to_point(self.att_center_x ,self.our_defender.y)

	if is_facing_target(angle):
	    self.current_state = self.POSITION;
	    return defender_stop()
	else:
	    return calculate_motor_speed(None, angle)

    def position(self):
        disp, angle = self.our_defender.get_direction_to_point(self.pass_x_position, self.pass_y_position)

        if has_matched(self.our_defender, x=self.pass_x_position, y=self.pass_y_position):
            self.current_state = self.CHECK
            return defender_stop()
        else:
            return calculate_motor_speed(disp, angle, backwards_ok=True, sideways_ok=True)

    def check(self):
	# blocked, avoid the attacker
	if has_matched(self.our_defender, x=self.our_defender.x, y=self.their_attacker.y):
	    self.pass_y_position = self._get_y_position()
	    self.current_state = self.ROTATE
	    return defender_stop()
	# not blocked, shoot
	else:
	    offset = 20
	    if self.pass_y_position > self.center_y:
		angle = self.our_defender.get_rotation_to_point(self.att_center_x ,self.pass_y_position + offset)
	    else:
		angle = self.our_defender.get_rotation_to_point(self.att_center_x ,self.pass_y_position - offset)
	    
	if is_facing_target(angle):
	    self.current_state = self.SHOOT;
	    return defender_stop()
	else:
	    return calculate_motor_speed(None, angle)

    def shoot(self):
        self.current_state = self.FINISHED
        self.our_defender.catcher = 'released'
        return kick_ball()

    def _get_y_position(self):
	offset = 80
	if self.their_attacker.y <= self.center_y:
	    return self.center_y + offset
	else:
	    return self.center_y - offset
       
class DefenderPosition(Strategy):

    PREPARE, POSITION, ROTATE, READY = 'PREPARE', 'POSITION', 'ROTATE', 'READY' 
    STATES = [PREPARE, POSITION, ROTATE, READY]
    LEFT, RIGHT = 'left', 'right'
    SIDES = [LEFT, RIGHT]

    def __init__(self, world):
        super(DefenderPosition, self).__init__(world, self.STATES)

        self.NEXT_ACTION_MAP = {
	    self.PREPARE: self.prepare,
	    self.POSITION: self.position,
            self.ROTATE: self.rotate,
	    self.READY: self.ready
        }
	
	self.our_goal = self.world.our_goal
        self.our_defender = self.world.our_defender
	self.our_attacker = self.world.our_attacker
	self.their_attacker = self.world.their_attacker

	def_zone = self.world._pitch._zones[self.world.our_defender.zone]

	min_x, max_x, self.min_y, self.max_y  = def_zone.boundingBox()
	self.center_y = (self.min_y + self.max_y)/2

    def prepare(self):
        self.current_state = self.POSITION

	if self.our_defender.catcher == 'closed' or self.our_defender.catcher == 'open':
	    self.our_defender.catcher = 'released'
	    return release_catcher()
	else:
	    return defender_stop()
	
    def position(self):
	goal_front_x = self.get_alignment_x(self.world._our_side)
        disp, angle = self.our_defender.get_direction_to_point(goal_front_x, self.center_y)

        if has_matched(self.our_defender, x=goal_front_x, y=self.center_y):
            self.current_state = self.ROTATE
            return defender_stop()
        else:
            return calculate_motor_speed(disp, angle, backwards_ok=True, sideways_ok=True)


    def rotate(self):
	angle_top = self.our_defender.get_rotation_to_point(self.our_defender.x, self.max_y)
	angle_bottom = self.our_defender.get_rotation_to_point(self.our_defender.x, self.min_y)
	
	if abs(angle_top) < abs(angle_bottom):
	    self.y_pos = self.max_y
	else:
	    self.y_pos = self.min_y

	angle = self.our_defender.get_rotation_to_point(self.our_defender.x, self.y_pos)

	if is_facing_target(angle):
            self.current_state = self.READY
            return defender_stop()
        else:
            return calculate_motor_speed(None, angle, backwards_ok=True)

  
    def ready(self):
	angle = self.our_defender.get_rotation_to_point(self.our_defender.x, self.y_pos)

	if not is_facing_target(angle):
            self.current_state = self.ROTATE
	return do_nothing()

    def get_alignment_x(self, side):
        assert side in self.SIDES
        if side == self.LEFT:
            return self.world.our_goal.x + self.GOAL_ALIGN_OFFSET
        else:
            return self.world.our_goal.x - self.GOAL_ALIGN_OFFSET

###########################################################################
# END OF USED DEFENDER STRATEGIES
###########################################################################

class DefenderPenalty(Strategy):

    PREPARE, DEFEND_GOAL = 'PREPARE', 'DEFEND_GOAL'
    STATES = [PREPARE, DEFEND_GOAL]
    LEFT, RIGHT = 'left', 'right'
    SIDES = [LEFT, RIGHT]

    def __init__(self, world):
        super(DefenderPenalty, self).__init__(world, self.STATES)

        self.NEXT_ACTION_MAP = {
	    self.PREPARE: self.prepare,
            self.DEFEND_GOAL: self.defend_goal
        }

        self.their_attacker = self.world.their_attacker
        self.our_defender = self.world.our_defender
        self.ball = self.world.ball
    
    def prepare(self):
        self.current_state = self.DEFEND_GOAL
        if self.our_defender.catcher == 'closed':
            self.our_defender.catcher = 'open'
	    return open_catcher()
        else:
            return do_nothing()
  
    def defend_goal(self):
        """
        Wait until the ball is fired, then try to block it.
        """
        # Predict where they are aiming.
	if self.ball.velocity <= BALL_VELOCITY: 
            predicted_y = predict_y_intersection(self.world, self.our_defender.x, self.their_attacker, bounce=False)
            return do_nothing()

	# Predict where the ball is moving and try to block it.
        elif self.ball.velocity > BALL_VELOCITY:
            predicted_y = predict_y_intersection(self.world, self.our_defender.x, self.ball, bounce=False)

            if (is_aligned(predicted_y, self.our_defender.y)):
                return defender_stop();
	    else:
            	return adjust_y_position(self.our_defender, predicted_y, self.world._our_side)

class DefenderDefendPenalty(Strategy):

    ANG_UNALIGNED, POS_UNALIGNED, DEFEND_GOAL, POS_UNALMOST = 'ANG_UNALIGNED', 'POS_UNALIGNED', 'DEFEND_GOAL', 'POS_UNALMOST'
    STATES = [ANG_UNALIGNED, POS_UNALIGNED, DEFEND_GOAL,POS_UNALMOST]
    LEFT, RIGHT = 'left', 'right'
    SIDES = [LEFT, RIGHT]

    GOAL_ALIGN_OFFSET = 30

    def __init__(self, world):
        super(DefenderDefendPenalty, self).__init__(world, self.STATES)
 
        self.NEXT_ACTION_MAP = {
            self.ANG_UNALIGNED: self.ang_align,
	    self.POS_UNALIGNED: self.pos_align,
            self.POS_UNALMOST: self.pos_almost,
            self.DEFEND_GOAL: self.defend_goal
        }

        self.our_goal = self.world.our_goal
        # Find the point we want to align to.
        self.goal_front_x = self.get_alignment_position(self.world._our_side)
        self.their_attacker = self.world.their_attacker
        self.our_defender = self.world.our_defender
        self.ball = self.world.ball
        self.their_goal = self.world.their_goal
    
    def pos_almost(self):
        if not is_aligned_almost(self.our_defender.y, self.our_goal.y):
            return adjust_y_position(self.our_defender, self.our_goal.y, self.world._our_side)
        elif not is_facing_target(self.our_defender.get_rotation_to_point(self.their_goal.x, self.their_goal.y)):
            self.current_sate = self.ANG_UNALIGNED
            return defender_stop()
        else:
            self.current_state = self.POS_UNALIGNED
            return defender_stop()

    def ang_align(self):
        """
        Align yourself to face the opposide side.
        """
        if is_facing_target(self.our_defender.get_rotation_to_point(self.their_goal.x, self.their_goal.y)):
            # Correct direction, ready to move
            self.current_state = self.POS_UNALIGNED
            return defender_stop()
        else:
            return adjust_angle(self.our_defender.get_rotation_to_point(self.their_goal.x, self.their_goal.y))
            

    def pos_align(self):
        """
        Align yourself to the middle of the goal.
        """
	if not is_aligned(self.our_defender.y, self.our_goal.y):
            return adjust_y_position(self.our_defender, self.our_goal.y, self.world._our_side)
	elif not is_facing_target(self.our_defender.get_rotation_to_point(self.their_goal.x, self.their_goal.y)):
	    self.current_state = self.ANG_UNALIGNED
	    #print 'Robot not aligned'
	    return defender_stop()
        else:
	    #print 'Robot aligned'
	    self.current_state = self.DEFEND_GOAL
            return defender_stop()
        

    def defend_goal(self):
        """
        Block the shot.
        """
	
	return defender_stop()
      
	if not is_aligned(self.our_defender.y, self.ball.y):
	    return adjust_y_position(self.our_defender, self.ball.y, self.world._our_side)
	else:
	   return defender_stop();
	

    def get_alignment_position(self, side):
        """
        Given the side, find the x coordinate of where we need to align to initially.
        """
        assert side in self.SIDES
        if side == self.LEFT:
            return self.world.our_goal.x + self.GOAL_ALIGN_OFFSET
        else:
            return self.world.our_goal.x - self.GOAL_ALIGN_OFFSET

    def get_almost_alignment(self, side):
        assert side in self.SIDES
        if side == self.LEFT:
            return self.world.our_goal.x + self.GOAL_ALMOST_OFFSET
        else:
            return self.world.our_goal.x - self.GOAL_ALMOST_OFFSET