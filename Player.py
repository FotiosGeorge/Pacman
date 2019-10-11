import pygame


class Player(object):
    def __init__(self, board):
        self.board = board
        self.x = 607
        self.y = 420
        self.pos = [(self.x, self.y)]
        self.score = 0

    def movement(self, x, y):
        self.x += x
        self.y += y
        self.pos = [self.x, self.y]

    def draw(self):
        pygame.draw.circle(self.board.window, (255, 255, 0), (self.x, self.y), 8)

    def score_system(self):
        score_font = pygame.font.Font(None, 50)
        score_surf = score_font.render(str(self.score), 1, (255, 255, 255))
        score_pos = [3 * self.board.cell_width, 13 * self.board.cell_height]
        self.board.window.blit(score_surf, score_pos)
        pygame.display.update()

    def update(self):
        score_font = pygame.font.Font(None, 50)
        score_surf = score_font.render("Score", 1, (255, 255, 255))
        score_pos = [2 * self.board.cell_width, 11.5 * self.board.cell_height]
        self.board.window.blit(score_surf, score_pos)

        for tup2 in self.board.dots:
            if (tup2[0] == self.x) and (tup2[1] == self.y):
                self.board.dots.remove(tup2)
                self.score += 1
                self.score_system()
                break
        self.score_system()
        pygame.display.update()

