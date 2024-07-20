from __future__ import annotations

import pygame


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    game = Game(screen, clock)
    game.game_loop()


class Game:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock) -> None:
        self.screen = screen
        self.clock = clock
        self.running = True
        self.dt = 0.0

    def game_loop(self) -> None:
        while self.running:
            self.handle_events()
            self.handle_clicks()
            self.screen.fill("purple")
            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def handle_clicks(self) -> None:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_F11]:
            pygame.display.toggle_fullscreen()
