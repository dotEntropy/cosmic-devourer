import pygame
from pygame import Surface
import pathlib


def load_image(path: str, angle_deg: float=0, scale: float=1) -> Surface:
    image = pygame.image.load(path).convert_alpha()
    scale_w = image.get_width() * scale
    scale_h = image.get_height() * scale
    if scale != 1:
        image = pygame.transform.scale(image, (scale_w, scale_h))
    if angle_deg:
        image = pygame.transform.rotate(image, angle_deg)
    return image


def modify_image(image: Surface, angle_deg: float=0, scale: float=1) -> Surface:
    scale_w = image.get_width() * scale
    scale_h = image.get_height() * scale
    if scale != 1:
        image = pygame.transform.scale(image, (scale_w, scale_h))
    if angle_deg:
        image = pygame.transform.rotate(image, angle_deg)
    return image


ASSET_DIR = pathlib.Path(__file__).parent


def get_asset(file_name: str) -> Surface:
    return load_image(ASSET_DIR / file_name)
