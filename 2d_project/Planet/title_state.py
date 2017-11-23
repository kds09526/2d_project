import game_framework
import space_map

import random
from pico2d import *

from astronaut import Astronaut
from menu_button import Menu_Button
import collision

name = "TitleState"
image = None
running = True

astronaut = None

menu_button = None

def enter():
    global image
    image = load_image('image/title_scene/title_background.png')
    global astronaut
    astronaut = Astronaut(512, 100, 68)

    global menu_button
    menu_button = [Menu_Button(500, 525, 435, 140, 'image/title_scene/button/title_name.png', None),
                   Menu_Button(512, 275, 180, 164, 'image/title_scene/button/start_button.png', space_map),
                   Menu_Button(236, 275, 156, 164, 'image/title_scene/button/help_button.png', None),
                   Menu_Button(788, 275, 156, 164, 'image/title_scene/button/exit_button.png', None)]

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

    if astronaut.is_shot == True:
        for button in  menu_button:
            t_button_left, t_button_bottom, t_button_right, t_button_top = button.get_bb()
            if collision.button_collid(frame_time, astronaut, t_button_left, t_button_bottom, t_button_right, t_button_top):
                if button.scene == None:
                    game_framework.quit()
                else:
                    astronaut.reset(512, 100)
                    game_framework.push_state(button.scene)

def pause():
    pass


def resume():
    pass






