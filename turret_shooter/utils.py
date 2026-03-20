# This file contains helper methods for the code
from pygame.image import load
from pygame.math import Vector2
from pathlib import Path

def load_sprite(name, with_alpha=True):
    filename = Path("turret_shooter/assets/sprites/" + name + ".png")
    sprite = load(filename.resolve())

    if with_alpha:
        return sprite.convert_alpha()

    return sprite.convert()

def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)