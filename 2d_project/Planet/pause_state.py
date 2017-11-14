import game_framework
from pico2d import *


name = "PauseState"
image = None
logo_time = 0.0


def enter():
    global image
    open_canvas()
    image = load_image('pause.png')

def exit():
    global image
    del(image)
    close_canvas()

def update():
    global logo_time
    delay(0.01)
    logo_time += 0.01
    logo_time %= 2

def draw():
    global image
    global logo_time
    clear_canvas()
    if(logo_time < 1):
       image.draw(400,300)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.pop_state()


def pause(): pass


def resume(): pass




