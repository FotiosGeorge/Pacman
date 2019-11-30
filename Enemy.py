import pygame


class Enemy:
    def __init__(self, board, colour, direction):
        self.board = board
        self.x = 607
        self.y = 276
        self.direction = direction
        self.colour = colour
        self.intersections = []
        self.matrix = []
        self.matrix_equivalent = {}

    def changeLocation(self, direction):
        self.direction = direction

    def moves(self):
        if self.direction == 'L':
            self.x -= self.board.cell_width
            pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)
        if self.direction == 'R':
            self.x += self.board.cell_width
            pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)
        if self.direction == 'U':
            self.y -= self.board.cell_height
            pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)
        if self.direction == 'D':
            self.y += self.board.cell_height
            pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)

    def update(self):
        pygame.draw.circle(self.board.window, (self.colour), (self.x, self.y), 8)
        pygame.display.update()

        "---------------------------------------------------------------------"

    def create_matrix(self):

        for value in self.board.free_pos:
            x1 = (value[0] + 1, value[1])
            x2 = (value[0] - 1, value[1])
            y1 = (value[0], value[1] + 1)
            y2 = (value[0], value[1] - 1)
            if x1 in self.board.free_pos or x2 in self.board.free_pos:
                if y1 in self.board.free_pos or y2 in self.board.free_pos:
                    if value not in self.intersections:
                        self.intersections.append((value[0], value[1]))

        index = 0
        for value in self.intersections:
            self.matrix_equivalent[value] = index
            index += 1
        for x in range(0, len(self.intersections)):
            self.matrix.append([])
            for y in range(0, len(self.intersections)):
                self.matrix[x].append(float("inf"))

        for index, value in enumerate(self.intersections):
            found = False
            for index2, value2 in enumerate(self.intersections):
                if value != value2 and found is False:
                    if value[0] == value2[0]:
                        found = True
                        weight = abs(value2[1] - value[1])
                        self.matrix[index][index2] = weight
                    if value[1] == value2[1]:
                        found = True
                        weight = abs(value2[0] - value[0])
                        self.matrix[index][index2] = weight
        print(self.matrix)
        print(self.matrix_equivalent)



    def neighbours_location(self):
        None

    def path_finding(self):
        None

    def matrix_values(self):
        None

    def board_location(self):
        None
