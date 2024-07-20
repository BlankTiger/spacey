import pygame


class Bullet:
    def __init__(self, x, y, screen):
        self.screen = screen
        self.rect = pygame.Rect(x, y, 10, 10)

    def draw(self):
        pygame.draw.rect(self.screen, "black", self.rect)
        self.rect.move_ip(10, 0)

    def get_position(self):
        return [self.rect.x, self.rect.y]
