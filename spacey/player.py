import pygame

from .bullet import Bullet, Direction
from .hitbox import Hitbox


class Player:
    def __init__(self, screen) -> None:
        x = 50
        y = 500
        width = 60
        height = 60
        self.rect = pygame.Rect(x, y, width, height)
        self.hitbox = Hitbox(x, y, width, height)
        self.screen = screen
        self.bullets: list[Bullet] = []
        self.cooldown = 180
        self.last = pygame.time.get_ticks()
        self.dead = False
        self.sound()
        self.sound_played = False

    def get_position(self):
        return [self.rect.x, self.rect.y]

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last > self.cooldown:
            self.last = now
            x, y = self.get_position()
            bullet = Bullet(x, y, Direction.Right, self.screen)
            self.bullets.append(bullet)
            pygame.mixer.Sound.play(self.shoot_sound)

    def update(self):
        self.handle_actions()
        for bullet in self.bullets:
            bullet.update()
            if bullet.get_position()[0] > 1920:
                self.bullets.remove(bullet)

    def draw(self):
        pygame.draw.rect(self.screen, self.get_color(), self.rect)
        for bullet in self.bullets:
            bullet.draw()

    def move(self, x_offset, y_offset):
        x, y = self.get_position()
        if x + x_offset < 0:
            return
        if x + x_offset > 1920 - self.rect.width:
            return
        if y + y_offset < 0:
            return
        if y + y_offset > 1080 - self.rect.height:
            return
        self.rect.move_ip(x_offset, y_offset)
        self.hitbox.update_pos(x_offset, y_offset)

    def sound(self):
        pygame.mixer.pre_init()
        pygame.mixer.init()
        self.death_sound = pygame.mixer.Sound("sounds/death.mp3")
        self.shoot_sound = pygame.mixer.Sound("sounds/bullet.mp3")
        pygame.mixer.Sound.set_volume(self.death_sound, 0.5)
        pygame.mixer.Sound.set_volume(self.shoot_sound, 0.1)
        pygame.mixer.music.load("sounds/song2.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.05)

    def death_sfx(self):
        if not self.sound_played:
            pygame.mixer.Sound.play(self.death_sound)
            self.sound_played = True

    def stop(self):
        pygame.mixer.music.stop()

    def die_if_shot(self, bullets):
        if self.dead:
            self.death_sfx()
            self.stop()
            return

        for bullet in bullets:
            if self.hitbox.overlaps(bullet.hitbox):
                print("You Died")
                self.dead = True
                self.died_at = pygame.time.get_ticks()

    def handle_actions(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.move(-10, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.move(10, 0)
        if pressed_keys[pygame.K_UP]:
            self.move(0, -10)
        if pressed_keys[pygame.K_DOWN]:
            self.move(0, 10)
        if pressed_keys[pygame.K_SPACE]:
            self.shoot()

    def get_color(self):
        if self.dead:
            return "black"
        return "blue"

    def die(self):
        print("BETON")
