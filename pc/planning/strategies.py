# -*- coding: utf-8 -*-
from utilities import *
import math
from random import randint
from glob import BallState

class Strategy(object):

    GOAL_ALIGN_OFFSET = 45
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

class DefenderPass(Strategy):
    '''
    Once the defender grabs the ball, move to the center of the zone and shoot towards
    the wall of the center of the opposite attacker zone, in order to reach our_attacker
    attacker zone.
    '''

    ROTATE, POSITION, CHECK, SHOOT, FINISHED = 'ROTATE', 'POSITION', 'CHECK', 'SHOOT', 'FINISHED'
    STATES = [ROTATE, POSITION, CHECK, SHOOT, FINISHED]

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

    def rotate(self):
	angle = self.our_defender.get_rotation_to_point(self.att_center_x ,self.our_defender.y)

	if is_facing_target(angle):
	    self.current_state = self.POSITION;
	    return defender_stop()
	else:
	    return calculate_motor_speed(None, angle)

    # position to pass
    def position(self):
        disp, angle = self.our_defender.get_direction_to_point(self.def_center_x, self.pass_y_position)

        if has_matched(self.our_defender, x=self.def_center_x, y=self.pass_y_position):
            self.current_state = self.CHECK
            return defender_stop()
        else:
            return calculate_motor_speed(disp, angle, backwards_ok=True, sideways_ok=True)

    def check(self):
	# Blocked, avoid the attacker
	if has_matched(self.our_defender, x=self.our_defender.x, y=self.their_attacker.y):
	    self.pass_y_position = self._get_y_position()
	    self.current_state = self.ROTATE
	    return defender_stop()
	# Not blocked, shoot
	else:
	    angle = self.our_defender.get_rotation_to_point(self.att_center_x ,self.our_defender.y)
	    
	if is_facing_target(angle):
	    self.current_state = self.SHOOT;
	    return defender_stop()
	else:
	    return calculate_motor_speed(None, angle)


    def shoot(self):
        """
        Kick.
        """
        self.current_state = self.FINISHED
        self.our_defender.catcher = 'open'
        return kick_ball()

    def _get_y_position(self):
	offset = 80
	if self.their_attacker.y <= self.center_y:
	    return self.center_y + offset
	else:
	    return self.center_y - offset

class DefenderGrab(Strategy):

    PREPARE, GO_TO_BALL, GRAB_BALL, GRABBED = 'PREPARE', 'GO_TO_BALL', 'GRAB_BALL', 'GRABBED'
    STATES = [PREPARE, GO_TO_BALL, GRAB_BALL, GRABBED]
    def __init__(self, world):
        super(DefenderGrab, self).__init__(world, self.STATES)

        self.NEXT_ACTION_MAP = {
            self.PREPARE: self.prepare,
            self.GO_TO_BALL: self.position,
            self.GRAB_BALL: self.grab,
        }

        self.our_defender = self.world.our_defender
        self.ball = self.world.ball

    # make sure the grabber is open
    def prepare(self):
        self.current_state = self.GO_TO_BALL
        self.our_defender.catcher = 'open'
        return open_catcher()

    # move towards the ball until it is possible to catch it
    def position(self):
        displacement, angle = self.our_defender.get_direction_to_point(self.ball.x, self.ball.y)
        if self.our_defender.can_catch_ball(self.ball):
            self.current_state = self.GRAB_BALL
            return defender_stop()
        else:
            return calculate_motor_speed(displacement, angle)

    # grab the ball
    def grab(self):
        if self.our_defender.has_ball(self.ball) or BallState.lost:
            self.current_state = self.GRABBED
            return defender_stop()
        else:
	    self.our_defender.catcher = 'closed'
	    self.current_state = self.GRABBED
	    return grab_ball()
            #if self.our_defender.can_catch_ball(self.ball):
            #    self.our_defender.catcher = 'closed'
            #    return grab_ball()
            #else:
            #	self.current_state = self.PREPARE
            #   return defender_stop()
       
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
	if self.our_defender.catcher == 'closed':
	    self.our_defender.catcher = 'open'
	    return kick_ball()
	else:
	    return do_nothing()
	
    def position(self):
	goal_front_x = self.get_alignment_x(self.world._our_side)
        disp, angle = self.our_defender.get_direction_to_point(goal_front_x, self.center_y)

        if has_matched(self.our_defender, x=goal_front_x, y=self.center_y):
            self.current_state = self.ROTATE
            return defender_stop()
        else:
            return calculate_motor_speed(disp, angle, backwards_ok=True, sideways_ok=True)


    def rotate(self):
	"""
	Rotate towards the opposite side
	"""
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
            return calculate_motor_speed(None, angle, backwards_ok=True, sideways_ok=True)

  
    def ready(self):
	"""
	Wait for something to happen
	"""
	angle = self.our_defender.get_rotation_to_point(self.our_defender.x, self.y_pos)

	if not is_facing_target(angle):
            self.current_state = self.ROTATE
	return do_nothing()

    def get_alignment_x(self, side):
        """
        Given the side, find the x coordinate of where we need to align to initially.
        """
        assert side in self.SIDES
        if side == self.LEFT:
            return self.world.our_goal.x + self.GOAL_ALIGN_OFFSET
        else:
            return self.world.our_goal.x - self.GOAL_ALIGN_OFFSET

