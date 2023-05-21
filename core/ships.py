from .objects import *


class PlayerShip(Ship):

    def __init__(self, keys):
        def offset(size):
            return Vector(-size.x / 2, 0)

        def offset2(size):
            return Vector(size.x / 2, 0)
        
        weapons = [Weapon(BulletType("images/laserBlue.png", 200, 2, Vector(5, 29)), offset, 200),
                        Weapon(BulletType("images/laserBlue.png", 200, 2, Vector(5, 29)), offset2, 200)]
        abilities = [LaserAbility(pygame.K_g, 10000, 1000)]

        super().__init__("images/playerShip.png", weapons, abilities)

        self.team = Team.PLAYER
        self.keys = keys

    def update(self):
        super().update()
        global player_pos
        
        set_x(self.center().x)
        set_y(self.center().y)
        set(self.center())

        pressed = pygame.key.get_pressed()
        
        for ability in self.abilities:
            ability.origin = (self.pos, self.size)
            ability.angle = self.angle
            if pressed[ability.key]:
                ability.use()
         
        if pygame.mouse.get_pressed()[0]:
            self.shoot(dn(Vector.from_tuple(pygame.mouse.get_pos())))
        if pressed[self.keys['up']] and self.vel.y > -0.5:
            self.impulse(Vector(0, -DEFAULT_SPEED))
        if pressed[self.keys['down']] and self.vel.y < 0.5:
            self.impulse(Vector(0, DEFAULT_SPEED))
        if pressed[self.keys['right']] and self.vel.x < 0.5:
            self.impulse(Vector(DEFAULT_SPEED, 0))
        if pressed[self.keys['left']] and self.vel.x > -0.5:
            self.impulse(Vector(-DEFAULT_SPEED, 0))
        if pressed[self.keys['debug']]:
            pass

        pos = pygame.mouse.get_pos()
        norm = normalize(self.center())
        self.angle = angle(pos[0] - norm.x, -(pos[1] - norm.y)) - 90


class AI(Ship):

    def __init__(self):

        def offset(size):
            return Vector(0, -size.y / 2)

        weapons = [Weapon(BulletType("images/laserRed.png", 1000, 2, Vector(5, 29)), offset, 100)]
        abilities = []

        super().__init__("./images/enemyBlack1.png", weapons, abilities)

    def update(self):
        Destroyable.update(self)

        pos = get()
        norm = self.center()
        self.angle = angle(pos.x - norm.x, -(pos.y - norm.y)) - 90

        velocity = 1
        self.vel = Vector(-velocity, 0).rotate(self.angle)
        self.pos += self.vel