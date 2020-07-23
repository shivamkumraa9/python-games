import pygame
import sys
import os
from math import pi as PI
import random


pygame.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
RED = (241, 73, 73)
GREEN = (120, 197, 243)
BLUE = (181, 104, 173)
HIGH_SCORE = (226, 226, 226)
BLACK = (0, 0, 0)
YELLOW = (233, 218, 122)
COLORS = [WHITE, RED, GREEN, BLUE, YELLOW]
BGCOLOR = (18, 18, 18)
width = 480
height = 500

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Color Escape")
clock = pygame.time.Clock()



class Block(pygame.sprite.Sprite):
    def __init__(self, col, x, y, xspeed):
        self.col = col
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((120, 20))
        self.image.fill(self.col)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.yspeed = 0
        self.xspeed = xspeed

    def update(self):
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        if self.rect.right == 0:
            self.rect.left = width
        elif self.rect.left == width:
            self.rect.right = 0
        if self.rect.top == width - 100:
            self.kill()


class ColorChanger(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.col = random.choice(COLORS)
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.col, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.rect.center = (250, 180)


class Player(pygame.sprite.Sprite):
    def __init__(self, col):
        self.col = col
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.col, (15, 15), 15)
        self.rect = self.image.get_rect()
        self.rect.center = (250, 450)
        self.vel = 0
        self.score = 0

    def update(self):
        pygame.draw.circle(self.image, self.col, (15, 15), 15)
        self.vel += 0.8
        self.rect.centery += self.vel
        if self.rect.centery > 450:
            self.rect.centery = 450
        if self.rect.centery < 20:
            self.rect.centery = 20
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            self.rect.centery += -16
            self.vel = 0


def refresh_vars():
    global all_sprites, blocks, color_changer, p, c
    window.fill(BGCOLOR)
    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    color_changer = pygame.sprite.Group()

    make_blocks(80)
    make_blocks(250)
    p = Player(RED)
    c = ColorChanger()

    all_sprites.add(p)
    all_sprites.add(c)
    color_changer.add(c)


def draw_txt(surf, text, size, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, HIGH_SCORE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def endgame():
    end_run = True
    window.fill(BGCOLOR)
    while end_run:
        keystate = pygame.key.get_pressed()
        for i in pygame.event.get():
            if i.type == pygame.QUIT or keystate[pygame.K_e]:
                sys.exit()
        if keystate[pygame.K_a]:
            end_run = False
        window.fill(BGCOLOR)
        try:
            with open("highscore.txt", 'r') as file:
                highscore_ = int(file.readline())
        except:
            with open("highscore.txt", 'w') as file:
                file.write(str(p.score))
            highscore_ = p.score
        if highscore_ < p.score:
            with open("highscore.txt", 'w') as file:
                file.write(str(p.score))
            highscore_ = p.score

        draw_txt(window, "Game Over !!", 70, width / 2, 50)
        draw_txt(window, f"Score = {p.score}", 30, width / 2, 200)
        draw_txt(window, f" HighScore = {highscore_}", 30, width / 2, 250)
        draw_txt(window, "Press 'a' to Play Again and 'e' to exit ", 20, width / 2, 450)
        pygame.display.flip()
    refresh_vars()


def make_blocks(height_):
    x_speed = random.choice([-5, 5])
    random.shuffle(COLORS)
    b = Block(COLORS[0], 0, height_, x_speed)
    r = Block(COLORS[1], 120, height_, x_speed)
    w = Block(COLORS[2], 240, height_, x_speed)
    g = Block(COLORS[3], 360, height_, x_speed)
    y = Block(COLORS[4], 480, height_, x_speed)
    all_sprites.add(b)
    all_sprites.add(g)
    all_sprites.add(w)
    all_sprites.add(r)
    all_sprites.add(y)
    blocks.add(b)
    blocks.add(g)
    blocks.add(w)
    blocks.add(r)
    blocks.add(y)


all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
color_changer = pygame.sprite.Group()

make_blocks(80)
make_blocks(250)
p = Player(RED)
c = ColorChanger()

all_sprites.add(p)
all_sprites.add(c)
color_changer.add(c)

running = True
while running:
    clock.tick(26)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False

    all_sprites.update()
    hit_list = pygame.sprite.spritecollide(p, blocks, False)
    color_changer_hit_list = pygame.sprite.spritecollide(p, color_changer, True)
    if len(blocks) == 5:
        for i in blocks:
            distance = i.rect.y
        make_blocks(distance - 180)

    if p.rect.y < width / 2:
        for i in blocks:
            i.yspeed = 5

    else:
        for i in blocks:
            i.yspeed = 0

    if hit_list:
        for i in hit_list:
            if i.col == p.col:
                p.score += 1
            else:
                endgame()
                p.col = i.col

    for i in color_changer_hit_list:
        p.col = i.col
        i.kill()

    if len(color_changer) == 0:
        if random.choice(list(range(150))) == 1:
            c = ColorChanger()
            all_sprites.add(c)
            color_changer.add(c)

    window.fill(BGCOLOR)
    all_sprites.draw(window)
    draw_txt(window, f'Score : {int(p.score)}', 22, width - 80, 5)
    pygame.display.flip()
pygame.quit()
