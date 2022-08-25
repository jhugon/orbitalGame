import pygame  # type: ignore
import math
from dataclasses import dataclass
from typing import Optional, Tuple, List, Any, TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from universe import UniverseView


@dataclass
class PathStyle:
    """
    Configuration options for path styles
    """

    color: Tuple[int, int, int, int] = (255, 255, 255, 100)
    textcolor: Tuple[int, int, int, int] = (0, 0, 0, 100)
    textbakcolor: Tuple[int, int, int, int] = (255, 255, 255, 100)
    width: int = 1
    textsize: int = 24
    showTimes: bool = False
    arrowWidth: int = 8
    arrowLength: int = 8
    arrowColor: Tuple[int, int, int, int] = (255, 255, 255, 100)


class FuturePathsView(pygame.sprite.Sprite):
    def __init__(self, universeView: "UniverseView") -> None:
        pygame.sprite.Sprite.__init__(self)
        self.universe: "UniverseView" = universeView
        self.image: pygame.surface.Surface = pygame.Surface(
            self.universe.size
        ).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect: pygame.rect.Rect = pygame.Rect((0, 0), self.universe.size)
        self.universe.hudGroup.add(self)

        self.pathStyle: PathStyle = PathStyle()
        self.pathSelectedStyle: PathStyle = PathStyle(
            color=(255, 255, 0, 255),
            textcolor=(0, 0, 0, 255),
            textbakcolor=(0, 255, 0, 255),
            width=2,
            arrowColor=(255, 255, 0, 255),
        )

        self.font: Optional[pygame.font.Font] = None
        self.selectedFont: Optional[pygame.font.Font] = None
        if pygame.font:
            self.font = pygame.font.Font(None, self.pathStyle.textsize)
            self.selectedFont = pygame.font.Font(None, self.pathSelectedStyle.textsize)
        maxArrowAxis = max(
            self.pathSelectedStyle.arrowLength, self.pathSelectedStyle.arrowWidth
        )
        maxArrowAxis = max(maxArrowAxis, self.pathStyle.arrowLength)
        maxArrowAxis = max(maxArrowAxis, self.pathStyle.arrowWidth)
        maxArrowAxis = int(1.4 * maxArrowAxis)
        self.arrowImgSize: Tuple[int, int] = (maxArrowAxis, maxArrowAxis)
        self.arrowRect: pygame.rect.Rect = pygame.Rect((0, 0), self.arrowImgSize)
        self.arrowImgSelected: pygame.surface.Surface = pygame.Surface(
            self.arrowImgSize
        ).convert_alpha()
        self.arrowImg: pygame.surface.Surface = pygame.Surface(
            self.arrowImgSize
        ).convert_alpha()
        self.arrowImgSelected.fill((0, 0, 0, 0))
        self.arrowImg.fill((0, 0, 0, 0))
        x = self.arrowRect.centerx
        y = self.arrowRect.centery
        w2 = self.pathStyle.arrowWidth / 2
        l2 = self.pathStyle.arrowLength / 2
        pygame.draw.polygon(
            self.arrowImg,
            self.pathStyle.arrowColor,
            [
                [x - w2, y + l2],
                [x + w2, y + l2],
                [x, y - l2],
            ],
        )
        w2 = self.pathSelectedStyle.arrowWidth / 2
        l2 = self.pathSelectedStyle.arrowLength / 2
        pygame.draw.polygon(
            self.arrowImgSelected,
            self.pathSelectedStyle.arrowColor,
            [
                [x - w2, y + l2],
                [x + w2, y + l2],
                [x, y - l2],
            ],
        )

    def addPath(
        self,
        selected: bool,
        pointList: List[Tuple[int, int]],
        burnList: List[float],
        timeList: Optional[List[float]] = None,
    ) -> None:
        print("addPath starting:")
        print(f"  selected: {selected}")
        print(f"  pointList: {pointList}")
        print(f"  burnList: {burnList}")
        print(f"  timeList: {timeList}")
        assert len(pointList) == len(pointList)
        if timeList is not None:
            assert len(timeList) == len(burnList)
        style = self.pathStyle
        font = None
        if selected:
            style = self.pathSelectedStyle
        if self.font != None:
            if selected:
                font = self.selectedFont
            else:
                font = self.font
        color = style.color
        textcolor = style.textcolor
        textbakcolor = style.textbakcolor
        width = style.width
        showTimes = style.showTimes
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
            self.image.blit(
                imgToBlit,
                (
                    point[0] - style.arrowWidth // 2,
                    point[1] - style.arrowLength // 2,
                ),
            )

        if not showTimes:
            return
        if (timeList is not None) and (font is not None):
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

                if font is not None:
                    timeString = "{0:.0f}".format(time) + append
                    textSurf = font.render(
                        timeString, True, textcolor
                    )  # ,textbakcolor)
                    textSurf = textSurf.convert_alpha()
                    textpos = textSurf.get_rect()
                    textBakSurf = pygame.Surface(
                        (textpos[2], textpos[3])
                    ).convert_alpha()
                    textBakSurf.fill(textbakcolor)
                    textBakSurf.blit(textSurf, (0, 0))
                    textpos.center = pos
                self.image.blit(textBakSurf, textpos)
