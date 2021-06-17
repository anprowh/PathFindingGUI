import pygame
from Algorithms.BasePF import BasePF
from SearchEnvironment import SearchEnvironment
from os.path import exists


class SimpleGUI:
    colors = {'S': (0, 255, 0),
              'E': (0, 0, 255),
              '*': (255, 0, 0),
              'o': (255, 0, 255)}

    def __init__(self, algorithm: BasePF, cell_size=32):
        self.algorithm = algorithm
        self.environment = algorithm.environment
        self.cell_size = cell_size
        self.height = self.environment.shape[1] * cell_size
        self.width = self.environment.shape[0] * cell_size

    def color(self, cell_type=' ', weight=1):
        if cell_type in self.colors.keys():
            return self.colors[cell_type]
        return (255 - int((-(1.1 ** (-(weight / 2))) + 1) * 255),) * 3

    def run(self):
        fill_value_surface, grid_surface, screen = self.initialize()

        def write(msg="1", size=self.cell_size, width_limit=self.cell_size, color=(0, 0, 0)):
            """
            Returns surface with text on it, sized to fit one cell
            :param msg:
            :param size:
            :param width_limit:
            :param color:
            :return:
            """
            font = pygame.font.SysFont("None", size)
            text = font.render(msg, True, color)
            text = text.convert_alpha()
            if text.get_rect().width > width_limit:
                font = pygame.font.SysFont("None", int(size * width_limit / text.get_rect().width))
                text = font.render(msg, True, color)
                text = text.convert_alpha()
            return text

        clock = pygame.time.Clock()
        working = False  # is algorithm processing data or user typing values
        drawing = False  # True if mouse button is pressed
        text_to_redraw = self.environment.get_coordinate_list()
        fill_value = 1  # value used to fill clicked cells with
        rect_array = []
        text_surfaces = [[None] * self.environment.shape[1] for _ in range(self.environment.shape[0])]
        fps_working_list = [2, 5, 10, 20, 30, 60, 120]
        fps_working_idx = 2  # FPS when algorithm is working (not user filling grid)
        fps_drawing = 60
        main_loop = True
        while main_loop:
            milliseconds = clock.tick(fps_working_list[fps_working_idx] if working else fps_drawing)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_loop = False  # pygame window closed by user
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    drawing = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    drawing = False
                if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN) and drawing:
                    for i, cells in enumerate(rect_array):
                        for j, cell in enumerate(cells):
                            if cell.collidepoint(event.pos):
                                self.environment.set_weight(i, j, fill_value)
                                self.algorithm.reset()
                                working = False
                                text_to_redraw.append((i, j))
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        main_loop = False  # user pressed ESC -> quit
                    elif event.key == pygame.K_RIGHT:
                        fps_working_idx = min(fps_working_idx + 1, len(fps_working_list)-1)
                    elif event.key == pygame.K_LEFT:
                        fps_working_idx = max(fps_working_idx - 1, 0)
                    elif event.key == pygame.K_m:
                        fps_working_idx = len(fps_working_list)-1
                    elif event.key == pygame.K_SPACE:
                        working = not working  # pausing and resuming
                    elif event.key == pygame.K_c:
                        fill_value = 0
                    elif event.key == pygame.K_r:
                        self.algorithm.reset()
                    elif event.key == pygame.K_s:  # saving current grid of weights to ./saved_envs/{fill_value}.txt
                        data = self.environment.get_grid()
                        file = open(f'saved_envs/{fill_value}.txt', 'w')
                        data = [' '.join([str(x) for x in ar]) for ar in data]  # all the
                        data = '\n'.join(data)
                        data += f'\n{self.environment.shape[0]} {self.environment.shape[1]} ' \
                                f'{self.environment.start[0]} {self.environment.start[1]} ' \
                                f'{self.environment.end[0]} {self.environment.end[1]}'
                        file.write(data)
                    # load environment from ./saved_envs/{fill_value}.txt
                    elif event.key == pygame.K_l and exists(f'saved_envs/{fill_value}.txt'):
                        file = open(f'saved_envs/{fill_value}.txt', 'r')
                        data = file.read().split('\n')
                        grid_data = [[int(x) for x in ar.split()] for ar in data[:-1]]
                        shape0, shape1, startx, starty, endx, endy = [int(x) for x in data[-1].split()]
                        new_environment = SearchEnvironment(shape0, shape1, startx, starty, endx, endy)
                        for i in range(shape0):
                            for j in range(shape1):
                                new_environment.set_weight(i, j, grid_data[i][j])
                        self.environment = new_environment
                        self.algorithm.environment = new_environment
                        self.algorithm.reset()
                        text_to_redraw = self.environment.get_coordinate_list()
                    elif event.unicode.isdigit():  # setting fill_value to fill grid with weights
                        fill_value *= 10
                        fill_value += int(event.unicode)
                    elif event.key == pygame.K_BACKSPACE:
                        fill_value //= 10

            if not self.algorithm.done and working:
                self.algorithm.next_step()

            if self.algorithm.done:
                working = False

            grid = [[' '] * self.environment.shape[1] for i in range(self.environment.shape[0])]
            for x, y in self.algorithm.to_display:
                grid[x][y] = '*'
            for x, y in self.algorithm.path:
                grid[x][y] = 'o'
            start = self.environment.start
            end = self.environment.end
            grid[start[0]][start[1]] = 'S'
            grid[end[0]][end[1]] = 'E'

            rect_array = [[] for _ in range(len(grid))]

            for i, ar in enumerate(grid):
                for j, cell_type in enumerate(ar):
                    # square with color depending on type of cell
                    rect_array[i].append(pygame.Rect(i * self.cell_size, j * self.cell_size,
                                                     self.cell_size, self.cell_size))
                    pygame.draw.rect(grid_surface, self.color(cell_type, self.environment.get_weight(i, j)),
                                     rect_array[i][-1])

                    # second element represents center of a text field
                    if (i, j) in text_to_redraw:
                        weight = self.environment.get_weight(i, j)
                        text_surface_and_pos = (write(str(weight), color=(0, 0, 0) if weight < 15 else (255, 255, 255)),
                                                (int((i + 0.5) * self.cell_size), int((j + 0.5) * self.cell_size)))
                        text_surfaces[i][j] = text_surface_and_pos

            text_to_redraw = []

            # drawing grid and text
            screen.blit(grid_surface, (0, 0))
            for i in range(len(text_surfaces)):
                for surface, position in text_surfaces[i]:
                    text_rect = surface.get_rect(center=position)
                    screen.blit(surface, text_rect)
            screen.blit(fill_value_surface, (0, self.height))
            screen.blit(write(str(fill_value), 40, self.width, False), (0, self.height + 5))
            pygame.display.set_caption(f"{type(self.algorithm).__name__} algorithm. {self.algorithm.n_checks} checks. "
                                       f"{self.algorithm.current_weight} weight. {int(clock.get_fps())} FPS")
            pygame.display.flip()

    def initialize(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height + 40), pygame.RESIZABLE)
        background = pygame.Surface(screen.get_size())
        # fill the background white (red,green,blue)
        background.fill((255, 255, 255))
        background = background.convert()  # faster blitting
        # create a new surface (black by default)
        grid_surface = pygame.Surface((self.width, self.height))
        fill_value_surface = pygame.Surface((self.width, 40))
        fill_value_surface.fill((200,) * 3)
        return fill_value_surface, grid_surface, screen
