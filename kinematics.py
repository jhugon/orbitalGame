"""
Kinematics of a point object
"""

from math import sqrt
from utils import Vec2
import math


class ObjectKinematics:
    """
    2D kinematics for an object

    First updateAcceleration for all objects, and then updatePosVel
    with the new accelerations
    """

    def __init__(
        self, position: Vec2, velocity: Vec2, acceleration: Vec2 = Vec2(0.0, 0.0)
    ) -> None:
        self.position: Vec2 = position
        self.velocity: Vec2 = velocity
        self.acceleration: Vec2 = acceleration
        self._updateDirections()

    def getPosition(self) -> Vec2:
        """
        Object position
        """
        return self.position

    def getVelocity(self) -> Vec2:
        """
        Object velocity
        """
        return self.velocity

    def getAcceleration(self) -> Vec2:
        """
        Object acceleration
        """
        return self.acceleration

    def getDirection(self) -> float:
        """
        Velocity direction in radians
        """
        return self.direction

    def getDirectionDeg(self) -> float:
        """
        Velocity direction in degres
        """
        return self.directionDeg

    def updateAcceleration(self, acceleration: Vec2) -> None:
        """
        Updates acceleration
        """
        self.acceleration = acceleration

    def updatePosVel(self, dt: float) -> None:
        """
        Updates velocity using acceleration
        and position using the updated velocity
        """
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt
        self._updateDirections()

    def _updateDirections(self) -> None:
        """
        Updates direction and directionDeg from velocity
        """
        self.direction = math.atan2(-self.velocity.y, self.velocity.x)
        self.directionDeg = math.degrees(self.direction)

    def __str__(self) -> str:
        result = f"ObjectKinematics(position={self.position},velocity={self.velocity},acceleration={self.acceleration})"
        return result

    def __repr__(self) -> str:
        return str(self)
