# -*- coding: utf-8 -*-
from models import *
from collisions import *
from strategies import *
from utilities import *


class Planner:

    def __init__(self, our_side, pitch_num):
        self._world = World(our_side, pitch_num)
        self._world.our_defender.catcher_area = {'width' : 35, 'height' : 30, 'front_offset' : -4}
        self._world.our_attacker.catcher_area = {'width' : 35, 'height' : 30, 'front_offset' : -4}

        # self._defender_defence_strat = DefenderDefence(self._world)
        # self._defender_attack_strat = DefaultDefenderAttack(self._world)

        self._attacker_strategies = {'defence' : [AttackerDefend],
                                     'grab' : [AttackerGrab, AttackerGrabCareful],
                                     'score' : [AttackerScore],
                                     'catch' : [AttackerPositionCatch, AttackerCatch]}

        self._defender_strategies = {'defence' : [DefenderPenalty],
                                     'grab' : [DefenderGrab],
                                     'pass' : [DefenderPass]}

        self._defender_state = 'defence'
        self._defender_current_strategy = self.choose_defender_strategy(self._world)

        self._attacker_state = 'defence'
        self._attacker_current_strategy = self.choose_attacker_strategy(self._world)

    # Provisional. Choose the first strategy in the applicable list.
    def choose_attacker_strategy(self, world):
        next_strategy = self._attacker_strategies[self._attacker_state][0]
        return next_strategy(world)

    # Provisional. Choose the first strategy in the applicable list.
    def choose_defender_strategy(self, world):
        next_strategy = self._defender_strategies[self._defender_state][0]
        return next_strategy(world)

    @property
    def attacker_strat_state(self):
        return self._attacker_current_strategy.current_state

    @property
    def defender_strat_state(self):
        return self._defender_current_strategy.current_state

    @property
    def attacker_state(self):
        return self._attacker_state

    @attacker_state.setter
    def attacker_state(self, new_state):
        assert new_state in ['defence', 'attack']
        self._attacker_state = new_state

    @property
    def defender_state(self):
        return self._defender_state

    @defender_state.setter
    def defender_state(self, new_state):
        assert new_state in ['defence', 'attack']
        self._defender_state = new_state

    def update_world(self, position_dictionary):
        self._world.update_positions(position_dictionary)

    def plan(self, robot='attacker'):
        assert robot in ['attacker', 'defender']
        our_defender = self._world.our_defender
        our_attacker = self._world.our_attacker
        their_defender = self._world.their_defender
        their_attacker = self._world.their_attacker
        ball = self._world.ball
        if robot=='attacker':
            print "planner starts. Initial attacker strategy: ", self._attacker_state
        #print our_attacker.catcher
        #print ball.x
        #print ball.y
        #print '-------------------------------------------------------'

        if robot == 'defender':
            # We have the ball in our zone, so we grab and pass:
	    if our_defender.catcher=='closed' and self._defender_state == 'pass':
	      # Assumed we catched successfully
	      print 'Finish the pass, no matter what'
	      return self._defender_current_strategy.generate()

	    if self._defender_current_strategy.current_state == 'GRABBED':
	      print 'Go to pass, no matter what is going on'
	      self._defender_state = 'pass'
	      self._defender_current_strategy = self.choose_defender_strategy(self._world)
              return self._defender_current_strategy.generate()

            if self._world.pitch.zones[our_defender.zone].isInside(ball.x, ball.y) and ball.velocity < BALL_VELOCITY:
		#print 'Ball in our defending zone!'
                # Check if we should switch from a grabbing to a scoring strategy.
                if  self._defender_state == 'grab' and self._defender_current_strategy.current_state == 'GRABBED':
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
		#print 'Ball not in our defending zone, DEFENDING!'
                # If the bal is not in the defender's zone, the state should always be 'defend'.
                if not self._defender_state == 'defence':
                    self._defender_state = 'defence'
                    self._defender_current_strategy = self.choose_defender_strategy(self._world)

                return self._defender_current_strategy.generate()

    #if robot attacker
        else:
            # If the ball is in their defender zone we defend:
            if self._world.pitch.zones[their_defender.zone].isInside(ball.x, ball.y):
                if not self._attacker_state == 'defence':
                    self._attacker_state = 'defence'
                    self._attacker_current_strategy = self.choose_attacker_strategy(self._world)
                return self._attacker_current_strategy.generate()
#milestone 2
            # If ball is in our attacker zone, then grab the ball and score:
            elif self._world.pitch.zones[our_attacker.zone].isInside(ball.x, ball.y):
                # Check if we should switch from a grabbing to a scoring strategy.
                if self._attacker_state == 'grab' and self._attacker_current_strategy.current_state == 'GRABBED':
                    if our_attacker.has_ball(ball):
                        self._attacker_state = 'score'
                    else:
                        self._attacker_state = 'grab'
                    self._attacker_current_strategy = self.choose_attacker_strategy(self._world)

                # Check if we should switch from a defence to a grabbing strategy.
                elif self._attacker_state in ['defence', 'catch'] :
                    self._attacker_state = 'grab'
                    self._attacker_current_strategy = self.choose_attacker_strategy(self._world)

#milestone 2 scoring
                elif self._attacker_state == 'score' and self._attacker_current_strategy.current_state == 'FINISHED':
                    self._attacker_state = 'grab'
                    self._attacker_current_strategy = self.choose_attacker_strategy(self._world)

                elif self._attacker_state == 'score':
                    if our_attacker.catcher=='open':
                        import ipdb
                        ipdb.set_trace()
                        self._attacker_state = 'grab'
                        self._attacker_current_strategy = self.choose_attacker_strategy(self._world)
		print 'GENERATING ATTACKER STRATEGY. strat:'
                print  self._attacker_state 

		return self._attacker_current_strategy.generate()
            elif self._attacker_current_strategy.current_state == 'GRABBED':
                 print 'returning a pre-nothing-matched-thing'
                 return self._attacker_current_strategy.generate()
            else:
		print 'Nothing matched, calling 0 0 0'
                return calculate_motor_speed(0, 0)