class DefenderDefend(Strategy):

    POSITION, DEFEND_GOAL = 'POSITION', 'DEFEND_GOAL'
    STATES = [POSITION, DEFEND_GOAL]

    LEFT, RIGHT = 'left', 'right'
    SIDES = [LEFT, RIGHT]
    
    def __init__(self, world):
        super(DefenderDefend, self).__init__(world, self.STATES)
 
        self.NEXT_ACTION_MAP = {
	    self.POSITION: self.position,
            self.DEFEND_GOAL: self.defend_goal
        }

        self.ball = self.world.ball
	self.our_defender = self.world.our_defender
	self.their_attacker = self.world.their_attacker
	
	def_zone = self.world._pitch._zones[self.world.our_defender.zone]
	min_x, max_x, self.min_y, self.max_y  = def_zone.boundingBox()
	self.center_y = (self.min_y + self.max_y)/2

	self.top_post = self.center_y + 60
	self.bottom_post = self.center_y - 60
    
    def position(self):
	goal_front_x = self.get_alignment_x(self.world._our_side)
        disp, angle = self.our_defender.get_direction_to_point(goal_front_x, self.center_y)

	if self.our_defender.catcher == 'closed':
	    self.our_defender.catcher = 'open'
	    return kick_ball()

        if has_matched(self.our_defender, x=goal_front_x, y=self.center_y):
            self.current_state = self.DEFEND_GOAL
            return defender_stop()
        else:
            return calculate_motor_speed(disp, angle, backwards_ok=True, sideways_ok=True)

    def defend_goal(self):
        """
        Block the shot
        """

	if BallState.lost:
	    track_y = self.their_attacker.y
	    print "Can't see ball, tracking their attacker"
	else:
	    track_y = self.ball.y

	# tracking coordinate not within the goal range, at the top
	if (track_y > self.top_post+10):
	    disp, angle = self.our_defender.get_direction_to_point(self.our_defender.x, self.top_post)
	    if has_matched(self.our_defender, x=self.our_defender.x, y=self.top_post):
		return defender_stop()
	    else:
		return calculate_motor_speed(disp, angle, backwards_ok=True, full_speed=True, sideways_ok=True)
	
	# tracking coordinate not within the goal range, at the bottom
	elif (track_y < self.bottom_post-10):
	    disp, angle = self.our_defender.get_direction_to_point(self.our_defender.x, self.bottom_post)
	    if has_matched(self.our_defender, x=self.our_defender.x, y=self.bottom_post):
		return defender_stop()
	    else:
		return calculate_motor_speed(disp, angle, backwards_ok=True, full_speed=True, sideways_ok=True)
	
	# ball within the goal range
	elif has_matched(self.our_defender, x=self.our_defender.x, y=track_y):
	    return defender_stop()
	else:
	    disp, angle = self.our_defender.get_direction_to_point(self.our_defender.x, track_y)
	    return calculate_motor_speed(disp, angle, backwards_ok=True, full_speed=True, sideways_ok=True)
	
    def get_alignment_x(self, side):
        """
        Given the side, find the x coordinate of where we need to align to initially.
        """
        assert side in self.SIDES
        if side == self.LEFT:
            return self.world.our_goal.x + self.GOAL_ALIGN_OFFSET
        else:
            return self.world.our_goal.x - self.GOAL_ALIGN_OFFSET

