import pygame
import random
import math
from pygame import mixer

# Initializing_pygame
pygame.init()

# creating_screen
porda = pygame.display.set_mode((800, 600))

# Background
ronokhetro = pygame.image.load('ronokhetro.jpg')

# siren_of_war
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('Mohakasher Juddho')
chhobi = pygame.image.load('spaceship.png')
pygame.display.set_icon(chhobi)

# player
khelowarImg = pygame.image.load('rocket.png')
khelowarX = 370
khelowarY = 480
khelowarX_change = 0
khelowarY_change = 0

# enemy
shotruImg = []
shotruX = []
shotruY = []
shotruX_change = []
shotruY_change = []
shotru_no = 6
for i in range(shotru_no):
    shotruImg.append(pygame.image.load('shotru.png'))
    shotruX.append(random.randint(0, 768))
    shotruY.append(random.randint(15, 150))
    shotruX_change.append(0.25)
    shotruY_change.append(32)

# guli
guliImg = pygame.image.load('guli.png')
guliX = 0
guliY = 480
guliY_change = 0.75
guli_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (0, 127, 127))
    porda.blit(score, (x, y))


def khelowar(x, y):
    porda.blit(khelowarImg, (x, y))


def shotru(x, y, i):
    porda.blit(shotruImg[i], (x, y))


def fire_guli(x, y):
    global guli_state
    guli_state = 'fire'

    porda.blit(guliImg, (x + 20, y + 20))


def isCollision(x1, y1, x2, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance < 34:
        return True
    else:
        return False


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (0, 170, 170))
    porda.blit(over_text, (200, 250))


# Game_loop
running = True
while running:

    # RGB - Red, Green, Blue
    porda.fill((0, 0, 0))
    # background
    porda.blit(ronokhetro, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke + check key.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                khelowarX_change = -0.4
            if event.key == pygame.K_RIGHT:
                khelowarX_change = 0.4
            if event.key == pygame.K_UP:
                khelowarY_change = -0.4
            if event.key == pygame.K_DOWN:
                khelowarY_change = 0.4
            if event.key == pygame.K_SPACE:
                if guli_state == 'ready':
                    dishkiao = mixer.Sound('laser.wav')
                    dishkiao.play()
                    guliX = khelowarX
                    guliY = khelowarY
                    fire_guli(guliX, guliY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                khelowarX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                khelowarY_change = 0

    khelowarX += khelowarX_change
    khelowarY += khelowarY_change

    if khelowarX <= 0:
        khelowarX = 0
    elif khelowarX >= 736:
        khelowarX = 736
    if khelowarY <= 0:
        khelowarY = 0
    elif khelowarY >= 500:
        khelowarY = 500
    shotruX += shotruX_change

    # shotru_movement
    for i in range(shotru_no):

        # Game_Over
        crash = isCollision(shotruX[i], shotruY[i], khelowarX, khelowarY)
        if shotruY[i] > 450 or crash == True:
            for j in range(shotru_no):
                shotruY[j] = 2000
            boom = mixer.Sound('explosion.wav')
            boom.play()
            game_over_text()
            break

        shotruX[i] += shotruX_change[i]
        if shotruX[i] < 0:
            shotruX[i] = 0
            shotruX_change[i] = 0.25
            shotruY[i] += shotruY_change[i]
        elif shotruX[i] > 736:
            shotruX[i] = 736
            shotruX_change[i] = -0.25
            shotruY[i] += shotruY_change[i]

        # Collision
        collision = isCollision(shotruX[i], shotruY[i], guliX, guliY)
        if collision:
            boom = mixer.Sound('explosion.wav')
            boom.play()
            guliY = 480
            guli_state = 'ready'
            score_value += 1
            shotruX[i] = random.randint(0, 768)
            shotruY[i] = random.randint(15, 150)

        shotru(shotruX[i], shotruY[i], i)

    # guli_norachora
    if guliY < 0:
        guliY = 480
        guli_state = 'ready'
    if guli_state == 'fire':
        fire_guli(guliX, guliY)
        guliY -= guliY_change

    khelowar(khelowarX, khelowarY)
    show_score(textX, textY)
    pygame.display.update()
