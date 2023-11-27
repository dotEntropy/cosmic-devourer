import pygame 

from level import Level

from assets.assets import get_asset_png
from config import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption("Cosmic Devourer")
        pygame.display.set_icon(get_asset_png("body.png"))
        self.level = Level()
        self.clock = pygame.time.Clock()
    
    def run(self) -> None:
        while True:
            dt = self.clock.tick(FPS) / 1000
            self.level.run(dt)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
