import pygame

class Text:

    def __init__(self, text, font, color):
        self.text = text
        self.font = font
        self.color = color

class Clicked:

    def __init__(self, color, border):
        self.color = color
        self.border = border

class Border:
    
    def __init__(self, width, color, radius):
        self.width = width
        self.color = color
        self.radius = radius

class Label:

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw(self, window):
        txt = self.text.font.render(self.text.text, False, self.text.color)
        sz = txt.get_size()
        window.blit(txt, (self.x, self.y) + sz)

    def update(self, events):
        pass


class Button:
    
    def __init__(self, x, y, width, height, clicked, color=(255, 0, 0), border: Border=None, cmd=lambda: (), 
                 text=Text("", None, (0, 0, 0))):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.text = text
        self.border = border
        self.color = color
        self.cmd = cmd
        self.clicked = clicked
        self.is_clicked = False
        
    def draw(self, window):
        color = (self.color, self.clicked.color)[self.is_clicked]
        border = (self.border, self.clicked.border)[self.is_clicked]
        if border:
            pygame.draw.rect(window, color, (self.x, self.y, self.width, self.height), 0, border.radius)
            bw = border.width
            pygame.draw.rect(window, border.color, (self.x - bw, self.y - bw, self.width + bw, self.height + bw), bw, border.radius)
        else:
            pygame.draw.rect(window, color, (self.x, self.y, self.width, self.height))
        
        txt = self.text.font.render(self.text.text, False, self.text.color)
        window.blit(txt, (self.x + (self.width - txt.get_width()) / 2, self.y + (self.height - txt.get_height()) / 2) + txt.get_size())

    def update(self, events):
        rc = pygame.Rect(self.x, self.y, self.width, self.height)
        for i in events:
            if i.type == pygame.MOUSEBUTTONDOWN and rc.collidepoint(pygame.mouse.get_pos()):
                self.is_clicked = True
            if i.type == pygame.MOUSEBUTTONUP and self.is_clicked:
                self.is_clicked = False
                self.cmd()