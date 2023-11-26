import pygame 
from level import Level
from config import *


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_mode([WIDTH, HEIGHT])
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
