import random
import json
import os
import math

from pico2d import *

import game_framework
import title_state
import sun_scene_state

name = "Space_Map"

back_ground_image = None

planets = None

class Planet:
    draw_bb_bool = False

    def __init__(self, degree, planet_radius, revolution_radius, revolution_speed, image_location):
        self.x = math.cos(degree) * revolution_radius + 400
        self.y = math.sin(degree) * revolution_radius + 384
        self.revolution_radius = revolution_radius
        self.revolution_speed = revolution_speed
        self.planet_radius = planet_radius
        self.degree = degree
        self.image = load_image(image_location)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_F12:
            self.draw_bb_bool = not self.draw_bb_bool

    def get_bb(self):
        return self.x - self.planet_radius, self.y - self.planet_radius, self.x + self.planet_radius, self.y + self.planet_radius

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def draw(self,frame_time):
        self.image.draw(self.x,self.y)
        if self.draw_bb_bool:
            self.draw_bb()

    def update(self, frame_time):
        self.degree += self.revolution_speed * frame_time
        self.degree %= 360
        self.x = math.cos(self.degree) * self.revolution_radius + 400
        self.y = math.sin(self.degree) * self.revolution_radius + 384

def enter():
    global background_image
    background_image = load_image('map_background.png')

    global planets
    planets = [Planet(random.randint(0, 360), 33, 0, 0, 'map_sun.png'),
               Planet(random.randint(0, 360), 22.5, 95, 1.1, 'map_earth.png'),
               Planet(random.randint(0, 360), 18, 160, 0.9, 'map_mars.png'),
               Planet(random.randint(0, 360), 31.5, 235, 0.7, 'map_jupiter.png'),
               Planet(random.randint(0, 360), 27, 320, 0.5, 'map_saturn.png')]

def exit():
    global background_image
    del (background_image)
    global planets
    for planet in planets:
        del(planet)

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
            elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
                game_framework.push_state(sun_scene_state)
            else:
                global planets
                for planet in planets:
                    planet.handle_event(event)

def update(frame_time):
    global planets
    for planet in planets:
        planet.update(frame_time)
    # delay(0.3)

def draw(frame_time):
    clear_canvas()
    background_image.draw(512, 384)
    global planets
    for planet in planets:
        planet.draw(frame_time)
    update_canvas()