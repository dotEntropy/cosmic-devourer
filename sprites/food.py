import pygame
from pygame.math import Vector2
from random import choice

from assets.get_assets import get_asset
from config import *


class Food(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2) -> None:
        super().__init__()
        self.pos = pos
        self._update_image()
    
    def _update_image(self) -> None:
        self.food_images = [
            get_asset("food_red.png"),
            get_asset("food_blue.png"),
            get_asset("food_yellow.png")
        ]
        self.image = choice(self.food_images)
        self.rect = self.image.get_rect(topleft=self.pos)
