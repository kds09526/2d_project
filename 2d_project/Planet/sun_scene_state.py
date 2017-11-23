import random
import json
import os

from pico2d import *
from astronaut import Astronaut
from plate import Plate

import game_framework
import space_map
import collision

name = "SunSceneState"

background_image = None
plate_timer = 0.0
plates = None
astronaut = None

def enter():
    global background_image
    background_image = load_image('image/sun_stage_scene/SunSceneBackGround1.png')

    global plates
    plates = [Plate(351, 187, 286, 72, 'image/sun_stage_scene/plate/sun_short_plate.png'),
              Plate(572, 346, 286, 72, 'image/sun_stage_scene/plate/sun_short_plate.png'),
              Plate(189, 505, 286, 72, 'image/sun_stage_scene/plate/sun_short_plate.png'),
              Plate(440, 37, 864, 73, 'image/sun_stage_scene/plate/sun_long_plate.png')]

    global astronaut
    astronaut = Astronaut(512, 500, 115)

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
                game_framework.pop_state()
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
            t_collide = False
            t_collide, astronaut.jump_gap = collision.plate_collide(frame_time, astronaut, plate)
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