###########################################################################
# END OF DEFENDER STRATEGIES
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

class AttackerDefend(Strategy):

    UNALIGNED, BLOCK_PASS = 'UNALIGNED', 'BLOCK_PASS'
    STATES = [UNALIGNED, BLOCK_PASS]

    def __init__(self, world):
        super(AttackerDefend, self).__init__(world, self.STATES)

        self.NEXT_ACTION_MAP = {
            self.UNALIGNED: self.align,
            self.BLOCK_PASS: self.block_pass
        }

        zone = self.world._pitch._zones[self.world.our_attacker.zone]
        min_x, max_x, min_y, max_y  = zone.boundingBox()
        self.center_x = (min_x + max_x)/2
        self.center_y = (min_y + max_y)/2
        self.our_attacker = self.world.our_attacker
        self.our_defender = self.world.our_defender
        self.their_attacker = self.world.their_attacker
        self.their_defender = self.world.their_defender

    def align(self):
        """
        Align yourself with the middle of our zone.
        """
        if has_matched(self.our_attacker, x=self.center_x, y=self.our_attacker.y):
            # We're there. Advance the states and formulate next action.
            self.current_state = self.BLOCK_PASS
            return do_nothing()
        else:
            displacement, angle = self.our_attacker.get_direction_to_point(
                self.center_x, self.our_attacker.y)
            return calculate_motor_speed(displacement, angle, backwards_ok=True)

    def block_pass(self):
        predicted_y = predict_y_intersection(self.world, self.our_attacker.x, self.their_defender, full_width=True, bounce=True)
        if predicted_y is None:
            ideal_x = self.our_attacker.x
            ideal_y = (self.their_attacker.y + self.their_defender.y) / 2
        else:
            ideal_x = self.our_attacker.x
            ideal_y = predicted_y - 7  *math.sin(self.our_attacker.angle)

        displacement, angle = self.our_attacker.get_direction_to_point(ideal_x, ideal_y)
        if not has_matched(self.our_attacker, ideal_x, ideal_y):
            return calculate_motor_speed(displacement, angle, backwards_ok=True)
        else:
            return do_nothing()


class AttackerCatch(Strategy):

    PREPARE, CATCH = 'PREPARE', 'CATCH'
    STATES = [PREPARE, CATCH]

    def __init__(self, world):
        super(AttackerCatchStrategy, self).__init__(world, STATES)

        self.NEXT_ACTION_MAP = {
            self.PREPARE: self.prepare,
            self.CATCH: self.catch
        }

        self.our_attacker = self.world.our_attacker
        self.ball = self.world.ball

    def prepare(self):
        self.current_state = self.CATCH
        if self.our_attacker.catcher == 'closed':
            self.our_attacker.catcher = 'open'
	    return open_catcher()
        else:
            return do_nothing()

    def catch(self):
        ideal_x = self.our_attacker.x
        ideal_y = self.ball.y

        displacement, angle = self.our_attacker.get_direction_to_point(ideal_x, ideal_y)
        return calculate_motor_speed(displacement, angle, backwards_ok=True)


