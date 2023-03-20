from asyncore import loop
from hashlib import new
from itertools import count
from os import cpu_count
from pickle import FALSE, TRUE
from constants import *
from environment import *
from state import State
"""
solution.py

This file is a template you should use to implement your solution.

You should implement each section below which contains a TODO comment.

COMP3702 2022 Assignment 2 Support Code

Last updated by njc 08/09/22
"""


class Solver:

    def __init__(self, environment: Environment):
        self.environment = environment
        #
        # TODO: Define any class instance variables you require (e.g. dictionary mapping state to VI value) here.
        #
        self.values = dict()
        self.policy = dict()
        self.initalised_states = []
        self.action_values = dict()
        self.state_best_action = dict()        
        self.converged = FALSE
        self.gamma = self.environment.gamma
        self.epsilon = self.environment.epsilon
        self.differences = [self.epsilon]
        self.total_reward = 0
        self.exit_state = 0
    # === Value Iteration ==============================================================================================

    def vi_initialise(self):
        """
        Initialise any variables required before the start of Value Iteration.
        """
        #
        # TODO: Implement any initialisation for Value Iteration (e.g. building a list of states) here. You should not
        #  perform value iteration in this method.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        self.initalised_states = [self.environment.get_init_state()]
        frontier = [self.environment.get_init_state()]

        while len(frontier) > 0:
            current = frontier.pop(0)
            if not self.environment.is_solved(current):
                for x in ROBOT_ACTIONS:
                    valid, cost, next_state = self.environment.get_iterations(current, x)
                    if valid:
                        if next_state not in self.initalised_states:
                            frontier.append(next_state)
                            self.initalised_states.append(next_state)
        
        for state in self.initalised_states:
            if self.environment.is_solved(state):
                self.values[state] = 0.0
                self.exit_state = state
                   
            else:
                self.values[state] = 0
        print(len(self.initalised_states))
        #print(self.values.values())
        # self.values = {state: 0 for state in self.initalised_states}

        
    def vi_is_converged(self):
        """
        Check if Value Iteration has reached convergence.
        :return: True if converged, False otherwise
        """
        #
        # TODO: Implement code to check if Value Iteration has reached convergence here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        max_diff = max(self.differences)
        
        if max_diff < self.epsilon:
            return TRUE
        return self.converged

    def vi_iteration(self):
        """
        Perform a single iteration of Value Iteration (i.e. loop over the state space once).
        """
        #
        # TODO: Implement code to perform a single iteration of Value Iteration here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        print(1)
        new_values = dict()
        new_policy = dict()
        for state in self.initalised_states:
            action_values = dict()
            for x in ROBOT_ACTIONS:
                        
                total = 0
                if self.environment.is_solved(state):
                        print("victory state at: ", total, " ", x)
                
                for stoch_action, p in self.environment.stoch_action(x).items():
                    vi = 0
                    #print(x, stoch_action, p)
                    reward, next_state = self.environment.perform_action(state, stoch_action)
                    for y in p:
                        cost, next_s = self.environment.apply_dynamics(state, stoch_action)
                        v = y * (cost + reward + (self.gamma * self.values[next_state]))
                        vi += v
                    #    print(reward, v)
                    #print(vi)
                    total += vi
            action_values[x] = total
            self.state_best_action[state] = max(action_values, key=action_values.get())
            new_values[state] = max(action_values.values())

        self.values = new_values
        #     if s == self.exit_state1:
        #         new_values[s] = 10000.0
        #         continue
            
        #     x = self.vi_select_action(s)
        #     total = 0
        #     for stoch_action, p in self.environment.stoch_action(x).items():
        #         vi = 0
        #         reward, next_state = self.environment.perform_action(s, stoch_action)
        #         for y in p:
        #             v = y * (reward + (self.gamma * self.vi_get_state_value(next_state)))
        #             vi += v
             
        #         total += vi

        #     new_values[s] = total 
        
        
        
        
            
            
    def vi_plan_offline(self):
        """
        Plan using Value Iteration.
        """
        # !!! In order to ensure compatibility with tester, you should not modify this method !!!
        self.vi_initialise()
        while not self.vi_is_converged():
            self.vi_iteration()

    def vi_get_state_value(self, state: State):
        """
        Retrieve V(s) for the given state.
        :param state: the current state
        :return: V(s)
        """
        #
        # TODO: Implement code to return the value V(s) for the given state (based on your stored VI values) here. If a
        #  value for V(s) has not yet been computed, this function should return 0.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        return self.values.get(state, 0)

    def vi_select_action(self, state: State):
        """
        Retrieve the optimal action for the given state (based on values computed by Value Iteration).
        :param state: the current state
        :return: optimal action for the given state (element of ROBOT_ACTIONS)
        """
        #``
        # TODO: Implement code to return the optimal action for the given state (based on your stored VI values) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        best_action = self.state_best_action[state]
        while not self.converged:
            if state == self.exit_state:
                self.vi_iteration()
                best_action = self.state_best_action[state]
        return best_action
        

        # action_values = dict()
        # for x in ROBOT_ACTIONS:
            
            
        #     total = 0
        #     if self.environment.is_solved(state):
        #             print("victory state at: ", total, " ", x)
            
        #     for stoch_action, p in self.environment.stoch_action(x).items():
        #         vi = 0
        #         #print(x, stoch_action, p)
        #         reward, next_state = self.environment.perform_action(state, stoch_action)
        #         for y in p:
        #             cost, next_s = self.environment.apply_dynamics(state, stoch_action)
        #             v = y * (cost + reward + (self.gamma * self.values[next_state]))
        #             vi += v
        #         #    print(reward, v)
        #         #print(vi)
        #         total += vi
            
        #     action_values[x] = total
        #     self.values[state] = max(action_values.values())
        #     print(max(action_values, key=action_values.get)) 
        # #(self.values.values())
        # return max(action_values, key=action_values.get)
        # # old_values = self.values.get(state)
        # # action_values = dict()

        # for x in ROBOT_ACTIONS:
        #     total = 0
        #     action_p = self.environment.stoch_action(x)
        #     action_list = self.environment.stoch_action_list(x)
            
        #     for y in action_p:
        #         vi = 0
                
        #         for z in action_list[y]:
                    
        #             reward_p, next_state_p = self.environment.perform_action(state, z)
        #             reward_p += self.get_reward(state)
        #             vi += action_p[y] * (reward_p + (self.gamma * self.values[next_state_p]))
        #         total += vi
        #     # print(self.values[state], total)
        #     action_values[x] = total
        #     # print(action_values[x], x)
        #     # reward, next_state = self.environment.perform_action(state, x)
        #     # total += (1-self.environment.drift_cw_probs[x]-self.environment.drift_ccw_probs[x]) * (reward + (self.gamma * self.values[next_state]))
            
        #     # for action, p in self.environment.stoch_action(state, x).items():
        #     #     reward_p, next_state_p = self.environment.perform_action(state, action)
        #     #     vi = p * (reward_p + (self.gamma * self.values[next_state_p]))
        #     #     total += vi
                
        # self.values[state] = max(action_values.values())
        # #print(max(action_values.values()), max(action_values, key=action_values.get))
        
        # differences = abs(self.values[state] - old_values)
        # self.differences.append(differences)
        
        # # max_diff = max(self.differences)
        
        # # if max_diff < self.epsilon:
        # #     self.converged = TRUE

        # return max(action_values, key=action_values.get) 

    # === Policy Iteration =============================================================================================

    def pi_initialise(self):
        """
        Initialise any variables required before the start of Policy Iteration.
        """
        #
        # TODO: Implement any initialisation for Policy Iteration (e.g. building a list of states) here. You should not
        #  perform policy iteration in this method. You should assume an initial policy of always move FORWARDS.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        self.initalised_states = [self.environment.get_init_state()]
        frontier = [self.environment.get_init_state()]

        while len(frontier) > 0:
            current = frontier.pop(0)
            if not self.environment.is_solved(current):
                for x in ROBOT_ACTIONS:
                    valid, cost, next_state = self.environment.get_iterations(current, x)
                    if valid:
                        if next_state not in self.initalised_states:
                            frontier.append(next_state)
                            self.initalised_states.append(next_state)
        
        self.policy = {state: FORWARD for state in self.initalised_states}
        print(len(self.initalised_states))
        # self.values = {state: 0 for state in self.initalised_states}

    def pi_is_converged(self):
        """
        Check if Policy Iteration has reached convergence.
        :return: True if converged, False otherwise
        """
        #
        # TODO: Implement code to check if Policy Iteration has reached convergence here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    def pi_iteration(self):
        """
        Perform a single iteration of Policy Iteration (i.e. perform one step of policy evaluation and one step of
        policy improvement).
        """
        #
        # TODO: Implement code to perform a single iteration of Policy Iteration (evaluation + improvement) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    def pi_plan_offline(self):
        """
        Plan using Policy Iteration.
        """
        # !!! In order to ensure compatibility with tester, you should not modify this method !!!
        self.pi_initialise()
        while not self.pi_is_converged():
            self.pi_iteration()

    def pi_select_action(self, state: State):
        """
        Retrieve the optimal action for the given state (based on values computed by Value Iteration).
        :param state: the current state
        :return: optimal action for the given state (element of ROBOT_ACTIONS)
        """
        #
        # TODO: Implement code to return the optimal action for the given state (based on your stored PI policy) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        old_policy = self.policy.get(state)
        action_values = dict()

        for x in ROBOT_ACTIONS:
            total = 0
            action_p = self.environment.stoch_action(x)
            action_list = self.environment.stoch_action_list(x)
            
            for y in action_p:
                for z in action_list[y]:
                    reward_p, next_state_p = self.environment.perform_action(state, z)

                vi = action_p[y] * (reward_p + (self.gamma * self.values[next_state_p]))
                total += vi
            # print(self.values[state], total)
            action_values[x] = total
            print(action_values[x], x)
            # reward, next_state = self.environment.perform_action(state, x)
            # total += (1-self.environment.drift_cw_probs[x]-self.environment.drift_ccw_probs[x]) * (reward + (self.gamma * self.values[next_state]))
            
            # for action, p in self.environment.stoch_action(state, x).items():
            #     reward_p, next_state_p = self.environment.perform_action(state, action)
            #     vi = p * (reward_p + (self.gamma * self.values[next_state_p]))
            #     total += vi
                

        self.values[state] = max(action_values.values())
        print(max(action_values.values()))
        pass
            # === Helper Methods ===============================================================================================
    #
    #
    # TODO: Add any additional methods here
    #
    #
    def get_reward(self, state: State):
        if self.environment.is_solved(state):
            return 10000.0
        else:
            return self.values[state]
