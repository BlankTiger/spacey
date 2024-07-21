import pygame

from spacey.bullet import Bullet, Direction
from spacey.hitbox import Hitbox
from spacey.position import Position


class Player(pygame.sprite.Sprite):
    def __init__(self, screen) -> None:
        super()
        self.pos = Position(50, 500)
        width = 140
        height = 140
        self.load_full_health(width, height)
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pygame.Rect(self.pos.x, self.pos.y, width, height)
        pos = self.pos_for_hitbox()
        self.hitbox = Hitbox(pos[0], pos[1], width / 2, height / 2)
        self.screen = screen
        self.bullets: list[Bullet] = []
        self.cooldown = 180
        self.last = pygame.time.get_ticks()
        self.dead = False
        self.sound()
        self.sound_played = False

    def pos_for_hitbox(self):
        return self.pos.x + 30, self.pos.y + 35

    def load_full_health(self, width, height):
        self.image = pygame.image.load("images/ship/ship_full_health.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image = pygame.transform.rotate(self.image, 270)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last > self.cooldown:
            self.last = now
            bullet = Bullet(self.pos.x, self.pos.y, Direction.Right, self.screen)
            self.bullets.append(bullet)
            pygame.mixer.Sound.play(self.shoot_sound)

    def update(self):
        self.handle_actions()
        for bullet in self.bullets:
            bullet.update()
            if bullet.pos.x > 1920:
                self.bullets.remove(bullet)

    def draw(self):
        self.screen.blit(self.image, (self.pos.x, self.pos.y))
        for bullet in self.bullets:
            bullet.draw()

    def move(self, x_offset, y_offset):
        if self.pos.x + x_offset < 0:
            return
        if self.pos.x + x_offset > 1920 - self.rect.width:
            return
        if self.pos.y + y_offset < 0:
            return
        if self.pos.y + y_offset > 1080 - self.rect.height:
            return
        self.rect.move_ip(x_offset, y_offset)
        self.pos.x += x_offset
        self.pos.y += y_offset
        pos = self.pos_for_hitbox()
        self.hitbox.update_pos(pos[0], pos[1])

    def sound(self):
        pygame.mixer.pre_init()
        pygame.mixer.init()
        self.death_sound = pygame.mixer.Sound("sounds/death.mp3")
        self.shoot_sound = pygame.mixer.Sound("sounds/bullet.mp3")
        pygame.mixer.Sound.set_volume(self.death_sound, 0.5)
        pygame.mixer.Sound.set_volume(self.shoot_sound, 0.1)
        pygame.mixer.music.load("sounds/song2.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.15)

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
