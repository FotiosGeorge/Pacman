import pygame
from Powerup import *


class Player(object):
    def __init__(self, board):
        self.board = board
        self.power = "empty"
        self.x = 607
        self.y = 420
        self.pos = [(self.x, self.y)]
        self.music_count = 0
        self.score = 0
        self.player_lives = 3
        self.last_intersection = []

    def movement(self, x, y):
        if self.pos in self.board.intersections:
            self.last_intersection.append(self.pos)
        self.x += x
        self.y += y
        self.pos = (self.x, self.y)

    def draw(self):
        pygame.draw.circle(self.board.window, (255, 255, 0), (self.x, self.y), 8)

    def score_system(self):
        score_font = pygame.font.Font(None, 50)
        score_surf = score_font.render(str(self.score), 1, (255, 255, 255))
        score_pos = [3 * self.board.cell_width, 13 * self.board.cell_height]
        self.board.window.blit(score_surf, score_pos)

    def lives_system(self):
        lives_font = pygame.font.Font(None, 50)
        lives_surf = lives_font.render(str(self.player_lives), 1, (255, 255, 255))
        lives_pos = [3 * self.board.cell_width, 17 * self.board.cell_height]
        self.board.window.blit(lives_surf, lives_pos)

    def update(self):
        score_font = pygame.font.Font(None, 50)
        score_surf = score_font.render("Score", 1, (255, 255, 255))
        score_pos = [2 * self.board.cell_width, 11.5 * self.board.cell_height]
        lives_font = pygame.font.Font(None, 50)
        lives_surf = lives_font.render("Lives", 1, (255, 255, 255))
        lives_pos = [2 * self.board.cell_width, 15.5 * self.board.cell_height]
        self.board.window.blit(lives_surf, lives_pos)
        self.board.window.blit(score_surf, score_pos)

        for tup2 in self.board.dots:
            if (tup2[0] == self.x) and (tup2[1] == self.y):
                if self.music_count % 4 == 0:
                    pygame.mixer.music.load("pacman_chomp.wav")
                    pygame.mixer.music.set_volume(0.1)
                    pygame.mixer.music.play(1)
                self.board.dots.remove(tup2)
                self.score += 1
                self.score_system()
                self.music_count += 1
                break
        self.score_system()

        for tup2 in self.board.enemy:
            if (tup2.x == self.x) and (tup2.y == self.y):
                pygame.mixer.music.load("pacman_death.wav")
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(1)
                self.player_lives -= 1
                self.board.player.x = 607
                self.board.player.y = 420
                break
        self.lives_system()



