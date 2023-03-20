import sys
import time
import math
from constants import *
from environment import *
from state import State
import matplotlib.pyplot as plt
from solution import *

env = Environment("./testcases/ex3.txt")
env.alpha = 0.25
agent1 = RLAgent(env)
agent1.q_learn_train()

env.alpha = 0.5
agent2 = RLAgent(env)
agent2.q_learn_train()

env.alpha = 0.75
agent3 = RLAgent(env)
agent3.q_learn_train()


line1 = []
line2 = []
line3 = []
xAxis = []

x = 50
num_episodes = len(agent1.rewards)
while x < num_episodes:
    xAxis.append(x)
    line1.append(sum(agent1.rewards[x-50:x])/50)
    line2.append(sum(agent2.rewards[x-50:x])/50)
    line3.append(sum(agent3.rewards[x-50:x])/50)
    x += 1


plt.plot(xAxis, line1, '-r', label = "alpha = 0.25")
plt.plot(xAxis, line2, '-g', label = "alpha = 0.5")
plt.plot(xAxis, line3, '-b', label = "alpha = 0.75")
plt.title("Q-learn with different alphas", fontsize = 20)
plt.xlabel("Episode", fontsize = 20)
plt.ylabel("50-step reward average", fontsize = 20)
plt.legend(frameon=False, loc='lower center', prop = {'size' : 20})
plt.show()
