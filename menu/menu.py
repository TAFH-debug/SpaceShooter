from .widgets import *

menu = list()

def draw_menu(window):
    for i in menu:
        i.draw(window)

def update_menu(events):
    for i in menu:
        i.update(events)

def add_widget(widget):
    menu.append(widget)