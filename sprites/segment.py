import pygame
from pygame.math import Vector2

from assets.assets import get_asset_png
from assets.assets import modify_image
from config import *


class Segment(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2) -> None:
        super().__init__()
        self.second_segment = False
        self.pos = pos.copy()
        self.angle_deg = 180
        self.asset_dict = {
            "clockwise-body": get_asset_png("clockwise-body.png"),
            "counter-clockwise-body": get_asset_png("counter-clockwise-body.png"),
            "head": get_asset_png("head.png"), 
            "body": get_asset_png("body.png"),
            "tail": get_asset_png("tail.png")
            }

    def move_to_head(self, pos: Vector2) -> None:
        self.pos = pos.copy()
        self.rect.topleft = self.pos
    
    def update_image(self, segment_type: str, direction: Vector2=None) -> None:
        self._update_angle_deg(direction)
        self.image = modify_image(self.asset_dict[segment_type], angle_deg=self.angle_deg)
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

