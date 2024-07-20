from __future__ import annotations

import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    game = Game(screen, clock)
    game.game_loop()


class Player:
    def __init__(self, screen) -> None:
        self.rect = pygame.Rect(50, 500, 60, 60)
        self.screen = screen
        self.projectiles = []

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def shoot(self):
        x, y = self.get_position()
        rect = pygame.Rect(x, y, 10, 10)
        self.projectiles.append(rect)

    def draw(self):
        pygame.draw.rect(self.screen, "blue", self.rect)
        for bullet in self.projectiles:
            pygame.draw.rect(self.screen, "black", bullet)
            bullet.move_ip(10, 0)

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


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.dt = 0.0
        self.player = Player(self.screen)

    def game_loop(self):
        while self.running:
            self.handle_events()
            self.handle_clicks()
            self.player.handle_actions()
            self.draw()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

    def draw(self):
        self.screen.fill("gray")
        self.player.draw()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def handle_clicks(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_F11]:
            pygame.display.toggle_fullscreen()
        if pressed_keys[pygame.K_ESCAPE]:
            self.running = False
