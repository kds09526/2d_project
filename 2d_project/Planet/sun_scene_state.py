import random
import json
import os

from pico2d import *
from astronaut import Astronaut

import game_framework
import title_state
import collision

name = "SunSceneState"

background_image = None
plate_timer = 0.0
plates = None
short_plate_num = 0
astronaut = None

class Long_Plate:
    x = 440
    y = 37
    draw_bb_bool = False

    def __init__(self):
        self.image = load_image('sun_long_plate.png')

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_F12:
            self.draw_bb_bool = not self.draw_bb_bool

    def get_bb(self):
        return self.x - 432, self.y - 36, self.x + 432, self.y + 36

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw(self,frame_time):
        self.image.draw(self.x,self.y)
        if self.draw_bb_bool:
            self.draw_bb()

class Short_Plate:
    image = None
    x = None
    y = None
    draw_bb_bool = False

    def __init__(self):
        if self.image == None:
            self.image = load_image('sun_short_plate.png')

        global short_plate_num
        short_plate_num+=1
        if short_plate_num == 1:
            self.x,self.y = 351, 768 - 581
        elif short_plate_num == 2:
            self.x,self.y = 572, 768 - 422
        elif short_plate_num == 3:
            self.x,self.y = 189, 768 - 263
        if random.randint(0, 1) == 0:
            self.y_plus = 1
        else:
            self.y_plus = -1

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_F12:
            self.draw_bb_bool = not self.draw_bb_bool

    def get_bb(self):
        return self.x - 143, self.y - 36, self.x + 143, self.y + 36

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw(self,frame_time):
        self.image.draw(self.x,self.y)
        if self.draw_bb_bool:
            self.draw_bb()

def enter():
    global background_image
    background_image = load_image('SunSceneBackGround1.png')

    global plates
    plates = [Short_Plate() for i in range(3)]
    long_plate = [Long_Plate()]
    plates = plates + long_plate

    global astronaut
    astronaut = Astronaut()

def exit():
    global background_image
    del(background_image)
    global astronaut
    del(astronaut)
    global plates
    for plate in plates:
        del(plate)


def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            else:
                astronaut.handle_event(event)
                global plates
                for plate in plates:
                    plate.handle_event(event)


def update(frame_time):
    global plate_timer
    global plates
    global astronaut

    # 발판 충돌 체크
    if not(astronaut.jump_state == Astronaut.JUMP):
        for plate in plates:
            t_plate_left, t_plate_bottom, t_plate_right, t_plate_top = plate.get_bb()
            t_collide = False
            t_collide, astronaut.jump_gap = collision.plate_collide(frame_time, astronaut, t_plate_left, t_plate_bottom, t_plate_right, t_plate_top)
            if t_collide:
                astronaut.jump_state = Astronaut.NOT_JUMP
                astronaut.now_jump_speed = 0
                break
            astronaut.jump_state = Astronaut.FALLING

    astronaut.update(frame_time)

    #delay(0.3)

def draw(frame_time):
    clear_canvas()
    background_image.draw(512, 384)

    global plates
    for plate in plates:
        plate.draw(frame_time)

    astronaut.draw(frame_time)
    update_canvas()