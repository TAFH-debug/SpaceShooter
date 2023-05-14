import pygame

__objects = []

def get_objects():
    return __objects

def add_object(obj):
    __objects.append(obj)

def remove_object(obj):
    __objects.remove(obj)

def draw(window):
    for i in __objects:
        if hasattr(i, "draw"):
            i.draw(window)

def update():
    for i in __objects:
        i.update()

    for i in range(len(__objects)):
        if not hasattr(__objects[i], "hitbox"):
            continue
        for j in range(i + 1, len(__objects)):
            if not hasattr(__objects[j], "hitbox"):
                continue

            rc = pygame.Rect(__objects[i].hitbox)
            rc2 = pygame.Rect(__objects[j].hitbox)
            if rc.colliderect(rc2):
                __objects[i].handle_collide(__objects[j])
                __objects[j].handle_collide(__objects[i])
