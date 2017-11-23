import random
from pico2d import *

class Astronaut:
    image = None

    # 제일아래 발판
    last_plate = 0

    # 거리 환산
    PIXEL_PER_METER = (1 / 0.03)  # 1 pixel 3 cm

    # 바운딩 박스 체크
    draw_bb_bool = False

    # 걷는 속도
    RUN_SPEED_KMPH = 25  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    # 공격 여부 (False == 1, True = 세로 0,1 반복)
    is_shot = False
    shot_frame = 0
    shot_total_frame = 0
    # 무기 프레임설정
    TIME_PER_SHOT = 2
    SHOT_PER_TIME = 1.0 / TIME_PER_SHOT
    FRAME_PER_SHOT = 2
    NORMAL_WEAPON, PURPLE_WEAPON, YELLOW_WEAPON, GREAN_WEAPON, RED_WEAPON = 0, 3, 6, 9, 12
    weapon = NORMAL_WEAPON
    def weapon_change(self):
        if(self.weapon == self.NORMAL_WEAPON):
            self.TIME_PER_SHOT = 2
        elif(self.weapon == self.PURPLE_WEAPON):
            self.TIME_PER_SHOT = 3
        elif(self.weapon == self.YELLOW_WEAPON):
            self.TIME_PER_SHOT = 5
        elif(self.weapon == self.GREAN_WEAPON):
            self.TIME_PER_SHOT = 2.5
        elif(self.weapon == self.RED_WEAPON):
            self.TIME_PER_SHOT = 1
        self.SHOT_PER_TIME = 1.0 / self.TIME_PER_SHOT

    # 방향
    LEFT_DIRECT, RIGHT_DIRECT, FRONT_DIRECT = 6, 3 ,0
    direction = RIGHT_DIRECT

    # 걷기 프레임 설정 (False == 1, True = 가로 0,1,2 반복)
    is_move = 0
    move_frame = 0
    move_total_frame = 0
    TIME_PER_MOVE = 3.8
    MOVE_PER_TIME = 1.0 / TIME_PER_MOVE
    FRAME_PER_MOVE = 3

    # 점프 관련
    NOT_JUMP, JUMP, FALLING = 0, 1, 2
    jump_state = FALLING
    now_jump_speed = 0
    jump_gap = 0
    down_key = False

    GRAVITY_ACCELERATION_MPH = 98

    JUMP_SPEED_KMPH = 20  # Km / Hour
    JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
    JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
    JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

    JUMP_MOVE_SPEED_KMPH = 15  # Km / Hour
    JUMP_MOVE_SPEED_MPM = (JUMP_MOVE_SPEED_KMPH * 1000.0 / 60.0)
    JUMP_MOVE_SPEED_MPS = (JUMP_MOVE_SPEED_MPM / 60.0)
    JUMP_MOVE_SPEED_PPS = (JUMP_MOVE_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self, x, y, last_plate):
        if self.image == None:
            self.image = load_image('image/astronaut/astronaut.png')
            self.x, self.y = x, y
            self.last_plate = last_plate

    def reset(self, x, y):
        self.x, self.y = x, y
        self.direction = Astronaut.RIGHT_DIRECT
        self.is_move = 0
        self.move_frame = 0
        self.move_total_frame = 0
        self.jump_state = Astronaut.FALLING
        self.now_jump_speed = 0
        self.jump_gap = 0
        self.is_shot = False
        self.shot_frame = 0
        self.shot_total_frame = 0

    def update(self, frame_time):
        # 공격
        if self.is_shot == True:
            self.shot_frame = int(self.shot_total_frame) % 2 + 1
            self.shot_total_frame += Astronaut.FRAME_PER_SHOT * self.TIME_PER_SHOT * frame_time

        # 이동
        if self.is_move == 0:
            self.move_frame = 1
        else:
            self.move_total_frame += Astronaut.FRAME_PER_MOVE * self.TIME_PER_MOVE * frame_time
            if self.direction == self.LEFT_DIRECT:
                self.move_frame = 2 - int(self.move_total_frame) % 3
                if self.jump_state == Astronaut.JUMP or self.jump_state == Astronaut.FALLING:
                    self.x -= self.JUMP_MOVE_SPEED_PPS * frame_time
                else:
                    self.x -= self.RUN_SPEED_PPS * frame_time
                self.x = max(self.x, 16)
            else:
                self.move_frame = int(self.move_total_frame) % 3
                if self.jump_state == Astronaut.JUMP or self.jump_state == Astronaut.FALLING:
                    self.x += self.JUMP_MOVE_SPEED_PPS * frame_time
                else:
                    self.x += self.RUN_SPEED_PPS * frame_time
                self.x = min(self.x, 1006)

        # 점프
        if self.jump_state == Astronaut.JUMP or self.jump_state == Astronaut.FALLING:
            self.move_frame = 2
            if self.jump_state == Astronaut.JUMP:
                self.now_jump_speed = self.now_jump_speed - Astronaut.GRAVITY_ACCELERATION_MPH * frame_time
                self.y += self.now_jump_speed * frame_time
                if self.now_jump_speed <= 0:
                    self.jump_state = Astronaut.FALLING
            elif self.jump_state == Astronaut.FALLING:
                self.now_jump_speed = self.now_jump_speed + Astronaut.GRAVITY_ACCELERATION_MPH * frame_time
                self.y -= self.now_jump_speed * frame_time
        elif self.jump_gap > 0 and not(self.jump_state == self.JUMP):
            self.y += self.jump_gap
            self.jump_gap = 0
        if self.y <= self.last_plate:
            self.y = self.last_plate
            self.jump_state = Astronaut.NOT_JUMP

    def handle_event(self, event):
        # 바운딩박스 그리기
        if event.type == SDL_KEYDOWN and event.key == SDLK_F12:
            self.draw_bb_bool = not self.draw_bb_bool

        # 방향전환
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            self.direction = self.LEFT_DIRECT
            self.is_move += 1
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            self.is_move -= 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            self.direction = self.RIGHT_DIRECT
            self.is_move += 1
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            self.is_move -= 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DOWN:
            self.down_key = True
        elif event.type == SDL_KEYUP and event.key == SDLK_DOWN:
            self.down_key = False

        # 무기 교체
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            self.weapon = self.NORMAL_WEAPON
            self.weapon_change()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            self.weapon = self.PURPLE_WEAPON
            self.weapon_change()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            self.weapon = self.YELLOW_WEAPON
            self.weapon_change()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_4:
            self.weapon = self.GREAN_WEAPON
            self.weapon_change()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_5:
            self.weapon = self.RED_WEAPON
            self.weapon_change()

        # 총발사
        elif event.type == SDL_KEYDOWN and event.key == SDLK_c:
            self.is_shot = True
        elif event.type == SDL_KEYUP and event.key == SDLK_c:
            self.is_shot = False
            self.shot_total_frame = 0
            self.shot_frame = 0

        # 점프
        elif event.type == SDL_KEYDOWN and event.key == SDLK_x and self.jump_state == Astronaut.NOT_JUMP:
            if self.down_key == False:
                self.now_jump_speed = Astronaut.JUMP_SPEED_PPS
                self.jump_state = Astronaut.JUMP
            else:
                self.y -= 0.5
                self.jump_state = Astronaut.FALLING

    def get_bb(self):
        return self.x - 18, self.y - 42, self.x + 18, self.y + 27

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw(self,frame_time):
        self.image.clip_draw((self.weapon * 72) + self.move_frame * 72, (self.direction - self.shot_frame) * 96,72, 96, self.x, self.y)
        if self.draw_bb_bool:
            self.draw_bb()
            draw_rectangle(0,self.last_plate - 42,1024,0)
