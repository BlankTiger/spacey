from enum import Enum

import pygame

from spacey.position import Position

from .hitbox import Hitbox
from .spritesheet import Spritesheet


class Direction(Enum):
    Left = 1
    Right = 2


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class BulletImages(metaclass=Singleton):
    def __init__(self, width, height):
        spritesheet = Spritesheet("images/projectiles/bullet.png", (32, 128))
        self.images = [spritesheet.get_sprite((0, x)) for x in range(4)]
        self.images = [
            pygame.transform.smoothscale(image, (width, height)) for image in self.images
        ]
        self.images_left = [pygame.transform.rotate(image, 90) for image in self.images]
        self.images_right = [pygame.transform.rotate(image, 270) for image in self.images]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, screen):
        super()
        self.pos = Position(x, y)
        self.screen = screen
        width = 32 * 2
        height = 64 * 2
        images = BulletImages(width, height)
        self.direction = direction
        if self.direction == Direction.Right:
            self.images = images.images_right
            self.x_change = 10
            self.hitbox_offset_x = -100
            self.hitbox_offset_y = -20
        elif self.direction == Direction.Left:
            self.images = images.images_left
            self.x_change = -10
            self.hitbox_offset_x = 0
            self.hitbox_offset_y = -20
        self.curr_img = 0
        self.image = self.images[self.curr_img]
        self.hitbox = Hitbox(self.pos, 30, 30)

    def update(self):
        self.pos.x += self.x_change
        self.hitbox.update_pos(self.pos)
        self.curr_img += 0.1
        if self.curr_img >= len(self.images):
            self.curr_img = 0
        self.image = self.images[int(self.curr_img)]

    def draw(self):
        self.screen.blit(
            self.image, (self.pos.x + self.hitbox_offset_x, self.pos.y + self.hitbox_offset_y)
        )
