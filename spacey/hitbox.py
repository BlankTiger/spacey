import pygame

from spacey.position import Position


class Hitbox:
    def __init__(self, pos: Position, width, height):
        self.pos = pos
        self.width = width
        self.height = height

    def update_pos(self, pos: Position):
        self.pos = pos

    def draw(self, screen):
        pygame.draw.rect(screen, "green", (self.pos.x, self.pos.y, self.width, self.height))

    def overlaps(self, other):
        if self.pos.x + self.width < other.pos.x:
            return False
        if self.pos.x > other.pos.x + other.width:
            return False
        if self.pos.y + self.height < other.pos.y:
            return False
        if self.pos.y > other.pos.y + other.height:
            return False
        return True
