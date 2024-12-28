import pygame 
from pygame.math import Vector2

from src.states.parent import State
from src.sprites.templates import Button
from src.constants import DEFAULT_WIDTH, DEFAULT_HEIGHT, SPRITE_SCALE


class MainMenu(State):
    def __init__(self) -> None:
        super().__init__('main-menu')
    
    def _init_groups(self) -> None:
        self.button_group = pygame.sprite.Group()

    def _init_sprites(self):
        self.play_button = Button(
            self.button_group,
            Vector2(DEFAULT_WIDTH / 2, DEFAULT_HEIGHT / 3),
            self.switch_to_play,
            scale=2*SPRITE_SCALE,
            is_toggle=False,
            released_animation={
                'asset_id': 'button-release'
                },
            hovered_animation={
                'asset_id': 'button-hover',
                },
            pressed_animation={
                'asset_id': 'button-press',
                },
            )
    
    def switch_to_play(self):
        self.switch_state('play')

    def handle_mouse_held(self, buttons: tuple[int]) -> None:
        for sprites in self.button_group.sprites():
            sprites.mouse_held(buttons)

    def update(self, dt: float) -> None:
        mouse_pos = Vector2(pygame.mouse.get_pos())
        self.button_group.update(dt=dt, mouse_pos=mouse_pos)

    def draw(self) -> None:
        self.SCREEN.fill('black')
        self.button_group.draw(self.SCREEN)
    

def setup() -> None:

    MainMenu()
