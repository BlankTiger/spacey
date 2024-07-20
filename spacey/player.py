import pygame

from .bullet import Bullet


class Player:
    def __init__(self, screen) -> None:
        self.rect = pygame.Rect(50, 500, 60, 60)
        self.screen = screen
        self.bullets = []
        self.cooldown = 180
        self.last = pygame.time.get_ticks()

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last > self.cooldown:
            self.last = now
            x, y = self.get_position()
            bullet = Bullet(x, y, self.screen)
            self.bullets.append(bullet)

    def draw(self):
        pygame.draw.rect(self.screen, "blue", self.rect)
        for bullet in self.bullets:
            bullet.draw()
            if bullet.get_position()[0] > 1920:
                self.bullets.remove(bullet)

    def handle_actions(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(10, 0)
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 10)
        if pressed_keys[pygame.K_SPACE]:
            self.shoot()
