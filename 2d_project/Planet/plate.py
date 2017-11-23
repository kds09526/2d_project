import random
from pico2d import *

class Plate:
    def __init__(self, x, y, width, height, image_location):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.image = load_image(image_location)
        self.draw_bb_bool = False

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_F12:
            self.draw_bb_bool = not self.draw_bb_bool

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw(self,frame_time):
        self.image.draw(self.x,self.y)
        if self.draw_bb_bool:
            self.draw_bb()