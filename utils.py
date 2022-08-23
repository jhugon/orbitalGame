import pygame  # type: ignore
import math
from math import sqrt
import os.path
from typing import Dict, Tuple, Optional

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
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


class Vec2:
    """
    2D vector class useful for kinematics and geometry
    """

    ## coordinate storage
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        """
        x and y are the coordinates
        """
        self.x = x
        self.y = y

    def distance(self, other: "Vec2") -> float:
        """
        Distance between other and self
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt(dx**2 + dy**2)

    def isClose(self, other: "Vec2", distance: float) -> bool:
        """
        Is other within distance of self?
        """
        d = self.distance(other)
        return d <= distance

    def rotate(self, angleDeg: float) -> None:
        """
        rotate this instance
        """
        angle = math.radians(angleDeg)
        x = self.x
        y = self.y
        self.x = x * math.cos(angle) - y * math.sin(angle)
        self.y = x * math.sin(angle) + y * math.cos(angle)

    def rotated(self, angleDeg: float) -> "Vec2":
        """
        return a new rotated version of this instance
        """
        result = Vec2(self.x, self.y)
        result.rotate(angleDeg)
        return result

    def tuple(self) -> Tuple[float, float]:
        """
        return vector as a tuple of floats (x,y)
        """
        return self.x, self.y

    def magnitude(self) -> float:
        """
        return sqrt(x**2+y**2)
        """
        return sqrt(self.x**2 + self.y**2)

    def normalize(self) -> None:
        """
        normalizes this vector i.e. makes it's magnitude one
        """
        mag = self.magnitude()
        self.x /= mag
        self.y /= mag

    def normalized(self) -> "Vec2":
        """
        returns a normalized version of this vector
            i.e. same direction but magnitude one
        """
        result = Vec2(self.x, self.y)
        result.normalize()
        return result

    def __add__(self, other: "Vec2") -> "Vec2":
        """
        Vector addition == translation
        """
        return Vec2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: "Vec2") -> "Vec2":
        """
        Vector addition == translation
        In-place
        """
        self.x += other.x
        self.y += other.y
        return self

    def __mul__(self, sf: float) -> "Vec2":
        """
        Return this vector scaled by scale factor sf
        """
        return Vec2(self.x * sf, self.y * sf)

    def __rmul__(self, sf: float) -> "Vec2":
        """
        Return this vector scaled by scale factor sf
        """
        return self * sf

    def __imul__(self, sf: float) -> "Vec2":
        """
        Scale this vector by scale factor sf
        """
        self.x *= sf
        self.y *= sf
        return self

    def __eq__(self, other) -> bool:
        """
        Equality of underlying coordinates
        """
        # return (self.x - other.x) < 1e-9 and (self.y - other.y) < 1e-9
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self) -> str:
        return f"Vec2({self.x},{self.y})"

    def __repr__(self) -> str:
        return str(self)
