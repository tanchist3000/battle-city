import pygame
import os
import sys
import random

import pygame.sprite

pygame.init()
current_path = os.path.dirname(__file__)
os.chdir(current_path)
WIDTH = 1200
HEIGHT = 800
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
lvl = 'game'

from load import *


def lvlGame():
    sc.fill("Black")
    brick_group.update()
    brick_group.draw(sc)
    iron_group.update()
    iron_group.draw(sc)
    water_group.update()
    water_group.draw(sc)
    enemy_group.update()
    enemy_group.draw(sc)
    player_group.update()
    player_group.draw(sc)
    flag_group.update()
    flag_group.draw(sc)
    Bullet_player_group.update()
    Bullet_player_group.draw(sc)
    Bullet_enemy_group.update()
    Bullet_enemy_group.draw(sc)
    bush_group.update()
    bush_group.draw(sc)
    pygame.display.update()


def drawMaps(nameFile):
    maps = []
    source = "game lvl/" + str(nameFile)
    with open(source, "r") as file:
        for i in range(0, 20):
            maps.append(file.readline().replace("\n", "").split(",")[0:-1])

    pos = [0, 0]
    for i in range(0, len(maps)):
        pos[1] = i * 40
        for j in range(0, len(maps[0])):
            pos[0] = 40 * j
            if maps[i][j] == '1':
                brick = Brick(brick_image, pos)
                brick_group.add(brick)
            elif maps[i][j] == '2':
                bush = Bush(bush_image, pos)
                bush_group.add(bush)
            elif maps[i][j] == '3':
                iron = Iron(iron_image, pos)
                iron_group.add(iron)
            elif maps[i][j] == '4':
                water = Water(water_image, pos)
                water_group.add(water)
            elif maps[i][j] == '7':
                flag = Flag(flag_image, pos)
                flag_group.add(flag)


class Brick(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if pygame.sprite.spritecollide(self, player_group, False):
            if player.dir == "left":
                player.rect.left = self.rect.right
            if player.dir == "right":
                player.rect.right = self.rect.left
            if player.dir == "top":
                player.rect.top = self.rect.bottom
            if player.dir == "bottom":
                player.rect.bottom = self.rect.top


class Bush(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Iron(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if pygame.sprite.spritecollide(self, player_group, False):
            if player.dir == "left":
                player.rect.left = self.rect.right
            elif player.dir == "right":
                player.rect.right = self.rect.left
            elif player.dir == "top":
                player.rect.top = self.rect.bottom
            elif player.dir == "bottom":
                player.rect.bottom = self.rect.top


class Water(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        if pygame.sprite.spritecollide(self, player_group, False):
            if player.dir == "left":
                player.rect.left = self.rect.right
            if player.dir == "right":
                player.rect.right = self.rect.left
            if player.dir == "top":
                player.rect.top = self.rect.bottom
            if player.dir == "bottom":
                player.rect.bottom = self.rect.top


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speed = 5
        self.dir = "top"
        self.timer_shot = 0
        self.frame = 0
        self.timer_anime = 0

        self.anime = False

    def update(self):
        self.timer_shot += 1
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            self.image = pygame.transform.rotate(player_image[self.frame], 90)
            self.rect.x -= self.speed
            self.dir = "left"
            self.anime = True

        elif key[pygame.K_d]:
            self.image = pygame.transform.rotate(player_image[self.frame], -90)
            self.rect.x += self.speed
            self.dir = "right"
            self.anime = True
        elif key[pygame.K_w]:
            self.image = pygame.transform.rotate(player_image[self.frame], 360)
            self.rect.y -= self.speed
            self.dir = "top"
            self.anime = True
        elif key[pygame.K_s]:
            self.image = pygame.transform.rotate(player_image[self.frame], -180)
            self.rect.y += self.speed
            self.dir = "bottom"
            self.anime = True
        else:
            self.anime = False

        if self.anime:
            self.timer_anime += 1
            if self.timer_anime / FPS > 0.1:
                if self.frame == len(player_image) - 1:
                    self.frame = 0
                else:
                    self.frame += 1
                self.timer_anime = 0

        if key[pygame.K_SPACE] and self.timer_shot / FPS > 1:
            bullet = Bullet_player(player_bullet, self.rect.center, self.dir)
            Bullet_player_group.add(bullet)
            self.timer_shot = 0


class Flag(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Bullet_player(pygame.sprite.Sprite):
    def __init__(self, image, pos, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = dir
        self.speed = 5
        self.anime = False
        self.timer_anime = 0
        self.frame = 0

    def update(self):
        if self.dir == 'left':
            self.rect.x -= self.speed
        elif self.dir == 'right':
            self.rect.x += self.speed
        elif self.dir == 'top':
            self.rect.y -= self.speed
        elif self.dir == 'bottom':
            self.rect.y += self.speed

        pygame.sprite.groupcollide(Bullet_player_group, brick_group, True, True)
        pygame.sprite.groupcollide(Bullet_player_group, water_group, False, False)
        pygame.sprite.groupcollide(Bullet_player_group, iron_group, True, False)
        pygame.sprite.groupcollide(Bullet_player_group, flag_group, True, True)
        pygame.sprite.groupcollide(Bullet_player_group, enemy_group, True, True)

        if pygame.sprite.spritecollide(self, enemy_group, dokill=True):
            self.anime = True
            self.speed = 0

class Bullet_enemy(pygame.sprite.Sprite):
    def __init__(self, image, pos, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.dir = dir
        self.speed = 5
        self.anime = False
        self.timer_anime = 0
        self.frame = 0

    def update(self):
        if self.dir == 'left':
            self.rect.x -= self.speed
        elif self.dir == 'right':
            self.rect.x += self.speed
        elif self.dir == 'top':
            self.rect.y -= self.speed
        elif self.dir == 'bottom':
            self.rect.y += self.speed

        pygame.sprite.groupcollide(Bullet_player_group, brick_group, True, True)
        pygame.sprite.groupcollide(Bullet_player_group, water_group, False, False)
        pygame.sprite.groupcollide(Bullet_player_group, iron_group, True, False)
        pygame.sprite.groupcollide(Bullet_player_group, flag_group, True, True)
        pygame.sprite.groupcollide(Bullet_player_group, enemy_group, True, True)

        if pygame.sprite.spritecollide(self, enemy_group, dokill=True):
            self.anime = True
            self.speed = 0

brick_group = pygame.sprite.Group()
bush_group = pygame.sprite.Group()
iron_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
Bullet_enemy_group = pygame.sprite.Group()
Bullet_player_group = pygame.sprite.Group()
player = Player(player_image[0], (200, 640))
player_group.add(player)

drawMaps('1.txt')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if lvl == 'game':
        lvlGame()
    clock.tick(FPS)