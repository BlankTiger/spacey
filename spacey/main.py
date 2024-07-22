from __future__ import annotations

import math
import random

import pygame

from spacey.enemy import Enemy
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
        self.bg = pygame.image.load("images/bgs/lvl1.png").convert()
        self.tiles_horizontally = math.ceil(1920 / self.bg.get_width()) + 2
        self.tiles_vertically = math.ceil(1080 / self.bg.get_height()) + 2
        self.scroll = 0
        self.clock = clock
        self.running = True
        self.dt = 0.0
        self.player = Player(self.screen)
        self.enemies: list[Enemy] = []
        self.create_enemies(5)

    def create_enemies(self, amount):
        x_range = [1500, 1900]
        y_range = [0, 1080]
        for _ in range(amount):
            x = random.randint(x_range[0], x_range[1])
            y = random.randint(y_range[0], y_range[1])
            enemy = Enemy(x, y, self.screen)
            self.enemies.append(enemy)

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
            return
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        self.handle_shots()
        self.scroll -= 10
        if abs(self.scroll) >= self.bg.get_width():
            self.scroll = 0

    def draw(self):
        if len(self.enemies) == 0:
            self.winning_screen()
            return
        self.screen.fill("gray")
        for i in range(self.tiles_horizontally):
            for j in range(self.tiles_vertically):
                self.screen.blit(
                    self.bg,
                    (i * self.bg.get_width() + self.scroll, j * self.bg.get_height()),
                )
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.flip()
        pygame.display.update()

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

            self.player.lose_health_if_shot(enemy.bullets)

    def winning_screen(self):
        # white = (255, 255, 255)
        # green = (0, 255, 0)
        black = (0, 0, 0, 0)
        # blue = (0, 0, 128)
        light_blue = (0, 255, 255)
        font = pygame.font.Font("freesansbold.ttf", 128)
        text = font.render("You Win!", True, light_blue, black)
        textRect = text.get_rect()
        textRect.center = (1920 // 2, 1080 // 2)  # (X // 2, Y // 2)
        self.screen.blit(text, textRect)
        pygame.display.update()
        pygame.display.flip()
