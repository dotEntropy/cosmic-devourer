import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
from pygame.sprite import Group
from pygame import time

from src.sprites.parents import Animation
from src.loader import get_sfx
from src.constants import SPRITE_SCALE


class Segment(Sprite, Animation):
    def __init__(self, pos: Vector2) -> None:
        super().__init__()
        self.second_segment = False
        self.ORIGIN_POS = pos.copy()
        self._load_animation_configs()
    
    def _overrides(self):
        self.scale = SPRITE_SCALE
        self.pos = self.ORIGIN_POS
        self.angle_deg = 180
        self.pos_type = 'topleft'

    def _load_animation_configs(self) -> None:
        Animation.__init__(self, 'body', 'body')
        self._create_config('head', 'head')
        self._create_config('tail', 'tail')
        self._create_config('clockwise-body', 'clockwise-body')
        self._create_config('counter-clockwise-body', 'counter-clockwise-body')

    def move_to_head(self, pos: Vector2) -> None:
        self.pos = pos.copy()
        self.update_image()
    
    def update_segment(self, segment_type: str, direction: Vector2=None) -> None:
        self._update_angle_deg(direction)
        self._switch_config(segment_type)

    def _update_angle_deg(self, direction: Vector2) -> None:
        if direction is None: 
            return

        if direction.x == 1:
            angle_deg = 0
        if direction.x == -1:
            angle_deg = 180
        if direction.y == 1:
            angle_deg = 270 
        if direction.y == -1:
            angle_deg = 90

        self.update_angle(angle_deg)


from src.sprites.parents import Controls
from src.constants import N_TILES_X, N_TILES_Y, TILE_SIZE, DEFAULT_WIDTH, DEFAULT_HEIGHT
from utils import tools, convert


class Devourer(Controls):
    def __init__(self, segment_group: Group) -> None:
        self.segment_group = segment_group
        self._init_music()
        self._init_devourer()
    
    def _init_music(self) -> None:
        self.eat_sfx = get_sfx('devour')
        self.music_sfx = get_sfx('music')
        self.ate_self_sfx = get_sfx('ate-self')
        self.crash_sfx = get_sfx('crash')
        self.eat_sfx.set_volume(0.25)
        self.music_sfx.set_volume(0.5)
        self.ate_self_sfx.set_volume(0.25)
        self.crash_sfx.set_volume(0.25)
    
    def _init_devourer(self) -> None:
        self.music_sfx.stop()
        self.segment_group.empty()
        self.head_pos = Vector2((N_TILES_X // 2) - 1, N_TILES_Y // 2)
        self.head_pos = convert.to_real_pos(self.head_pos)
        self.segments: list[Segment] = []
        self.start_length = 3
        self.segments_pending = 0
        self.second_segment_image_type = 'body'
        self.control_direction = Vector2(-1, 0) 
        self.direction = Vector2(-1, 0)
        self.is_started = False
        self.move_delay_ms = 100
        self.time_moved_ms = 0

        spawn_pos = self.head_pos.copy()
        for _ in range(self.start_length):
            segment = Segment(spawn_pos)
            spawn_pos.x += TILE_SIZE
            self.segment_group.add(segment)
            self.segments.append(segment)
        self._update_segments()

    def key_tap(self, key: int) -> None:
        if key == pygame.K_d:
            self._delta_direction_horizontal(1)
        if key == pygame.K_a:
            self._delta_direction_horizontal(-1)
        if key == pygame.K_s:
            self._delta_direction_vertical(1)
        if key == pygame.K_w:
            self._delta_direction_vertical(-1)

    def _delta_direction_horizontal(self, direction: int) -> None:
        if self.direction.x == -direction: return
        self.control_direction.y = 0
        self.control_direction.x = direction
        if not self.is_started: self._start()
    
    def _delta_direction_vertical(self, direction: int) -> None:
        if self.direction.y == -direction: return
        self.control_direction.x = 0
        self.control_direction.y = direction
        if not self.is_started: self._start()
    
    def _start(self) -> None:
        self.is_started = True
        self.music_sfx.play(loops=-1)
    
    def update(self, food_group: Group) -> None:
        if not (self._can_update() and self.is_started): 
            return
        self._update_second_segment_image_type()
        self._move()
        self.food_sprites = food_group.sprites()
        self._check_devoured_food()
        self._check_ate_self()
        self._check_border_bump()

    def _can_update(self) -> bool:
        return time.get_ticks() - self.time_moved_ms > self.move_delay_ms
    
    def _update_second_segment_image_type(self) -> None:
        direction_angle_deg = tools.get_angle(Vector2(), self.direction, degrees=True)
        control_direction_angle_deg = tools.get_angle(Vector2(), self.control_direction, degrees=True)

        if control_direction_angle_deg > 180 and direction_angle_deg == 0:
            direction_angle_deg = 360
        if direction_angle_deg > 180 and control_direction_angle_deg == 0:
            control_direction_angle_deg = 360

        angle_deg_diff = control_direction_angle_deg - direction_angle_deg
        if angle_deg_diff > 0:
            self.second_segment_image_type = 'counter-clockwise-body'
        elif angle_deg_diff < 0:
            self.second_segment_image_type = 'clockwise-body'
        else:
            self.second_segment_image_type = 'body'

    def _move(self) -> None:
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
        self.head_segment.update_segment('head', self.direction)

        second_segment_type = self.second_segment_image_type
        self.second_segment = self.segments[1]
        self.second_segment.second_segment = True
        self.second_segment.update_segment(second_segment_type, self.direction)

        self.body_segments = self.segments[2:-1]
        for body_segment in self.body_segments:
            if body_segment.second_segment: continue
            body_segment.update_segment('body')

        self.tail_segment = self.segments[-1]
        self.tail_segment.update_segment('tail')

    def _check_devoured_food(self) -> None:
        for food in self.food_sprites:
            if self.head_pos != food.pos: 
                return
            food.relocate()
            self.eat_sfx.play()
            self.segments_pending += 1
            self.move_delay_ms -= 0.25

    def _check_ate_self(self) -> None:
        body_segments = self.segments[1:]
        for body in body_segments:
            if self.head_segment.pos != body.pos: continue
            self._cut_self(body, body_segments)
    
    def _cut_self(self, body: Segment, body_segments: list) -> None:
        self.ate_self_sfx.play()
        body_index = body_segments.index(body)
        for body in body_segments[body_index:]: 
            self.segments.remove(body)
            body.kill()
    
    def _check_border_bump(self) -> None:
        if 0 <= self.head_pos.x < DEFAULT_WIDTH and 0 <= self.head_pos.y < DEFAULT_HEIGHT: return
        self.crash_sfx.play()
        self._init_devourer()
