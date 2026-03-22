from pygame.math import Vector2
from pathlib import Path
from pygame.image import load


def get_direction(a, b):
    difference = b - a
    if difference.length() > 0:
        direction = difference.normalize()
        return direction
    return Vector2(0, 0)

def load_sprite(name, with_alpha=True):
    filename = Path(__file__).parent / Path("assets/sprites/" + name + ".png")
    sprite = load(filename.resolve())

    if with_alpha:
        return sprite.convert_alpha()

    return sprite.convert()

