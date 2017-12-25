import random
import json
from pico2d import *

class Sun:
    image = None
    font = None
    life_bar_image = None

    # 상태
    NORMAL_STATE, ATTACK_STATE1, ATTACK_STATE2, ATTACK_STATE3, DEAD_STATE = "0", "1", "2", "3", "5"

    NONE, UP_AND_DOWN, VIBRATE = 0, 1, 2
    boss_state_file = open('json/boss/state.json', 'r')
    state_set = json.load(boss_state_file)
    boss_state_file.close()

    # 라이프 바
    life_bar_length = 675
    life_bar_y = 730
    lb_base_x = 370

    def __init__(self):
        if self.font == None:
            self.font = load_font('font/ENCR10B.TTF',16)
        if self.image == None:
            self.image = load_image('image/boss/boss_sun.png')
        if self.life_bar_image == None:
            self.life_bar_image = load_image('image/boss/boss_lifebar.png')
        self.x = 898
        self.y = 381
        self.y_plus = 10
        self.width = 252
        self.height = 801

        self.max_hp = 2000
        self.hp = self.max_hp
        self.life_per = self.hp // self.max_hp
        self.lb_real_x = Sun.lb_base_x
        self.lb_real_length = Sun.life_bar_length
        self.lb_now_x = Sun.lb_base_x

        self.state = Sun.NORMAL_STATE
        self.state_frame = 0
        self.state_total_frame = 0

        self.circle_x = self.x - 114
        self.circle_y = self.y - 30
        self.circle_radius = 318
        self.vibrate_degree = 0
        self.dead_x = 0

        self.live = True

        # 바운딩 박스 체크
        self.draw_bc_bool = False

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

        # 바운딩 서클
        self.circle_x = self.x + 226
        self.circle_y = self.y - 26

        self.state_frame = int(self.state_total_frame) % Sun.state_set[self.state]['total_frame']
        self.state_total_frame += Sun.state_set[self.state]['frame_per'] * self.state_set[self.state]['time_per'] * frame_time

        self.lb_real_length = (self.hp // (self.max_hp // 200)) * (Sun.life_bar_length // 200)

    def handle_event(self, event):
        # 바운딩서클 그리기
        if event.type == SDL_KEYDOWN and event.key == SDLK_F12:
            self.draw_bc_bool = not self.draw_bc_bool

        if event.type == SDL_KEYDOWN and event.key == SDLK_q:
            self.state_total_frame = 0
            self.state = Sun.ATTACK_STATE3
        if event.type == SDL_KEYDOWN and event.key == SDLK_w:
            self.state = Sun.NORMAL_STATE

    def get_bc(self):
        return self.circle_x, self.circle_y, self.circle_radius

    def draw_bc(self):
        draw_rectangle(self.circle_x - self.circle_radius, self.circle_y + self.circle_radius,
                       self.circle_x + self.circle_radius, self.circle_y - self.circle_radius)

    def draw(self, frame_time):
        self.image.clip_draw(self.state_frame * self.width,Sun.state_set[self.state]['draw_frame_num']* self.height, self.width,self.height,self.x ,self.y)
        self.font.draw(self.x - 200, self.y + 300, 'HP: %d' %self.hp, (255,255,0))
        if self.draw_bc_bool:
            self.draw_bc()

        self.life_bar_image.clip_draw(0, 90 , 705, 45, Sun.lb_base_x, Sun.life_bar_y)
        self.life_bar_image.clip_draw(0, 0 , Sun.life_bar_length, 45, Sun.lb_base_x, Sun.life_bar_y)
        self.life_bar_image.clip_draw(0, 45 , Sun.life_bar_length, 45, Sun.lb_base_x, Sun.life_bar_y, self.lb_real_length, 45)