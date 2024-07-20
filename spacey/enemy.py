import pygame


class Enemy:
    def __init__(self, screen) -> None:
        self.rect = pygame.Rect(1500, 500, 60, 60)
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, "red", self.rect)
