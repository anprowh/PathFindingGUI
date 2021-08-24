""" Simple test PF algorithm """

from Algorithms.BasePF import BasePF
from SearchEnvironment import SearchEnvironment


class TwoSidesPF(BasePF):
    """
    checked = {}
    done = False
    path = []
    environment = None
    """

    def __init__(self, environment: SearchEnvironment):
        super(TwoSidesPF, self).__init__(environment)
        self.paths_s = {self.start: [self.start]}  # paths to all processed points
        self.paths_e = {self.end: [self.end]}  # paths to all processed points
        self.weights_s = {self.start: 0}  # weights of paths to all processed points from start
        self.weights_e = {self.end: 0}  # weights of paths to all processed points from end

        self.checking_now_s = [self.start]  # points that are about to be processed on the next step
        self.checking_now_e = [self.end]  # points that are about to be processed on the next step

        self.current_weight = 0  # used for sequential work of algorithm. For GUI to display step by step

    def reset(self):
        super(TwoSidesPF, self).reset()
        self.start = self.environment.get_start()
        self.end = self.environment.get_end()
        self.paths_s = {self.start: [self.start]}  # paths to all processed points
        self.paths_e = {self.end: [self.end]}  # paths to all processed points
        self.weights_s = {self.start: 0}  # weights of paths to all processed points from start
        self.weights_e = {self.end: 0}  # weights of paths to all processed points from end

        self.checking_now_s = [self.start]  # points that are about to be processed on the next step
        self.checking_now_e = [self.end]  # points that are about to be processed on the next step

    def next_step(self):
        # Algorithm's steps are based on weight of path to points that are being processed
        min_weight = 10 ** 9
        for el in self.checking_now_s:
            min_weight = min(self.weights_s[el] - self.current_weight, min_weight)
        for el in self.checking_now_e:
            min_weight = min(self.weights_e[el] - self.current_weight, min_weight)
        self.current_weight += min_weight
        # points with too big weight won't be processed on the current step, so they are kept
        new_checking_s = {x for x in self.checking_now_s if self.weights_s[x] > self.current_weight}
        new_checking_e = {x for x in self.checking_now_e if self.weights_e[x] > self.current_weight}
        for point in self.checking_now_s:
            if self.weights_s[point] <= self.current_weight:
                # getting points that we are going to update info about
                new_points = self.environment.get_neighbour_graph_element(*point)
                # processed points aren't needed. No duplicates also
                new_checking_s |= {x for x in new_points.keys() if x not in self.checking_now_s and not self.checked[x]}

                self.update_paths_for_point_s(new_points, point)

                self.checked[point] = True

        intersection = set.intersection(new_checking_s, set(self.checking_now_e))
        intersection = {x for x in intersection if self.weights_s[x] <= self.current_weight + 1 and
                        self.weights_e[x] <= self.current_weight}
        if len(intersection) != 0:
            min_weight = 10 ** 9
            min_path = []
            for point in intersection:
                if self.weights_s[point] + self.weights_e[point] < min_weight:
                    min_weight = self.weights_s[point] + self.weights_e[point]
                    min_path = self.paths_s[point] + self.paths_e[point][::-1]
            self.done = True
            self.path = min_path
            self.current_weight = min_weight
            self.to_display = list(new_checking_s) + self.checking_now_e
            return

        self.checking_now_s = list(new_checking_s)

        for point in self.checking_now_e:
            if self.weights_e[point] <= self.current_weight:
                # getting points that we are going to update info about
                new_points = self.environment.get_neighbour_graph_element(*point)
                # processed points aren't needed. No duplicates also
                new_checking_e |= {x for x in new_points.keys() if x not in self.checking_now_e and not self.checked[x]}

                self.update_paths_for_point_e(new_points, point)

                self.checked[point] = True

        intersection = set.intersection(new_checking_e, set(self.checking_now_s))
        intersection = {x for x in intersection if self.weights_s[x] <= self.current_weight + 1 and
                        self.weights_e[x] <= self.current_weight+1}
        if len(intersection) != 0:
            min_weight = 10 ** 9
            min_path = []
            for point in intersection:
                if self.weights_s[point] + self.weights_e[point] < min_weight:
                    min_weight = self.weights_s[point] + self.weights_e[point]
                    min_path = self.paths_s[point] + self.paths_e[point][::-1]
            self.done = True
            self.path = min_path
            self.current_weight = min_weight
            self.to_display = self.checking_now_s + list(new_checking_e)
            return

        self.checking_now_e = list(new_checking_e)
        self.to_display = list(new_checking_s | new_checking_e)

    def update_paths_for_point_s(self, new_points, point):
        # updating info
        for next_point, next_weight in new_points.items():
            self.weights_s.setdefault(next_point, 10 ** 9)
            self.n_checks += 1
            if self.weights_s[next_point] > self.weights_s[point] + next_weight:
                self.weights_s[next_point] = self.weights_s[point] + next_weight
                self.paths_s[next_point] = self.paths_s[point] + [next_point]

    def update_paths_for_point_e(self, new_points, point):
        # updating info
        for next_point, next_weight in new_points.items():
            self.weights_e.setdefault(next_point, 10 ** 9)
            self.n_checks += 1
            if self.weights_e[next_point] > self.weights_e[point] + next_weight:
                self.weights_e[next_point] = self.weights_e[point] + next_weight
                self.paths_e[next_point] = self.paths_e[point] + [next_point]
