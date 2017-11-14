import game_framework
import sun_scene_state
from pico2d import *


name = "TitleState"
image = None
running = True

def enter():
    global image
    image = load_image('title.png')

def exit():
    global image
    del(image)

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type,event.key) == (SDL_KEYDOWN,SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) ==(SDL_KEYDOWN, SDLK_SPACE):
               game_framework.change_state(sun_scene_state)


def draw(frame_time):
    global image
    clear_canvas()
    image.draw(512,384)
    update_canvas()

def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass






