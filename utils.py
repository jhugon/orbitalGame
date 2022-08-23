import pygame  # type: ignore
import math
from math import sqrt
import os.path

main_dir = os.path.split(os.path.abspath(__file__))[0]
sprites_dir = os.path.join(main_dir, "sprites")


def load_image(name, colorkey=None):
    # fullname = os.path.join(sprites_dir, name)
    fullname = name
    try:
        image = pygame.image.load(fullname)
    except pygame.error as e:
        print(("Cannot load image:", fullname))
        raise SystemExit(e)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, angleDeg):
        angle = math.radians(angleDeg)
        x = self.x
        y = self.y
        self.x = x * math.cos(angle) - y * math.sin(angle)
        self.y = x * math.sin(angle) + y * math.cos(angle)

    def translate(self, x, y):
        self.x += x
        self.y += y

    def scale(self, f):
        self.x *= f
        self.y *= f

    def tup(self):
        return self.x, self.y

    def __tuple__(self):
        return self.tup()
