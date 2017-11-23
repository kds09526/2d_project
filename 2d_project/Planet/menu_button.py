import random
from pico2d import *
from astronaut import Astronaut

class Menu_Button:
    # 프레임 설정
    TIME_PER_MOVE = 1
    MOVE_PER_TIME = 1.0 / TIME_PER_MOVE
    FRAME_PER_MOVE = 8

    def __init__(self, x, y, width, height, image_name, scene):
        self.image = load_image(image_name)
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.move_total_frame = random.randint(0,8)
        self.scene = scene

        self.draw_bb_bool = False
        self.move_total_frame = 0
        self.move_frame = 0

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_F12:
            self.draw_bb_bool = not self.draw_bb_bool

    def get_bb(self):
        return self.x - (self.width / 2), self.y - (self.height / 2), self.x + (self.width / 2), self.y + (self.height / 2)

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def update(self, frame_time):
        self.move_total_frame += Astronaut.FRAME_PER_MOVE * self.TIME_PER_MOVE * frame_time
        self.move_frame = int(self.move_total_frame) % 8

    def draw(self,frame_time):
        self.image.clip_draw(self.move_frame * self.width, 0, self.width, self.height, self.x, self.y)
        if self.draw_bb_bool:
            self.draw_bb()
