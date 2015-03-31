# -*- coding: utf-8 -*-
from models import *
from collisions import *
from strategies import *
from utilities import *
from glob import BallState

class Planner:

    def __init__(self, our_side, pitch_num):
        self._world = World(our_side, pitch_num)
        self._world.our_defender.catcher_area = {'width' : 26, 'height' : 24, 'front_offset' : 10}
        self._world.our_attacker.catcher_area = {'width' : 26, 'height' : 24, 'front_offset' : 10}

        self._defender_strategies = {'defence'  : [DefenderDefend],
				     'confuse'  : [DefenderConfuse],
                                     'grab'     : [DefenderGrab],
                                     'pass'     : [DefenderPass],
				     'position' : [DefenderPosition]}

        self._defender_state = 'defence'
        self._defender_current_strategy = self.choose_defender_strategy(self._world)

	self._time_ball_entered_our_zone = 0
	
	generate_speed_coeff_matrix()

    # Choose the first strategy in the applicable list.
    def choose_defender_strategy(self, world):
        next_strategy = self._defender_strategies[self._defender_state][0]
        return next_strategy(world)

    @property
    def defender_strat_state(self):
        return self._defender_current_strategy.current_state

    @property
    def defender_state(self):
        return self._defender_state

    @defender_state.setter
    def defender_state(self, new_state):
        assert new_state in ['defence', 'attack']
        self._defender_state = new_state

    def update_world(self, position_dictionary):
        self._world.update_positions(position_dictionary)

    def plan(self, robot='defender'):
        assert robot in ['defender']
        our_defender = self._world.our_defender
        our_attacker = self._world.our_attacker
        their_defender = self._world.their_defender
        their_attacker = self._world.their_attacker
        ball = self._world.ball

	if not self._world.pitch.zones[our_defender.zone].isInside(ball.x, ball.y):
	    self._time_ball_entered_our_zone = 0
	else:
	    if self._time_ball_entered_our_zone == 0:
		self._time_ball_entered_our_zone = time.clock()

	# Ball in our zone for longer than two seconds, so can proceed with grabbing
	if self._world.pitch.zones[our_defender.zone].isInside(ball.x, ball.y) and time.clock() - self._time_ball_entered_our_zone > 0.5:
           
	   # If we grabbed, switch from grabbing to passing
           if self._defender_state == 'grab' and self._defender_current_strategy.current_state == 'GRABBED':
	      self._defender_state = 'pass'
              self._defender_current_strategy = self.choose_defender_strategy(self._world)

           # Switch from defence to grabbing
           elif self._defender_state == 'defence':
	      self._defender_state = 'grab'
              self._defender_current_strategy = self.choose_defender_strategy(self._world)

	   # Switch from pass to grab as finished with the pass
           elif self._defender_state == 'pass' and self._defender_current_strategy.current_state == 'FINISHED':
              self._defender_state = 'grab'
              self._defender_current_strategy = self.choose_defender_strategy(self._world)
  
	   # Switch from pass to grab because ball was missed
	   elif self._defender_state == 'pass' and not BallState.lost and not has_matched(our_defender, x=ball.x, y=ball.y, distance_threshold=45):
	      self._defender_state = 'grab'
              self._defender_current_strategy = self.choose_defender_strategy(self._world)

	   # Switch from position to grab
	   elif self._defender_state == 'position':
	      self._defender_state = 'grab'
	      self._defender_current_strategy = self.choose_defender_strategy(self._world)

	   # Switch from confuse to grab
	   elif self._defender_state == 'confuse':
	      self._defender_state = 'grab'
	      self._defender_current_strategy = self.choose_defender_strategy(self._world)
	  
	   return self._defender_current_strategy.generate()

	# Ball in our attacker's zone or their defender's zone, go to the middle of the zone and align
	elif self._world.pitch.zones[our_attacker.zone].isInside(ball.x, ball.y) or self._world.pitch.zones[their_defender.zone].isInside(ball.x, ball.y):
	   if not self._defender_state == 'position': 
	      self._defender_state = 'position' 
	      self._defender_current_strategy = self.choose_defender_strategy(self._world)

	   return self._defender_current_strategy.generate()
    
	# Otherwise, we need to defend as the opposite side have the ball
        else:
	   if not self._world.pitch.zones[our_defender.zone].isInside(ball.x, ball.y) and not self._world.pitch.zones[their_attacker.zone].isInside(ball.x, ball.y):
	      return defender_stop()

	   if BallState.lost or has_matched(their_attacker, x=ball.x, y=ball.y):
	      if not self._defender_state == 'confuse':
		  self._defender_state = 'confuse'
		  self._defender_current_strategy = self.choose_defender_strategy(self._world)
    
           elif not self._defender_state == 'defence':
	      self._defender_state = 'defence'
              self._defender_current_strategy = self.choose_defender_strategy(self._world)

           return self._defender_current_strategy.generate()