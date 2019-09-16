from math import *
import pygame
import sys
import random
from random import randint
from pygame.locals import *

#set up the pygame
pygame.init()
mainClock = pygame.time.Clock()

#Sets up the window
WINDOWWIDTH = 800
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Pong With No Walls')

#Setting up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Set up the ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__() #calling the parent constructor

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        #draw the ball
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.velocity = [randint(4, 8), randint(4, 8)]

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = floor(copysign(randint(1, 8), self.velocity[1]))

    def bouncehorizontal(self):
        self.velocity[1] = -self.velocity[1]
        self.velocity[0] = floor(copysign(randint(1, 8), self.velocity[0]))

    def resetball1(self, horizontal, vertical):
        ball.rect.x = (WINDOWWIDTH / 2) - 10
        ball.rect.y = (WINDOWHEIGHT / 2) - 10
        self.velocity = [horizontal, vertical]
        moveBall = False

#Sound files
_Sound = ['sounds/blip1.wav', 'sounds/blip2.wav', 'sounds/blip3.wav']
#Set up the player and ball
AI = pygame.Rect(10, (WINDOWHEIGHT/2) - 50, 10, 100)
AITop = pygame.Rect(150, 10, 100, 10)
AIBottom = pygame.Rect(150, WINDOWHEIGHT - 20, 100, 10)
#Player
player1 = pygame.Rect(WINDOWWIDTH - 20, (WINDOWHEIGHT/2) - 50, 10, 100)
player1Top = pygame.Rect(WINDOWWIDTH - 250, 10, 100, 10)
player1Bottom = pygame.Rect(WINDOWWIDTH - 250, WINDOWHEIGHT - 20, 100, 10)
#Ball
ball = Ball(WHITE, 10, 10)
ball.rect.x = (WINDOWWIDTH/2) - 10
ball.rect.y = (WINDOWHEIGHT/2) - 10
#Scores, have 11 scores will add 1 to gameScore. 3 gameScores will prompt winner or loser
score1 = 0
score2 = 0
gameScore1 = 0
gameScore2 = 0

#adds to sprite list
sprite_list = pygame.sprite.Group()
sprite_list.add(ball)

#Set up the movements for AI
move1Left = False
move1Right = False
move1Up = False
move1Down = False
#Seet up the movements for the player
move2Left = False
move2Right = False
move2Up = False
move2Down = False

MOVESPEED = 10

#plays background music
pygame.mixer.music.load('music/Peace And Tranquility.mp3')
pygame.mixer.music.play()

