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