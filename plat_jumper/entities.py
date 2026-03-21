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

    def jump(self, impulse=-10):
        self.velocity.y = impulse

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
        self.dead = False

    def get_rect(self):
        return pygame.Rect(self.position.x, self.position.y, self.WIDTH, self.HEIGHT)

    def on_land(self, jumper):
        """Called by collision detection when the jumper lands on this platform."""
        jumper.jump()


class CrumblingPlatform(Platform):
    """Disappears shortly after the player lands on it."""
    CRUMBLE_FRAMES = 45  # ~0.75 s at 60 fps

    def __init__(self, position):
        super().__init__(position)
        self.sprite.fill(pygame.Color("peru"))
        self._crumbling = False
        self._timer = self.CRUMBLE_FRAMES

    def on_land(self, jumper):
        jumper.jump()
        self._crumbling = True

    def update(self, surface):
        if self._crumbling:
            self._timer -= 1
            if self._timer <= 0:
                self.dead = True

    def draw(self, surface):
        # Flash every 6 frames while crumbling to warn the player
        if self._crumbling and (self._timer // 6) % 2 == 0:
            return
        surface.blit(self.sprite, self.position)


class SpringPlatform(Platform):
    """Launches the player much higher than a normal jump."""
    IMPULSE = -18

    def __init__(self, position):
        super().__init__(position)
        self.sprite.fill(pygame.Color("limegreen"))

    def on_land(self, jumper):
        jumper.jump(self.IMPULSE)