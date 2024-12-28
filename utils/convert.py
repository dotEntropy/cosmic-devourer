from pygame.math import Vector2
from src.constants import TILE_SIZE


def to_real_pos(tile_pos: Vector2) -> Vector2:
    tile_pos = tile_pos * TILE_SIZE
    return tile_pos
    