import pygame

from spacey.direction import Direction
from spacey.hitbox import Hitbox
from spacey.position import Position
from spacey.projectiles.projectile import Projectile
from spacey.singleton import Singleton
from spacey.spritesheet import Spritesheet


class SpecialBeamCannonImages(metaclass=Singleton):
    def __init__(self, width, height):
        spritesheet = Spritesheet("images/projectiles/special_beam_cannon.png", (38, 72))
        self.images = [spritesheet.get_sprite((0, x)) for x in range(2)]
        self.images = [
            pygame.transform.smoothscale(image, (width, height)) for image in self.images
        ]
        self.images = [pygame.transform.rotate(image, 270) for image in self.images]


class SpecialBeamCannon(Projectile, pygame.sprite.Sprite):
    def __init__(self, x, y, direction, screen):
        super()
        self.damage = 50
        self.pos = Position(x, y)
        self.screen = screen
        width = 32 * 2
        height = 1600 * 2
        images = SpecialBeamCannonImages(width, height).images
        self.direction = direction
        self.images = images
        if self.direction == Direction.Right:
            self.hitbox_offset_x = -310
            self.hitbox_offset_y = -20
        elif self.direction == Direction.Left:
            self.hitbox_offset_x = -1510
            self.hitbox_offset_y = -8
        self.curr_img = 0
        self.image = self.images[self.curr_img]
        self.hitbox = Hitbox(self.pos.x, self.pos.y, 1700, 45)
        self._hit = False
        self.shot_at = pygame.time.get_ticks()

    def hit(self):
        self._hit = True

    @property
    def did_hit(self):
        return self._hit

    @property
    def should_disappear(self):
        return pygame.time.get_ticks() - self.shot_at > 3000

    def update(self):
        self.hitbox.update_pos(self.pos.x, self.pos.y)
        self.curr_img += 0.1
        if self.curr_img >= len(self.images):
            self.curr_img = 0
        self.image = self.images[int(self.curr_img)]

    def draw(self):
        self.screen.blit(
            self.image, (self.pos.x + self.hitbox_offset_x, self.pos.y + self.hitbox_offset_y)
        )
