from tasks.search import SearchAgent, SearchTask
from think import World

if __name__ == "__main__":
    agent = SearchAgent()
    task = SearchTask(agent)
    World(task, agent).run(30)
