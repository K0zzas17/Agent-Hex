from cProfile import label
from cgi import test
from collections import deque
from os import environ
from re import T
from statistics import mean
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import math

from constants import *
from environment import *
from state import State
from solution import RLAgent

env_q = Environment('testcases/ex3.txt')
env_sarsa = Environment('testcases/ex4.txt')

#agent_q = RLAgent(env_q)
agent_sarsa = RLAgent(env_sarsa)

env_q.alpha = 0.01
agent_1 = RLAgent(env_q)
agent_1.q_learn_train()

env_q.alpha = 0.5
agent_2 = RLAgent(env_q)
agent_2.q_learn_train()

env_q.alpha = 0.9
agent_3 = RLAgent(env_q)
agent_3.q_learn_train()

ALPHA = [0.01, 0.5, 0.9]
COLOR = ['r', 'b', 'g']
x_points_q = []
y_points_q = []
test_y = 0

plt.plot(agent_1.x_array_q, agent_1.y_array_q, color="r", label=f"Learning rate: {agent_1.alpha}")
plt.plot(agent_2.x_array_q, agent_2.y_array_q, color="b", label=f"Learning rate: {agent_2.alpha}")
plt.plot(agent_3.x_array_q, agent_3.y_array_q, color="g", label=f"Learning rate: {agent_3.alpha}")

plt.title("50 Step Reward Moving Average")
plt.xlabel("Episode Number")
plt.ylabel("50-step Average Reward")

plt.legend()
plt.show()
