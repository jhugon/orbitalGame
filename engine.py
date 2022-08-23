#!/usr/bin/python

# This code is so you can run the samples without installing the package

# Import Modules
import os
import os.path
import math
from math import sqrt
from copy import deepcopy
import pygame
from pygame.locals import *

if not pygame.font:
    print("Warning, fonts disabled")
if not pygame.mixer:
    print("Warning, sound disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]
sprites_dir = os.path.join(main_dir, "sprites")

######################################################


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


######################################################


class SpaceObjectModel:
    def __init__(self, x, y, mass=0.0):
        self.x = x  # Position
        self.y = y  # Position
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0
        self.maxThrust = 1.0e-1  #  m/s^2
        self.thrust = 0.0
        self.tx = 0.0  #  m/s^2
        self.ty = 0.0  #  m/s^2
        self.m = mass
        self.universe = None

        self.burnSchedule = []  # Each entry is a list [startTime,endTime,thrust]

    def update1(self, dt):
        obj = self
        # Update Acceleration
        obj.ax, obj.ay = self.universe.getA(obj.x, obj.y)
        obj.ax += obj.tx
        obj.ay += obj.ty

        # Update Thrust Control
        self.thrust = 0.0
        for iEntry in reversed(list(range(len(self.burnSchedule)))):
            self.burnSchedule[iEntry][0] -= dt
            self.burnSchedule[iEntry][1] -= dt
            if self.burnSchedule[iEntry][1] <= 0.0:
                self.burnSchedule.pop(iEntry)
            elif self.burnSchedule[iEntry][0] <= 0.0:
                self.thrust = self.burnSchedule[iEntry][2]

    def update2(self, dt):
        obj = self
        # Update Velocity
        obj.vx += obj.ax * dt
        obj.vy += obj.ay * dt

        # Update Position
        obj.x += obj.vx * dt
        obj.y += obj.vy * dt
        # print obj.x, obj.y

        # Update Actual Thrust
        v = sqrt(obj.vx**2 + obj.vy**2)
        vxNorm = 1.0
        vyNorm = 0.0
        if v > 0.0:
            vxNorm = obj.vx / v
            vyNorm = obj.vy / v
        obj.tx = obj.thrust * vxNorm * obj.maxThrust
        obj.ty = obj.thrust * vyNorm * obj.maxThrust

    def scheduleBurn(self, startTime, endTime, thrustDirection):
        self.burnSchedule += [[startTime, endTime, thrustDirection]]

    def __str__(self):
        result = ""
        m = 0.0
        if self.m != None:
            m = self.m
        result = "m: {0:9.2e} p: ({1:9.2e},{2:9.2e}) v: ({3:9.2e},{4:9.2e}) a: ({5:9.2e},{6:9.2e})\n"
        result = result.format(m, self.x, self.y, self.vx, self.vy, self.ax, self.ay)
        for i in self.burnSchedule:
            result += "  burn start: {0:10.2e}s, end: {1:10.2e}s, direction: {2:5.2f}\n".format(
                *i
            )
        return result


class UniverseModel:
    def __init__(self, size, G=6.67e-11, rPower=-2.0):
        """
        size is the size of the universe in model units (meters)
        G is the gravitational constant
        rPower is the power of gravity, e.g. a = G*M*r^(rPower)
        """
        self.size = size
        self.massiveObjects = []
        self.masslessObjects = []
        self.G = G
        self.rPower = rPower

    def addObject(self, obj):
        obj.universe = self
        if obj.m > 0.0:
            self.massiveObjects += [obj]
        else:
            self.masslessObjects += [obj]

    def getA(self, x, y):
        ax = 0.0
        ay = 0.0
        for mo in self.massiveObjects:
            dx = mo.x - x
            dy = mo.y - y
            rSqr = dx**2 + dy**2
            r = sqrt(rSqr)
            if r < 0.001:
                continue
            a = self.G * mo.m * r ** (self.rPower)
            # print("mo.x: {:9.2e} mo.y: {:9.2e} x: {:9.2e} y: {:9.2e}".format(mo.x,mo.y,x,y))
            # print("r: {:9.2e} rSqr: {:9.2e} dx: {:9.2e} dy: {:9.2e}".format(r,rSqr,dx,dy))
            # print("a: {:9.2e} ax: {:9.2e} ay: {:9.2e} ".format(a,a*dx/r,a*dy/r))
            # print("G: {:9.2e} rPower: {:9.2e} mo.m: {:9.2}".format(self.G,self.rPower,mo.m))
            # print("2**(self.rPower): {:9.2e}".format(2.**(self.rPower)))
            ax += a * dx / r
            ay += a * dy / r
        return ax, ay

    def update(self, dt):
        for obj in self.massiveObjects + self.masslessObjects:
            obj.update1(dt)
        for obj in self.massiveObjects + self.masslessObjects:
            obj.update2(dt)

    def __str__(self):
        result = ""
        for obj in self.massiveObjects + self.masslessObjects:
            result += str(obj)
        return result

    def getFuture(self, dtList, selectedObj=None, dtStepSize=1e2):  # in seconds
        futureUniverse = deepcopy(self)
        mlos = futureUniverse.masslessObjects
        if selectedObj != None:
            foundSelected = False
            mlosNew = []
            for obj in mlos:
                if obj.x == selectedObj.x and obj.y == selectedObj.y:
                    if obj.vx == selectedObj.vx and obj.vy == selectedObj.vy:
                        selectedObj = obj
                        foundSelected = True
                        continue
                mlosNew += [obj]
            mlos = mlosNew
            if foundSelected:
                mlos.append(selectedObj)
                mlos.reverse()
            assert foundSelected

        futurePositionList = [[] for i in mlos]
        futureBurnList = [[] for i in mlos]
        iDt = 0
        dtTotal = 0.0
        while True:
            dt = dtList[iDt]
            dtStep = dtStepSize
            recordThisStep = False
            if dt - dtTotal < dtStepSize:
                dtStep = dt - dtTotal
                recordThisStep = True
            futureUniverse.update(dtStep)
            if recordThisStep:
                for i in range(len(mlos)):
                    x = mlos[i].x
                    y = mlos[i].y
                    futurePositionList[i] += [[x, y]]
                    burn = 0.0
                    for burnTime in mlos[i].burnSchedule:
                        if burnTime[0] <= 0.0:
                            burn += burnTime[2]
                    futureBurnList[i] += [burn]
                iDt += 1
            dtTotal += dtStep
            if iDt >= len(dtList):
                break
        print(("Current Selected x,y: %6.2e %6.2e" % (selectedObj.x, selectedObj.y)))
        print("Future Pos List: ")
        print(futurePositionList)
        for path in futurePositionList:
            print("  Path")
            for pos in path:
                print(("   {0:6.2e} {1:6.2e}".format(*pos)))
        return futurePositionList, futureBurnList


######################################################3


class UniverseView(pygame.Surface):
    def __init__(self, size, backgroundImageLoc):
        """
        size is a tuple (x,y): the size of the layer (world) in pixels
        """
        self.screen = pygame.display.set_mode(size)
        pygame.Surface.__init__(self, size)
        self.fill((0, 0, 0))
        self.background = None
        if backgroundImageLoc == None:
            self.background = pygame.Surface(size)
            self.background.fill((0, 0, 0))
        else:
            try:
                self.background = pygame.image.load(backgroundImageLoc)
            except pygame.error as e:
                print(("Cannot load background image:", backgroundImageLoc))
                raise SystemExit(e)
            self.background = self.background.convert()
            self.background = pygame.transform.smoothscale(self.background, size)
            self.blit(self.background, (0, 0))
        self.size = size

        pygame.display.set_caption("Orbital Game")
        self.screen.blit(self, (0, 0))
        pygame.display.update()

        self.objects = pygame.sprite.RenderUpdates()
        self.selected = pygame.sprite.Group()
        self.hudGroup = pygame.sprite.RenderUpdates()
        self.toUpdateRectsList = []

        self.updateAllFlag = False

    def addObject(self, obj):
        obj.setUniverse(self)
        self.objects.add(obj)

    def update(self):
        # Draw Everything
        if self.updateAllFlag:
            self.blit(self.background, (0, 0))
        self.screen.blit(self, (0, 0))
        self.objects.update()
        self.toUpdateRectsList += self.objects.draw(self.screen)
        self.toUpdateRectsList += self.hudGroup.draw(self.screen)

        if self.updateAllFlag:
            pygame.display.update()
            self.updateAllFlag = False
        else:
            pygame.display.update(self.toUpdateRectsList)
        self.toUpdateRectsList = []

    def preUpdate(self):
        for obj in self.selected:
            obj.preUpdate()

    def deselectAll(self):
        for obj in self.objects:
            obj.deSelect()

    def showPaths(self, futurePaths, futureBurns, timePoints=None, selected=False):
        pathsView = FuturePathsView(self)
        selectedBools = [False for i in range(len(futurePaths))]
        selectedBools[0] = selected
        for objPath, objBurns, selectedPathBool in reversed(
            list(zip(futurePaths, futureBurns, selectedBools))
        ):
            pathsView.addPath(selectedPathBool, objPath, objBurns, timePoints)


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
        position = Vec2(self.rect.w / 2 - arrowSize[0] / 2, 0)
        position.rotate(rotation)
        position.translate(self.rect.w / 2, self.rect.h / 2)
        for i in range(len(points)):
            points[i].rotate(rotation)
            points[i].translate(position.x, position.y)
        points = [i.tup() for i in points]
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


class FuturePathsView(pygame.sprite.Sprite):
    def __init__(self, universeView):
        pygame.sprite.Sprite.__init__(self)
        self.universe = universeView
        self.image = pygame.Surface(self.universe.size).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = pygame.Rect((0, 0), self.universe.size)
        self.universe.hudGroup.add(self)

        self.pathSelectedStyle = {
            "color": (255, 255, 0, 255),
            "textcolor": (0, 0, 0, 255),
            "textbakcolor": (0, 255, 0, 255),
            "width": 2,
            "textsize": 24,
            "showTimes": False,
            "arrowWidth": 8,
            "arrowLength": 8,
            "arrowColor": (255, 255, 0, 255),
        }
        self.pathStyle = {
            "color": (255, 255, 255, 100),
            "textcolor": (0, 0, 0, 100),
            "textbakcolor": (255, 255, 255, 100),
            "width": 1,
            "textsize": 24,
            "showTimes": False,
            "arrowWidth": 8,
            "arrowLength": 8,
            "arrowColor": (255, 255, 255, 100),
        }

        self.font = None
        self.selectedFont = None
        if pygame.font:
            self.font = pygame.font.Font(None, self.pathStyle["textsize"])
            self.selectedFont = pygame.font.Font(
                None, self.pathSelectedStyle["textsize"]
            )
        maxArrowAxis = max(
            self.pathSelectedStyle["arrowLength"], self.pathSelectedStyle["arrowWidth"]
        )
        maxArrowAxis = max(maxArrowAxis, self.pathStyle["arrowLength"])
        maxArrowAxis = max(maxArrowAxis, self.pathStyle["arrowWidth"])
        maxArrowAxis = int(1.4 * maxArrowAxis)
        self.arrowImgSize = (maxArrowAxis, maxArrowAxis)
        self.arrowRect = pygame.Rect((0, 0), self.arrowImgSize)
        self.arrowImgSelected = pygame.Surface(self.arrowImgSize).convert_alpha()
        self.arrowImg = pygame.Surface(self.arrowImgSize).convert_alpha()
        self.arrowImgSelected.fill((0, 0, 0, 0))
        self.arrowImg.fill((0, 0, 0, 0))
        x = self.arrowRect.centerx
        y = self.arrowRect.centery
        w2 = self.pathStyle["arrowWidth"] / 2
        l2 = self.pathStyle["arrowLength"] / 2
        pygame.draw.polygon(
            self.arrowImg,
            self.pathStyle["arrowColor"],
            [
                [x - w2, y + l2],
                [x + w2, y + l2],
                [x, y - l2],
            ],
        )
        w2 = self.pathSelectedStyle["arrowWidth"] / 2
        l2 = self.pathSelectedStyle["arrowLength"] / 2
        pygame.draw.polygon(
            self.arrowImgSelected,
            self.pathSelectedStyle["arrowColor"],
            [
                [x - w2, y + l2],
                [x + w2, y + l2],
                [x, y - l2],
            ],
        )

    def addPath(self, selected, pointList, burnList, timeList=None):
        style = self.pathStyle
        font = None
        if selected:
            style = self.pathSelectedStyle
        if self.font != None:
            if selected:
                font = self.selectedFont
            else:
                font = self.font
        color = style["color"]
        textcolor = style["textcolor"]
        textbakcolor = style["textbakcolor"]
        width = style["width"]
        showTimes = style["showTimes"]
        pygame.draw.lines(self.image, color, False, pointList, width)
        for i in range(0, len(burnList) - 1):
            if burnList[i] == 0.0:
                continue
            burn = burnList[i]
            point = pointList[i]
            dy = pointList[i + 1][1] - point[1]
            dx = pointList[i + 1][0] - point[0]
            rotation = math.degrees(math.atan2(-dy, dx))
            rotation -= 90.0
            if burn < 0:
                rotation += 180.0

            imgToBlit = self.arrowImg
            if selected:
                imgToBlit = self.arrowImgSelected
            imgToBlit = pygame.transform.rotate(imgToBlit, rotation)
            point[0] -= style["arrowWidth"] / 2
            point[1] -= style["arrowLength"] / 2
            self.image.blit(imgToBlit, point)

        if not showTimes:
            return
        if timeList != None and font != None:
            iTime = -1
            pointList = pointList[4:]
            timeList = timeList[4:]
            for pos, time in reversed(list(zip(pointList, timeList))):
                iTime += 1
                if iTime % 5 != 0:
                    continue
                origTime = time
                append = "s"
                if time > 120.0:
                    time = time / 60.0
                    append = "m"
                if time > 120.0 and append == "m":
                    time = time / 60.0
                    append = "h"
                if time > 48.0 and append == "h":
                    time = time / 24.0
                    append = "d"
                if time > 60.0 and append == "d":
                    time = time / 30.0
                    append = "Mo"
                if time > 23.0 and append == "Mo":
                    time = time / 12.0
                    append = "y"

                timeString = "{0:.0f}".format(time) + append
                textSurf = font.render(timeString, True, textcolor)  # ,textbakcolor)
                textSurf = textSurf.convert_alpha()
                textpos = textSurf.get_rect()
                textBakSurf = pygame.Surface((textpos[2], textpos[3])).convert_alpha()
                textBakSurf.fill(textbakcolor)
                textBakSurf.blit(textSurf, (0, 0))
                textpos.center = pos
                self.image.blit(textBakSurf, textpos)


######################################################3


class UniverseCtrl:
    def __init__(self, size, backgroundImageLoc, debug=False):
        """
        size is a tuple (x,y): the size of the layer (world) in pixels
        """
        self.viewSize = size
        self.debug = debug
        modelSize = 3.5e7 * 3.0
        # self.meterPerPixel = 1e10
        self.meterPerPixel = modelSize / self.viewSize[1]
        self.speedUpFactor = 5e3
        self.updateModelEvery = 1e2  # seconds of model time
        self.dRClickPath = 25.0

        convertCoordsModel2View = getattr(self, "convertCoordsModel2View")
        convertCoordsView2Model = getattr(self, "convertCoordsView2Model")

        self.model = UniverseModel(convertCoordsView2Model(*size))
        self.view = UniverseView(size, backgroundImageLoc)
        self.objects = []

        self.selected = []

        self.pauseModel = False
        self.selectedModeFlag = False

        self.selectedPathPoints = None
        self.selectedPathPointsView = None
        self.selectedPathTimes = None
        self.selectedBurnStartIndex = None

    def addObject(self, obj):
        self.objects += [obj]
        self.model.addObject(obj.model)
        self.view.addObject(obj.view)

    def convertCoordsModel2View(self, x, y):
        return (
            x / self.meterPerPixel + self.viewSize[0] / 2,
            -y / self.meterPerPixel + self.viewSize[1] / 2,
        )

    def convertCoordsView2Model(self, x, y):
        return (x - self.viewSize[0] / 2) * self.meterPerPixel, (
            y - self.viewSize[1] / 2
        ) * self.meterPerPixel

    def updateViewToModel(self):
        for obj in self.objects:
            obj.updateViewToModel()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        counter = 0.0
        while running:
            clock.tick(60)
            dt = clock.get_time() / 1000.0  # Convert from ms to s
            counter += dt
            if counter > 2.0:
                if self.debug:
                    print(("fps: {0}".format(clock.get_fps())))
                    print((self.model))
                counter = 0.0

            self.view.preUpdate()

            # Handle Input Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False

                elif event.type == KEYDOWN and event.key == K_UP:
                    for obj in self.selected:
                        obj.model.thrust = 1.0
                elif event.type == KEYDOWN and event.key == K_DOWN:
                    for obj in self.selected:
                        obj.model.thrust = -1.0
                elif event.type == KEYUP and (event.key == K_UP or event.key == K_DOWN):
                    for obj in self.objects:
                        obj.model.thrust = 0.0
                elif event.type == MOUSEBUTTONDOWN and event.dict["button"] == 1:
                    mousePosition = event.dict["pos"]
                    clickedObjects = self.findObjectsAtPoint(mousePosition)
                    nClickedObjects = len(clickedObjects)
                    if nClickedObjects == 1:
                        self.selectedMode(clickedObjects[0])
                    elif self.selectedModeFlag:
                        startIndex = self.isCloseToFuturePath(mousePosition)
                        if startIndex != None:
                            self.selectedBurnStartIndex = startIndex
                        else:
                            self.deSelectedMode()
                    elif nClickedObjects == 0.0:
                        self.deSelectedMode()
                elif event.type == MOUSEBUTTONUP:
                    mousePosition = event.dict["pos"]
                    if self.selectedModeFlag and self.selectedBurnStartIndex != None:
                        endIndex = self.isCloseToFuturePath(mousePosition)
                        if endIndex != None and endIndex != self.selectedBurnStartIndex:
                            burnStartT = self.selectedPathTimes[
                                self.selectedBurnStartIndex
                            ]
                            burnEndT = self.selectedPathTimes[endIndex]
                            if burnEndT > burnStartT:
                                self.selected[0].scheduleBurn(burnStartT, burnEndT, 1.0)
                            if burnEndT < burnStartT:
                                self.selected[0].scheduleBurn(
                                    burnEndT, burnStartT, -1.0
                                )
                        else:
                            self.selectedBurnStartIndex = None

            # Update Model
            if not self.pauseModel:
                dtModel = dt * self.speedUpFactor
                nModelUpdates = int(dtModel / self.updateModelEvery)
                dtRemainder = dtModel % self.updateModelEvery
                for i in range(nModelUpdates):
                    self.model.update(self.updateModelEvery)
                self.model.update(dtRemainder)
            # Update View to model
            self.updateViewToModel()

            # Update View
            self.view.update()

        ## End of event loop
        pygame.quit()

    def findObjectsAtPoint(self, point):
        result = []
        for obj in self.objects:
            if obj.view.rect.collidepoint(*point):
                result += [obj]
        return result

    def selectedMode(self, selectedObject):
        self.deSelectedMode()
        selectedObject.select()
        self.pauseModel = True
        self.selectedModeFlag = True
        self.showPaths()

    def deSelectedMode(self):
        self.pauseModel = False
        self.selectedModeFlag = False
        for obj in self.objects:
            obj.selected = False
        self.view.deselectAll()
        self.view.hudGroup.empty()
        self.selected = []
        self.selectedPathPoints = None
        self.selectedPathPointsView = None
        self.selectedPathTimes = None
        self.selectedBurnStartIndex = None

    def showPaths(self):
        self.view.hudGroup.empty()
        timePoints = [i * 1e3 for i in range(30)]
        selectedModel = self.selected[0].model
        if selectedModel == None or selectedModel.m > 0.0:
            selectedModel = None
        futurePaths, futureBurns = self.model.getFuture(
            timePoints, selectedObj=selectedModel
        )
        futurePathsView = []
        for path in futurePaths:
            pathView = []
            for p in path:
                pView = self.convertCoordsModel2View(*p)
                pView = [int(i) for i in pView]
                pathView += [pView]
            futurePathsView += [pathView]
        selected = True
        if selectedModel == None or selectedModel.m > 0.0:
            selected = False
        self.view.showPaths(futurePathsView, futureBurns, timePoints, selected=selected)

        if selectedModel != None and selectedModel.m == 0.0:
            self.selectedPathPoints = futurePaths[0]
            self.selectedPathPointsView = futurePathsView[0]
            self.selectedPathTimes = timePoints

    def isCloseToFuturePath(self, pos):
        if self.selectedPathPointsView == None:
            return None
        drMax2 = self.dRClickPath**2
        x, y = pos
        dR2List = [
            (xS - x) ** 2 + (yS - y) ** 2 for xS, yS in self.selectedPathPointsView
        ]
        minR2 = min(dR2List)
        result = minR2 < drMax2
        if not result:
            return None
        # print("minR: {0:.1f}, result: {1}".format(sqrt(minR2),result))
        iMinR2 = dR2List.index(minR2)
        return iMinR2


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
        self.model = SpaceObjectModel(x, y, mass)
        self.universe.addObject(self)
        self.selected = False

    def updateViewToModel(self):
        viewX, viewY = self.universe.convertCoordsModel2View(self.model.x, self.model.y)
        self.view.setXY(viewX, viewY)
        self.view.direction = math.atan2(-self.model.vy, self.model.vx)
        self.view.directionDeg = math.degrees(self.view.direction)
        self.view.thrust = self.model.thrust

    def select(self):
        self.selected = True
        self.universe.selected += [self]
        self.view.select()

    def scheduleBurn(self, startTime, endTime, thrust):
        self.model.scheduleBurn(startTime, endTime, thrust)
        self.universe.showPaths()


#######################################################################


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
