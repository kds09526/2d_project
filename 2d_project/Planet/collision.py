from pico2d import *

import game_framework

from astronaut import Astronaut

def plate_collide(frametime, character, plate_left, plate_bottom, plate_right, plate_top):
    character_left, character_bottom, character_right, character_top = character.get_bb()
    if plate_left <= character_right and character_right <= plate_right:
        if character_bottom + (character.now_jump_speed * frametime) * 2 >= plate_top and character_bottom <= plate_top:
            return True, plate_top - character_bottom
    elif plate_left <= character_left and character_left <= plate_right:
        if character_bottom + (character.now_jump_speed * frametime) * 2 >= plate_top and character_bottom <= plate_top:
            return True, plate_top - character_bottom
    return False, 0