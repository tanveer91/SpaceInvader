import pygame
import math
import random
from pygame import mixer

# Initialize the pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('Background.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('Space.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('Player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_alien = 10

for i in range(num_alien):
    alienImg.append(pygame.image.load('Alien.png'))
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(50, 150))
    alienX_change.append(3)
    alienY_change.append(40)

# Bullet
bulletImg = pygame.image.load('Bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 8
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt((math.pow(alienX - bulletX, 2)) + (math.pow(alienY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True

while running:
    # RGB for the screen
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # press the key for movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5

            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX + (4*playerX_change)
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Alien movement
    for i in range(num_alien):
        # Game over
        if alienY[i] > 440:
            for j in range(num_alien):
                alienY[j] = 2000
            game_over()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 3
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -3
            alienY[i] += alienY_change[i]

        # Collision
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 736)
            alienY[i] = random.randint(50, 150)

        alien(alienX[i], alienY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
