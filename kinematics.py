"""
Kinematics of a point object
"""

from math import sqrt
from utils import Vec2
import math


class ObjectKinematics:
    def __init__(self, position: Vec2, velocity: Vec2, mass: float = 0.0) -> None:
        self.position: Vec2 = position
        self.velocity: Vec2 = velocity
        self.acceleration: Vec2 = Vec2(0.0, 0.0)
        self.mass: float = mass

    def updateAcceleration(self, acceleration: Vec2) -> None:
        # Update Acceleration
        self.acceleration = acceleration

    def updatePosVel(self, dt: float) -> None:
        # Update Velocity
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

        self.direction = math.atan2(-self.velocity.y, self.velocity.x)
        self.directionDeg = math.degrees(self.direction)

    def __str__(self) -> str:
        result = f"ObjectKinematics(position={self.position},velocity={self.velocity},mass={self.mass})"
        return result
