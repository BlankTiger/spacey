import pygame

from .bullet import Bullet, Direction
from .hitbox import Hitbox


class Player:
    def __init__(self, screen) -> None:
        x = 50
        y = 500
        width = 60
        height = 60
        self.rect = pygame.Rect(x, y, width, height)
        self.hitbox = Hitbox(x, y, width, height)
        self.screen = screen
        self.bullets = []
        self.cooldown = 180
        self.last = pygame.time.get_ticks()
        self.dead = False

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last > self.cooldown:
            self.last = now
            x, y = self.get_position()
            bullet = Bullet(x, y, Direction.Right, self.screen)
            self.bullets.append(bullet)

    def draw(self):
        pygame.draw.rect(self.screen, self.get_color(), self.rect)
        for bullet in self.bullets:
            bullet.draw()
            if bullet.get_position()[0] > 1920:
                self.bullets.remove(bullet)

    def move(self, x_offset, y_offset):
        x, y = self.get_position()
        if x + x_offset < 0:
            return
        if x + x_offset > 1920 - self.rect.width:
            return
        if y + y_offset < 0:
            return
        if y + y_offset > 1080 - self.rect.height:
            return
        self.rect.move_ip(x_offset, y_offset)
        self.hitbox.update_pos(x_offset, y_offset)

    def die_if_shot(self, bullets):
        for bullet in bullets:
            if self.hitbox.overlaps(bullet.hitbox):
                print("You Died")
                self.dead = True
                self.died_at = pygame.time.get_ticks()

    def handle_actions(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.move(-10, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.move(10, 0)
        if pressed_keys[pygame.K_UP]:
            self.move(0, -10)
        if pressed_keys[pygame.K_DOWN]:
            self.move(0, 10)
        if pressed_keys[pygame.K_SPACE]:
            self.shoot()

    def get_color(self):
        if self.dead:
            return "black"
        return "blue"

    def die(self):
        print("BETON")
