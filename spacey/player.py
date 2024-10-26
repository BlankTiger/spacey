import pygame

from spacey.hitbox import Hitbox
from spacey.position import Position
from spacey.projectiles.bullet import Bullet, Direction
from spacey.singleton import Singleton


class Health:
    def __init__(self, screen):
        self._health = 100
        self.screen = screen
        self.rect = pygame.rect.Rect(100, 70, self.get_health_width(), 40)
        self.outline = self.rect.copy()
        self.outline.x -= 4.4
        self.outline.y -= 4
        self.outline.width = 1.01 * self.rect.width
        self.outline.height = 1.2 * self.rect.height

    def get_health_width(self):
        return self._health * 9

    def draw(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect)
        pygame.draw.rect(self.screen, (255, 0, 0), self.outline, 2)

    def update(self):
        self.rect.width = self.get_health_width()
        if self._health <= 0:
            self._health = 0

    def shot_for(self, damage):
        self._health -= damage

    @property
    def health(self):
        return self._health


class PlayerDamageImages(metaclass=Singleton):
    def __init__(self, width, height):
        self.damaged_images = self.load_damaged_images(width, height)

    def load_damaged_images(self, width, height):
        images = []
        for idx in range(3):
            image = pygame.image.load(f"images/ship/ship_damage_{idx}.png")
            image = pygame.transform.scale(image, (width, height))
            image = pygame.transform.rotate(image, 270)
            images.append(image)
        return images


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
        self._health = Health(self.screen)
        self.shot_by = set()
        self.took_damage = False
        self.damaged_images = PlayerDamageImages(width, height).damaged_images

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
            bullet = Bullet(
                self.pos.x + 90, self.pos.y + 58, Direction.Right, self.screen
            )
            self.bullets.append(bullet)
            pygame.mixer.Sound.play(self.shoot_sound)

    def update(self):
        self.handle_actions()
        self._health.update()
        self.update_image_based_on_health()
        for bullet in self.bullets:
            bullet.update()
            if bullet.pos.x > 1920 or bullet.did_hit:
                self.bullets.remove(bullet)

    def update_image_based_on_health(self):
        if self.health == 100:
            self.image = self.image
        elif self.health < 100 and self.health >= 50:
            self.image = self.damaged_images[0]
        elif self.health < 50 and self.health > 25:
            self.image = self.damaged_images[1]
        elif self.health <= 25:
            self.image = self.damaged_images[2]

    @property
    def health(self):
        return self._health.health

    def draw(self):
        self.screen.blit(self.image, (self.pos.x, self.pos.y))
        for bullet in self.bullets:
            bullet.draw()
        self._health.draw()

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
        self.death_sound = pygame.mixer.Sound("sounds/death2.mp3")
        self.shoot_sound = pygame.mixer.Sound("sounds/bullet.mp3")
        pygame.mixer.Sound.set_volume(self.death_sound, 0.3)
        pygame.mixer.Sound.set_volume(self.shoot_sound, 0.1)
        pygame.mixer.music.load("sounds/song3.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    def death_sfx(self):
        if not self.sound_played:
            pygame.mixer.Sound.play(self.death_sound)
            self.sound_played = True
            pygame.mixer.music.stop()

    def getting_shot_sfx(self):
        self.getting_shot_sound = pygame.mixer.Sound("sounds/take_damage.mp3")
        pygame.mixer.Sound.play(self.getting_shot_sound)
        pygame.mixer.Sound.set_volume(self.getting_shot_sound, 0.3)

    def lose_health_if_shot(self, bullets: list[Bullet]):
        if self._health.health <= 0:
            self.dead = True
            self.died_at = pygame.time.get_ticks()
            self.death_sfx()
            return

        for bullet in bullets:
            if self.hitbox.overlaps(bullet.hitbox):
                bullet.hit()
                print("You got shot")
                self._health.shot_for(bullet.damage)
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
