# -*- coding: utf-8 -*-
from models import *
from collisions import *
from strategies import *
from utilities import *

class Planner:

    def __init__(self, our_side, pitch_num):
        self._world = World(our_side, pitch_num)
        self._world.our_defender.catcher_area = {'width' : 32, 'height' : 22, 'front_offset' : 8}
        self._world.our_attacker.catcher_area = {'width' : 32, 'height' : 22, 'front_offset' : 8}

        self._defender_strategies = {'defence'  : [DefenderDefend],
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
	if self._world.pitch.zones[our_defender.zone].isInside(ball.x, ball.y) and time.clock() - self._time_ball_entered_our_zone > 1.0:
           
	   # If we grabbed, switch from grabbing to passing
           if self._defender_state == 'grab' and self._defender_current_strategy.current_state == 'GRABBED':
	      self._defender_state = 'pass'
              self._defender_current_strategy = self.choose_defender_strategy(self._world)

           # Switch from defence to grabbing
           elif self._defender_state == 'defence':
	      self._defender_state = 'grab'
              self._defender_current_strategy = self.choose_defender_strategy(self._world)

	   # Switch from pass to grab
           elif self._defender_state == 'pass' and self._defender_current_strategy.current_state == 'FINISHED':
              self._defender_state = 'grab'
              self._defender_current_strategy = self.choose_defender_strategy(self._world)

	   # Switch from position to grab
	   elif self._defender_state == 'position':
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
           if not self._defender_state == 'defence':
	      self._defender_state = 'defence'
              self._defender_current_strategy = self.choose_defender_strategy(self._world)

           return self._defender_current_strategy.generate()