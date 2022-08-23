#!/usr/bin/python

from math import sqrt
import pygame  # type: ignore

# from pygame.locals import *  # type: ignore


class SpaceApplication:
    def __init__(self):
        pygame.init()
        windowsize = (800, 600)
        backgroundImageLoc = (
            "backgroundExt/night-sky-milky-way-galaxy-astrophotography_0p25.jpg"
        )
        universe = UniverseCtrl(windowsize, backgroundImageLoc)

        mEarth = 6.0e24  # kg
        rVehicle = 3.5e7  # meters
        G = 6.67e-11  # in mks
        vVehicle = sqrt(G * mEarth / rVehicle)  # For circular orbit
        earth = SpaceObjectCtrl(universe, "sprites/planet3.png", 0.5, 0.0, 0.0, mEarth)
        vehicle = SpaceObjectCtrl(
            universe, "sprites/FighterLaser_springgreen.png", 1.0, rVehicle, 0.0
        )
        vehicle2 = SpaceObjectCtrl(
            universe, "sprites/SatelliteBase16_red.png", 1.0, 0.0, rVehicle
        )
        vehicle3 = SpaceObjectCtrl(
            universe, "sprites/FrigateMissile_cyan.png", 1.0, 0.0, -rVehicle
        )
        vehicle.model.vy = vVehicle
        vehicle2.model.vx = vVehicle
        vehicle3.model.vx = -vVehicle

        universe.run()


if __name__ == "__main__":
    sa = SpaceApplication()
