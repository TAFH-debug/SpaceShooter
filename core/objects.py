import enum

import pygame
from . import object_manager
from .player import *
from .player import Vector

DEBUG = False

class Team(enum.Enum):
    PLAYER = "player"
    ENEMY = "enemy"

class ObjectType(enum.Enum):
    BULLET = "bullet"
    SHIP = "ship"
    COLLIDEABLE = "collideable"

class HitboxType(enum.Enum):
    LINE = "line"
    BOX = "box"


class Object:

    def __init__(self, path, size: Vector=None):
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        if not (size == None):
            self.sprite = pygame.transform.scale(pygame.image.load(path).convert_alpha(), size.to_tuple())
            self.size = size
        else:
            self.sprite = pygame.image.load(path).convert_alpha()
            self.size = Vector.from_tuple(self.sprite.get_size())
        self.angle = 0
        self.hitbox = (0, 0, 0, 0)
        self.hitbox_type = HitboxType.BOX
        
    def draw(self, window):
        rs, rect = rot_center(self.sprite, self.angle, self.center())
        nzed = normalize(Vector(rect.x, rect.y))
        rect.x = nzed.x
        rect.y = nzed.y
        if DEBUG:
            pygame.draw.rect(window, (0, 255, 0), self.hitbox, 1)
        self.hitbox = rect
        window.blit(rs, rect)
    
    def update(self):
        pass

    def center(self):
        return self.pos + Vector(self.size.x / 2, self.size.y / 2)

    def handle_collide(self, other):
        pass


class GameObject(Object, PhysicalBody):
    
    def __init__(self, path, ot, team=Team.PLAYER, size: Vector = None):
        Object.__init__(self, path, size)
        PhysicalBody.__init__(self)
        self.team = team
        self.object_type = ot

    def handle_collide(self, other):
        if other.object_type == ObjectType.COLLIDEABLE:
            self.pos -= self.vel - self.a

class Destroyable:
    
    def __init__(self, max_health):
        self.health = max_health
        self.max_health = max_health

    def draw(self, window):
        norm = normalize(self.pos)
        pygame.draw.rect(window, (255, 0, 0), (norm.x, norm.y - 10, self.size.x, 10))
        pygame.draw.rect(window, (0, 255, 0), (norm.x, norm.y - 10, self.size.x * self.health / self.max_health, 10))

    def update(self):
        if self.health <= 0:
            object_manager.remove_object(self)


class BulletType:

    def __init__(self, path, lifetime, speed, damage, size=None):
        self.path = path
        self.damage = damage
        self.speed = speed
        self.lifetime = lifetime
        self.size = size

    def create_instance(self, origin, angle, parent):
        bullet = Bullet(parent, self.path, self.lifetime, self.speed, self, origin.x, origin.y, angle, self.damage, self.size)
        object_manager.add_object(bullet)

class Ability:
    
    def __init__(self, key, cooldown: int, use_time: int):
        self.parent = None
        self.size = (0, 0)
        self.object_type = ObjectType.BULLET
        self.key = key
        self.cooldown = Counter(cooldown, False)
        self.use_time = Counter(use_time)
        self.using = False
        self.origin = Vector(0, 0), Vector(0, 0)
        self.angle = 0
        self.hitbox = (0, 0, 0, 0)
    
    def use(self):
        if not self.cooldown.done():
            return
        self.using = True
        
    def update(self):
        if self.use_time.done():
            self.using = False
        elif self.using == True:
            self.use_time.step()
        self.cooldown.step()

    def draw(self, window):
        pass

class SuperAbility(Ability):
    
    def __init__(self, key, cooldown: int, use_time: int):
        super().__init__(key, cooldown, use_time)
        self.tp = BulletType("./images/spaceMissiles19.png", 1000, 0.5, 50, Vector(40, 80))
    
    def use(self):
        if not self.cooldown.done():
            return
        self.tp.create_instance(self.parent.center(), self.parent.angle, self.parent)
        self.using = True
        

