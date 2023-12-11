import pygame
from pygame.math import Vector2
from random import choice, randrange

from assets.assets import get_asset_png
import convert
from config import *


class Food(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2) -> None:
        super().__init__()
        self.pos = pos
        self.update_image()
    
    def update_image(self) -> None:
        self.food_images = [
            get_asset_png("food_red.png"),
            get_asset_png("food_blue.png"),
            get_asset_png("food_yellow.png")
        ]
        self.image = choice(self.food_images)
        self.rect = self.image.get_rect(topleft=self.pos)

    def relocate(self) -> None:
        tile_pos = Vector2(randrange(n_tiles_x), randrange(n_tiles_y))
        self.pos = Vector2(convert.to_real_pos(tile_pos))
        self.update_image()