class AttackerPositionCatch(Strategy):
    '''
    This catching strategy positions the robot in the middle of the zone
    so that (ideally) it does not need to do anything
    '''
    PREPARE, ALIGN, ROTATE = 'PREPARE', 'ALIGN', 'ROTATE'
    STATES = [PREPARE, ALIGN, ROTATE]

    def __init__(self, world):
        super(AttackerPositionCatch, self).__init__(world, self.STATES)

        self.NEXT_ACTION_MAP = {
            self.PREPARE: self.prepare,
            self.ALIGN: self.align,
            self.ROTATE: self.rotate
        }

        self.our_attacker = self.world.our_attacker
        self.our_defender = self.world.our_defender
        self.ball = self.world.ball
        zone = self.world._pitch._zones[self.our_attacker.zone]
        min_x, max_x, min_y, max_y  = zone.boundingBox()
        self.center_x = (min_x + max_x)/2
        self.center_y = (min_y + max_y)/2

    def prepare(self):
        self.current_state = self.ALIGN
        if self.our_attacker.catcher == 'closed':
            self.our_attacker.catcher = 'open'
            return open_catcher()
        else:
            return do_nothing()

    def align(self):
        if has_matched(self.our_attacker, x=self.center_x, y=self.center_y):
            self.current_state = self.ROTATE
            return do_nothing()
        else:
            displacement, angle = self.our_attacker.get_direction_to_point(
                self.center_x, self.center_y)
            return calculate_motor_speed(displacement, angle, backwards_ok=True)

    def rotate(self):
        '''
        Rotate in the center of the zone in order to intercept the pass of the defender.
        Tries to match the correct angle given the angle of the defender.
        '''
        defender_angle = self.our_defender.angle
        attacker_angle = None
        our_side = self.world._our_side
        if our_side == 'left':
            if defender_angle > 0 and defender_angle < pi / 2:
                attacker_angle = 3 * pi / 4
            elif defender_angle > 3 * pi / 2:
                attacker_angle = 5 * pi / 4
        else:
            if defender_angle > pi / 2 and defender_angle < pi:
                attacker_angle = pi / 4
            elif defender_angle > pi and defender_angle < 3 * pi / 2:
                attacker_angle = 7 * pi / 4

        if attacker_angle:
            # Offsets the attacker's position in the direction of the desired angled in order to calculate the
            # required rotation.
            displacement, angle = self.our_attacker.get_direction_to_point(self.our_attacker.x + 10 * math.cos(attacker_angle),
                                                                           self.our_attacker.y + 10 * math.sin(attacker_angle))
            return calculate_motor_speed(None, angle, careful=True)
        
        return do_nothing()

class AttackerGrab(Strategy):

    PREPARE, GO_TO_BALL, GRAB_BALL, GRABBED = 'PREPARE', 'GO_TO_BALL', 'GRAB_BALL', 'GRABBED'
    STATES = [PREPARE, GO_TO_BALL, GRAB_BALL, GRABBED]
    def __init__(self, world):
        super(AttackerGrab, self).__init__(world, self.STATES)

        self.NEXT_ACTION_MAP = {
            self.PREPARE: self.prepare,
            self.GO_TO_BALL: self.position,
            self.GRAB_BALL: self.grab,
            self.GRABBED: do_nothing
        }

        self.our_attacker = self.world.our_attacker
        self.ball = self.world.ball

    def prepare(self):
        self.current_state = self.GO_TO_BALL
        if self.our_attacker.catcher == 'closed':
            self.our_attacker.catcher = 'open'
            return open_catcher()
        else:
            return do_nothing()

    def position(self):
        displacement, angle = self.our_attacker.get_direction_to_point(self.ball.x, self.ball.y)

        if self.our_attacker.can_catch_ball(self.ball):
            self.current_state = self.GRAB_BALL
            return do_nothing()
        else:
            return calculate_motor_speed(displacement, angle)

    def grab(self):
        if self.our_attacker.has_ball(self.ball):
            self.current_state = self.GRABBED
            return do_nothing()
        else:
            if self.our_attacker.can_catch_ball(self.ball):
                self.our_attacker.catcher = 'closed'
		self.current_state = self.GRABBED
                return grab_ball()
            else:
            	self.current_state = self.PREPARE
                return do_nothing()

