import pygame
from pygame.math import Vector2


class DebugText:
    def __init__(self) -> None:
        self.WIN = pygame.display.get_surface()
        self.font = pygame.font.SysFont("Consolas", 24)
        self.spacing = self.font.get_linesize() + 2
        self.texts = [] 
        self.total_ticks = 0
    
    def update_texts(self, texts: list=[], rate_ms: float=1):
        self.total_ticks = (self.total_ticks + 1) % rate_ms
        if self.total_ticks: return
        if type(texts) is list:
            self.texts = texts.copy()
            return
        self.texts = [texts]

    def draw(self) -> None:
        if not len(self.texts): return
        pos = Vector2(20, 20)
        for text in self.texts:
            surface = self.font.render(str(text), True, "white")
            self.WIN.blit(surface, pos)
            pos.y += self.spacing
        pos.y = 20
