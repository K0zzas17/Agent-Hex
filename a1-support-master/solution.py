from calendar import c
from queue import PriorityQueue
from cmath import cos, cosh
import heapq
from multiprocessing import heap
from platform import node
import queue
from shutil import move
import sys
import time
from webbrowser import get
from constants import *
from environment import *
from state import State
"""
solution.py

This file is a template you should use to implement your solution.

You should implement 

COMP3702 2022 Assignment 1 Support Code

Last updated by njc 01/08/22
"""


class Solver:

    def __init__(self, environment, loop_counter):
        self.environment = environment
        self.loop_counter = loop_counter
        #
        # TODO: Define any class instance variables you require here.
        #

    def solve_ucs(self):
        """
        Find a path which solves the environment using Uniform Cost Search (UCS).
        :return: path (list of actions, where each action is an element of ROBOT_ACTIONS)
        """

        #
        #
        # TODO: Implement your UCS code here
        #
        # === Important ================================================================================================
        # To ensure your code works correctly with tester, you should include the following line of code in your main
        # search loop:
        #
        # self.loop_counter.inc()
        #
        # e.g.
        # while loop_condition():
        #   self.loop_counter.inc()
        #   ...
        #
        # ==============================================================================================================
        #
        #
        frontier = PriorityQueue()
        frontier.put(self.environment.get_init_state())
        visited_hex = {self.environment.get_init_state(): 0} # a dict of `vertex: cost_so_far`
        path = {self.environment.get_init_state(): []}
        path_list = []
        while not frontier.empty():
            self.loop_counter.inc()
            current = frontier.get()
            visited_hex[current] == current.priority
            if self.environment.is_solved(current):
                # print("visited states: ", len(visited_hex))
                # print("Frontier states: ", frontier.qsize())
                return current.action_from_parent#path.get(current)
            
            successor = current.get_successors()
            for next_state, cost, action in successor:
                current_total_cost = visited_hex.get(current) + cost
                if (next_state not in visited_hex) or (current_total_cost < visited_hex.get(next_state)): 
                    visited_hex.update({next_state: current_total_cost})
                    # This is the only way that works for some reason
                    #path[next_state] = path[current] + [action]
                    next_state.action = action
                    next_state.action_from_parent = current.action_from_parent + [action]

                    next_state.priority = current_total_cost
                    frontier.put(next_state)
        return
        
    def solve_a_star(self):
        """
        Find a path which solves the environment using A* search.
        :return: path (list of actions, where each action is an element of ROBOT_ACTIONS)
        """

        #
        #
        # TODO: Implement your A* search code here
        #
        # === Important ================================================================================================
        # To ensure your code works correctly with tester, you should include the following line of code in your main
        # search loop:
        #
        # self.loop_counter.inc()
        #
        # e.g.
        # while loop_condition():
        #   self.loop_counter.inc()
        #   ...
        #
        # ==============================================================================================================
        #
        #
        frontier = PriorityQueue()
        frontier.put(self.environment.get_init_state())
        visited_hex = {self.environment.get_init_state(): 0} # a dict of `vertex: cost_so_far`
        path = {self.environment.get_init_state(): []}

        while not frontier.empty():
            self.loop_counter.inc()
            current = frontier.get()
            visited_hex[current] == current.priority
            if self.environment.is_solved(current):
            #if self.environment.is_solved(self.environment.get_solved_state()):
                # print("visited states: ", len(visited_hex))
                # print("Frontier states: ", frontier.qsize())
                return current.action_from_parent
            
            successor = current.get_successors()
            for next_state, cost, action in successor:
                current_total_cost = visited_hex.get(current) + cost
                if (next_state not in visited_hex) or (current_total_cost < visited_hex.get(next_state)): 
                    visited_hex.update({next_state: current_total_cost})
                    # This is the only way that works for some reason
                    #path[next_state] = path[current] + [action]
                    
                    next_state.action_from_parent = current.action_from_parent + [action]
                    #next_state.action.update({current: action})

                    h = self.manhattan_distance_heurestic(self.environment, next_state)
                    
                    next_state.priority = current_total_cost + h
                    frontier.put(next_state)
        return

    #
    #
    # TODO: Add any additional methods here
    #
    #
    def manhattan_distance_heurestic(self, env: Environment, state: State):
        #x distance away from the tgt - x position of state
        #y distance away from the tgt - y position of state
        xtgt_distances = []
        ytgt_distances = []
        x_state_distance = []
        y_state_distance = []
        for t in env.target_list:
            xtgt_distances.append(t[0])
            ytgt_distances.append(t[1])

        for w in state.widget_centres:
            x_state_distance.append(w[0])
            y_state_distance.append(w[1])
        distance = abs(min(xtgt_distances) - min(x_state_distance)) + abs(min(ytgt_distances) - min(y_state_distance))

        return distance
