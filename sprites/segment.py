import pygame
from pygame.math import Vector2
from random import choice

from assets.get_assets import get_asset
from config import *


class Segment(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2, is_head: bool=False) -> None:
        super().__init__()
        self.is_head = is_head
        self.pos = pos
        self._update_image()
    
    def _update_image(self) -> None:
        self.segment_image = get_asset("head.png") if self.is_head else get_asset("body.png")
        self.image = self.segment_image
        self.rect = self.image.get_rect(topleft=self.pos)
