import random

import pygame

from spacey.position import Position

from .bullet import Bullet, Direction
from .hitbox import Hitbox


class Enemy:
    def __init__(self, x, y, screen) -> None:
        width = 60
        height = 60
        self.pos = Position(x, y)
        self.rect = pygame.Rect(x, y, width, height)
        self.hitbox = Hitbox(self.pos.x, self.pos.y, width, height)
        self.screen = screen
        self.cooldown = 1000
        self.last = pygame.time.get_ticks()
        self.last_bullet = pygame.time.get_ticks()
        self.bullets: list[Bullet] = []
        self.dead = False
        self.died_at = 0
        self.sound()

    def update(self):
        random_x = random.randint(-50, 50)
        random_y = random.randint(-50, 50)
        now = pygame.time.get_ticks()
        if now - self.last > self.cooldown:
            self.last = now
            self.move(random_x, random_y)
        self.shoot()
        for bullet in self.bullets:
            bullet.update()
            if bullet.pos.x < 0:
                self.bullets.remove(bullet)

    def draw(self):
        pygame.draw.rect(self.screen, self.get_color(), self.rect)
        for bullet in self.bullets:
            bullet.draw()

    def get_color(self):
        if self.dead:
            return "black"
        return "red"

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_bullet > self.cooldown:
            self.last_bullet = now
            bullet = Bullet(self.pos.x, self.pos.y, Direction.Left, self.screen)
            self.bullets.append(bullet)
            pygame.mixer.Sound.play(self.shoot_sound)

    def move(self, x_offset, y_offset):
        if self.pos.x + x_offset < 0:
            return
        if self.pos.x + x_offset > 1920 - self.rect.width:
            return
        if self.pos.y + y_offset < 0:
            return
        if self.pos.y + y_offset > 1080 - self.rect.height:
            return
        self.rect.move_ip(x_offset, y_offset)
        self.pos.x += x_offset
        self.pos.y += y_offset
        self.hitbox.update_pos(self.pos.x, self.pos.y)

    def sound(self):
        pygame.mixer.pre_init()
        pygame.mixer.init()
        self.death_sound = pygame.mixer.Sound("sounds/kill.mp3")
        self.damage_sound = pygame.mixer.Sound("sounds/take_damage.mp3")
        self.shoot_sound = pygame.mixer.Sound("sounds/shoot2.mp3")
        pygame.mixer.Sound.set_volume(self.shoot_sound, 0.035)
        pygame.mixer.Sound.set_volume(self.death_sound, 0.2)
        pygame.mixer.Sound.set_volume(self.damage_sound, 0.2)

    def die_if_shot(self, bullets):
        if self.dead:
            return

        for bullet in bullets:
            if self.hitbox.overlaps(bullet.hitbox):
                print("Enemy hit!")
                pygame.mixer.Sound.play(self.damage_sound)
                self.dead = True
                self.died_at = pygame.time.get_ticks()
