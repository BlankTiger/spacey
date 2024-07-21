from enum import Enum

import pygame

from .hitbox import Hitbox


class Direction(Enum):
    Left = 1
    Right = 2


class Bullet:
    def __init__(self, x, y, direction, screen):
        self.screen = screen
        width = 10
        height = 10
        self.hitbox = Hitbox(x, y, width, height)
        self.rect = pygame.Rect(x, y, 10, 10)
        self.direction = direction
        self.x = 0
        if self.direction == Direction.Right:
            self.x = 10
        elif self.direction == Direction.Left:
            self.x = -10

    def update(self):
        self.rect.move_ip(self.x, 0)
        self.hitbox.update_pos(self.x, 0)

    def draw(self):
        pygame.draw.rect(self.screen, "black", self.rect)

    def get_position(self):
        return [self.rect.x, self.rect.y]
