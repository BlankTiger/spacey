import random

import pygame

from .bullet import Bullet, Direction
from .hitbox import Hitbox


class Enemy:
    def __init__(self, screen) -> None:
        x = 1500
        y = 500
        width = 60
        height = 60
        self.rect = pygame.Rect(x, y, width, height)
        self.hitbox = Hitbox(x, y, width, height)
        self.screen = screen
        self.cooldown = 1000
        self.last = pygame.time.get_ticks()
        self.last_bullet = pygame.time.get_ticks()
        self.bullets = []
        self.dead = False
        self.died_at = 0

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def draw(self):
        random_x = random.randint(-50, 50)
        random_y = random.randint(-50, 50)
        now = pygame.time.get_ticks()
        if now - self.last > self.cooldown:
            self.last = now
            self.move(random_x, random_y)
        self.shoot()
        pygame.draw.rect(self.screen, self.get_color(), self.rect)
        for bullet in self.bullets:
            bullet.draw()
            if bullet.get_position()[0] < 0:
                self.bullets.remove(bullet)

    def get_color(self):
        if self.dead:
            return "black"
        return "red"

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_bullet > self.cooldown:
            self.last_bullet = now
            x, y = self.get_position()
            bullet = Bullet(x, y, Direction.Left, self.screen)
            self.bullets.append(bullet)

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

    def die_if_shot(self, bullets):
        for bullet in bullets:
            if self.hitbox.overlaps(bullet.hitbox):
                print("Enemy hit!")
                self.dead = True
                self.died_at = pygame.time.get_ticks()
