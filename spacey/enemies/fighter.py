import random

import pygame

from spacey.enemies.enemy import Enemy
from spacey.hitbox import Hitbox
from spacey.position import Position
from spacey.projectiles.bullet import Bullet, Direction
from spacey.singleton import Singleton
from spacey.spritesheet import Spritesheet


class FighterDyingImages(metaclass=Singleton):
    def __init__(self, width, height):
        self.dying_images = self.load_dying_images(width, height)

    def load_dying_images(self, width, height):
        spritesheet = Spritesheet("images/enemies/fighter_death_spritesheet.png", (64, 576))
        images = [spritesheet.get_sprite((0, x)) for x in range(9)]
        images = [pygame.transform.smoothscale_by(image, 3) for image in images]
        images = [pygame.transform.rotate(image, 90) for image in images]
        return images


class EnemyFighter(Enemy, pygame.sprite.Sprite):
    def __init__(self, x, y, screen) -> None:
        width = 60
        height = 60
        self.score_for_killing = 5
        self.pos = Position(x, y)
        self.rect = pygame.Rect(x, y, width, height)
        pos = self.pos_for_hitbox()
        self.hitbox = Hitbox(pos.x, pos.y, width, height)
        self.screen = screen
        self.cooldown = 1000
        self.last = pygame.time.get_ticks()
        self.last_bullet = pygame.time.get_ticks()
        self.projectiles: list[Bullet] = []
        self.dead = False
        self.died_at = 0
        self.sound()
        self.image = pygame.image.load("images/enemies/fighter.png")
        self.image = pygame.transform.scale_by(self.image, 3)
        self.image = pygame.transform.rotate(self.image, 90)
        self.dying_images = FighterDyingImages(width, height).dying_images
        self.dying_image_idx = 0

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
        for bullet in self.projectiles:
            bullet.update()

            if bullet.pos.x < 0 or bullet.did_hit:
                self.projectiles.remove(bullet)

    def die_animation(self):
        self.dying_image_idx += 0.2
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
            bullet = Bullet(self.pos.x + 40, self.pos.y + 86, Direction.Left, self.screen)
            self.projectiles.append(bullet)
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

    def die_if_shot(self, bullets: list[Bullet]):
        if self.dead:
            return

        for bullet in bullets:
            if self.hitbox.overlaps(bullet.hitbox):
                bullet.hit()
                self.die()

    def die(self):
        print("Enemy hit!")
        pygame.mixer.Sound.play(self.damage_sound)
        self.dead = True
        self.died_at = pygame.time.get_ticks()
        self._finished_dying = False

    def finished_dying(self):
        return self._finished_dying