class AttackerScore(Strategy):
    """
    """
    ROTATE, SHOOT, FINISHED = 'ROTATE', 'SHOOT', 'FINISHED'
    STATES = [ROTATE, SHOOT, FINISHED]

    UP, DOWN = 'UP', 'DOWN'

    def __init__(self, world):
        super(AttackerScore, self).__init__(world, self.STATES)

        # Map states into functions
        self.NEXT_ACTION_MAP = {
	    self.ROTATE: self.rotate,
            self.SHOOT: self.shoot,
            self.FINISHED: do_nothing
        }

        self.our_attacker = self.world.our_attacker
        self.ball = self.world.ball

        # Find the position to shoot from and cache it
        self.shooting_pos = self._get_shooting_coordinates(self.our_attacker)

    def rotate(self):
	"""
	Rotate
	"""

	angle = self.our_attacker.get_rotation_to_point(self.world.their_goal.x, self.world.their_goal.y)

	if is_facing_target(angle):
            self.current_state = self.SHOOT
            return do_nothing()
        else:
            return calculate_motor_speed(-1, angle)

    def shoot(self):
        """
        Kick.
        """

        self.current_state = self.FINISHED
        self.our_attacker.catcher = 'closed'
        return kick_ball()

    def _get_shooting_coordinates(self, robot):
        """
        Retrive the coordinates to which we need to move before we set up the pass.
        """
        zone_index = robot.zone
        zone_poly = self.world.pitch.zones[zone_index][0]

        min_x = int(min(zone_poly, key=lambda z: z[0])[0])
        max_x = int(max(zone_poly, key=lambda z: z[0])[0])

        x = min_x + (max_x - min_x) / 2
        y =  self.world.pitch.height / 2

        return (x, y)


class AttackerDriveBy(Strategy):
    """
    Strategy where we drive forward and backwards, rotate and shoot.
    Idea:
        1) Move to a location either in the UP or DOWN section, opposite to
           the location of the opposite defender
        2) If path is clear, proceed. Otherwise, switch sides.
        3) Rotate to face the goal
        4) Shoot
    """

    DRIVE, ALIGN_GOAL, SHOOT, FINISHED = 'DRIVE', 'ALIGN_GOAL', 'SHOOT', 'FINISHED'
    STATES = [DRIVE, ALIGN_GOAL, SHOOT, FINISHED]

    X_OFFSET = 70
    Y_OFFSET = 100

    UP, DOWN = 'UP', 'DOWN'

    def __init__(self, world):
        super(AttackerDriveBy, self).__init__(world, self.STATES)

        self.NEXT_ACTION_MAP = {
            self.DRIVE: self.drive,
            self.ALIGN_GOAL: self.align_to_goal,
            self.SHOOT: self.shoot,
            self.FINISHED: do_nothing
        }

        self.our_attacker = self.world.our_attacker
        self.their_defender = self.world.their_defender
        self.drive_side = None
        self._get_goal_points()
        self.pick_side()

    def pick_side(self):
        '''
        At first, choose side opposite to their defender.
        '''
        middle_y = self.world.pitch.height / 2
        if self.world.their_defender.y < middle_y:
            self.drive_side = self.UP
        self.drive_side = self.DOWN

    def drive(self):
        x = self.get_zone_attack_x_offset()
        if self.drive_side == self.UP:
            y = self.world.pitch.height
        else:
            y = 0

        # offset the y
        if self.drive_side == self.UP:
            y -= self.Y_OFFSET
        else:
            y += self.Y_OFFSET

        distance, angle = self.our_attacker.get_direction_to_point(x, y)
        if has_matched(self.our_attacker, x=x, y=y):
            self.current_state = self.ALIGN_GOAL
            return do_nothing()

        return calculate_motor_speed(distance, angle)

    def align_to_goal(self):
        other_side = self.UP if self.drive_side == self.DOWN else self.DOWN
        goal_x = self.world.their_goal.x
        goal_y = self.goal_points[self.drive_side]

        angle = self.our_attacker.get_rotation_to_point(goal_x, goal_y)

        if has_matched(self.our_attacker, angle=angle, angle_threshold=math.pi/30):
            if is_shot_blocked(self.world, self.our_attacker, self.their_defender):
                # Drive to the other side.
                self.drive_side = other_side
                self.current_state = self.DRIVE
            else:
                self.current_state = self.SHOOT
            return do_nothing()

        return calculate_motor_speed(None, angle)

    def shoot(self):
        self.current_state = self.FINISHED
        return kick_ball()

    def get_zone_attack_x(self):
        """
        Find the border coordinate for our attacker zone and their defender.
        """
        attacker = self.world.our_attacker
        zone_poly = self.world.pitch.zones[attacker.zone][0]

        f = max if attacker.zone == 2 else min
        return f(zone_poly, key=lambda x: x[0])[0]

    def get_zone_attack_x_offset(self):
        """
        Get the x coordinate already offset
        """
        our_attacker = self.world.our_attacker
        middle_x = self.get_zone_attack_x()
        if our_attacker.zone == 2:
            middle_x -= self.X_OFFSET
        else:
            middle_x += self.X_OFFSET
        return middle_x

    def _get_goal_corner_y(self, side):
        """
        Get the coordinates of where to aim / shoot.
        """
        assert side in [self.UP, self.DOWN]
        if side == self.UP:
            # y coordinate of the goal is DOWN, offset by the width
            return self.world.their_goal.y + self.world.their_goal.width / 2
        return self.world.their_goal.y - self.world.their_goal.width / 2

    def _get_goal_points(self):
        # Get the polygon of their defender's zone.
        zone_poly = self.world.pitch.zones[self.their_defender.zone][0]
        goal_points = sorted(zone_poly, key=lambda z: z[0], reverse=(self.world._our_side=='left'))[:2]
        goal_points = sorted(goal_points, key=lambda z: z[1])
        self.goal_points = {self.DOWN: goal_points[0][1]+30, self.UP: goal_points[1][1]-30}


