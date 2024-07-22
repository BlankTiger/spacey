from __future__ import annotations

import random

import pygame

from spacey.enemies.fighter import EnemyFighter
from spacey.level import load_levels
from spacey.player import Player


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Spacey")
    clock = pygame.time.Clock()
    game = Game(screen, clock)
    game.game_loop()


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.dt = 0.0
        self.player = Player(self.screen)
        self.score = 0
        self.levels = load_levels(self.screen)
        self.curr_level = 0
        self.level = self.levels[self.curr_level]
        self.level.init()
        self.enemies: list[EnemyFighter] = self.level.enemies
        self.load_top_score()

    def next_level(self):
        self.curr_level += 1
        self.level = self.levels[self.curr_level]
        self.level.init()
        self.enemies = self.level.enemies

    def game_loop(self):
        while self.running:
            self.update()
            self.draw()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

    def update(self):
        self.handle_events()
        self.handle_clicks()
        if len(self.enemies) == 0:
            self.next_level()
        if self.player.dead:
            self.save_top_score()
            self.load_top_score()
            return
        if self.won_the_game():
            return
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        self.handle_shots()
        self.level.scroll -= self.level.scroll_speed
        if abs(self.level.scroll) >= self.level.bg.get_width():
            self.level.scroll = 0

    def draw(self):
        if self.player.dead:
            self.show_top_score()
            return
        if self.won_the_game():
            self.winning_screen()
            return
        self.screen.fill("gray")
        for i in range(self.level.tiles_horizontally):
            for j in range(self.level.tiles_vertically):
                self.screen.blit(
                    self.level.bg,
                    (
                        i * self.level.bg.get_width() + self.level.scroll,
                        j * self.level.bg.get_height(),
                    ),
                )
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()

        self.show_score()
        pygame.display.flip()
        pygame.display.update()

    def won_the_game(self):
        return self.levels.index(self.level) == len(self.levels)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def handle_clicks(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_F11]:
            pygame.display.toggle_fullscreen()
        if pressed_keys[pygame.K_ESCAPE]:
            self.running = False

    def handle_shots(self):
        for enemy in self.enemies:
            enemy.die_if_shot(self.player.bullets)
            if enemy.dead and enemy.finished_dying():
                self.enemies.remove(enemy)
                self.add_score(5)

            self.player.lose_health_if_shot(enemy.bullets)

    def winning_screen(self):
        black = (0, 0, 0, 0)
        light_blue = (0, 255, 255)
        font = pygame.font.Font("freesansbold.ttf", 128)
        text = font.render("You win!", True, light_blue, black)
        textRect = text.get_rect()
        textRect.center = (1920 // 2, 1080 // 2)
        self.screen.blit(text, textRect)
        pygame.display.update()
        pygame.display.flip()

    def add_score(self, amount):
        self.score += amount

    def show_score(self):
        black = (0, 0, 0, 255)
        light_blue = (0, 255, 255)
        font = pygame.font.Font("freesansbold.ttf", 64)
        text = font.render(f"{self.score}", True, light_blue, black)
        textRect = text.get_rect()
        textRect.center = (1800, 1080 // 12)
        self.screen.blit(text, textRect)

    def save_top_score(self):
        if self.score <= int(self.top_score):
            return
        with open("top_score", "w") as f:
            f.write(str(self.score))

    def load_top_score(self):
        with open("top_score", "r") as f:
            self.top_score = f.read()

    def show_top_score(self):
        black = (0, 0, 0)
        light_blue = (0, 255, 255)
        font = pygame.font.Font("freesansbold.ttf", 128)
        font1 = pygame.font.Font("freesansbold.ttf", 64)
        text1 = font.render("You lose!", True, light_blue, black)
        text = font1.render(
            f"Current high score: {self.top_score}", True, light_blue, black
        )
        textRect = text.get_rect()
        textRect1 = text1.get_rect()
        textRect1.center = (1920 // 2, 1080 // 2.1)
        textRect.center = (1920 // 2, 1080 // 1.6)
        self.screen.blit(text, textRect)
        self.screen.blit(text1, textRect1)
        pygame.display.update()
        pygame.display.flip()
