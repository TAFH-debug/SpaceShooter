__objects = []

def get_objects():
    return __objects

def add_object(obj):
    __objects.append(obj)

def remove_object(obj):
    __objects.remove(obj)

def draw(window):
    for i in __objects:
        i.draw(window)

def update():
    for i in __objects:
        i.update()