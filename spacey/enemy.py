import pygame
import random
from .bullet import Bullet, Direction


class Enemy:
    def __init__(self, screen) -> None:
        self.rect = pygame.Rect(1500, 500, 60, 60)
        self.screen = screen
        self.cooldown = 1000
        self.last = pygame.time.get_ticks()
        self.last_bullet = pygame.time.get_ticks()
        self.bullets = []

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
        pygame.draw.rect(self.screen, "red", self.rect)
        for bullet in self.bullets:
            bullet.draw()
            if bullet.get_position()[0] < 0:
                self.bullets.remove(bullet)

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
