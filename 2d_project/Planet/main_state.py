import random
import json
import os

from pico2d import *

import game_framework
import title_state



name = "MainState"

boy = None
grass = None
font = None
pause_check = 1
image = None
Pimage = None
logo_time = 0.0

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)



class Boy:
    def __init__(self):
        self.x, self.y = 0, 90
        self.frame = 0
        self.image = load_image('run_animation.png')
        self.dir = 1

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        if self.x >= 800:
            self.dir = -1
        elif self.x <= 0:
            self.dir = 1

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


def enter():
    global boy, grass, Pimage
    boy = Boy()
    grass = Grass()
    Pimage = load_image('pause.png')


def exit():
    global boy, grass
    del(boy)
    del(grass)


def pause():
    global pause_check
    pause_check = -pause_check

    pass


def resume():
    pass


def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            pause()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)


def update():
    global image
    global logo_time
    delay(0.01)
    logo_time += 0.1
    logo_time %= 2

    if (pause_check > 0):
        boy.update()


def draw():
    global Pimage
    global logo_time
    clear_canvas()
    if (pause_check > 0):
        grass.draw()
        boy.draw()
    elif (pause_check < 0):
        if(logo_time < 1):
            Pimage.draw(400,300)
    update_canvas()






