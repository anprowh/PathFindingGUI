""" Simple test PF algorithm """

from Algorithms.BasePF import BasePF
from SearchEnvironment import SearchEnvironment
from numba import jit


class AStar(BasePF):
    """
    checked = {}
    done = False
    path = []
    environment = None
    """

    def __init__(self, environment: SearchEnvironment):
        super(AStar, self).__init__(environment)
        self.paths = {self.start: [self.start]}  # paths to all processed points
        self.weights = {self.start: 0}  # weights of paths to all processed points

        self.checking_now = [self.start]  # points that are about to be processed on the next step
        self.current_weight = 0  # used for sequential work of algorithm. For GUI to display step by step

        self.a_weights = self.a_star_weights()

    def reset(self):
        super(AStar, self).reset()
        start = self.environment.get_start()
        self.end = self.environment.get_end()
        self.paths = {start: [start]}  # paths to all processed points
        self.weights = {start: 0}  # weights of paths to all processed points
        self.checking_now = [start]  # points that are about to be processed on the next step
        self.a_weights = self.a_star_weights()

    def next_step(self):
        # Algorithm's steps are based on weight of path to points that are being processed
        min_weight = 10 ** 9
        for el in self.checking_now:
            min_weight = min(self.weights[el] - self.current_weight, min_weight)
        self.current_weight += min_weight
        # points with too big weight won't be processed on the current step, so they are kept
        new_checking = {x for x in self.checking_now if self.weights[x] > self.current_weight}
        for point in self.checking_now:
            if self.weights[point] <= self.current_weight:
                # getting points that we are going to update info about
                new_points = self.environment.get_neighbour_graph_element(*point)
                # adding a_star weights
                for new_point in new_points.keys():
                    new_points[new_point] += self.a_weights[new_point[0]][new_point[1]]
                # processed points aren't needed. No duplicates also
                new_checking |= {x for x in new_points.keys() if x not in self.checking_now and not self.checked[x]}

                self.update_paths_for_point(new_points, point)

                self.checked[point] = True

        self.checking_now = list(new_checking)
        self.to_display = self.checking_now

        if self.checked[self.end]:
            self.done = True
            self.path = self.paths[self.end]
            self.current_weight = self.weights[self.end]


    def update_paths_for_point(self, new_points, point):
        # updating info
        for next_point, next_weight in new_points.items():
            self.weights.setdefault(next_point, 10 ** 9)
            self.n_checks += 1
            if self.weights[next_point] > self.weights[point] + next_weight:
                self.weights[next_point] = self.weights[point] + next_weight - self.a_weights[point[0]][point[1]]
                self.paths[next_point] = self.paths[point] + [next_point]

    def a_star_weights(self):
        star_weights = [[0] * self.environment.shape[1] for i in range(self.environment.shape[0])]
        # finding first height plus width smallest weights to estimate minimal possible weight of path from this point
        first_h_plus_w_weights = []
        for el in self.environment.get_grid():
            first_h_plus_w_weights += el
        first_h_plus_w_weights = sorted(first_h_plus_w_weights)[:sum(self.environment.shape)]
        for i in range(self.environment.shape[0]):
            for j in range(self.environment.shape[1]):
                star_weights[i][j] = sum(first_h_plus_w_weights[:abs(self.end[0] - i) + abs(self.end[1] - j)])

        # is set to 0 because will be substracted on first steps of the algorithm
        star_weights[self.start[0]][self.start[1]] = 0

        return star_weights
