from tasks.pvt import PVTAgent, PVTTask
from think import World

if __name__ == "__main__":
    agent = PVTAgent()
    task = PVTTask(agent)
    World(task, agent).run(30)
