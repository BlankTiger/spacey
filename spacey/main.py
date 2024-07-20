from __future__ import annotations

import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()
    game = Game(screen, clock)
    game.game_loop()


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.rect = pygame.Rect(30, 30, 60, 60)
        self.dt = 0.0

    def game_loop(self):
        while self.running:
            self.handle_events()
            self.handle_clicks()
            self.draw()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

    def draw(self):
        self.screen.fill("purple")
        rect = pygame.Rect(30, 30, 60, 60)
        pygame.draw.rect(self.screen, "blue", rect)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def handle_clicks(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_F11]:
            pygame.display.toggle_fullscreen()
