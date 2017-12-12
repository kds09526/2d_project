from pico2d import *

import game_framework

from astronaut import Astronaut
from plate import Plate
from menu_button import Menu_Button
from bullet import Bullet
from boss import Sun

def circle_collid(cirAx, cirAy, cirAradius, cirBx, cirBy, cirBradius):
    dis = math.sqrt((cirAx - cirBx) * (cirAx - cirBx) + (cirAy - cirBy) * (cirAy - cirBy))
    if dis <= cirAradius + cirBradius:
        return True
    return False

def plate_collide(frame_time, character, plate):
    character_left, character_bottom, character_right, character_top = character.get_bb()
    plate_left, plate_bottom, plate_right, plate_top = plate.get_bb()
    if plate_left <= character_right and character_right <= plate_right:
        if character_bottom + (character.now_jump_speed * frame_time) * 2 >= plate_top and character_bottom <= plate_top:
            return True, plate_top - character_bottom
    elif plate_left <= character_left and character_left <= plate_right:
        if character_bottom + (character.now_jump_speed * frame_time) * 2 >= plate_top and character_bottom <= plate_top:
            return True, plate_top - character_bottom
    return False, 0

def button_collid(frame_time, character, button):
    character_left, character_bottom, character_right, character_top = character.get_bb()
    button_left, button_bottom, button_right, button_top = button.get_bb()

    if character_left > button_right: return False
    if character_right < button_left: return False
    if character_top < button_bottom : return False
    if character_bottom > button_top : return False
    return True

def bullet_colid(frame_time, color, bullet, sun):
    sun_x, sun_y, sun_radius = sun.get_bc()
    bullet_left, bullet_bottom, bullet_right, bullet_top = bullet.get_bb()
    if color == Bullet.RED:
        pass
    else:
        if bullet_bottom >= sun_y:
            return circle_collid(bullet_right - 20, bullet_bottom, 0, sun_x, sun_y, sun_radius)
        else:
            return circle_collid(bullet_right - 20, bullet_top, 0, sun_x, sun_y, sun_radius)