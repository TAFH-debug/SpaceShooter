import pygame

from .physics import *

keys1 = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "right": pygame.K_d,
    "left": pygame.K_a,
    "debug": pygame.K_f
}

class Camera:
    
    def __init__(self):
        self.pos = Vector(0, 0)

__cam = Camera()
player_pos = Vector(0, 0)

def normalize(pos: Vector) -> Vector:
    display = pygame.display.get_surface()
    width, height = display.get_size()
    return Vector((pos.x - __cam.pos.x + width / 2), (pos.y - __cam.pos.y + height / 2))

def dn(pos: Vector) -> Vector:
    display = pygame.display.get_surface()
    width, height = display.get_size()
    return Vector((pos.x + __cam.pos.x - width / 2), (pos.y + __cam.pos.y - height / 2))

def set_x(dx):
    __cam.pos.x = dx

def set_y(dy):
    __cam.pos.y = dy

def add(dp: Vector):
    __cam.pos += dp

def set(vc: Vector):
    global player_pos
    player_pos = vc

def get() -> Vector:
    return player_pos