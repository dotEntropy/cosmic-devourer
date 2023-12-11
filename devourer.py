import pygame
from pygame.math import Vector2
from pygame.sprite import Group
from pygame import time
from pygame.event import Event

from sprites.segment import Segment
from assets.assets import get_asset_wav

from config import *
import vectors
import convert


class Devourer:
    def __init__(self, segment_group: Group) -> None:
        self.segment_group = segment_group
        self.devour_sfx = get_asset_wav("devour.wav")
        self.devour_sfx.set_volume(0.25)
        self.move_sfx = get_asset_wav("move.wav")
        self.move_sfx.set_volume(0.1)
        self._initialize(quantity=6)
    
    def _initialize(self, quantity: int) -> None:
        self.segment_group.empty()
        self.head_pos = Vector2((n_tiles_x//2) - 1, n_tiles_y // 2)
        self.head_pos = convert.to_real_pos(self.head_pos)
        self.segments: list[Segment] = []
        self.segments_pending = 0
        self.second_segment_image_type = "body"
        self.control_direction = Vector2(-1, 0) 
        self.direction = Vector2(-1, 0)
        self.started_moving = False
        self.move_delay_ms = 100
        self.time_moved_ms = 0

        spawn_pos = self.head_pos.copy()
        for _ in range(quantity):
            segment = Segment(spawn_pos)
            spawn_pos.x += tile_size
            self.segment_group.add(segment)
            self.segments.append(segment)
        self._update_segments()

    def delta_direction(self, event: Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_d:
            self._delta_direction_horizontal(1)
        if event.key == pygame.K_a:
            self._delta_direction_horizontal(-1)
            self.started_moving = True
        if event.key == pygame.K_s:
            self._delta_direction_vertical(1)
            self.started_moving = True
        if event.key == pygame.K_w:
            self._delta_direction_vertical(-1)
            self.started_moving = True

    def _delta_direction_horizontal(self, direction: int) -> None:
        if self.direction.x: return
        self.control_direction.y = 0
        self.control_direction.x = direction
    
    def _delta_direction_vertical(self, direction: int) -> None:
        if self.direction.y: return
        self.control_direction.x = 0
        self.control_direction.y = direction
    
    def update(self) -> None:
        if not (self._can_update() and self.started_moving): return
        self._update_second_segment_image_type()
        self._move()
        self._check_if_ate_self()
        self._check_if_outside_border()

    def _can_update(self) -> bool:
        return time.get_ticks() - self.time_moved_ms > self.move_delay_ms
    
    def _update_second_segment_image_type(self) -> None:
        direction_angle_deg = vectors.get_angle(Vector2(), self.direction, degrees=True)
        control_direction_angle_deg = vectors.get_angle(Vector2(), self.control_direction, degrees=True)

        if control_direction_angle_deg > 180 and direction_angle_deg == 0:
            direction_angle_deg = 360
        if direction_angle_deg > 180 and control_direction_angle_deg == 0:
            control_direction_angle_deg = 360

        angle_deg_diff = control_direction_angle_deg - direction_angle_deg
        if angle_deg_diff > 0:
            self.second_segment_image_type = "counter-clockwise-body"
        elif angle_deg_diff < 0:
            self.second_segment_image_type = "clockwise-body"
        else:
            self.second_segment_image_type = "body"

    def _move(self) -> None:
        self.move_sfx.play()
        self.direction = self.control_direction.copy()
        
        self.time_moved_ms = time.get_ticks()
        self.head_pos += convert.to_real_pos(self.direction)

        if self.segments_pending:
            self._create_new_segment()
            self.segments_pending -= 1
        else:
            self._move_tail_to_head()
        self._update_segments()
    
    def _create_new_segment(self) -> None:
        segment = Segment(self.head_pos)
        self.segment_group.add(segment)
        self.segments.insert(0, segment)
    
    def _move_tail_to_head(self) -> None:
        # tail becomes head
        tail_segment = self.segments.pop()
        tail_segment.pos = self.head_pos.copy()
        self.segments.insert(0, tail_segment)

    def _update_segments(self) -> None:
        self.head_segment = self.segments[0]
        self.head_segment.update_image("head", self.direction)

        second_segment_type = self.second_segment_image_type
        self.second_segment = self.segments[1]
        self.second_segment.second_segment = True
        self.second_segment.update_image(second_segment_type, self.direction)

        self.body_segments = self.segments[2:-1]
        for body_segment in self.body_segments:
            if body_segment.second_segment: continue
            body_segment.update_image("body")

        self.tail_segment = self.segments[-1]
        self.tail_segment.update_image("tail")


    def _check_if_ate_self(self) -> None:
        body_segments = self.segments[1:]
        for body in body_segments:
            if self.head_segment.pos != body.pos: continue
            self._initialize(3)
    
    def _check_if_outside_border(self) -> None:
        if 0 <= self.head_pos.x < WIDTH and 0 <= self.head_pos.y < HEIGHT: return
        self._initialize(3)

