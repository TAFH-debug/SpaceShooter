import pygame


class Border:
    
    def __init__(self, width, color, radius):
        self.width = width
        self.color = color
        self.radius = radius
        
class Button:
    
    def __init__(self, x, y, width, height, color=(255, 0, 0), border: Border=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.border = border
        self.color = color
        
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        if self.border:
            bw = self.border.width
            pygame.draw.rect(window, self.border.color, (self.x - bw, self.y - bw, self.width + bw, self.height + bw), bw, self.border.radius)
    
    def update(self):
        pass