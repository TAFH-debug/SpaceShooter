import pygame

from physics import *
from objects import *
import object_manager

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