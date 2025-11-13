import pygame

class Shield(object):
    def __init__(self, x, y, width, height, assets):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.assets = assets
        self.vel = 1.4
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        self.hitbox = (self.x, self.y, self.width, self.height)
        win.blit(self.assets.shield, (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

class ScoreMultiplier(object):
    def __init__(self, x, y, width, height, assets):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.assets = assets
        self.vel = 1.4
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        self.hitbox = (self.x, self.y, self.width, self.height)
        win.blit(self.assets.score_multiplier, (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1] and rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False
