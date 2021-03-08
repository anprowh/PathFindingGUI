"""
Base pathfinding algorithm class, which processes data about it's environment
and step by step returns information about state of algorithm's processing
allowing to gui to visualise algorithm's work
"""

from SearchEnvironment import SearchEnvironment


class BasePF:
    checked = {}
    done = False
    path = []
    environment = None

    def __init__(self, environment: SearchEnvironment):
        self.checking_now = [environment.start]
        self.environment = environment
        self.start = environment.start
        self.end = environment.end
        to_process = self.environment.get_coordinate_list()
        self.checked = {x: False for x in to_process}

    def next_step(self):
        """ performs next step of graph processing to find the best path. Updates checked and done vars """

    def reset(self):
        self.checking_now = [self.environment.start]
        to_process = self.environment.get_coordinate_list()
        self.checked = {x: False for x in to_process}
        self.path = [self.environment.start]
        self.done = False

    def get_checked(self):
        return self.checked.copy()

    def get_path(self):
        return self.path.copy()


