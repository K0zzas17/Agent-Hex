from collections import deque
from constants import *
from environment import *
from state import State
import numpy as np
"""
solution.py

This file is a template you should use to implement your solution.

You should implement each section below which contains a TODO comment.

"""


class Solver:

    def __init__(self, environment: Environment):
        self.environment = environment
        #
        # TODO: Define any class instance variables you require (e.g. dictionary mapping state to VI value) here.
        #
        self.values = dict()
        self.policy_VI = dict()
        self.initalised_states = []
        self.action_values = dict()
        self.state_best_action = dict()        
        self.converged = False
        self.gamma = self.environment.gamma
        self.epsilon = self.environment.epsilon
        self.differences = [self.epsilon]
        self.total_reward = 0
        self.exit_state = []

        #PI variables
        self.pi_states = []
        self.state_values = dict()
        self.policy_pi = dict()
        self.r_model = []
        self.pi_converged = False
        self.exit_state_pi = []
        self.LIN_ALG = False
        self.t_model = 0
        self.policy_before_last = dict()

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
        frontier = deque()
        frontier.append(self.environment.get_init_state())
        
        while len(frontier) > 0:
            current = frontier.popleft()
            if self.environment.is_solved(current):
                self.exit_state.append(current)
            for x in ROBOT_ACTIONS:
                movements = self.environment.apply_action_noise(x)
                
                for m in movements:
                    cost, nxt_state = self.environment.apply_dynamics(current, m)
                    if (cost < ACTION_BASE_COST[m] + ACTION_PUSH_COST[m]):
                        valid, cost, next_state = self.environment.get_iterations(current, m)
                        if valid:
                            if next_state not in self.initalised_states and nxt_state == next_state:
                                    frontier.append(next_state)
                                    self.initalised_states.append(next_state)
                            
               
        self.values = {state: 0 for state in self.initalised_states}
        self.policy_VI = {state: FORWARD for state in self.initalised_states}
        # print(len(self.initalised_states))
        # print(len(self.exit_state))

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
        new_values = dict()
        new_policies = dict()
        count = 0
        for s in self.initalised_states:
            count += 1
            #print(count)
            if self.environment.is_solved(s):
                new_values[s] = 0.0
                continue

            action_values = dict()
            for x in ROBOT_ACTIONS:
                total = 0
                vi = 0.0
                possible_movements = self.environment.stoch_action2(x)
                
                for stoch_action, p in possible_movements:
                    total_reward = []
                    for movement in stoch_action:
                    # movements = self.environment.apply_action_noise(stoch_action)
                    
                        reward, next_state = self.environment.apply_dynamics(s, movement)   
                        
                        total_reward.append(reward)
                                            
                    v = p * (min(total_reward) + (self.gamma * self.values[next_state]))
                    # print(v, min(total_reward))
                    vi = vi + v
                    total += vi  

                action_values[x] = total
                    
            new_values[s] = max(action_values.values())
            new_policies[s] = self.dict_argmax(action_values)

        differences = [abs(self.values[s] - new_values[s]) for s in self.initalised_states] 
        # print(differences)       
        max_diff = max(differences)
        self.differences.append(max_diff)
        
        if max_diff < self.epsilon:
            self.converged = True

        self.values = new_values
        self.policy_VI = new_policies
        


        # print(max(self.values.values()))

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
        #
        # TODO: Implement code to return the optimal action for the given state (based on your stored VI values) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        action_values = dict()
        for x in ROBOT_ACTIONS:
            total = 0
            possible_movements = self.environment.stoch_action2(x)
            vi = 0.0
            for stoch_action, p in possible_movements:
                total_reward = []
                for movement in stoch_action:
                    reward, next_state = self.environment.apply_dynamics(state, movement)   
                    total_reward.append(reward)
                    
                v = p * (min(total_reward) + (self.gamma * self.values[next_state]))
                vi = vi + v
                total += v
            action_values[x] = total
                
        #Optimal action
        return max(action_values, key=action_values.get)
       
        #Compute Value Iteration
        # check if value goes to the best state. If not, keep doing actions until this works

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
        frontier = deque()
        frontier.append(self.environment.get_init_state())
        
        while len(frontier) > 0:
            current = frontier.popleft()
            if self.environment.is_solved(current):
                self.exit_state.append(current)
            for x in ROBOT_ACTIONS:
                movements = self.environment.apply_action_noise(x)
                
                for m in movements:
                    cost, nxt_state = self.environment.apply_dynamics(current, m)
                    if (cost < ACTION_BASE_COST[m] + ACTION_PUSH_COST[m]):
                        valid, cost, next_state = self.environment.get_iterations(current, m)
                        if valid:
                            if next_state not in self.initalised_states and nxt_state == next_state:
                                    frontier.append(next_state)
                                    self.initalised_states.append(next_state)
                            
               
        self.values = {state: 0 for state in self.initalised_states}
        self.policy_VI = {state: FORWARD for state in self.initalised_states}
        
        # Reward vector
    #     r_model = np.zeros([len(self.pi_states), len(ROBOT_ACTIONS)])
    #     #print(r_model)
    #     for j, a in enumerate(ROBOT_ACTIONS):
    #         for i, state in enumerate(self.pi_states):
    #             # total = 0
    #             # possible_movements = self.environment.stoch_action2(a)
    #             # vi = 0.0
    #             # for stoch_action, p in possible_movements:
    #             #     total_reward = []
    #             # for movement in stoch_action:
    #             #     reward, next_state = self.environment.apply_dynamics(state, movement)   
    #             #     total_reward.append(reward)
                    
    #             # v = p * (min(total_reward) + (self.gamma * self.state_values[next_state]))
    #             # vi = vi + v
    #             # total += v
    #             if self.environment.is_solved(state):
    #                 r_model[i][j] = 1.0
    #             else:
    #                 r_model[i][j] = self.get_reward(state)
    #     self.r_model = r_model
    #     #print(r_model)
    #     #Transition matrix
    #     t_model = np.zeros([len(self.pi_states), len(ROBOT_ACTIONS), len(self.pi_states)])
    #     for x, s in enumerate(self.pi_states):
    #         for y, a in enumerate(ROBOT_ACTIONS):
    #             if self.environment.is_solved(s):
    #                 self.r_model[x] = 0.0
    #                 z = self.pi_states.index(s)
    #                 t_model[x][y][z] = 0
    #             else:
    #                 #get Responsibilities
    #                 transition = self.transition_probabilities(s, a)
    #                 for next_state, p in transition.items():
    #                     z = self.pi_states.index(next_state)
                        
    #                     t_model[x][y][z] = p
                        
                
       
    #     self.t_model = t_model       
        
    #    # lin alg policy
    #     la_policy = np.zeros([len(self.pi_states)], dtype=np.int64)
    #     for i, s in enumerate(self.policy_pi):
    #         la_policy[i] = self.policy_pi[s] # FORWARD initial policy as defined above
    #     self.la_policy = la_policy

    #     state_numbers = np.array(range(len(self.pi_states)))  # indices of every state
    #     t_pi = self.t_model[state_numbers, self.la_policy]
    #     #print(self.r_model)
    #     #print(self.la_policy)
    #     #print(self.t_model)

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
        return self.pi_converged

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
        # self.vi_initialise()
        # while not self.converged:
        #     self.vi_iteration()
        
        new_values = dict()
        new_policies = dict()
        count = 0
        for s in self.initalised_states:
            count += 1
            #print(count)
            if self.environment.is_solved(s):
                new_values[s] = 0.0
                continue

            action_values = dict()
            for x in ROBOT_ACTIONS:
                total = 0
                vi = 0.0
                possible_movements = self.environment.stoch_action2(x)
                
                for stoch_action, p in possible_movements:
                    total_reward = []
                    for movement in stoch_action:
                    # movements = self.environment.apply_action_noise(stoch_action)
                    
                        reward, next_state = self.environment.apply_dynamics(s, movement)   
                        
                        total_reward.append(reward)
                                            
                    v = p * (min(total_reward) + (self.gamma * self.values[next_state]))
                    # print(v, min(total_reward))
                    vi = vi + v
                    total += vi  

                action_values[x] = total
                    
            new_values[s] = max(action_values.values())
            new_policies[s] = self.dict_argmax(action_values)

        differences = [abs(self.values[s] - new_values[s]) for s in self.initalised_states] 
        # print(differences)       
        max_diff = max(differences)
        self.differences.append(max_diff)
        
        if max_diff < self.epsilon:
            self.pi_converged = True

        self.values = new_values
        self.policy_VI = new_policies
        




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
        action_values = dict()
        for x in ROBOT_ACTIONS:
            total = 0
            for stoch_action, p in self.environment.stoch_action2(x):
                vi = 0.0
                total_reward = []
                for movement in stoch_action:
                    reward, next_state = self.environment.apply_dynamics(state, movement)   
                    total_reward.append(reward)
                    
                v = p * (self.get_reward(state) + (self.gamma * self.values[next_state]))
                vi = vi + v
                total += v
                action_values[x] = total
        return self.dict_argmax(action_values)
        

    # === Helper Methods ===============================================================================================
    #
    #
    # TODO: Add any additional methods here
    #
    #
    def dict_argmax(self, values):
        max_value = max(values.values())
        for k, v in values.items():
            if v == max_value:
                return k

    def transition_probabilities(self, s, a):
        """ Calculates the probability distribution over next states given
            action a is taken in state s.

        Parameters:
            s: The state the agent is in
            a: The action requested

        Returns:
            A map from the reachable next states to the probabilities of reaching
            those state; i.e. each item in the returned dictionary is of form
            s' : P(s'|s,a)
        """
        probabilities = {}
        possible_moves = self.environment.stoch_action2(a)
        for action, p in possible_moves:
            for movement in action:
                reward, next_state = self.environment.apply_dynamics(s, movement)
            # if probabilities.get(next_state, 0) == 0:
            #     probabilities[next_state] = p
            probabilities[next_state] = probabilities.get(s, 0) + p
        return probabilities           

    def get_reward(self, state, a=None):

        if a == None:
            action = self.policy_VI[state]
        else:
            action = a
        action_values = dict()
        total = 0
        possible_movements = self.environment.stoch_action2(action)
        vi = 0.0
        p_reward = []
        for stoch_action, p in possible_movements:
            total_reward = []
            for movement in stoch_action:
                reward, next_state = self.environment.apply_dynamics(state, movement)   
                total_reward.append(reward)
                
            p_reward.append(p * min(total_reward))

        
        total = sum(p_reward)
        #print(action, p_reward, total)
        
        #Make sure theres no solutions
        
        return total

    def policy_improvement(self):
        new_policy = dict()
        
        for s in self.pi_states:
            action_values = dict()
            for x in ROBOT_ACTIONS:
                total = 0
                for stoch_action, p in self.environment.stoch_action2(x):
                    vi = 0.0
                    total_reward = []
                    for movement in stoch_action:
                        reward, next_state = self.environment.apply_dynamics(s, movement)   
                        total_reward.append(reward)
                        
                    v = p * (min(total_reward) + (self.gamma * self.state_values[next_state]))
                    vi = vi + v
                    total += v
                action_values[x] = total
            new_policy[s] = self.dict_argmax(action_values)
        return new_policy

    def convergence_check(self, new_policy):
        # if len(self.policy_before_last) != 0:
        #     if self.policy_before_last == new_policy:
        #         self.pi_converged = True
        #     elif self.policy_before_last == self.policy_pi:
        #         self.pi_converged = True
        
        
        if new_policy == self.policy_pi:
            self.pi_converged = True
        
        count = 0
        #print(self.la_policy)
        for s in self.pi_states:
            if new_policy[s] != self.policy_pi[s]:
                count += 1

        for i, s in enumerate(self.pi_states):
                self.la_policy[i] = self.policy_pi[s]

        #print(count, "Are different")
        self.policy_pi = new_policy 
        