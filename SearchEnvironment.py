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
