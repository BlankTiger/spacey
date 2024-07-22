import random

import pygame

from spacey.enemies.enemy import Enemy
from spacey.hitbox import Hitbox
from spacey.position import Position
from spacey.projectiles.bullet import Bullet, Direction
from spacey.projectiles.projectile import Projectile
from spacey.projectiles.special_beam_cannon import SpecialBeamCannon
from spacey.singleton import Singleton
from spacey.spritesheet import Spritesheet


class FrankDyingImages(metaclass=Singleton):
    def __init__(self, width, height):
        self.dying_images = self.load_dying_images(width, height)

    def load_dying_images(self, width, height):
        spritesheet = Spritesheet("images/enemies/frank_death_spritesheet.png", (128, 1536))
        images = [spritesheet.get_sprite((0, x)) for x in range(12)]
        images = [pygame.transform.smoothscale_by(image, 1.5) for image in images]
        images = [pygame.transform.rotate(image, 90) for image in images]
        return images


class Frank(Enemy, pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        self.score_for_killing = 30
        width = 60
        height = 60
        self.pos = Position(x, y)
        self.rect = pygame.Rect(x, y, width, height)
        pos = self.pos_for_hitbox()
        self.hitbox = Hitbox(pos.x, pos.y, width, height)
        self.screen = screen
        self.cooldown = 4000
        self.last = pygame.time.get_ticks()
        self.last_bullet = pygame.time.get_ticks()
        self.projectiles: list[Projectile] = []
        self.dead = False
        self.died_at = 0
        self.sound()
        self.image = pygame.image.load("images/enemies/frank.png")
        self.image = pygame.transform.scale_by(self.image, 1.5)
        self.image = pygame.transform.rotate(self.image, 90)
        self.dying_images = FrankDyingImages(width, height).dying_images
        self.dying_image_idx = 0
        self.health = 100

    def update(self):
        if self.dead:
            self.die_animation()
        random_x = random.randint(-50, 50)
        random_y = random.randint(-50, 50)
        now = pygame.time.get_ticks()
        if now - self.last > self.cooldown:
            self.last = now
            self.move(random_x, random_y)
        self.shoot()
        for projectile in self.projectiles:
            projectile.update()

            if projectile.did_hit or projectile.should_disappear:
                self.projectiles.remove(projectile)

    def die_animation(self):
        self.dying_image_idx += 0.15
        if self.dying_image_idx >= len(self.dying_images):
            self._finished_dying = True
            return
        self.image = self.dying_images[int(self.dying_image_idx)]

    def draw(self):
        self.screen.blit(self.image, (self.pos.x, self.pos.y))
        for bullet in self.projectiles:
            bullet.draw()

    def get_color(self):
        if self.dead:
            return "black"
        return "red"

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_bullet > self.cooldown:
            self.last_bullet = now
            sbc = SpecialBeamCannon(
                self.pos.x - 1660,
                self.pos.y + 75,
                Direction.Left,
                self.screen,
            )
            self.projectiles.append(sbc)
            pygame.mixer.Sound.play(self.shoot_sound)

    def move(self, x_offset, y_offset):
        if self.pos.x + x_offset < 0:
            return
        if self.pos.x + x_offset > 1920 - self.hitbox.width:
            return
        if self.pos.y + y_offset < 0:
            return
        if self.pos.y + y_offset > 1080 - self.hitbox.height:
            return
        self.rect.move_ip(x_offset, y_offset)
        self.pos.x += x_offset
        self.pos.y += y_offset
        pos = self.pos_for_hitbox()
        self.hitbox.update_pos(pos.x, pos.y)

    def pos_for_hitbox(self):
        return Position(self.pos.x + 65, self.pos.y + 64)

    def sound(self):
        self.death_sound = pygame.mixer.Sound("sounds/kill.mp3")
        self.damage_sound = pygame.mixer.Sound("sounds/take_damage.mp3")
        self.shoot_sound = pygame.mixer.Sound("sounds/shoot2.mp3")
        pygame.mixer.Sound.set_volume(self.shoot_sound, 0.035)
        pygame.mixer.Sound.set_volume(self.death_sound, 0.2)
        pygame.mixer.Sound.set_volume(self.damage_sound, 0.2)

    def die_if_shot(self, projectiles: list[Projectile]):
        if self.dead:
            return

        for projectile in projectiles:
            if self.hitbox.overlaps(projectile.hitbox):
                projectile.hit()
                self.take_damage()
                if self.health <= 0:
                    self.die()

    def take_damage(self):
        self.health -= 34
        pygame.mixer.Sound.play(self.damage_sound)

    def die(self):
        print("Enemy hit!")
        pygame.mixer.Sound.play(self.damage_sound)
        self.dead = True
        self.died_at = pygame.time.get_ticks()
        self._finished_dying = False

    def finished_dying(self):
        return self._finished_dying
