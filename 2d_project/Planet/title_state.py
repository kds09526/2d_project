import game_framework
import space_map

import random
from pico2d import *
from astronaut import Astronaut


name = "TitleState"
image = None
running = True

astronaut = None

menu_button = None

class Menu_Button:
    x = 0
    y = 0
    width = 0
    height = 0
    draw_bb_bool = False

    # 프레임 설정
    TIME_PER_MOVE = 1
    MOVE_PER_TIME = 1.0 / TIME_PER_MOVE
    FRAME_PER_MOVE = 8

    move_total_frame = 0
    move_frame = 0

    def __init__(self, x, y, width, height, image_name):
        self.image = load_image(image_name)
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.move_total_frame = random.randint(0,8)

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

def enter():
    global image
    image = load_image('title_background.png')
    global astronaut
    astronaut = Astronaut(512, 100, 68)

    global menu_button
    menu_button = [Menu_Button(500, 500, 435, 140, 'title_name.png')]

def exit():
    global image
    del(image)
    global astronaut
    del(astronaut)

    global menu_button
    for button in  menu_button:
        del(button)

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type,event.key) == (SDL_KEYDOWN,SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) ==(SDL_KEYDOWN, SDLK_SPACE):
                astronaut.reset(512, 100)
                game_framework.push_state(space_map)
            else:
                astronaut.handle_event(event)
                global menu_button
                for button in menu_button:
                    button.handle_event(event)

def draw(frame_time):
    global image, astronaut
    clear_canvas()
    image.draw(512,384)

    global menu_button
    for button in menu_button:
        button.draw(frame_time)

    astronaut.draw(frame_time)
    update_canvas()

def update(frame_time):
    global astronaut
    astronaut.update(frame_time)
    global menu_button
    for button in menu_button:
        button.update(frame_time)


def pause():
    pass


def resume():
    pass






