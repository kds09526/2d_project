import random
import json
from pico2d import *

class Sun:
    image = None
    font = None

    # 상태
    NORMAL_STATE, ATTACK_STATE, DEAD_STATE = 0, 1, 5

    UP_AND_DOWN, VIBRATE = 0, 1
    state_set = {NORMAL_STATE : {'draw_frame_num':0,'total_frame' : 3, 'time_per' : 2, 'frame_per' : 2, 'animation': UP_AND_DOWN},
                 DEAD_STATE   : {'draw_frame_num':5,'total_frame' : 2, 'time_per' : 2, 'frame_per' : 2, 'animation': VIBRATE}}

    def __init__(self):
        if self.font == None:
            self.font = load_font('font/ENCR10B.TTF',16)
        if self.image == None:
            self.image = load_image('image/boss/boss_sun.png')
        self.x = 898
        self.y = 381
        self.y_plus = 10
        self.width = 252
        self.height = 801
        self.hp = 3000

        self.state = Sun.NORMAL_STATE
        self.state_frame = 0
        self.state_total_frame = 0

        self.circle_x = self.x -114
        self.circle_radius = 332
        self.vibrate_degree = 0
        self.dead_x = 0

        self.live = True

    def update(self, frame_time):
        if Sun.state_set[self.state]['animation'] == Sun.UP_AND_DOWN:
            self.y += self.y_plus * frame_time
            if self.y > 388 or self.y < 374:
                self.y_plus *= -1
        elif Sun.state_set[self.state]['animation'] == Sun.VIBRATE:
            self.vibrate_degree += 25 * frame_time
            self.x = math.sin(self.vibrate_degree) * 4 + 903
            self.y = math.cos(self.vibrate_degree) * 4 + 381

        if self.state == Sun.DEAD_STATE:
            self.dead_x += 35 * frame_time
            self.x += self.dead_x
            if self.x > 1170:
                self.live = False

        self.state_frame = int(self.state_total_frame) % Sun.state_set[self.state]['total_frame']
        self.state_total_frame += Sun.state_set[self.state]['frame_per'] * self.state_set[self.state]['time_per'] * frame_time

    def handle_event(self, event):
        pass

    def draw(self, frame_time):
        self.image.clip_draw(self.state_frame * self.width,Sun.state_set[self.state]['draw_frame_num']* self.height, self.width,self.height,self.x ,self.y)
        self.font.draw(self.x - 300, self.y + 300, 'HP: %d' %self.hp, (255,255,0))