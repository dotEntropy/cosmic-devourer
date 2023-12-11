import pygame, os, time

from level import Level

from config import *
from assets.assets import get_asset_png


class Game:
    def __init__(self) -> None:
        os.system("cls")
        pygame.init()
        pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption("Cosmic Devourer")
        pygame.display.set_icon(get_asset_png("icon.png"))
        self.level = Level()
        self.clock = pygame.time.Clock()
    
    def run(self) -> None:
        pre_time = time.time()
        while True:
            dt = time.time() - pre_time
            pre_time = time.time()

            self.level.run(dt)

            # self._update_debug(dt)
            # self.debug.draw()
            pygame.display.update()
            self.clock.tick(FPS)
    
    def _update_debug(self, dt: float) -> None:
        if not dt: return
        self.debug.update_texts(round(1 / dt), 100)


if __name__ == "__main__":
    game = Game()
    game.run()
