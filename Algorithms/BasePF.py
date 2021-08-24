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
        self.to_display = [environment.start]
        self.environment = environment
        self.start = environment.start
        self.end = environment.end
        self.path = []
        to_process = self.environment.get_coordinate_list()
        self.checked = {x: False for x in to_process}
        self.n_checks = 0
        self.current_weight = 0
        self.done = False

    def next_step(self):
        """ performs next step of graph processing to find the best path. Updates checked and done vars """

    def reset(self):
        self.to_display = [self.environment.start]
        to_process = self.environment.get_coordinate_list()
        self.checked = {x: False for x in to_process}
        self.path = [self.environment.start]
        self.done = False
        self.n_checks = 0
        self.current_weight = 0

    def get_checked(self):
        return self.checked.copy()

    def get_path(self):
        return self.path.copy()

    def get_types_grid(self):
        grid = [[' '] * self.environment.shape[1] for i in range(self.environment.shape[0])]
        for x, y in self.to_display:
            grid[x][y] = '*'
        for x, y in self.path:
            grid[x][y] = 'o'
        start = self.environment.start
        end = self.environment.end
        grid[start[0]][start[1]] = 'S'
        grid[end[0]][end[1]] = 'E'
        return grid

