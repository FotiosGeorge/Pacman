import pygame
from Powerup import *


class Player(object):
    def __init__(self, board, name):
        self.board = board
        self.name = name
        self.power = "empty"
        self.immune = False
        self.immunity_count = 1
        self.x = 607
        self.y = 420
        self.pos = [(self.x, self.y)]
        self.music_count = 0
        self.score = 0
        self.player_lives = 3
        self.cost_speed = 2
        self.last_intersection = []
        self.cloak = False
        self.laser = False

    def movement(self, x, y):
        if self.pos in self.board.intersections:
            self.last_intersection.append(self.pos)
        self.x += x
        self.y += y
        self.pos = (self.x, self.y)

    def draw(self):
        if self.board.state == "Single":
            pygame.draw.circle(self.board.window, (255, 255, 0), (self.x, self.y), 8)
        if (self.board.state == "Multiplayer") and (self.name == "Player1"):
            pygame.draw.circle(self.board.window, (255, 0, 0), (self.x, self.y), 8)
        if (self.board.state == "Multiplayer") and (self.name == "Player2"):
            pygame.draw.circle(self.board.window, (0, 0, 255), (self.x, self.y), 8)
        for tup2 in self.board.dots:
            if (tup2[0] == self.x) and (tup2[1] == self.y):
                if self.music_count % 4 == 0:
                    self.board.music.eating_music()
                self.board.dots.remove(tup2)
                self.score += 1
                self.score_system()
                self.music_count += 1
                break
        self.score_system()

        for tup2 in self.board.enemy:
            if (tup2.x == self.x) and (tup2.y == self.y) and (self.immune is False):
                self.board.music.death_music()
                self.player_lives -= 1
                self.board.player.x = 607
                self.board.player.y = 420
                self.power = "empty"
                self.immune = True
                break
        self.lives_system()

        if self.score % 100 == 0:
            if self.cost_speed <= 30:
                self.cost_speed += 1

    def score_system(self):
        if self.name == "Player1":
            self.score_display(3)
        if self.name == "Player2":
            self.score_display(24)

    def score_display(self, value):
        score_font = pygame.font.Font(None, 50)
        score_surf = score_font.render(str(self.score), 1, (255, 255, 255))
        score_pos = [value * self.board.cell_width, 13 * self.board.cell_height]
        self.board.window.blit(score_surf, score_pos)

    def lives_system(self):
        if self.name == "Player1":
            self.lives_display(3)
        if self.name == "Player2":
            self.lives_display(24)

    def lives_display(self, value):
        lives_font = pygame.font.Font(None, 50)
        lives_surf = lives_font.render(str(self.player_lives), 1, (255, 255, 255))
        lives_pos = [value * self.board.cell_width, 17 * self.board.cell_height]
        self.board.window.blit(lives_surf, lives_pos)

    def update(self):
        if self.name == "Player1":
            self.update_display(2)
        if self.name == "Player2":
            self.update_display(24)

    def update_display(self, value):
        score_font = pygame.font.Font(None, 50)
        score_surf = score_font.render("Score", 1, (255, 255, 255))
        score_pos = [value * self.board.cell_width, 11.5 * self.board.cell_height]
        lives_font = pygame.font.Font(None, 50)
        lives_surf = lives_font.render("Lives", 1, (255, 255, 255))
        lives_pos = [value * self.board.cell_width, 15.5 * self.board.cell_height]
        self.board.window.blit(lives_surf, lives_pos)
        self.board.window.blit(score_surf, score_pos)

    def immunity(self):
        if self.immunity_count % 50 == 0:
            self.immune = False
        elif self.immune is True:
            self.immunity_count += 1
