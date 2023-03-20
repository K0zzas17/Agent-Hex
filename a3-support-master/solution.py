
from re import T
from statistics import mean
import sys
import time
import numpy as np
import math
from constants import *
from environment import *
from state import State
"""
solution.py

This file is a template you should use to implement your solution.

You should implement code for each of the TODO sections below.

COMP3702 2022 Assignment 3 Support Code

Last updated by njc 12/10/22
"""


class RLAgent:

    #
    # TODO: (optional) Define any constants you require here.
    #

    def __init__(self, environment: Environment):
        self.environment = environment
        #
        # TODO: (optional) Define any class instance variables you require (e.g. Q-value tables) here.
        #
        self.alpha = self.environment.alpha
        self.gamma = self.environment.gamma
        self.q_table = dict()

        self.sarsa_epsilon = 0.1
         
        self.x_array_q = []
        self.y_array_q = []

        self.x_array_sarsa = []
        self.y_array_sarsa = []
        

    # === Q-learning ===================================================================================================

    def q_learn_train(self):
        """
        Train this RL agent via Q-Learning.
        """
        #
        # TODO: Implement your Q-learning training loop here.
        max_episodes = 4000
        max_steps = 95
        total_rewards = []
       
        epsilon = 0.75
        
        eps_iteration = 0
        current_rewards = []
        exit_counter = 0
        
        for episode in range(max_episodes):
            state = self.environment.get_init_state()
            
            episode_reward = 0
            solved = False
            episode_start = eps_iteration

            while not solved and (eps_iteration - episode_start < max_steps):
                #epsilon = epsilon_end + (epsilon_start - epsilon_end) * math.exp(-1.0 * eps_iteration / epsilon_decay)
                # epsilon = 0.5
                q_action_action = self.q_learn_select_action(state)
                if (q_action_action is None or random.random() < epsilon):
                    q_action_action = random.choice(ROBOT_ACTIONS)

                reward, next_state = self.environment.perform_action(state, q_action_action)

                if (self.environment.is_solved(next_state)):
                    solved = True

                episode_reward += reward
                eps_iteration += 1

                #update q values
                old_q_value = self.q_table.get((state, q_action_action), 0)


                q_next_state = 0
                if not solved:
                    q_next = float('-inf')
                    for action in ROBOT_ACTIONS:
                        q_value = self.q_table.get((next_state, action))
                        if q_value is not None and q_value > q_next:
                            q_next = q_value
                            q_next_state = q_value
                
                new_q_value = old_q_value + self.alpha * (reward + self.gamma * q_next_state - old_q_value)
                self.q_table[(state, q_action_action)] = new_q_value

                state = next_state

            total_rewards.append(episode_reward)
            #print(f"Episode {episode}, steps taken {eps_iteration - episode_start}, reward: {episode_reward}, R100: {np.mean(total_rewards[-100:])}, epsilon: {self.sarsa_epsilon}")
            self.x_array_q.append(episode)
            self.y_array_q.append(np.mean(total_rewards[-50:]))

         
    def q_learn_select_action(self, state: State):
        """
        Select an action to perform based on the values learned from training via Q-learning.
        :param state: the current state
        :return: approximately optimal action for the given state
        """
        #
        # TODO: Implement code to return an approximately optimal action for the given state (based on your learned
        #  Q-learning Q-values) here.
        #
        
        best_action = None
        best_q = float('-inf')

        for x in ROBOT_ACTIONS:
            
            # find best action from here
            this_q = self.q_table.get((state, x))
            if this_q is not None and this_q > best_q:
                best_q = this_q
                best_action = x
        #print(best_action)
        return best_action

    # === SARSA ========================================================================================================

    def sarsa_train(self):
        """
        Train this RL agent via SARSA.
        """
        #
        # TODO: Implement your SARSA training loop here.
        #
        max_episodes = 3000
        max_steps = 3500
        
        total_rewards = []
        
        epsilon_start = 0.5
        epsilon_end = 0.3
        epsilon_decay = 1000
        eps_iteration = 0

        for episode in range(max_episodes):
            state = self.environment.get_init_state()
            sarsa_action = self.sarsa_select_action(state)
            #print(sarsa_action)
            episode_reward = 0
            solved = False
            episode_start = eps_iteration

            while not solved and (eps_iteration - episode_start < max_steps):
                
                self.sarsa_epsilon = epsilon_end + (epsilon_start - epsilon_end) * math.exp(-1.0 * eps_iteration / epsilon_decay)

                reward, next_state = self.environment.perform_action(state, sarsa_action)

                if (self.environment.is_solved(next_state)):
                    solved = True

                episode_reward += reward
                eps_iteration += 1

                old_sarsa_value = self.q_table.get((state, sarsa_action), 0)

                #Next action found by following policy
                next_action = self.sarsa_select_action(next_state)

                next_sarsa_value = self.q_table.get((next_state, next_action), 0)                
                
                new_q_value = old_sarsa_value + self.alpha * (reward + self.gamma * next_sarsa_value - old_sarsa_value)
                self.q_table[(state, sarsa_action)] = new_q_value

                state = next_state
                sarsa_action = next_action
               
            total_rewards.append(episode_reward)
            #print(f"Episode {episode}, steps taken {eps_iteration - episode_start}, reward: {episode_reward}, R50: {np.mean(total_rewards[-50:])}, epsilon: {self.sarsa_epsilon}")
            self.x_array_sarsa.append(episode)
            self.y_array_sarsa.append(np.mean(total_rewards[-50:]))

               

    def sarsa_select_action(self, state: State):
        """
        Select an action to perform based on the values learned from training via SARSA.
        :param state: the current state
        :return: approximately optimal action for the given state
        """
        #
        # TODO: Implement code to return an approximately optimal action for the given state (based on your learned
        #  SARSA Q-values) here.
        #
        sarsa_action = self.q_learn_select_action(state)
        #print(sarsa_action)
        #print(f"{random.choice(ROBOT_ACTIONS) if (sarsa_action is None) or (random.random() < self.sarsa_epsilon) else sarsa_action }")
        return random.choice(ROBOT_ACTIONS) if (sarsa_action is None) or (random.random() < self.sarsa_epsilon) else sarsa_action
        

    # === Helper Methods ===============================================================================================
    #
    #
    # TODO: (optional) Add any additional methods here.
    #
    #

