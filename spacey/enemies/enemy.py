from typing import Protocol

import pygame

from spacey.projectiles.projectile import Projectile


class Enemy(Protocol):
    screen: pygame.surface.Surface
    score_for_killing: int
    projectiles: list[Projectile]

    def __init__(self, x, y, screen):
        raise NotImplementedError
