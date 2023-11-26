from pygame.math import Vector2
from config import *


def get_tile_pos(x_tile: int, y_tile: int) -> Vector2:
    tile_pos = Vector2(x_tile, y_tile) * TILE_SIZE
    return tile_pos
    