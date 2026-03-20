from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import load_sprite, wrap_position

DIRECTION_UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, position)

    def move(self, surface):
        move_to = self.position + self.velocity
        self.position = wrap_position(move_to, surface)

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        return distance < self.radius + other.radius


class Turret(GameObject):
    ROTATION_SPEED = 3
    ACCELERATION = 0.25

    def __init__(self, position):
        super().__init__(position, load_sprite("turret2"), Vector2(0))
        self.direction = Vector2(DIRECTION_UP)

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.ROTATION_SPEED * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION

    def draw(self, surface):
        angle = self.direction.angle_to(Vector2(DIRECTION_UP))
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())

        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