class AttackerDriveByTurn(Strategy):

    CENTER, ROTATE, DRIVE, SHOOT, FINISHED = 'CENTER', 'ROTATE', 'DRIVE', 'SHOOT', 'FINISHED'
    STATES = [CENTER, ROTATE, DRIVE, SHOOT, FINISHED]

    Y_OFFSET = 0

    UP, DOWN = 'UP', 'DOWN'

    def __init__(self, world):
        super(AttackerDriveByTurn, self).__init__(world, self.STATES)

        self.NEXT_ACTION_MAP = {
            self.CENTER: self.center,
            self.ROTATE: self.rotate,
            self.DRIVE: self.drive,
            self.SHOOT: self.shoot,
            self.FINISHED: do_nothing
        }

        self.our_attacker = self.world.our_attacker
        self.our_defender = self.world.our_defender
        self.their_defender = self.world.their_defender
        self.drive_side = None
        self.align_y = None
        self._get_goal_points()
        self.pick_side()
        self.laps_left = 5

    def pick_side(self):
        '''
        At first, choose side opposite to their defender.
        '''
        middle_y = self.world.pitch.height / 2
        if self.world.their_defender.y < middle_y:
            self.drive_side = self.UP
        self.drive_side = self.DOWN

    def center(self):
        if has_matched(self.our_attacker, x=self._get_zone_center_x(), y=self.our_attacker.y):
            # We're there. Advance the states and formulate next action.
            if self.our_attacker.angle < math.pi:
                self.align_y = self.world.pitch.height
            else:
                self.align_y = 0
            self.current_state = self.ROTATE
            return do_nothing()
        else:
            displacement, angle = self.our_attacker.get_direction_to_point(
                self._get_zone_center_x(), self.our_attacker.y)
            return calculate_motor_speed(displacement, angle, backwards_ok=True, careful=True)

    def rotate(self):
        displacement, angle = self.our_attacker.get_direction_to_point(self.our_attacker.x, self.align_y)
        if has_matched(self.our_attacker, angle=angle, angle_threshold=math.pi/30):
            self.current_state = self.DRIVE
            return do_nothing()
        else:
            return calculate_motor_speed(None, angle, careful=True)

    def drive(self):
        y = self.goal_points[self.drive_side] - 10 * math.sin(self.our_attacker.angle)

        distance, angle = self.our_attacker.get_direction_to_point(self.our_attacker.x, y)
        if has_matched(self.our_attacker, x=self.our_attacker.x, y=y):
            #print abs(self.our_attacker.y - self.their_defender.y)
            if abs(self.our_attacker.y - self.their_defender.y) > 30 or self.laps_left == 0:
                self.current_state = self.SHOOT
            else:
                self.drive_side = self.UP if self.drive_side == self.DOWN else self.DOWN
                self.laps_left -= 1
                self.current_state = self.ROTATE
            return do_nothing()
        else:
            return calculate_motor_speed(distance, angle, backwards_ok=True)

    def shoot(self):
        # Decide the direction of the right angle turn, based on our position and
        # side on the pitch.
        if self.world._our_side == 'right':
            if self.our_attacker.angle < math.pi:
                orientation = 1
            else:
                orientation = -1
        else:
            if self.our_attacker.angle < math.pi:
                orientation = -1
            else:
                orientation = 1
        self.current_state = self.FINISHED
        self.our_attacker.catcher = 'open'
        return turn_shoot(orientation)

    def _get_zone_center_x(self):
        """
        Find the border coordinate for our attacker zone and their defender.
        """
        attacker = self.world.our_attacker
        zone_poly = self.world.pitch.zones[attacker.zone][0]

        min_x = int(min(zone_poly, key=lambda z: z[0])[0])
        max_x = int(max(zone_poly, key=lambda z: z[0])[0])

        return (min_x + max_x) / 2

    def _get_goal_points(self):
        # Get the polygon of their defender's zone.
        zone_poly = self.world.pitch.zones[self.their_defender.zone][0]
        goal_points = sorted(zone_poly, key=lambda z: z[0], reverse=(self.world._our_side=='left'))[:2]
        goal_points = sorted(goal_points, key=lambda z: z[1])
        self.goal_points = {self.DOWN: goal_points[0][1]+40, self.UP: goal_points[1][1]-40}


