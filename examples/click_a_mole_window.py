import random

from examples.click_a_mole import ClickAMoleAgent, ClickAMoleTask
from think import Agent, Environment, Motor, Mouse, Task, Vision, World

if __name__ == '__main__':
    env = Environment(window=(500, 500))
    task = ClickAMoleTask(env)
    agent = ClickAMoleAgent(env)
    World(task, agent).run(20, real_time=True)
