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
        self.height = self.sprite.get_height()
        self.position -= Vector2(self.sprite.get_size()) // 2

    def jump(self):
        self.velocity.y = 0
        self.velocity.y -= 13

    def move_sideways(self, right=True):
        direction = 1 if right else -1
        self.position.x += direction * self.SPEED

    def update(self, surface):
        self.velocity += self.gravity
        self.position += self.velocity

        # Ensure jumper does not fall off the bottom of the screen
        if self.position.y + self.height > surface.get_height():
            self.position.y = surface.get_height() - self.height