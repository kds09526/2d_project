import random
import json
import os

from pico2d import *
from astronaut import Astronaut
from plate import Plate
from boss import Sun
from bullet import Bullet

import game_framework
import space_map
import collision

name = "SunSceneState"

background_image = None
plate_timer = 0.0
plates = None
astronaut = None
sun = None
bullets = []
draw_bb = False
result_image = None

def enter():
    global background_image
    background_image = load_image('image/sun_stage_scene/SunSceneBackGround1.png')
    global result_image
    result_image = load_image('image/sun_stage_scene/result.png')

    global plates
    plates = [Plate(351, 187, 286, 72, 'image/sun_stage_scene/plate/sun_short_plate.png'),
              Plate(572, 346, 286, 72, 'image/sun_stage_scene/plate/sun_short_plate.png'),
              Plate(189, 505, 286, 72, 'image/sun_stage_scene/plate/sun_short_plate.png'),
              Plate(440, 37, 864, 73, 'image/sun_stage_scene/plate/sun_long_plate.png')]

    global astronaut
    astronaut = Astronaut(512, 500, 115)

    global sun
    sun = Sun()

def exit():
    global background_image
    del(background_image)
    global astronaut
    del(astronaut)
    global plates
    for plate in plates:
        del(plate)
    global sun
    del(sun)


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
                if event.type == SDL_KEYDOWN and event.key == SDLK_F12:
                    global draw_bb
                    draw_bb = not draw_bb
                astronaut.handle_event(event)
                global plates
                for plate in plates:
                    plate.handle_event(event)
                global bullets
                for bullet in bullets:
                    bullet.handle_event(event)
                global sun
                sun.handle_event(event)


def update(frame_time):
    global plate_timer
    global plates
    global astronaut
    global sun
    global bullets

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
    if sun.state == Sun.ATTACK_STATE3:
        astronaut.x += Astronaut.PULL_SPEED_PPS * frame_time;

    if astronaut.shot_frame == 1 and not astronaut.make_bullet:
        astronaut.make_bullet = True

    if astronaut.shot_frame == 2 and astronaut.make_bullet:
        bullets.append(Bullet(astronaut.weapon, astronaut.x, astronaut.y, astronaut.direction, draw_bb))
        astronaut.make_bullet = False

    for bullet in bullets:
        bullet.update(frame_time)
        if not (bullet.color == Bullet.RED):
            bullet.is_draw = not collision.bullet_colid(frame_time, bullet.color, bullet, sun)
        if not bullet.is_draw:
            bullets.remove(bullet)
            if bullet.direct == Bullet.RIGHT:
                sun.hp -= Bullet.Set[bullet.color]['damage']
                if sun.hp <= 0:
                    sun.hp = 0
                    if not sun.state == Sun.DEAD_STATE:
                        sun.state = Sun.DEAD_STATE
                        sun.dead_x = 0


    sun.update(frame_time)
    if not sun.live:
        game_framework.pop_state()
    #delay(0.3)

def draw(frame_time):
    clear_canvas()
    background_image.draw(512, 384)

    global plates
    for plate in plates:
        plate.draw(frame_time)

    for bullet in bullets:
        bullet.draw(frame_time)

    sun.draw(frame_time)
    astronaut.draw(frame_time)

    if sun.hp == 0:
        result_image.clip_draw(0, 190, 651, 190, 512, 384)
    elif astronaut.life == 0:
        result_image.clip_draw(0, 0, 651, 190, 512, 384)

    update_canvas()