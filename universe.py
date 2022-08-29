"""
Universe controls all of the SpaceObjects
"""

import pygame  # type: ignore
from pygame.locals import QUIT, KEYUP, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN  # type: ignore
from math import sqrt
from copy import deepcopy
from typing import Optional, List, Any, Tuple, TYPE_CHECKING

from utils import Vec2
from futurepaths import FuturePathsView
from spaceobject import SpaceObjectModel, SpaceObjectCtrl, SpaceObjectView
from ui import MainWindow

if TYPE_CHECKING:
    from spaceobject import SpaceObjectModel, SpaceObjectView, SpaceObjectCtrl


class UniverseModel:
    """
    Models the dynamics of the universe of SpaceObjectModels
    """

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
        """
        Get the gravitational acceleration at a point in space
        """
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
        """
        Update all of the objects' acceleration, velocity, position, and thrusts
        """
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
        Get the future positions and thrusts of all massless objects in the universe

        dtStepSize is in model seconds, just like dtList
        """
        futureUniverse, mlos = self.copyUniverse(selectedObj)

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
        return futurePositionList, futureBurnList

    def copyUniverse(
        self, selectedObj: Optional["SpaceObjectModel"] = None
    ) -> Tuple["UniverseModel", List[SpaceObjectModel]]:
        """
        Make a copy of this universe and also return a list of its massless objects.
        If selectedObj is not None, then make sure it is first in the list
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
        return futureUniverse, mlos


######################################################3


class UniverseView:
    def __init__(self, window: "MainWindow") -> None:
        self.window = window
        self.objects: pygame.sprite.RenderUpdates = pygame.sprite.RenderUpdates()
        self.selected = pygame.sprite.Group()
        self.hudGroup = pygame.sprite.RenderUpdates()
        self.toUpdateRectsList: List[pygame.rect.Rect] = []

    def addObject(self, obj: "SpaceObjectView") -> None:
        obj.setUniverse(self)
        self.objects.add(obj)

    def update(self) -> None:
        """
        Update everything
        """
        self.objects.update()
        self.toUpdateRectsList += self.objects.draw(self.window.screen)
        self.toUpdateRectsList += self.hudGroup.draw(self.window.screen)

        pygame.display.update(self.toUpdateRectsList)  # type: ignore
        self.toUpdateRectsList = []

    def deselectAll(self) -> None:
        """
        Make sure no objects are selected
        """
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
        """
        Draw the future paths, highlighting the first entry in the list, if selected is True
        """
        pathsView = FuturePathsView(self)
        selectedBools = [False for i in range(len(futurePaths))]
        selectedBools[0] = selected
        for objPath, objBurns, selectedPathBool in reversed(
            list(zip(futurePaths, futureBurns, selectedBools))
        ):
            pathsView.addPath(selectedPathBool, objPath, objBurns, timePoints)


######################################################3


