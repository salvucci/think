import random

from examples.click_a_mole import ClickAMoleAgent, ClickAMoleTask
from think import Agent, Machine, Motor, Mouse, Task, Vision, World

if __name__ == '__main__':
    machine = Machine(window=(500, 500))
    task = ClickAMoleTask(machine)
    agent = ClickAMoleAgent(machine)
    World(task, agent).run(20, real_time=True)
