# -*- coding: utf-8 -*-
from models import *
from collisions import *
from strategies import *
from utilities import *

class Planner:

    def __init__(self, our_side, pitch_num):
        self._world = World(our_side, pitch_num)
        self._world.our_defender.catcher_area = {'width' : 35, 'height' : 30, 'front_offset' : -5}
        self._world.our_attacker.catcher_area = {'width' : 35, 'height' : 30, 'front_offset' : -5}

        self._defender_strategies = {'defence' : [DefenderPenalty],
                                     'grab'    : [DefenderGrab],
                                     'pass'    : [DefenderPass]}

        self._defender_state = 'defence'
        self._defender_current_strategy = self.choose_defender_strategy(self._world)

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

        # We have the ball in our zone, so we grab and pass:
	if our_defender.catcher=='closed' and self._defender_state == 'pass':
	   # Assumed we catched successfully
	   return self._defender_current_strategy.generate()

	if self._defender_current_strategy.current_state == 'GRABBED':
	   self._defender_state = 'pass'
	   self._defender_current_strategy = self.choose_defender_strategy(self._world)
           return self._defender_current_strategy.generate()

        if self._world.pitch.zones[our_defender.zone].isInside(ball.x, ball.y) and ball.velocity < BALL_VELOCITY:
           # Check if we should switch from a grabbing to a scoring strategy.
           if self._defender_state == 'grab' and self._defender_current_strategy.current_state == 'GRABBED':
	      self._defender_state = 'pass'
              self._defender_current_strategy = self.choose_defender_strategy(self._world)

            # Check if we should switch from a defence to a grabbing strategy.
           elif self._defender_state == 'defence':
	      self._defender_state = 'grab'
              self._defender_current_strategy = self.choose_defender_strategy(self._world)

           elif self._defender_state == 'pass' and self._defender_current_strategy.current_state == 'FINISHED':
              self._defender_state = 'grab'
              self._defender_current_strategy = self.choose_defender_strategy(self._world)

	   return self._defender_current_strategy.generate()
	    
	 # Otherwise, we need to defend:
        else:
	    # If the bal is not in the defender's zone, the state should always be 'defend'.
           if not self._defender_state == 'defence':
	      self._defender_state = 'defence'
              self._defender_current_strategy = self.choose_defender_strategy(self._world)

           return self._defender_current_strategy.generate()
