"""
Main screen/window through which the user plays the game
"""

import pygame  # type: ignore
from typing import Optional, List, Any, Tuple, TYPE_CHECKING


class MainWindow(pygame.Surface):
    """
    Main screen/window through which the user plays the game
    """

    def __init__(self, size: Tuple[int, int], backgroundImageLoc: str) -> None:
        """
        size is a tuple (x,y): the size of the layer (world) in pixels
        """
        self.screen = pygame.display.set_mode(size)
        pygame.Surface.__init__(self, size)
        self.fill((0, 0, 0))
        self.background: Optional[pygame.surface.Surface] = None
        if backgroundImageLoc is None:
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

    def update(self) -> None:
        """
        Draw Everything
        """
        if self.background is None:
            raise ValueError("background has not been set")
        self.screen.blit(self, (0, 0))
