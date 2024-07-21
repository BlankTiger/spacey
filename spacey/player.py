import pygame

from spacey.bullet import Bullet, Direction
from spacey.hitbox import Hitbox
from spacey.position import Position


class Health:
    def __init__(self, screen):
        self.health = 100
        self.screen = screen
        self.rect = pygame.rect.Rect(100, 70, self.get_health_width(), 40)
        self.outline = self.rect.copy()
        self.outline.x -= 5
        self.outline.y -= 5
        self.outline.width = 1.01 * self.rect.width
        self.outline.height = 1.2 * self.rect.height

    def get_health_width(self):
        return self.health * 9

    def draw(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect)
        pygame.draw.rect(self.screen, (255, 0, 0), self.outline, 2)

    def update(self):
        self.rect.width = self.get_health_width()
        if self.health <= 0:
            self.health = 0

    def shot(self):
        self.health -= 10


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
        self.health = Health(self.screen)
        self.shot_by = set()

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
        self.health.update()
        for bullet in self.bullets:
            bullet.update()
            if bullet.pos.x > 1920:
                self.bullets.remove(bullet)

    def draw(self):
        self.screen.blit(self.image, (self.pos.x, self.pos.y))
        for bullet in self.bullets:
            bullet.draw()
        self.health.draw()

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
        self.death_sound = pygame.mixer.Sound("sounds/death2.mp3")
        self.shoot_sound = pygame.mixer.Sound("sounds/bullet.mp3")
        pygame.mixer.Sound.set_volume(self.death_sound, 0.3)
        pygame.mixer.Sound.set_volume(self.shoot_sound, 0.1)
        pygame.mixer.music.load("sounds/song2.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.15)

    def death_sfx(self):
        if not self.sound_played:
            pygame.mixer.Sound.play(self.death_sound)
            self.sound_played = True
            pygame.mixer.music.stop()

    def getting_shot_sfx(self): ...

    def get_shot(self, bullets):
        if self.health.health <= 0:
            print("You died")
            self.dead = True
            self.died_at = pygame.time.get_ticks()
            self.death_sfx()
            return

        for bullet in bullets:
            if self.hitbox.overlaps(bullet.hitbox) and bullet not in self.shot_by:
                print("You got shot")
                self.health.shot()
                self.shot_by.add(bullet)
                self.getting_shot_sfx()

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
