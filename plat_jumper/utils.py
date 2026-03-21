from pygame.image import load
from pygame.mixer import Sound
from pathlib import Path


def load_image(name, with_alpha=True):
    filename = Path(__file__).parent / Path("assets/images/" + name + ".png")
    sprite = load(filename.resolve())
    if with_alpha:
        return sprite.convert_alpha()
    return sprite.convert()

def load_sound(name):
    filename = Path(__file__).parent / Path("assets/sounds/" + name + ".wav")
    return Sound(filename)