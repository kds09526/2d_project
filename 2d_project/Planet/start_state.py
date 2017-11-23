import game_framework
import title_state
from pico2d import *


name = "StartState"
logo_image1 = None
logo_image2 = None
logo_time = 0.0


def enter():
    global logo_image1, logo_image2
    open_canvas(1024,768)
    logo_image1 = load_image('image/logo_scene/logo1.png')
    logo_image2 = load_image('image/logo_scene/logo2.png')

def exit():
    global logo_image1, logo_image2
    del(logo_image1)
    del(logo_image2)
    close_canvas()

def update(frame_time):
    global logo_time

    if (logo_time > 2):
        logo_time = 0
        game_framework.push_state(title_state)
    delay(0.01)
    logo_time += 0.01

def draw(frame_time):
    global logo_image1
    global logo_image2
    clear_canvas()
    if(logo_time < 1):
        logo_image1.draw(512, 384)
    else:
        logo_image2.draw(512, 384)
    update_canvas()

def handle_events(frame_time):
    events = get_events()
    pass


def pause(): pass


def resume(): pass




