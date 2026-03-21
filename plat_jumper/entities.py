import pygame
from pygame import Vector2
from utils import load_image


class GameObject:
    def __init__(self, position, sprite):
        self.position = Vector2(position)
        self.sprite = sprite

    def update(self, surface):
        pass

    def draw(self, surface):
        surface.blit(self.sprite, self.position)


class Jumper(GameObject):
    SPEED = 6

    def __init__(self, position):
        super().__init__(position, load_image("jumper2"))
        self.velocity = Vector2(0, 0)
        self.gravity = Vector2(0, 0.25)
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.position -= Vector2(self.sprite.get_size()) // 2

    def get_rect(self):
        return pygame.Rect(self.position.x, self.position.y, self.width, self.height)

    def jump(self):
        self.velocity.y = 0
        self.velocity.y -= 10

    def move_sideways(self, right=True):
        direction = 1 if right else -1
        self.position.x += direction * self.SPEED

    def update(self, surface):
        self.velocity += self.gravity
        self.position += self.velocity

        # Wrap horizontally: exit one side, reappear on the other
        if self.position.x + self.width < 0:
            self.position.x = surface.get_width()
        elif self.position.x > surface.get_width():
            self.position.x = -self.width


class Platform(GameObject):
    WIDTH = 80
    HEIGHT = 12

    def __init__(self, position):
        sprite = pygame.Surface((self.WIDTH, self.HEIGHT))
        sprite.fill(pygame.Color("sienna"))
        super().__init__(position, sprite)

    def get_rect(self):
        return pygame.Rect(self.position.x, self.position.y, self.WIDTH, self.HEIGHT)