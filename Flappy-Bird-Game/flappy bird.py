import pygame
import random
import sys
import os


width = 600
height = 650

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")
clock_ = pygame.time.Clock()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (180, 0, 0)
WALL_COLOR = (119, 200, 43)
BACKGROUND = (131, 208, 245)
IMAGE_PATH = os.path.join(os.getcwd(), 'img')
SOUND_PATH = os.path.join(os.getcwd(), 'sound')
BACKGROUND_IMAGE = pygame.image.load(os.path.join(IMAGE_PATH, 'background.png'))
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (width, height))
SCORE_IMAGES = {'0': pygame.image.load(os.path.join(IMAGE_PATH, '0.png')),
                '1': pygame.image.load(os.path.join(IMAGE_PATH, '1.png')),
                '2': pygame.image.load(os.path.join(IMAGE_PATH, '2.png')),
                '3': pygame.image.load(os.path.join(IMAGE_PATH, '3.png')),
                '4': pygame.image.load(os.path.join(IMAGE_PATH, '4.png')),
                '5': pygame.image.load(os.path.join(IMAGE_PATH, '5.png')),
                '6': pygame.image.load(os.path.join(IMAGE_PATH, '6.png')),
                '7': pygame.image.load(os.path.join(IMAGE_PATH, '7.png')),
                '8': pygame.image.load(os.path.join(IMAGE_PATH, '8.png')),
                '9': pygame.image.load(os.path.join(IMAGE_PATH, '9.png'))
                }
SCORE_TUPLE = (250, 275, 300, 325)
FLAPPY_BIRD = pygame.image.load(os.path.join(IMAGE_PATH, 'flappy.png'))
FLAPPY_BIRD = pygame.transform.scale(FLAPPY_BIRD, (35, 35))
GAME_OVER = pygame.image.load(os.path.join(IMAGE_PATH, 'gameover.png'))
PIPE = pygame.image.load(os.path.join(IMAGE_PATH, 'pop.png'))
PIPE_ = pygame.image.load(os.path.join(IMAGE_PATH, 'pop1.png'))
BACKGROUND_SOUND = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'bg.ogg'))
JUMP_SOUND = pygame.mixer.Sound(os.path.join(SOUND_PATH, 'jump.ogg'))


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((35, 35), pygame.SRCALPHA)
        self.image.blit(FLAPPY_BIRD, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (90, 570)
        self.score = 0
        self.speed=0
        self.current_frames=0
        self.frames_limit=8
        self.up_speed=-18
        self.down_speed=9


    def update(self):
        self.score += 1 / 10
        self.rect.bottom+=self.speed
        self.current_frames+=1
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.speed=self.up_speed
            if self.current_frames > self.frames_limit:
                self.current_frames=0
                JUMP_SOUND.play()
        else:
            self.speed=self.down_speed


class Wall(pygame.sprite.Sprite):
    def __init__(self, len_, place='down'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((70, len_), pygame.SRCALPHA)
        if place == 'down':
            self.pipe_image = pygame.transform.scale(PIPE, (70, len_))
        else:
            self.pipe_image = pygame.transform.scale(PIPE_, (70, len_))
        self.image.blit(self.pipe_image, (0, 0))
        self.rect = self.image.get_rect()
        if place == 'up':
            self.rect.top = 0
        else:
            self.rect.bottom = height
        self.speedx = -5
        self.rect.left = width

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()


def create_wall():
    height_num = random.randint(150, 350)
    wall = Wall(height_num, 'up')
    wall1 = Wall(random.randint(height - height_num - 250, height - height_num - 200))
    all_sprites.add(wall)
    all_sprites.add(wall1)
    wall_sprites.add(wall)
    wall_sprites.add(wall1)


def draw_txt(surf, text, size, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def end_page():
    run = True
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_e]:
                sys.exit()
        if keys[pygame.K_a]:
            run = False
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        screen.blit(GAME_OVER, (200, 200))
        display_score(y=(275, 300, 325), x=275)
        draw_txt(screen, "Press 'a' To Play Again And 'e' To Exit", 25, 300, 460)
        pygame.display.flip()
    refresh_vars()


def display_score(y=SCORE_TUPLE, x=20):
    score = str(int(bird.score))
    for i in range(len(score)):
        screen.blit(SCORE_IMAGES[score[i]], (y[i], x))


def refresh_vars():
    global all_sprites, wall_sprites, bird, last_time, running, wall_create_time
    all_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    bird = Bird()
    all_sprites.add(bird)
    create_wall()
    last_time = pygame.time.get_ticks()
    running = True
    wall_create_time = 3000


all_sprites = pygame.sprite.Group()
wall_sprites = pygame.sprite.Group()
bird = Bird()
all_sprites.add(bird)
create_wall()
last_time = pygame.time.get_ticks()
running = True
wall_create_time = 3000
BACKGROUND_SOUND.play(-1)

while running:
    clock_.tick(26)
    if pygame.time.get_ticks() - last_time > wall_create_time:
        create_wall()
        last_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    all_sprites.update()
    if pygame.sprite.spritecollide(bird, wall_sprites, False):
        end_page()
    screen.fill(BACKGROUND)
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    all_sprites.draw(screen)
    display_score()
    pygame.display.flip()
pygame.quit()
