""" Simple test PF algorithm """

from Algorithms.BasePF import BasePF
from SearchEnvironment import SearchEnvironment


class SimplePF(BasePF):
    """
    checked = {}
    done = False
    path = []
    environment = None
    """

    def __init__(self, environment: SearchEnvironment):
        super(SimplePF, self).__init__(environment)
        self.paths = {self.start: [self.start]}  # paths to all processed points
        self.weights = {self.start: 0}  # weights of paths to all processed points

        self.checking_now = [self.start]  # points that are about to be processed on the next step
        self.current_weight = 0  # used for sequential work of algorithm. For GUI to display step by step

    def reset(self):
        start = self.environment.get_start()
        self.end = self.environment.get_end()
        self.paths = {start: [start]}  # paths to all processed points
        self.weights = {start: 0}  # weights of paths to all processed points
        self.checking_now = [start]  # points that are about to be processed on the next step
        self.current_weight = 0  # used for sequential work of algorithm. For GUI to display step by step
        to_process = self.environment.get_coordinate_list()
        self.checked = {x: False for x in to_process}
        self.done = False
        self.path = []

    def next_step(self):
        # Algorithm's steps are based on weight of path to points that are being processed
        min_weight = 10 ** 12
        for el in self.checking_now:
            min_weight = min(self.weights[el]-self.current_weight,min_weight)
        self.current_weight += min_weight
        # points with too big weight won't be processed on the current step, so they are kept
        new_checking = {x for x in self.checking_now if self.weights[x] > self.current_weight}
        for point in self.checking_now:
            if self.weights[point] <= self.current_weight:
                # getting points that we are going to update info about
                new_points = self.environment.get_neighbour_graph_element(*point)
                # processed points aren't needed. No duplicates also
                new_checking |= {x for x in new_points.keys() if x not in self.checking_now and not self.checked[x]}

                self.update_paths_for_point(new_points, point)

                self.checked[point] = True

        self.checking_now = list(new_checking)

        if self.checked[self.end]:
            self.done = True
            self.path = self.paths[self.end]

    def update_paths_for_point(self, new_points, point):
        # updating info
        for next_point, next_weight in new_points.items():
            self.weights.setdefault(next_point, 10 ** 9)
            if self.weights[next_point] > self.weights[point] + next_weight:
                self.weights[next_point] = self.weights[point] + next_weight
                self.paths[next_point] = self.paths[point] + [next_point]
