from pygame.image import load
from pathlib import Path


def load_image(name, with_alpha=True):
    filename = Path(__file__).parent / Path("assets/images/" + name + ".png")
    sprite = load(filename.resolve())
    if with_alpha:
        return sprite.convert_alpha()
    return sprite.convert()