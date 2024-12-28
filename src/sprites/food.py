import pygame
from pygame.sprite import Sprite, Group
from pygame.math import Vector2

from random import choice, randrange

from src.sprites.parents import Animation
from src.constants import N_TILES_X, N_TILES_Y, SPRITE_SCALE
from utils import convert


class Food(Sprite, Animation):
    def __init__(self, group: Group) -> None:
        super().__init__(group)
        self.count = 0
        self.tile_pos = Vector2(randrange(N_TILES_X), randrange(N_TILES_Y))
        self._set_value()
        self._load_animation_configs()
    
    def _overrides(self):
        self.pos = convert.to_real_pos(self.tile_pos)
        self.scale = SPRITE_SCALE
        self.pos_type = 'topleft'

    def _load_animation_configs(self) -> None:
        Animation.__init__(self, 'food-red', 'food-red')
        self._create_config('food-blue', 'food-blue')
        self._create_config('food-yellow', 'food-yellow')
        self._switch_config(choice(list(self.configs.keys())))

    def relocate(self) -> None:
        self.tile_pos = Vector2(randrange(N_TILES_X), randrange(N_TILES_Y))
        self.pos = convert.to_real_pos(self.tile_pos)
        self._set_value()
        self.count += 1
        self._switch_config(choice(list(self.configs.keys())))
    
    def _set_value(self) -> None:
        if self._at_corner(): 
            self.value = 4
        elif self._at_edge():
            self.value = 2
        else:
            self.value = 1

    def _at_corner(self) -> bool:
        return any((
            self.tile_pos == (0, 0),
            self.tile_pos == (N_TILES_X-1, 0),
            self.tile_pos == (0, N_TILES_Y-1),
            self.tile_pos == (N_TILES_X-1, N_TILES_Y-1)
        ))
    
    def _at_edge(self) -> bool:
        return any((
            self.tile_pos.x == 0,
            self.tile_pos.y == 0,
            self.tile_pos.x == N_TILES_X-1, 
            self.tile_pos.y == N_TILES_Y-1
        ))
