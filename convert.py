from pygame.math import Vector2
from config import *


def to_real_pos(tile_pos: Vector2) -> Vector2:
    tile_pos = tile_pos * tile_size
    return tile_pos
    