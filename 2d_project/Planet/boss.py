import random
import json
from pico2d import *

class Sun:
    image = None

    # 상태
    NORMAL_STATE, ATTACK_STATE = 0, 1
    state_set = {NORMAL_STATE : {'draw_frame_num':0,'total_frame' : 3, 'time_per' : 2, 'frame_per' : 2},
                 ATTACK_STATE : {}}

    def __init__(self):
        if self.image == None:
            self.image = load_image('image/boss/boss_sun.png')
        self.x = 898
        self.y = 381
        self.width = 252
        self.height = 801
        self.state = Sun.NORMAL_STATE
        self.state_frame = 0
        self.state_total_frame = 0

    def update(self, frame_time):
        if self.state == Sun.NORMAL_STATE:
            self.state_frame = int(self.state_total_frame) % Sun.state_set[self.state]['total_frame']
            self.state_total_frame += Sun.state_set[self.state]['frame_per'] * self.state_set[self.state]['time_per'] * frame_time


    def draw(self, frame_time):
        self.image.clip_draw(self.state_frame * self.width,Sun.state_set[self.state]['draw_frame_num']* self.height, self.width,self.height,self.x ,self.y)