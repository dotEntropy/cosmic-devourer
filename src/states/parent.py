import pygame
import colorama

from src.variables import GameVars
from src.constants import STATE_LOGGING


class State:
    def __init__(self, alias: str) -> None:
        colorama.init(autoreset=True)
        self.alias = str(alias)
        self.SCREEN = pygame.display.get_surface()
        self._init_buttons()
        self._init_groups()
        self._init_sprites()
        self._load_state()
    
    def _load_state(self) -> None:
        is_reloaded = self.alias in GameVars.states
        load_str = 'reloaded' if is_reloaded else 'loaded'
        self.__log('load', load_str=load_str)
        GameVars.states[self.alias] = self

    def switch_state(self, alias: str) -> None:
        state = GameVars.states.get(alias)
        if state is None:
            self.__log('no switch', alias=alias)
        else:
            self.__log('switch', alias=alias)
            GameVars.active_state = state 
    
    def reset_state(self, alias) -> None:
        state = GameVars.states.get(alias)
        if state:
            state.__init__()
        else:
            self.__log('no reset', alias=alias)
    
    def __log(self, log_type: str, **kwargs) -> None:
        if not STATE_LOGGING:
            return

        alias = kwargs.get('alias')
        load_str = kwargs.get('load_str')

        match log_type:
            case 'switch':
                print(f'{colorama.Fore.GREEN}Switch to state: {colorama.Fore.YELLOW}{alias}')
            case 'load':
                print(f'{colorama.Fore.GREEN}State {load_str}: {colorama.Fore.YELLOW}{self.alias}')
            case 'no switch':
                print(f'{colorama.Fore.RED}State "{alias}" not found. Cannot switch.')
            case 'no reset':
                print(f'{colorama.Fore.RED}State "{alias}" not found. Cannot reset.')

    def _init_buttons(self) -> None: ... 
    def _init_sprites(self) -> None: ...
    def _init_groups(self) -> None: ...
    def update(self, dt: float) -> None: ...
    def draw(self) -> None: ...
    def handle_key_tap(self, key: int) -> None: ...
    def handle_key_held(self, keys: dict) -> None: ...
    def handle_mouse_tap(self, button: int) -> None: ...
    def handle_mouse_held(self, buttons: tuple) -> None: ...
 