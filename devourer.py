import pygame
from pygame import time
from pygame.event import Event


class Devourer:
    def __init__(self) -> None:
        self.started = 0
        self.direction = ""
        self.move_delay_ms = 200
        self.current_time_ms = time.get_ticks()
        self.time_moved_ms = 0
    
    def delta_direction(self, event: Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_w:
            self.direction = "up"
        if event.key == pygame.K_s:
            self.direction = "down"
        if event.key == pygame.K_d:
            self.direction = "left"
        if event.key == pygame.K_a:
            self.direction = "right"
        