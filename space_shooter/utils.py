# This file contains helper methods for the code
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame import Color
from pathlib import Path

def load_sprite(name, with_alpha=True):
    filename = Path(__file__).parent / Path("assets/sprites/" + name + ".png")
    sprite = load(filename.resolve())

    if with_alpha:
        return sprite.convert_alpha()

    return sprite.convert()

def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)

def load_sound(name):
    filename = Path(__file__).parent / Path("assets/sounds/" + name + ".wav")
    return Sound(filename)

def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = surface.get_rect().center
    surface.blit(text_surface, text_rect)