class LaserAbility(Ability):
    
    def __init__(self, key, cooldown: int, use_time: int):
        super().__init__(key, cooldown, use_time)
        self.damage = 1
        self.width = 30
        self.height = 200
    
    def update(self):
        super().update()     
        
    def draw(self, window):
        if self.using:
            center_offset = Vector(self.origin[1].x / 2, self.origin[1].y / 2) + self.origin[0]
            start_pos = normalize((Vector(0, -self.origin[1].y / 2).rotate(self.angle - 90) + center_offset)).to_tuple()
            end_pos = normalize((Vector(0, -(self.origin[1].y / 2 + self.height)).rotate(self.angle - 90) + center_offset)).to_tuple()
            pygame.draw.line(window, (255, 0, 0),
                             start_pos,
                             end_pos,
                             int(5 * math.sin(self.use_time.counter / 100) + self.width - 5))
            pygame.draw.line(window, (255, 125, 0),
                             start_pos,
                             end_pos,
                             10)
            pygame.draw.circle(window, (255, 0, 0), end_pos, int(5 * math.sin(self.use_time.counter / 100) + 25) / 2)

class Weapon:

    def __init__(self, bullet_type, offset_calc, cooldown):
        self.bullet_type = bullet_type
        self.offset_calc = offset_calc
        self.cooldown = Counter(cooldown, False)

    def update(self):
        self.cooldown.step()

    def shoot(self, target: Vector, origin: Vector, angle, parent):
        if not self.cooldown.done():
            return
        self.bullet_type.create_instance(origin, angle, parent)

class Bullet(GameObject):

    def __init__(self, parent, path, lifetime, speed, btype, x, y, angle, damage, size=None):
        GameObject.__init__(self, path, ObjectType.BULLET, parent.team, size)
        self.damage = damage
        self.parent = parent
        self.pos = Vector(x, y)
        self.lifetime = Counter(lifetime)
        self.speed = speed
        self.btype = btype
        self.angle = angle
        self.vel = Vector(-self.speed, 0).rotate(self.angle)

    def update(self):
        if self.lifetime.step():
            object_manager.remove_object(self)
            return
        self.pos += self.vel

    def handle_collide(self, other):
        if other.team != self.team:
            object_manager.remove_object(self)

class Ship(GameObject, Destroyable):
    
    def __init__(self, path, weapons=[], abilities=[], size=None):
        GameObject.__init__(self, path, ObjectType.SHIP, Team.ENEMY, size)
        Destroyable.__init__(self, 100)
        self.weapons = weapons
        self.coords = []
        self.abilities = abilities
        self.__gcounter = 0

        for ability in abilities:
            ability.parent = self
            object_manager.add_object(ability)

        for weapon in weapons:
            object_manager.add_object(weapon)
        
    def shoot(self, target):
        for weapon in self.weapons:
            offset = weapon.offset_calc(self.size).rotate(self.angle + 90)
            weapon.shoot(target, offset + self.center(), self.angle, self)

    def update(self):
        Destroyable.update(self)
        PhysicalBody.update(self)

        if len(self.coords) == 0 or (self.pos.x != self.coords[-1].x or self.pos.y != self.coords[-1].y):
            self.coords.append(self.pos + Vector(0, self.size.y / 2).rotate(self.angle - 90) + Vector(self.size.x / 2, self.size.y / 2))
            if len(self.coords) > 100:
                self.coords.pop(0)

        pos = normalize(self.center())
        self.hitbox = (pos.x - 37.5, pos.y - 37.5, 75, 75)

    def draw(self, window):
        Destroyable.draw(self, window)

        cpos = normalize((self.pos + Vector(0, self.size.y / 2).rotate(self.angle - 90) + Vector(self.size.x / 2, self.size.y / 2))).to_tuple()
        pygame.draw.circle(window, (255, 75, 0), cpos, abs(5 * math.sin(self.__gcounter / 100)) + 10)
        pygame.draw.circle(window, (255, 125, 0), cpos, 5)
        
        self.__gcounter += 1
        
        idx = 0
        for i in self.coords:
            idx += 1
            pygame.draw.circle(window, (255, 0, 0), normalize(i).to_tuple(), 7.5 * idx / 100)
            
        super().draw(window)

    def handle_collide(self, other):
        GameObject.handle_collide(self, other)
        if other.object_type == ObjectType.BULLET and self.team != other.team:
            self.health -= other.damage
