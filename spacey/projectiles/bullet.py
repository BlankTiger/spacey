import pygame

from spacey.direction import Direction
from spacey.hitbox import Hitbox
from spacey.position import Position
from spacey.projectiles.projectile import Projectile
from spacey.singleton import Singleton
from spacey.spritesheet import Spritesheet


class BulletImages(metaclass=Singleton):
    def __init__(self, width, height):
        spritesheet = Spritesheet("images/projectiles/bullet.png", (32, 128))
        self.images = [spritesheet.get_sprite((0, x)) for x in range(4)]
        self.images = [
            pygame.transform.smoothscale(image, (width, height)) for image in self.images
        ]
        self.images_left = [pygame.transform.rotate(image, 90) for image in self.images]
        self.images_right = [pygame.transform.rotate(image, 270) for image in self.images]


class Bullet(Projectile, pygame.sprite.Sprite):
    def __init__(self, x, y, direction, screen):
        super()
        self.damage = 10
        self.pos = Position(x, y)
        self.screen = screen
        width = 32 * 2
        height = 180 * 2
        images = BulletImages(width, height)
        self.direction = direction
        if self.direction == Direction.Right:
            self.images = images.images_right
            self.x_change = 10
            self.hitbox_offset_x = -310
            self.hitbox_offset_y = -20
        elif self.direction == Direction.Left:
            self.images = images.images_left
            self.x_change = -10
            self.hitbox_offset_x = -20
            self.hitbox_offset_y = -20
        self.curr_img = 0
        self.image = self.images[self.curr_img]
        self.hitbox = Hitbox(self.pos.x, self.pos.y, 30, 30)
        self._hit = False

    def hit(self):
        self._hit = True

    @property
    def did_hit(self):
        return self._hit

    def update(self):
        self.pos.x += self.x_change
        self.hitbox.update_pos(self.pos.x, self.pos.y)
        self.curr_img += 0.1
        if self.curr_img >= len(self.images):
            self.curr_img = 0
        self.image = self.images[int(self.curr_img)]

    def draw(self):
        self.screen.blit(
            self.image, (self.pos.x + self.hitbox_offset_x, self.pos.y + self.hitbox_offset_y)
        )
