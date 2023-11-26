import pygame 
from pygame.math import Vector2
from pygame.sprite import Group
from pygame.event import Event

from random import randrange
import sys

from devourer import Devourer
from sprites.food import Food
from sprites.segment import Segment
import convert
from config import *


class Level:
    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()
        self.devourer = Devourer()
        self._setup_sprites()
    
    def _setup_sprites(self) -> None:
        self.food_group = Group()
        self.segment_group = Group()
        self._spawn_food()
    
    def _spawn_food(self) -> None: 
        x_tile = randrange(N_TILES_X)
        y_tile = randrange(N_TILES_Y)
        self.food = Food(convert.get_tile_pos(x_tile, y_tile))
        self.food_group.add(self.food)

    def run(self, dt: float) -> None:
        print(self.devourer.direction)
        self._handle_events()
        self._update_sprite_groups(dt)
        self._draw_sprite_groups()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            self._quit_event(event)
            self.devourer.delta_direction(event)
    
    @staticmethod
    def _quit_event(event: Event) -> None:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type != pygame.KEYDOWN: return
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    def _update_sprite_groups(self, dt: float) -> None:
        self.food_group.update(dt)
        self.segment_group.update(dt)

    def _draw_sprite_groups(self) -> None:
        self.screen.fill(BG_COLOR)
        self.food_group.draw(self.screen)
        self.segment_group.draw(self.screen)
