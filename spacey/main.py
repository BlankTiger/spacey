from __future__ import annotations

import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    game = Game(screen, clock)
    game.game_loop()


class Player:
    def __init__(self) -> None:
        self.rect = pygame.Rect(30, 30, 60, 60)

    def handle_movement(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(10, 0)
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 10)


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.dt = 0.0
        self.player = Player()

    def game_loop(self):
        while self.running:
            self.handle_events()
            self.handle_clicks()
            self.player.handle_movement()
            self.draw()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

    def draw(self):
        self.screen.fill("gray")
        pygame.draw.rect(self.screen, "blue", self.player.rect)
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
