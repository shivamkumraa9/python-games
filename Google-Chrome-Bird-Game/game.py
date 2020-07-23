import pygame
import random
import os

ASSERTS_DIR=os.path.join(os.getcwd(),'asserts')
BIRDS_DIR=os.path.join(ASSERTS_DIR,"Birds")
OTHERS_DIR=os.path.join(ASSERTS_DIR,"Others")
CHAR_DIR=os.path.join(ASSERTS_DIR,'Chars')

width = 800
height = 350

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE=(0,0,255)
FPS = 30


D_UP_SPEED = -30
D_DOWN_SPEED = 15
Sprite_speed = -15
FPS_Increaser = 0
Obs_size_lis=[(17,35),(34,35),(25,50),(47,50),(51,35)]
max_dino_up=85
score_tup=(700,711,722,733,744,755,766)
high_score_tup=(581,592,603,614,625)


pygame.init()
pygame.display.set_caption("Chrome T-Rex Game")
window = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

try:
    with open('high_score.txt','r') as file:
        h_score=int(file.read())
except:
    h_score=0

CLOUD_IMAGE=pygame.image.load(os.path.join(OTHERS_DIR, 'cloud.png'))
DOWN_IMAGE=pygame.image.load(os.path.join(OTHERS_DIR, 'Down.png'))

BIRDS_IMAGES=[
pygame.image.load(os.path.join(BIRDS_DIR, '1.png')),
pygame.image.load(os.path.join(BIRDS_DIR, '2.png'))
]

DOWN_BIRDS_IMAGES=[
pygame.image.load(os.path.join(BIRDS_DIR, '3.png')),
pygame.image.load(os.path.join(BIRDS_DIR, '4.png')),
]

OBSTACKLES_IMAGES={
        (17,35):pygame.image.load(os.path.join(OTHERS_DIR, 'obs_1.png')),
        (34,35):pygame.image.load(os.path.join(OTHERS_DIR, 'obs_2.png')),
        (25,50):pygame.image.load(os.path.join(OTHERS_DIR, 'obs_3.png')),
        (47,50):pygame.image.load(os.path.join(OTHERS_DIR, 'obs_4.png')),
        (51,35):pygame.image.load(os.path.join(OTHERS_DIR, 'obs_5.png')),
}

SCORES_IMAGES={'0': pygame.image.load(os.path.join(CHAR_DIR, '0.png')),
                '1': pygame.image.load(os.path.join(CHAR_DIR, '1.png')),
                '2': pygame.image.load(os.path.join(CHAR_DIR, '2.png')),
                '3': pygame.image.load(os.path.join(CHAR_DIR, '3.png')),
                '4': pygame.image.load(os.path.join(CHAR_DIR, '4.png')),
                '5': pygame.image.load(os.path.join(CHAR_DIR, '5.png')),
                '6': pygame.image.load(os.path.join(CHAR_DIR, '6.png')),
                '7': pygame.image.load(os.path.join(CHAR_DIR, '7.png')),
                '8': pygame.image.load(os.path.join(CHAR_DIR, '8.png')),
                '9': pygame.image.load(os.path.join(CHAR_DIR, '9.png')),
                'H': pygame.image.load(os.path.join(CHAR_DIR, 'H.png')),
                'I': pygame.image.load(os.path.join(CHAR_DIR, 'I.png'))
}

FLYING_BIRDS_IMAGES=[
pygame.image.load(os.path.join(BIRDS_DIR, 'Enemy_bird_1.png')),
pygame.image.load(os.path.join(BIRDS_DIR, 'Enemy_bird_2.png')),
]

