import math
import random
import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("VIRUS")
icon = pygame.image.load('vcc.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('vcc.png')
playerX = 370
playerY = 480
playerX_change = 0

# cov
covImg = []
covX = []
covY = []
covX_change = []
covY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    covImg.append(pygame.image.load('cov.png'))
    covX.append(random.randint(0, 736))
    covY.append(random.randint(50, 150))
    covX_change.append(4)
    covY_change.append(40)

# vc

# Ready - You can't see the vc on the screen
# Fire - The vc is currently moving

vcImg = pygame.image.load('vc.png')
vcX = 0
vcY = 480
vcX_change = 0
vcY_change = 10
vc_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 28)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 28)


def show_score(x, y):
    score = font.render("SCORE : " + str(score_value), True, (255, 255, 160))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("STAY SAFE VIRUS KILLED : "+ str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def cov(x, y, i):
    screen.blit(covImg[i], (x, y))


def fire_vc(x, y):
    global vc_state
    vc_state = "fire"
    screen.blit(vcImg, (x + 16, y + 10))


def isCollision(covX, covY, vcX, vcY):
    distance = math.sqrt(math.pow(covX - vcX, 2) + (math.pow(covY - vcY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if vc_state is "ready":
                    vcSound = mixer.Sound("laser.wav")
                    vcSound.play()
                    # Get the current x cordinate of the spaceship
                    vcX = playerX
                    fire_vc(vcX, vcY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # cov Movement
    for i in range(num_of_enemies):

        # Game Over
        if covY[i] > 440:
            for j in range(num_of_enemies):
                covY[j] = 2000
            game_over_text()
            break

        covX[i] += covX_change[i]
        if covX[i] <= 0:
            covX_change[i] = 4
            covY[i] += covY_change[i]
        elif covX[i] >= 736:
            covX_change[i] = -4
            covY[i] += covY_change[i]

        # Collision
        collision = isCollision(covX[i], covY[i], vcX, vcY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            vcY = 480
            vc_state = "ready"
            score_value += 1
            covX[i] = random.randint(0, 736)
            covY[i] = random.randint(50, 150)

        cov(covX[i], covY[i], i)

    # vc Movement IN SCREEN
    if vcY <= 0:
        vcY = 480
        vc_state = "ready"

    if vc_state is "fire":
        fire_vc(vcX, vcY)
        vcY -= vcY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
