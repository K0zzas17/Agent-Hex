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

agent_sarsa = RLAgent(env_sarsa)
agent_q = RLAgent(env_q)

agent_q.q_learn_train()
agent_sarsa.sarsa_train()


plt.plot(agent_q.x_array_q, agent_q.y_array_q, color="r", label=f"Q_Learning quality")
plt.plot(agent_sarsa.x_array_sarsa, agent_sarsa.y_array_sarsa, color="b", label=f"SARSA Quality")


plt.title("50 Step Reward Moving Average")
plt.xlabel("Episode Number")
plt.ylabel("50-step Average Reward")

plt.legend()
plt.show()