class AttackerTurnScore(Strategy):
    """
    Move up and down the opponent's goal line and suddenly turn 90 degrees and kick if the
    path is clear.
    """

    UNALIGNED, POSITION, KICK, FINISHED = 'UNALIGNED', 'POSITION', 'KICK', 'FINISHED'
    STATES = [UNALIGNED, POSITION, KICK, FINISHED]

    def __init__(self, world):
        super(AttackerTurnScore, self).__init__(world, self.STATES)

        self.NEXT_ACTION_MAP = {
            self.UNALIGNED: self.align,
            self.POSITION: self.position,
            self.KICK: self.kick,
            self.FINISHED: do_nothing
        }

        self.their_goal = self.world.their_goal
        self.our_attacker = self.world.our_attacker
        self.their_defender = self.world.their_defender

        # Distance that the attacker should keep from its boundary.
        self.offset = 60

        # Opponent's goal edge where our attacker is currently heading.
        self.point = 0

    def align(self):
        '''
        Go to the boundary of the attacker's zone and align with the center
        of the goal line.
        '''
        ideal_x = self._get_alignment_x()
        ideal_y = self.their_goal.y

        if has_matched(self.our_attacker, x=ideal_x, y=ideal_y):
            self.current_state = self.POSITION
            return do_nothing()
        else:
            distance, angle = self.our_attacker.get_direction_to_point(ideal_x, ideal_y)
            return calculate_motor_speed(distance, angle)

    def position(self):
        '''
        Go up an down the goal line waiting for the first opportunity to shoot.
        '''
        our_attacker = self.our_attacker
        # Check if we have a clear shot
        if not is_attacker_shot_blocked(self.world, self.our_attacker, self.their_defender) and \
               (abs(our_attacker.angle - math.pi / 2) < math.pi / 20 or \
               abs(our_attacker.angle - 3*math.pi/2) < math.pi / 20):
            self.current_state = self.KICK
            return self.kick()

        else:
            # If our shot is blocked, continue moving up and down the goal line.
            # We want the center of the robot to be inside the goal line.
            goal_width = self.their_goal.width/2
            goal_edges = [self.their_goal.y - goal_width + 10,
                          self.their_goal.y + goal_width - 10]
            ideal_x = self.our_attacker.x
            ideal_y = goal_edges[self.point]

            if has_matched(self.our_attacker, x=self.our_attacker.x, y=ideal_y):
                # Go to the other goal edge
                self.point = 1 - self.point
                ideal_y = goal_edges[self.point]

            distance, angle = self.our_attacker.get_direction_to_point(ideal_x, ideal_y)
            return calculate_motor_speed(distance, angle, backwards_ok=True)

    def kick(self):
        # Decide the direction of the right angle turn, based on our position and
        # side on the pitch.
        if self.world._our_side == 'left':
            if self.our_attacker.angle > 0 and self.our_attacker.angle < math.pi:
                orientation = -1
            else:
                orientation = 1
        else:
            if self.our_attacker.angle > 0 and self.our_attacker.angle < math.pi:
                orientation = 1
            else:
                orientation = -1

        self.current_state = self.FINISHED
        return turn_shoot(orientation)

    def _get_alignment_x(self):
        # Get the polygon of our attacker's zone.
        zone = self.our_attacker.zone
        assert zone in [1,2]
        zone_poly = self.world.pitch.zones[zone][0]

        # Choose the appropriate function to determine the borderline of our
        # attacker's zone facing the opponent's goal.
        side = {1: min, 2: max}
        f = side[zone]

        # Get the x coordinate that our attacker needs to match.
        sign = {1: 1, 2: -1}
        boundary_x = int(f(zone_poly, key=lambda z: z[0])[0]) + sign[zone]*self.offset
        return boundary_x


