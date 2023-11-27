import pygame
from pygame.math import Vector2
from pygame.sprite import Group
from pygame import time
from pygame.event import Event

import sys

from sprites.segment import Segment
from assets.assets import get_asset_wav

import convert
from config import *


class Devourer:
    def __init__(self, segment_group: Group) -> None:
        self.segment_group = segment_group
        self.devour_sfx = get_asset_wav("devour.wav")
        self.devour_sfx.set_volume(0.25)
        self.move_sfx = get_asset_wav("move.wav")
        self.move_sfx.set_volume(0.1)
        self._initialize(quantity=2)
    
    def _initialize(self, quantity: int) -> None:
        self.segment_group.empty()
        self.head_pos = Vector2((N_TILES_X//2) - 1, N_TILES_Y // 2)
        self.head_pos = convert.to_real_pos(self.head_pos)
        self.segments: list[Segment] = []
        self.control_direction = Vector2(-1, 0) 
        self.direction = Vector2(-1, 0)
        self.is_moving = False
        self.segments_pending = 0
        self.move_delay_ms = 100
        self.time_moved_ms = 0

        spawn_pos = self.head_pos.copy()
        for _ in range(quantity):
            segment = Segment(spawn_pos)
            spawn_pos.x += TILE_SIZE
            self.segment_group.add(segment)
            self.segments.append(segment)
        self._declare_head_segment()

    def delta_direction(self, event: Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_d:
            self._delta_direction_horizontal(1)
        if event.key == pygame.K_a:
            self._delta_direction_horizontal(-1)
            self.is_moving = True
        if event.key == pygame.K_s:
            self._delta_direction_vertical(1)
            self.is_moving = True
        if event.key == pygame.K_w:
            self._delta_direction_vertical(-1)
            self.is_moving = True

    def _delta_direction_horizontal(self, direction: int) -> None:
        if self.direction.x: return
        self.control_direction.y = 0
        self.control_direction.x = direction
    
    def _delta_direction_vertical(self, direction: int) -> None:
        if self.direction.y: return
        self.control_direction.x = 0
        self.control_direction.y = direction
    
    def update(self) -> None:
        if not (self._can_update() and self.is_moving): return
        self._move()
        self._check_if_ate_self()
        self._check_if_outside_border()

    def _can_update(self) -> bool:
        return time.get_ticks() - self.time_moved_ms > self.move_delay_ms

    def _move(self) -> None:
        self.move_sfx.play()
        self.direction = self.control_direction.copy()
        self.time_moved_ms = time.get_ticks()
        self.head_pos += convert.to_real_pos(self.direction)
        self.controllable = True

        if self.segments_pending > 0:
            self._create_new_segment()
            self.segments_pending -= 1
            return
        self._move_tail_to_head_pos()
    
    def _create_new_segment(self) -> None:
        self._dethrone_head_segment()
        segment = Segment(self.head_pos)
        self.segment_group.add(segment)
        self.segments.insert(0, segment)
        self._declare_head_segment()
    
    def _move_tail_to_head_pos(self) -> None:
        self._dethrone_head_segment()
        # tail becomes head
        tail_segment = self.segments.pop()
        tail_segment.pos = self.head_pos.copy()
        self.segments.insert(0, tail_segment)
        self._declare_head_segment()
    
    def _declare_head_segment(self) -> None:
        self.head_segment = self.segments[0]
        self.head_segment.is_head = True
        self.head_segment.update_image(self.control_direction)

    def _dethrone_head_segment(self) -> None:
        self.head_segment.is_head = False
        self.head_segment.update_image()

    def _check_if_ate_self(self) -> None:
        body_segments = self.segments[1:]
        for body in body_segments:
            if self.head_segment.pos != body.pos: continue
            self._initialize(2)
    
    def _check_if_outside_border(self) -> None:
        if 0 <= self.head_pos.x < WIDTH and 0 <= self.head_pos.y < HEIGHT: return
        self._initialize(2)