class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images=BIRDS_IMAGES
        self.index=0
        self.image = pygame.Surface((45, 47),pygame.SRCALPHA)
        self.image.blit(BIRDS_IMAGES[self.index],(0,0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.bottom = (150, 231)
        self.yspeed = 0
        self.is_space_activated = True
        self.bottom = 231
        self.down_pressed_first=False
        self.score=0
        self.current_frames=0
        self.animation_frames=3

    def update(self):
        self.current_frames+=1

        if self.current_frames >= self.animation_frames:
            self.current_frames=0
            self.index+=1
            if self.index >= 2:
                self.index=0
            self.image.fill(WHITE)
            self.image.blit(self.images[self.index], (0, 0))

        self.rect.bottom += self.yspeed
        self.score=pygame.time.get_ticks()//100
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_SPACE] and self.is_space_activated:
            self.yspeed = D_UP_SPEED
            self.is_space_activated = False


        if keystate[pygame.K_DOWN] and self.is_space_activated ==True:
            self.images=DOWN_BIRDS_IMAGES
            self.down_pressed_first=True
            self.image=pygame.transform.scale(self.image,(57,30))
            self.rect=self.image.get_rect()
            self.rect.x, self.rect.bottom = (150, 235)
            self.bottom=230
        else:
            if self.down_pressed_first==True:
                self.image=pygame.transform.scale(self.image,(45,47))
                self.images=BIRDS_IMAGES
                self.bottom=214

        if self.rect.bottom >= self.bottom:
            self.rect.bottom = self.bottom
            self.is_space_activated = True

        if self.rect.bottom <= max_dino_up:
            self.rect.bottom = max_dino_up
            self.yspeed = D_DOWN_SPEED


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size=random.choice(Obs_size_lis)
        self.image = pygame.Surface(size,pygame.SRCALPHA)
        self.image.blit(OBSTACKLES_IMAGES[size], (0, 0))
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.bottom=width,235
        self.xspeed = Sprite_speed

    def update(self):
        self.rect.left += self.xspeed
        if self.rect.right <= 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((46, 13),pygame.SRCALPHA)
        self.image.blit(CLOUD_IMAGE, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, random.choice(list(range(80, 120))))
        self.xspeed = random.choice(list(range(-8, -2)))

    def update(self):
        self.rect.left += self.xspeed
        if self.rect.right <= 0:
            self.kill()


class Flyingbird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.index=0
        self.image = pygame.Surface((46, 34),pygame.SRCALPHA)
        self.image.blit(FLYING_BIRDS_IMAGES[self.index], (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.bottom = (width, random.choice([232, 180,195]))
        self.xspeed = Sprite_speed
        self.current_frames=0
        self.animation_frames=6


    def update(self):
        self.current_frames+=1

        if self.current_frames >= self.animation_frames:
            self.current_frames=0
            self.index+=1
            if self.index >= 2:
                self.index=0
            self.image.fill(WHITE)
            self.image.blit(FLYING_BIRDS_IMAGES[self.index], (0, 0))


        self.rect.left += self.xspeed
        if self.rect.right <= 0:
            self.kill()

class Bottom_line(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.Surface((1200,14), pygame.SRCALPHA)
        self.image.blit(DOWN_IMAGE, (0, 0))
        self.rect=self.image.get_rect()
        self.rect.x,self.rect.bottom=0,245

    def update(self):
        self.rect.left+=Sprite_speed
        if self.rect.right <= width:
            self.kill()
            make_bottom_line()

def make_clouds():
    for i in [random.choice([i for i in range(1000, 1600, 300)]) for j in range(2)]:
        cloud = Cloud(i)
        all_sprites.add(cloud)
        clouds.add(cloud)

def make_obstacle():
    obstacle = Obstacle()
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

def make_flyingbird():
    flyingbird = Flyingbird()
    Flyingbirds.add(flyingbird)
    all_sprites.add(flyingbird)

def make_bottom_line():
    bottom_line=Bottom_line()
    all_sprites.add(bottom_line)
    bottom_lines.add(bottom_line)


def draw_score():
    score=str(dinosaur.score)
    for i in range(len(score)):
        window.blit(SCORES_IMAGES[score[i]], (score_tup[i], 20))



def draw_highscore():
    score=str(h_score)
    window.blit(SCORES_IMAGES["H"], (550, 20))
    window.blit(SCORES_IMAGES["I"], (561, 20))
    for i in range(len(score)):
        window.blit(SCORES_IMAGES[score[i]], (high_score_tup[i], 20))

all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
clouds = pygame.sprite.Group()
Flyingbirds = pygame.sprite.Group()
bottom_lines=pygame.sprite.Group()

dinosaur = Dinosaur()
all_sprites.add(dinosaur)

make_bottom_line()

running = True
while running:
    Now = pygame.time.get_ticks()
    if Now - FPS_Increaser > 2000 and FPS <45:
        FPS_Increaser = Now
        FPS += 1
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    hit_list = pygame.sprite.spritecollide(dinosaur, obstacles, False)
    if hit_list:
        running = False

    hit_list_1 = pygame.sprite.spritecollide(dinosaur, Flyingbirds, False)
    if hit_list_1:
        running = False

    if len(clouds) <= 1:
        make_clouds()

    if len(Flyingbirds) == 0 and random.choice(list(range(0, 50))) == 1:
        if obstacles:
            for i in obstacles:
                if 500 > i.rect.x > 300:
                    make_flyingbird()

    if len(obstacles) == 0:
        make_obstacle()

    all_sprites.update()

    window.fill(WHITE)
    all_sprites.draw(window)
    draw_score()
    draw_highscore()
    pygame.display.flip()

if dinosaur.score >h_score:
    with open("high_score.txt",'w') as file:
        file.write(str(dinosaur.score))

pygame.quit()
