from __future__ import annotations

import random

import pygame

from .enemy import Enemy
from .player import Player


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
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
        self.enemies = []
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
        self.player.handle_actions()
        bullets = self.player.bullets
        for enemy in self.enemies:
            enemy.die_if_shot(bullets)
            if enemy.dead and pygame.time.get_ticks() - enemy.died_at > 1000:
                self.enemies.remove(enemy)
            self.player.die_if_shot(enemy.bullets)
            if (
                self.player.dead
                and pygame.time.get_ticks() - self.player.died_at > 1000
            ):
                self.player.die()

    def draw(self):
        self.screen.fill("gray")
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.flip()

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
