import pygame


class Enemy:
    def __init__(self, board, colour, direction):
        self.board = board
        self.x = 607
        self.y = 276
        self.direction = direction
        self.colour = colour
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
        index = 0
        for value in self.board.free_pos:
            self.matrix_equivalent[value] = index
            index += 1
        for x in range(0, len(self.board.free_pos)):
            self.matrix.append([])
            for y in range(0, len(self.board.free_pos)):
                self.matrix[x].append(float("inf"))
        for index, node in enumerate(self.board.free_pos):
            if ((node[0] + 1), (node[1])) in self.board.free_pos:
                index2 = self.board.free_pos.index(((node[0] + 1), (node[1])))
                self.matrix[index][index2] = 1
            if ((node[0] - 1), (node[1])) in self.board.free_pos:
                index2 = self.board.free_pos.index(((node[0] - 1), (node[1])))
                self.matrix[index][index2] = 1
            if ((node[0]), (node[1] + 1)) in self.board.free_pos:
                index2 = self.board.free_pos.index(((node[0]), (node[1] + 1)))
                self.matrix[index][index2] = 1
            if ((node[0]), (node[1] - 1)) in self.board.free_pos:
                index2 = self.board.free_pos.index(((node[0]), (node[1] - 1)))
                self.matrix[index][index2] = 1
        print(self.matrix)

    def neighbours_location(self):
        None

    def path_finding(self):
        None

    def matrix_values(self):
        None

    def board_location(self):
        None
