from pygame.sprite import Sprite
from pygame.math import Vector2
from pygame import Surface
from random import randint, randrange
import random


class Entity(Sprite):
    def __init__(self, position, size, color):
        Sprite.__init__(self)
        self.position = Vector2(position)
        self.image = Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=self.position)
        self.speed = 12

class Shooter(Entity):
    def __init__(self, position):
        color = (255, 0, 0)
        super().__init__(position, (100, 100), color)


class Mouse(Entity):
    def __init__(self, position):
        color = (30, 200, 90)
        super().__init__(position, (75, 75), color)
        self.move_timer = 0.0
        self.secs_to_move = random.random() * 2.5

    def update(self, dt, surface):
        self.move_timer += dt
        if self.move_timer >= self.secs_to_move:
            self.position.x += (randint(-1, 1) * self.speed)
            self.rect.center = self.position
            self.move_timer = 0.0

        if not surface.get_rect().colliderect(self.rect):
            self.kill()


class Bullet(Sprite):
    def __init__(self, sprite, position, direction):
        Sprite.__init__(self)
        self.position = Vector2(position)
        self.image = sprite
        self.rect = self.image.get_rect(center=self.position)
        self.speed = 5
        self.direction = direction

    def update(self, surface):
        self.position += self.direction * self.speed
        self.rect.center = self.position

        # Remove bullets off-screen
        if not surface.get_rect().colliderect(self.rect):
            self.kill()