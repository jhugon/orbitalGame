"""
SpaceObjects include planets and spacecraft
"""

import pygame  # type: ignore
from math import sqrt
from utils import load_image, Vec2
import math
from typing import Optional, List, Any

from kinematics import ObjectKinematics


class SpaceObjectModel:
    def __init__(self, position: Vec2, mass: float = 0.0) -> None:
        self.kinematics: ObjectKinematics = ObjectKinematics(position, Vec2(0.0, 0.0))
        self.maxThrust: float = 1.0e-1  #  m/s^2
        self.thrust: float = (
            0.0  # I think this really acts as -1 0 or 1, and is multiplied by maxThrust
        )
        self.thrustVec: Vec2 = Vec2(0.0, 0.0)
        self.mass: float = mass
        self.universe: Any = None

        self.burnSchedule: List[
            List[float]
        ] = []  # Each entry is a list [startTime,endTime,thrust]

    def update1(self, dt: float) -> None:
        currentPos = self.kinematics.getPosition()
        newA = self.universe.getA(currentPos)
        newA += self.thrustVec
        self.kinematics.updateAcceleration(newA)

        # Update Thrust Control
        self.thrust = 0.0
        for iEntry in reversed(list(range(len(self.burnSchedule)))):
            self.burnSchedule[iEntry][0] -= dt
            self.burnSchedule[iEntry][1] -= dt
            if self.burnSchedule[iEntry][1] <= 0.0:
                self.burnSchedule.pop(iEntry)
            elif self.burnSchedule[iEntry][0] <= 0.0:
                self.thrust = self.burnSchedule[iEntry][2]

    def update2(self, dt: float) -> None:
        self.kinematics.updatePosVel(dt)
        # Update Actual Thrust
        vNorm = Vec2(1.0, 0.0)  # in case velocity is 0.
        vMag = self.kinematics.getVelocity().magnitude()
        if vMag > 0.0:
            vNorm = self.kinematics.getVelocity().normalized()
        self.thrustVec = self.thrust * self.maxThrust * vNorm

    def scheduleBurn(self, startTime: float, endTime: float, thrustDirection: float):
        self.burnSchedule += [[startTime, endTime, thrustDirection]]

    def __str__(self) -> str:
        result = ""
        m = 0.0
        if self.mass != None:
            m = self.mass
        result = "SpaceObjectModel: m: {0:9.2e} {}\n"
        result = result.format(m, self.kinematics)
        for i in self.burnSchedule:
            result += "  burn start: {0:10.2e}s, end: {1:10.2e}s, direction: {2:5.2f}\n".format(
                *i
            )
        return result


class SpaceObjectView(pygame.sprite.Sprite):
    def __init__(self, img, scaleImg, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.objImage, self.objRect = load_image(img)
        self.objRect.w = self.objRect.w * scaleImg
        self.objRect.h = self.objRect.h * scaleImg
        self.objImage = pygame.transform.smoothscale(self.objImage, self.objRect.size)
        self.rect = pygame.Rect(self.objRect)
        self.rect.inflate_ip(self.objRect.w / 3, self.objRect.h / 3)
        self.rect.x = 0
        self.rect.y = 0
        self.objRect.centerx = self.rect.centerx
        self.objRect.centery = self.rect.centery
        self.image = pygame.Surface(self.rect.size).convert_alpha()
        self.image.fill((255, 255, 255, 0))
        self.image.blit(self.objImage, self.objRect)
        self.setXY(x, y)
        self.direction = 0.0
        self.directionDeg = 0.0
        self.thrust = 0.0
        self.thrustDrawn = False
        self.imageOrig = self.image.copy()
        self.selected = False
        self.universe = None

    def setUniverse(self, universe):
        self.universe = universe

    def setXY(self, x, y):
        self.oldRect = self.rect.copy()
        self.rect.center = x, y

    def getXY(self):
        return self.rect.center

    def select(self):
        self.selected = True
        self.universe.selected.add(self)
        self.image.fill((255, 255, 255, 255))
        innerRect = pygame.Rect(self.rect)
        innerRect.w = innerRect.w - 4
        innerRect.h = innerRect.h - 4
        innerRect.centerx = self.rect.w / 2
        innerRect.centery = self.rect.h / 2
        # innerRect.y = 0
        # innerRect.inflate(-innerRect.w/4,-innerRect.w/4)
        self.image.fill((255, 255, 255, 0), innerRect)
        self.image.blit(self.imageOrig, (0, 0))

    def drawDirection(self):
        arrowSize = (12, 12)
        arrowColor = (255, 200, 0, 255)
        w2 = arrowSize[0] / 2
        l2 = arrowSize[1] / 2
        rotation = self.directionDeg
        if self.thrust > 0.0:
            rotation += 180.0
        points = [
            Vec2(w2, l2),
            Vec2(w2, -l2),
            Vec2(-w2, 0),
        ]
        position = Vec2(self.rect.w / 2 - arrowSize[0] / 2, 0).rotated(rotation) + Vec2(
            self.rect.w / 2, self.rect.h / 2
        )
        for i in range(len(points)):
            points[i].rotate(rotation)
            points[i] += position
        points = [i.tuple() for i in points]
        pygame.draw.polygon(self.image, arrowColor, points)

    def deSelect(self):
        self.selected = False
        self.image = self.imageOrig.copy()

    def preUpdate(self):
        pass

    def update(self):
        if self.thrust != 0.0:
            self.image.fill((0, 0, 0, 0))
            self.image.blit(self.imageOrig, (0, 0))
            self.drawDirection()
            self.thrustDrawn = True
        elif self.thrustDrawn:
            self.image.fill((0, 0, 0, 0))
            self.image.blit(self.imageOrig, (0, 0))
            self.thrustDrawn = False


class SpaceObjectCtrl:
    def __init__(self, universe, img, scaleImg, x, y, mass=0.0):
        """
        x and y are in Model coords
        """
        self.universe = universe
        self.x = x
        self.y = y
        viewX, viewY = self.universe.convertCoordsModel2View(x, y)
        self.view = SpaceObjectView(img, scaleImg, viewX, viewY)
        self.model = SpaceObjectModel(Vec2(x, y), mass)
        self.universe.addObject(self)
        self.selected = False

    def updateViewToModel(self):
        viewX, viewY = self.universe.convertCoordsModel2View(
            *self.model.kinematics.getPosition().tuple()
        )
        self.view.setXY(viewX, viewY)
        self.view.direction = self.model.kinematics.getDirection()
        self.view.directionDeg = self.model.kinematics.getDirectionDeg()
        self.view.thrust = self.model.thrust

    def select(self):
        self.selected = True
        self.universe.selected += [self]
        self.view.select()

    def scheduleBurn(self, startTime, endTime, thrust):
        self.model.scheduleBurn(startTime, endTime, thrust)
        self.universe.showPaths()
