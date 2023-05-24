from .widgets import *

widgets = dict()

def add_menu(nm):
    widgets[nm] = []

def draw_menu(window, nm):
    for i in widgets[nm]:
        i.draw(window)

def update_menu(events, nm):
    for i in widgets[nm]:
        i.update(events)

def add_widget(nm, widget):
    widgets[nm].append(widget)