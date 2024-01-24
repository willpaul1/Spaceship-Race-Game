import pygame
import time
import math
from utilsfile import scale_image


BACKGROUND = pygame.image.load("Resources/Background_RCG.png")
TRACK = pygame.image.load("Resources/TrackComplete_RCG.png")

TRACK_BORDER = pygame.image.load("Resources/OnlyTrack_RCG.png")
FINISH = pygame.image.load("Resources/finish_RCG.png")

RED_SHIP = scale_image(pygame.image.load("Resources/red_ship.png"), 0.6)
BLUE_SHIP = pygame.image.load("Resources/blue_ship.png")

#setup display surface - should be the same size as track
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Race!")

#1b
FPS = 60

#function fordrawing images in a window (the visuals inside the game window)
def draw(win, images):
    for img, pos in images:
        win.blit(img, pos)

#setting up the event loop -run keeps the window alive
run = True

# setting a clock so that the window does not run faster than a set FPS, it should run at the same speed on every computer (see 1b, 1c)
clock = pygame.time.Clock()
images = [(BACKGROUND, (0,0)), (TRACK, (0,0))]

while run:
    #1c
    clock.tick(FPS)

    draw(WIN, images)
    # in Pygame 0,0 is top left corner, furthest right is max X value, furthest down is max Y value
    #WIN.blit(BACKGROUND, (0,0))
    #WIN.blit(TRACK, (0,0))
    #WIN.blit(FINISH, (0,0))
    #WIN.blit(RED_SHIP, (0,0))
    #update() is a method that needs to run every time to make sure everything is drawn
    pygame.display.update()

    for event in pygame.event.get():
        #check if the user has the window open of closed
        if event.type == pygame.QUIT:
            run = False
            break

pygame.quit()

# setting a clock so that the window does not run faster than a set FPS, it should run at the same speed on every computer
