import math
import random

import pygame

from spacey.enemies.fighter import EnemyFighter
from spacey.enemies.frank import Frank


class Level:
    def __init__(self, bg, screen, enemy_blueprint):
        self.screen = screen
        self.enemy_blueprint = enemy_blueprint
        self.bg = pygame.image.load(bg).convert()
        self.tiles_horizontally = math.ceil(1920 / self.bg.get_width()) + 2
        self.tiles_vertically = math.ceil(1080 / self.bg.get_height()) + 2
        self.scroll = 0
        self.scroll_speed = random.randint(5, 30)

    def init(self):
        self.enemies = self.create_enemies()

    def create_enemies(self):
        x_range = [1500, 1800]
        y_range = [100, 900]
        enemies = []
        for EnemyType, amount in self.enemy_blueprint.items():
            _enemies = [
                EnemyType(x, y, self.screen)
                for x, y in zip(
                    [random.randint(x_range[0], x_range[1]) for _ in range(amount)],
                    [random.randint(y_range[0], y_range[1]) for _ in range(amount)],
                )
            ]
            enemies.extend(_enemies)
        return enemies


def load_levels(screen):
    default_enemies = {EnemyFighter: 5}
    every_5th_level = {EnemyFighter: 8, Frank: 1}
    every_10th_level = {EnemyFighter: 10, Frank: 3}
    while True:
        for i in range(1, 34):
            if i % 10 == 0:
                yield Level(f"images/bgs/lvl{i}.png", screen, every_10th_level)
            elif i % 5 == 0:
                yield Level(f"images/bgs/lvl{i}.png", screen, every_5th_level)
            else:
                yield Level(f"images/bgs/lvl{i}.png", screen, default_enemies)

        default_enemies = update_enemy_count(default_enemies)
        every_5th_level = update_enemy_count(every_5th_level)
        every_10th_level = update_enemy_count(every_10th_level)


def update_enemy_count(blueprint):
    result = {}
    for t, amount in blueprint.items():
        result[t] = amount + 1
    return result


# def show_level(self):
#     black = (0, 0, 0, 0)
#     light_blue = (0, 255, 255)
#     font = pygame.font.Font("freesansbold.ttf", 128)
#     text = font.render("Text_here", True, light_blue, black)
#     textRect = text.get_rect()
#     textRect.center = (1920 // 2, 1080 // 2)
#     self.screen.blit(text, textRect)
#     pygame.display.update()
#     pygame.display.flip()
