from typing import Any
import pygame
from pygame.math import Vector2
from random import choice

from assets.assets import get_asset_png
from assets.assets import modify_image
from config import *


class Segment(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2) -> None:
        super().__init__()
        self.is_head = False
        self.pos = pos.copy()
        self.angle_deg = 180
        self.head_image = get_asset_png("head.png")
        self.body_image = get_asset_png("body.png")
        self.update_image()

    def move_to_head(self, pos: Vector2) -> None:
        self.is_head = True
        self.pos = pos.copy()
        self.rect.topleft = self.pos
    
    def update_image(self, direction: Vector2=None) -> None:
        self._update_angle_deg(direction)
        self.segment_image = self.head_image if self.is_head else self.body_image
        self.image = modify_image(self.segment_image, angle_deg=self.angle_deg)
        self.rect = self.image.get_rect(topleft=self.pos)

    def _update_angle_deg(self, direction: Vector2) -> None:
        if direction is None: return
        if direction.x == 1:
            self.angle_deg = 0
        if direction.x == -1:
            self.angle_deg = 180
        if direction.y == 1:
            self.angle_deg = 270 
        if direction.y == -1:
            self.angle_deg = 90

