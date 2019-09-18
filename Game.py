import pygame

pygame.init()
pygame.display.set_caption("Pacman")

screen_width = 1260
screen_height = 744


class Board(object):
    def __init__(self, grid):
        self.Maze = grid
        self.window = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.terminate = False
        self.keys = pygame.key.get_pressed()
        self.x_coord = 0
        self.y_coord = 0
        self.walls = []
        self.free_cells = []
        self.central_cells = []
        self.enemy_spawn = []
        self.cell_width = 45
        self.central_width = self.cell_width//2
        self.cell_height = 24
        self.central_height = self.cell_height//2
        self.user_events()

    def user_events(self):
        self.cells(self.Maze)
        while not self.terminate:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate = True
            self.load()
        self.clock.tick(60)
        pygame.quit()

    def draw_grid(self):
        for line in range(screen_width//45):
            pygame.draw.line(self.window, (107, 107, 107), (line*self.cell_width, 0), (line*self.cell_width, screen_height))
        for line in range(screen_height//24):
            pygame.draw.line(self.window, (107, 107, 107), (0, line*self.cell_height), (screen_width, line*self.cell_height))

    def cells(self, grid):
        for index1, row in enumerate(grid):
            for index2, cell in enumerate(row):
                if cell == 0:
                    self.free_cells.append((self.x_coord, self.y_coord))
                elif cell == 1:
                    self.walls.append((self.x_coord, self.y_coord))
                else:
                    self.enemy_spawn.append((self.x_coord, self.y_coord))
                self.x_coord += 45
                if self.x_coord == 1260:
                    self.x_coord = 0
            self.y_coord += 24

    def draw_pops(self):
        for value in self.free_cells:
            pygame.draw.circle(self.window, (255, 255, 0), (value[0] + self.central_width, value[1] + self.central_height), 5)
            x_value = value[0] + self.central_width
            y_value = value[1] + self.central_height
            self.central_cells.append((x_value, y_value))

    def load(self):
        self.background = pygame.image.load("Maze.png")
        self.background = pygame.transform.smoothscale(self.background, (screen_width, screen_height))
        self.window.blit(self.background, (0, 0))
        self.draw_grid()
        self.draw_pops()
        pygame.display.update()


