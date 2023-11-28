import pygame 
from pygame.math import Vector2
from pygame.sprite import Group
from pygame.event import Event

from random import randrange
import sys

from devourer import Devourer
from sprites.food import Food
from assets.assets import get_asset_png

import convert
from config import *


class Level:
    def __init__(self) -> None:
        self.screen = pygame.display.get_surface()
        self.food_group = Group()
        self.segment_group = Group()
        self._setup_entites()
    
    def _setup_entites(self) -> None:
        self.devourer = Devourer(self.segment_group)
        self._spawn_food()

    def run(self, dt: float) -> None:
        self._handle_events()
        self._update()
        self._draw()

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

    def _update(self) -> None:
        self._check_if_devoured()
        self.devourer.update()
    
    def _check_if_devoured(self) -> None:
        devourer = self.devourer
        food_sprites = self.food_group.sprites()
        for food in food_sprites:
            food: Food
            if devourer.head_pos != food.pos: return
            food.relocate()
            self.devourer.devour_sfx.play()
            self.devourer.segments_pending += 2
    
    def _spawn_food(self) -> None: 
        tile_pos = Vector2(randrange(N_TILES_X), randrange(N_TILES_Y))
        self.food = Food(convert.to_real_pos(tile_pos))
        self.food_group.add(self.food)

    def _draw(self) -> None:
        self.screen.fill(BG_COLOR)
        self.segment_group.draw(self.screen)
        self.food_group.draw(self.screen)
