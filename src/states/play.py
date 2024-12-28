import pygame 

from src.states.parent import State
from src.sprites.devourer import Devourer
from src.sprites.food import Food


class Play(State):
    def __init__(self) -> None:
        super().__init__('play')
    
    def _init_groups(self) -> None:
        self.segment_group = pygame.sprite.Group()
        self.food_group = pygame.sprite.Group()

    def _init_sprites(self):
        self.devourer = Devourer(self.segment_group)
        self.food = Food(self.food_group)

    def handle_key_tap(self, key: int):
        self.devourer.key_tap(key)

    def update(self, dt: float) -> None:
        self.segment_group.update(self.food_group)

    def draw(self) -> None:
        self.SCREEN.fill('black')
        self.devourer.update(self.food_group)
        self.segment_group.draw(self.SCREEN)
        self.food_group.draw(self.SCREEN)
    

def setup() -> None:
    Play()
