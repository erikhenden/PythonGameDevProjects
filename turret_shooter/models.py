from pygame.math import Vector2


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, position)

    def move(self):
        self.position += self.velocity

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        return distance < self.radius + other.radius