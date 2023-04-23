import math
import pygame

def isSameS(a, b):
    return not ((a >= 0) ^ (b >= 0))

def angle(x, y):
    deg = math.degrees(math.atan2(y, x))
    return deg % 360

def rot_center(image, angle, v):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (v.x, v.y)).center)

    return rotated_image, new_rect


class Counter:
    initial: int
    counter: int

    def __init__(self, initial, start=True):
        self.initial = initial
        self.counter = (0, initial)[start]

    def restart(self):
        self.counter = self.initial
   
    def step(self) -> bool:
        if self.counter == 0:
            return True
        self.counter -= 1
        return False
    
    def done(self) -> bool:
        if self.counter == 0:
            self.restart()
            return True
        return False