class UniverseCtrl:
    def __init__(
        self, size: Tuple[int, int], backgroundImageLoc: str, debug: bool = False
    ) -> None:
        """
        Controls the program

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

        self.mainwindow = MainWindow(size, backgroundImageLoc)
        self.model = UniverseModel()
        self.view = UniverseView(self.mainwindow)
        self.objects: List[SpaceObjectCtrl] = []

        self.selected: List[SpaceObjectCtrl] = []

        self.pauseModel = False
        self.selectedModeFlag = False

        self.selectedPathPointsView: Optional[List[Tuple[int, int]]] = None
        self.selectedPathTimes: Optional[List[float]] = None
        self.selectedBurnStartIndex: Optional[int] = None

    def addObject(self, obj: "SpaceObjectCtrl") -> None:
        self.objects += [obj]
        self.model.addObject(obj.model)
        self.view.addObject(obj.view)

    def convertCoordsModel2View(self, x: float, y: float) -> Tuple[int, int]:
        """
        Convert from model/dynamics coordinates to view/screen/window coordinates
        """
        return (
            int(x // self.meterPerPixel + self.viewSize[0] // 2),
            int(-y // self.meterPerPixel + self.viewSize[1] // 2),
        )

    def convertCoordsView2Model(self, x: int, y: int) -> Tuple[float, float]:
        """
        Convert from view/screen/window coordinates to model/dynamics coordinates
        """
        return (x - self.viewSize[0] / 2) * self.meterPerPixel, (
            y - self.viewSize[1] / 2
        ) * self.meterPerPixel

    def updateViewToModel(self) -> None:
        """
        Make sure the view/screen/window matches the model/dynamics
        """
        for obj in self.objects:
            obj.updateViewToModel()

    def run(self) -> None:
        """
        Start the game
        """
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
                running = running and self.handleUIEvents(event)

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
            self.mainwindow.update()
            self.view.update()

        ## End of event loop
        pygame.quit()

    def handleUIEvents(self, event: pygame.event.Event) -> bool:
        running = True
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
            self.handleMouseButtonDownEvent(event)
        elif event.type == MOUSEBUTTONUP:
            self.handleMouseButtonUpEvent(event)
        return running

    def handleMouseButtonDownEvent(self, event: pygame.event.Event) -> None:
        assert event.type == MOUSEBUTTONDOWN and event.dict["button"] == 1
        mousePosition = event.dict["pos"]
        clickedObjects = self.findObjectsAtPoint(mousePosition)
        nClickedObjects = len(clickedObjects)
        if nClickedObjects == 1:
            self.selectObject(clickedObjects[0])
        elif self.selectedModeFlag:
            startIndex = self.isCloseToFuturePath(mousePosition)
            if startIndex is not None:
                self.selectedBurnStartIndex = startIndex
            else:
                self.deselectAll()
        elif nClickedObjects == 0:
            self.deselectAll()

    def handleMouseButtonUpEvent(self, event: pygame.event.Event) -> None:
        assert event.type == MOUSEBUTTONUP
        mousePosition = event.dict["pos"]
        if (
            self.selectedModeFlag
            and self.selectedBurnStartIndex is not None
            and self.selectedPathTimes is not None
        ):
            endIndex = self.isCloseToFuturePath(mousePosition)
            if endIndex is not None and endIndex != self.selectedBurnStartIndex:
                burnStartT = self.selectedPathTimes[self.selectedBurnStartIndex]
                burnEndT = self.selectedPathTimes[endIndex]
                if burnEndT is not None:
                    if burnEndT > burnStartT:
                        self.selected[0].scheduleBurn(burnStartT, burnEndT, 1.0)
                    if burnEndT < burnStartT:
                        self.selected[0].scheduleBurn(burnEndT, burnStartT, -1.0)
            else:
                self.selectedBurnStartIndex = None

    def findObjectsAtPoint(self, point: Tuple[int, int]) -> List["SpaceObjectCtrl"]:
        """
        Find an object (if any) at the given (view/screen) point
        """
        result: List["SpaceObjectCtrl"] = []
        for obj in self.objects:
            if obj.view.rect.collidepoint(*point):
                result += [obj]
        return result

    def selectObject(self, selectedObject: "SpaceObjectCtrl") -> None:
        """
        Select a space object, and bring the UI into selected mode
        """
        self.deselectAll()
        selectedObject.select()
        self.pauseModel = True
        self.selectedModeFlag = True
        self.showPaths()

    def deselectAll(self) -> None:
        """
        Make sure no space object is selected and the UI isn't in selected mode
        """
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
        """
        Show space object paths in view
        """
        self.view.hudGroup.empty()
        timePoints = [i * 1e3 for i in range(30)]
        selectedModel: Optional[SpaceObjectModel] = self.selected[0].model
        if selectedModel is None or selectedModel.mass > 0.0:
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
        if selectedModel is None or selectedModel.mass > 0.0:
            selected = False
        self.view.showPaths(futurePathsView, futureBurns, timePoints, selected=selected)

        if selectedModel is not None and selectedModel.mass == 0.0:
            self.selectedPathPointsView = futurePathsView[0]
            self.selectedPathTimes = timePoints

    def isCloseToFuturePath(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Check if position is close to a path
        """
        if self.selectedPathPointsView is None:
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
