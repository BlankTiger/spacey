from typing import Protocol

from spacey.direction import Direction
from spacey.hitbox import Hitbox


class Projectile(Protocol):
    hitbox: Hitbox
    direction: Direction
    damage: int

    def hit(self):
        raise NotImplementedError

    def did_hit(self):
        raise NotImplementedError