class AttackerGrabCareful(Strategy):
    """
    Carefully grabbing the ball when it is located by the wall.
    Idea:
        Approach perpendicular to the wall to avoid getting stuck by the wall.
    """

    UNALIGNED, POSITIONED, ALIGNED, GRABBED = 'UNALIGNED', 'POSITIONED', 'ALIGNED', 'GRABBED'
    STATES = [UNALIGNED, POSITIONED, ALIGNED, GRABBED]
    BALL_Y_OFFSET = 80

    def __init__(self, world):
        super(AttackerGrabCareful, self).__init__(world, self.STATES)

        self.NEXT_ACTION_MAP = {
            self.UNALIGNED: self.position,
            self.POSITIONED: self.align,
            self.ALIGNED: self.grab,
            self.GRABBED: self.finish
        }

        self.ball_side = self.get_ball_side()

    def position(self):
        our_attacker = self.world.our_attacker
        ball = self.world.ball

        # Find ideal x and y
        ideal_x = ball.x
        if self.ball_side == self.UP:
            ideal_y = ball.y - self.BALL_Y_OFFSET
        else:
            ideal_y = ball.y + self.BALL_Y_OFFSET

        if has_matched(our_attacker, x=ideal_x, y=ideal_y):
            self.current_state = self.POSITIONED
            return self.align()

        distance, angle = our_attacker.get_direction_to_point(ideal_x, ideal_y)
        return calculate_motor_speed(distance, angle, careful=True)

    def align(self):
        our_attacker = self.world.our_attacker
        ball = self.world.ball

        distance, angle = our_attacker.get_direction_to_point(ball.x, ball.y)

        if has_matched(our_attacker, angle=angle):
            self.current_state = self.ALIGNED
            return self.grab()

        motors = calculate_motor_speed(None, angle, careful=True)
        return motors


    def grab(self):
        our_attacker = self.world.our_attacker
        ball = self.world.ball

        if our_attacker.can_catch_ball(ball):
            self.current_state = self.GRABBED
            return grab_ball()

        distance, angle = our_attacker.get_direction_to_point(ball.x, ball.y)
        return calculate_motor_speed(distance, angle, careful=True)

    def finish(self):
        return do_nothing()

    def get_ball_side(self):
        ball = self.world.ball
        middle = self.world.pitch.height / 2
        if ball.y < middle:
            return self.DOWN
        return self.UP