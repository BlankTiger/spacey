import math
import random

import pygame

from spacey.enemies.fighter import EnemyFighter


class Level:
    def __init__(self, bg, screen):
        self.screen = screen
        self.bg = pygame.image.load(bg).convert()
        self.tiles_horizontally = math.ceil(1920 / self.bg.get_width()) + 2
        self.tiles_vertically = math.ceil(1080 / self.bg.get_height()) + 2
        self.scroll = 0
        self.scroll_speed = random.randint(5, 50)

    def init(self):
        self.enemies = self.create_enemies(5)

    def create_enemies(self, amount):
        x_range = [1500, 1800]
        y_range = [100, 900]
        enemies = []
        for _ in range(amount):
            x = random.randint(x_range[0], x_range[1])
            y = random.randint(y_range[0], y_range[1])
            enemy = EnemyFighter(x, y, self.screen)
            enemies.append(enemy)
        return enemies


def load_levels(screen):
    return [Level(f"images/bgs/lvl{i}.png", screen) for i in range(1, 35)]
