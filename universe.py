"""
Universe controlls all of the SpaceObjects
"""

import pygame  # type: ignore
from math import sqrt
from copy import deepcopy


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
