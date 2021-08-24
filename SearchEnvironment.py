from os.path import exists
"""
Environment where PF algorithm does its job.
2D table of weights (difficulty) for cell entrance for agent
"""


class SearchEnvironment:
    grid = [[]]
    shape = (0, 0)
    start = (0, 0)
    end = (0, 0)

    def __init__(self, height, width, start_x, start_y, end_x, end_y):
        self.shape = (height, width)
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)
        self.grid = [[1] * self.shape[1] for i in range(self.shape[0])]

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def set_weight(self, x, y, w):
        self.grid[x][y] = w

    def get_grid(self):
        return [self.grid[i].copy() for i in range(self.shape[0])]

    def get_weight(self, x, y) -> int:
        return self.grid[x][y]

    def get_coordinate_list(self):
        all_coordinates = []
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                all_coordinates.append((i,j))
        return all_coordinates

    # function used to create edges of graph on which pathfinding algorithm will be applied
    def get_neighbour_graph_element(self, x, y, with_corners=False):
        resulting_connections = {}

        side_connections = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        if with_corners:
            corners = [(x - 1, y - 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1)]
            side_connections += corners
        for x_i, y_i in side_connections:
            if 0 <= x_i < self.shape[0] and 0 <= y_i < self.shape[1]:
                resulting_connections[(x_i, y_i)] = self.get_weight(x_i, y_i)

        return resulting_connections

    # connections graph for selected coordinates
    def get_part_graph(self, coordinates, with_corners=False):
        resulting_graph = {}

        for i, j in coordinates:
            resulting_graph[(i, j)] = self.get_neighbour_graph_element(i, j, with_corners)

        return resulting_graph

    # connections graph for all coordinates
    def get_full_graph(self, with_corners=False):
        return self.get_part_graph(self.get_coordinate_list(), with_corners)

    @staticmethod
    def load(env_id):
        if not exists(f'saved_envs/{env_id}.txt'):
            return self
        file = open(f'saved_envs/{env_id}.txt', 'r')
        data = file.read().split('\n')
        grid_data = [[int(x) for x in ar.split()] for ar in data[:-1]]
        shape0, shape1, startx, starty, endx, endy = [int(x) for x in data[-1].split()]
        new_environment = SearchEnvironment(shape0, shape1, startx, starty, endx, endy)
        for i in range(shape0):
            for j in range(shape1):
                new_environment.set_weight(i, j, grid_data[i][j])
        return new_environment

    def save(self, file_id):
        data = self.get_grid()
        file = open(f'saved_envs/{file_id}.txt', 'w')
        data = [' '.join([str(x) for x in ar]) for ar in data]  # all the
        data = '\n'.join(data)
        data += f'\n{self.shape[0]} {self.shape[1]} ' \
                f'{self.start[0]} {self.start[1]} ' \
                f'{self.end[0]} {self.end[1]}'
        file.write(data)