#Run the game loop
GameRunning = True
while GameRunning:
    # Causes the ball to move
    sprite_list.update()


    # Detect collisions between the ball and the paddles
    if AI.colliderect(ball) or player1.colliderect(ball):
        ball.bounce()
        effect = pygame.mixer.Sound(random.choice(_Sound))
        effect.play()

    if AITop.colliderect(ball) or AIBottom.colliderect(ball) or player1Top.colliderect(ball) or \
            player1Bottom.colliderect(ball):
        ball.bouncehorizontal()
        effect = pygame.mixer.Sound(random.choice(_Sound))
        effect.play()

    # Adds to the score when a player scores
    # AI score
    if ball.rect.x >= WINDOWWIDTH - 10 or ball.rect.y <= 10 and ball.rect.x > WINDOWWIDTH / 2 or \
            ball.rect.y >= WINDOWHEIGHT - 10 and ball.rect.x > WINDOWWIDTH / 2:
        score1 += 1
        if score1 >= 11 and (score1 - 2) >= score2:
            gameScore1 += 1
            score1 = 0
            score2 = 0
            if gameScore1 == 3:
                font = pygame.font.Font(None, 74)
                text = font.render("Would you like to play again?\nPress Y to continue or Esc to quit.", 1, WHITE)
                windowSurface.blit(text, (WINDOWWIDTH / 2 - 10, WINDOWHEIGHT/2))
        ball.resetball1(randint(-8, -1), randint(-8,8))

    # player2 score
    if ball.rect.x <= 10 or ball.rect.y >= WINDOWHEIGHT - 10 and ball.rect.x < WINDOWWIDTH / 2 or \
            ball.rect.y <= 10 and ball.rect.x < WINDOWWIDTH / 2:
        score2 += 1
        if score2 >= 11 and (score2 - 2) >= score1:
            gameScore2 += 1
            score1 = 0
            score2 = 0
            if gameScore2 == 3:
                font = pygame.font.Font(None, 74)
                text = font.render("Would you like to play again?\nPress Y to continue or Esc to quit.", 1, WHITE)
                windowSurface.blit(text, (WINDOWWIDTH / 2 - 10, WINDOWHEIGHT/2))
        ball.resetball1(randint(1, 8), randint(-8,8))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False #breaks the while
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                GameRunning = False #Breaks the while
                sys.exit()

            #I and O will affect the speed of the paddles
            if event.key == K_i:
                if 10 <= MOVESPEED < 20:
                    MOVESPEED += 1
            if event.key == K_o:
                if MOVESPEED > 10:
                    MOVESPEED -= 1
        #P will pause the game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            while True:
                event = pygame.event.wait()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    break #unpauses the game


    #Controls the movement of the paddles
        if event.type == KEYDOWN:
            #player 1
            if event.key ==K_w:
                move1Up = True
                move1Down = False
                move1Left = True
                move1Right = False
            if event.key ==K_s:
                move1Up = False
                move1Down = True
                move1Left = False
                move1Right = True

            #player 2
            if event.key == K_UP:
                move2Up = True
                move2Down = False
            if event.key == K_RIGHT:
                move2Left = False
                move2Right = True
            if event.key == K_DOWN:
                move2Up = False
                move2Down = True
            if event.key == K_LEFT:
                move2Left = True
                move2Right = False
        if event.type == KEYUP:
            #player 1
            if event.key == K_w:
                move1Up = False
                move1Left = False
            if event.key == K_s:
                move1Down = False
                move1Right = False

            #player 2
            if event.key == K_UP:
                move2Up = False
            if event.key == K_RIGHT:
                move2Right = False
            if event.key == K_DOWN:
                move2Down = False
            if event.key == K_LEFT:
                move2Left = False

    #Draws the background onto the surface
    windowSurface.fill(BLACK)

    #Moves player 1 main paddle.
    if move1Down and AI.bottom < WINDOWHEIGHT:
        AI.top += MOVESPEED
    if move1Up and AI.top > 0:
        AI.top -= MOVESPEED
    #moves player 1's top paddle
    if move1Left and AITop.left > 0:
        AITop.left -= MOVESPEED
    if move1Right and AITop.right < WINDOWWIDTH/2:
        AITop.right += MOVESPEED
    #moves player 1's bottom paddle
    if move1Left and AIBottom.left > 0:
        AIBottom.left -= MOVESPEED
    if move1Right and AIBottom.right < WINDOWWIDTH / 2:
        AIBottom.right += MOVESPEED

    #Moves player
    if move2Down and player1.bottom < WINDOWHEIGHT:
        player1.top += MOVESPEED
    if move2Up and player1.top > 0:
        player1.top -= MOVESPEED
    #moves player's top paddle
    if move2Left and player1Top.left > WINDOWWIDTH/2:
        player1Top.left -= MOVESPEED
    if move2Right and player1Top.right < WINDOWWIDTH:
        player1Top.right += MOVESPEED
    #moves player's bottom paddle
    if move2Left and player1Bottom.left > WINDOWWIDTH/2:
        player1Bottom.left -= MOVESPEED
    if move2Right and player1Bottom.right < WINDOWWIDTH:
        player1Bottom.right += MOVESPEED

    #Draw the player onto surface
    pygame.draw.rect(windowSurface, WHITE, AI)
    pygame.draw.rect(windowSurface, WHITE, AITop)
    pygame.draw.rect(windowSurface, WHITE, AIBottom)
    pygame.draw.rect(windowSurface, WHITE, player1)
    pygame.draw.rect(windowSurface, WHITE, player1Top)
    pygame.draw.rect(windowSurface, WHITE, player1Bottom)
    pygame.draw.rect(windowSurface, WHITE, ball)

    # Display scores:
    font = pygame.font.Font(None, 74)
    text = font.render(str(score1), 1, WHITE)
    windowSurface.blit(text, (WINDOWWIDTH/2 - 80, 10))
    text = font.render(str(score2), 1, WHITE)
    windowSurface.blit(text, (WINDOWWIDTH/2 + 50, 10))

    #Draw the net
    pygame.draw.line(windowSurface, WHITE, [(WINDOWWIDTH/2) - 1, 0], [(WINDOWWIDTH/2) - 1, WINDOWHEIGHT])

    #Draw the window onto the screen
    pygame.display.flip()
    mainClock.tick(30)

