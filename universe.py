"""
Universe controlls all of the SpaceObjects
"""

import pygame  # type: ignore
from pygame.locals import *  # type: ignore
from math import sqrt
from copy import deepcopy
from typing import Optional, List, Any, Tuple, TYPE_CHECKING

from utils import Vec2
from futurepaths import FuturePathsView
from spaceobject import SpaceObjectModel, SpaceObjectCtrl, SpaceObjectView

if TYPE_CHECKING:
    from spaceobject import SpaceObjectModel, SpaceObjectView, SpaceObjectCtrl


class UniverseModel:
    def __init__(self, G: float = 6.67e-11, rPower: float = -2.0) -> None:
        """
        G is the gravitational constant
        rPower is the power of gravity, e.g. a = G*M*r^(rPower)
        """
        self.massiveObjects: List[SpaceObjectModel] = []
        self.masslessObjects: List[SpaceObjectModel] = []
        self.G: float = G
        self.rPower: float = rPower

    def addObject(self, obj: SpaceObjectModel) -> None:
        obj.universe = self
        if obj.mass > 0.0:
            self.massiveObjects += [obj]
        else:
            self.masslessObjects += [obj]

    def getA(self, position: Vec2) -> Vec2:
        acceleration = Vec2(0.0, 0.0)
        for mo in self.massiveObjects:
            rVec = mo.kinematics.getPosition() - position
            r = rVec.magnitude()
            if r < 0.001:
                continue
            accmagfrommo = self.G * mo.mass * r ** (self.rPower)
            accfrommo = accmagfrommo * rVec.normalized()
            acceleration += accfrommo
        return acceleration

    def update(self, dt: float) -> None:
        for obj in self.massiveObjects + self.masslessObjects:
            obj.update1(dt)
        for obj in self.massiveObjects + self.masslessObjects:
            obj.update2(dt)

    def __str__(self) -> str:
        result = ""
        for obj in self.massiveObjects + self.masslessObjects:
            result += str(obj)
        return result

    def getFuture(
        self,
        dtList: List[float],
        selectedObj: Optional[SpaceObjectModel] = None,
        dtStepSize: float = 1e2,
    ) -> Tuple[List[List[Vec2]], List[List[float]]]:
        """
        dtStepSize is in model seconds, just like dtList
        """
        futureUniverse = deepcopy(self)
        mlos = futureUniverse.masslessObjects
        if selectedObj is not None:
            foundSelected = False
            mlosNew: List[SpaceObjectModel] = []
            for obj in mlos:
                if obj.kinematics == selectedObj.kinematics:
                    selectedObj = obj
                    foundSelected = True
                    continue
                mlosNew += [obj]
            mlos = mlosNew
            if foundSelected:
                mlos.append(selectedObj)
                mlos.reverse()
            assert foundSelected

        futurePositionList: List[List[Vec2]] = [[] for i in mlos]
        futureBurnList: List[List[float]] = [[] for i in mlos]
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
                    pos = mlos[i].kinematics.getPosition()
                    futurePositionList[i] += [pos]
                    burn = 0.0
                    for burnTime in mlos[i].burnSchedule:
                        if burnTime[0] <= 0.0:
                            burn += burnTime[2]
                    futureBurnList[i] += [burn]
                iDt += 1
            dtTotal += dtStep
            if iDt >= len(dtList):
                break
        if selectedObj is None:
            print(f"Nothing Current Selected")
        else:
            print(f"Current Selected {selectedObj.kinematics}")
        return futurePositionList, futureBurnList


######################################################3


class UniverseView(pygame.Surface):
    def __init__(self, size: Tuple[int, int], backgroundImageLoc: str) -> None:
        """
        size is a tuple (x,y): the size of the layer (world) in pixels
        """
        self.screen = pygame.display.set_mode(size)
        pygame.Surface.__init__(self, size)
        self.fill((0, 0, 0))
        self.background: Optional[pygame.surface.Surface] = None
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

        self.objects: pygame.sprite.RenderUpdates = pygame.sprite.RenderUpdates()
        self.selected = pygame.sprite.Group()
        self.hudGroup = pygame.sprite.RenderUpdates()
        self.toUpdateRectsList: List[pygame.rect.Rect] = []

        self.updateAllFlag = False

    def addObject(self, obj: "SpaceObjectView") -> None:
        obj.setUniverse(self)
        self.objects.add(obj)

    def update(self) -> None:
        """
        Draw Everything
        """
        if self.background is None:
            raise ValueError("background has not been set")
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
            pygame.display.update(self.toUpdateRectsList)  # type: ignore
        self.toUpdateRectsList = []

    def deselectAll(self) -> None:
        for obj in self.objects:
            if not hasattr(obj, "deSelect"):
                raise TypeError(
                    "object isn't an instance of SpaceObjectView or otherwise doesn't have deSelect method"
                )
            obj.deSelect()  # type: ignore

    def showPaths(
        self,
        futurePaths: List[List[Tuple[int, int]]],
        futureBurns: List[List[float]],
        timePoints: Optional[List[float]] = None,
        selected: bool = False,
    ) -> None:
        pathsView = FuturePathsView(self)
        selectedBools = [False for i in range(len(futurePaths))]
        selectedBools[0] = selected
        for objPath, objBurns, selectedPathBool in reversed(
            list(zip(futurePaths, futureBurns, selectedBools))
        ):
            pathsView.addPath(selectedPathBool, objPath, objBurns, timePoints)


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

        self.model = UniverseModel()
        self.view = UniverseView(size, backgroundImageLoc)
        self.objects = []

        self.selected = []

        self.pauseModel = False
        self.selectedModeFlag = False

        self.selectedPathPointsView = None
        self.selectedPathTimes = None
        self.selectedBurnStartIndex = None

    def addObject(self, obj):
        self.objects += [obj]
        self.model.addObject(obj.model)
        self.view.addObject(obj.view)

    def convertCoordsModel2View(self, x: float, y: float) -> Tuple[int, int]:
        return (
            int(x // self.meterPerPixel + self.viewSize[0] // 2),
            int(-y // self.meterPerPixel + self.viewSize[1] // 2),
        )

    def convertCoordsView2Model(self, x: int, y: int) -> Tuple[float, float]:
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
        self.selectedPathPointsView = None
        self.selectedPathTimes = None
        self.selectedBurnStartIndex = None

    def showPaths(self) -> None:
        self.view.hudGroup.empty()
        timePoints = [i * 1e3 for i in range(30)]
        selectedModel = self.selected[0].model
        if selectedModel == None or selectedModel.mass > 0.0:
            selectedModel = None
        futurePaths, futureBurns = self.model.getFuture(
            timePoints, selectedObj=selectedModel
        )
        futurePathsView: List[List[Tuple[int, int]]] = []
        for path in futurePaths:
            pathView: List[Tuple[int, int]] = []
            for p in path:
                pView = self.convertCoordsModel2View(*(p.tuple()))
                pathView += [pView]
            futurePathsView += [pathView]
        selected = True
        if selectedModel == None or selectedModel.mass > 0.0:
            selected = False
        self.view.showPaths(futurePathsView, futureBurns, timePoints, selected=selected)

        if selectedModel != None and selectedModel.mass == 0.0:
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
