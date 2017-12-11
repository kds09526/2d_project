import random
import json
from pico2d import *

class Bullet:
    BLUE, PURPLE, YELLOW, GREEN, RED = 0, 1, 2, 3, 4
    LEFT, RIGHT = 6, 3

    image = {BLUE: None, PURPLE: None, YELLOW: None, GREEN: None, RED: None}

    # 총알 세팅
    Set ={BLUE  : {'w': 27, 'h': 9, 'speed': 2, 'damage':20, LEFT: 1, RIGHT: 0, 'total_frame': 1, 'time_per': 1, 'frame_per': 1},
         PURPLE: {'w': 54, 'h': 15, 'speed': 1.5, 'damage':25, LEFT: 1, RIGHT: 0, 'total_frame': 2, 'time_per': 3, 'frame_per': 2},
         YELLOW: {'w': 27, 'h': 27, 'speed': 4, 'damage':5, LEFT: 1, RIGHT: 0, 'total_frame': 2, 'time_per': 5, 'frame_per': 2},
         GREEN : {'w': 27, 'h': 39, 'speed': 1, 'damage': 15, LEFT: 1, RIGHT: 0, 'total_frame': 4, 'time_per': 3, 'frame_per': 4},
         RED   : {'w': 1024, 'h': 21, 'speed': 0, 'damage': 40, LEFT: 3, RIGHT: 0, 'total_frame': 2, 'time_per': 3, 'frame_per': 2}}

    def __init__(self, color, astronaut_x, astronaut_y, direct):
        # 이미지 읽어오기
        if self.image[Bullet.BLUE] == None:
            self.image[Bullet.BLUE] = load_image('image/bullet/blue.png')
        if self.image[Bullet.PURPLE] == None:
            self.image[Bullet.PURPLE] = load_image('image/bullet/purple.png')
        if self.image[Bullet.YELLOW] == None:
            self.image[Bullet.YELLOW] = load_image('image/bullet/yellow.png')
        if self.image[Bullet.GREEN] == None:
            self.image[Bullet.GREEN] = load_image('image/bullet/green.png')
        if self.image[Bullet.RED] == None:
            self.image[Bullet.RED] = load_image('image/bullet/red.png')

        self.color = color
        self.direct = direct
        if self.direct == Bullet.RIGHT:
            self.x = astronaut_x + 15 + (Bullet.Set[self.color]['w'] // 2)
        if self.direct == Bullet.LEFT:
            self.x = astronaut_x - 15 - (Bullet.Set[self.color]['w'] // 2)
        self.y = astronaut_y - 17

        self.total_frame = 0
        self.frame = 0

        self.is_draw = True

    def update(self, frame_time):
        if self.color == Bullet.RED:
            self.frame = int(self.total_frame)
            self.total_frame += Bullet.Set[self.color]['frame_per'] * Bullet.Set[self.color]['time_per'] * frame_time
            if self.frame >= 3:
                self.is_draw = False
        else:
            if self.direct == Bullet.RIGHT:
                self.x += Bullet.Set[self.color]['speed']
                if self.x + (Bullet.Set[self.color]['w'])//2 >= 1024:
                    self.is_draw = False
            else:
                self.x -= Bullet.Set[self.color]['speed']
                if self.x - (Bullet.Set[self.color]['w'])//2 <= 0:
                    self.is_draw = False

            self.frame = int(self.total_frame) % Bullet.Set[self.color]['total_frame']
            self.total_frame += Bullet.Set[self.color]['frame_per'] * Bullet.Set[self.color]['time_per'] * frame_time

    def draw(self, frame_time):
        if self.color == Bullet.RED:
            self.image[self.color].clip_draw(0, Bullet.Set[self.color][self.direct] * Bullet.Set[self.color]['h'] + self.frame * Bullet.Set[self.color]['h'],
                                             Bullet.Set[self.color]['w'], Bullet.Set[self.color]['h'], self.x, self.y)
        else:
            self.image[self.color].clip_draw(self.frame * Bullet.Set[self.color]['w'],Bullet.Set[self.color][self.direct] * Bullet.Set[self.color]['h'],
                                            Bullet.Set[self.color]['w'], Bullet.Set[self.color]['h'], self.x, self.y)


