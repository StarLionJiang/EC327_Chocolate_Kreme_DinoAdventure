# transpose map matrix for compatibility

mapBorder = 150
mapOffsetX = 0
mapOffsetY = 0
mapMove = False
mapEdge = False

def transpose(l1, l2):
    for i in range(len(l1[0])):
        # print(i)
        row =[]
        for item in l1:
            row.append(item[i])
        l2.append(row)
    return l2

mainMapOg = [[2, 1, 2, 0, 2, 1, 0, 2, 1, 2, 0, 2, 1, 2, 0, 2, 1, 0, 2, 1, 2, 0], 
             [1, 1, 1, 0, 2, 1, 0, 2, 2, 0, 0, 1, 1, 1, 0, 2, 1, 0, 2, 2, 0, 0], 
             [1, 1, 2, 0, 0, 2, 1, 0, 0, 1, 1, 1, 1, 2, 0, 0, 2, 1, 0, 0, 1, 1], 
             [1, 2, 2, 2, 2, 0, 1, 2, 0, 1, 0, 1, 2, 2, 2, 2, 0, 1, 2, 0, 1, 0], 
             [0, 0, 0, 1, 2, 0, 0, 2, 2, 0, 1, 0, 0, 0, 1, 2, 0, 0, 2, 2, 0, 1], 
             [0, 2, 1, 0, 0, 1, 0, 1, 2, 2, 2, 0, 2, 1, 0, 0, 1, 1, 2, 2, 2, 0], 
             [0, 0, 1, 2, 1, 2, 1, 0, 1, 1, 1, 0, 0, 1, 2, 1, 2, 0, 1, 1, 1, 0], 
             [2, 1, 2, 0, 2, 1, 0, 2, 1, 2, 0, 2, 1, 2, 0, 2, 1, 2, 1, 2, 0, 2], 
             [1, 1, 1, 0, 2, 1, 0, 2, 2, 0, 0, 1, 1, 1, 0, 2, 1, 2, 2, 1, 2, 2], 
             [1, 1, 2, 0, 0, 2, 1, 0, 0, 1, 1, 1, 1, 2, 0, 0, 2, 0, 0, 0, 1, 1], 
             [1, 2, 2, 2, 2, 0, 1, 2, 0, 1, 0, 1, 2, 1, 2, 2, 2, 0, 2, 2, 1, 2], 
             [0, 0, 0, 1, 2, 0, 1, 2, 2, 2, 0, 2, 0, 0, 1, 1, 1, 0, 1, 2, 2, 0], 
             [0, 2, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 2, 1, 2, 0, 2, 1, 0, 0, 1], 
             [0, 0, 1, 2, 1, 2, 2, 1, 2, 0, 2, 0, 2, 2, 2, 0, 0, 1, 1, 2, 2, 2]]

mainMap = []
mainMap = transpose(mainMapOg, mainMap)

# map preview frunction
import pygame, sys
from spriteSheet import *
from assets import *

def TestMap():
    centeringX = int((swidth-len(mainMap)*tileDim*tileScale)/2)
    centeringY = int((sheight-len(mainMap[0])*tileDim*tileScale)/2)
    clock = pygame.time.Clock()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0,0,0))

        for x, i in enumerate(range(
            centeringX, 
            len(mainMap)*tileDim*tileScale+centeringX, 
            tileDim*tileScale
        )):
            for y, j in enumerate(range(
                centeringY, len(mainMap[0])*tileDim*tileScale+centeringY, 
                tileDim*tileScale
            )):
                screen.blit(tileList[mainMap[x][y]], (i,j))

        pygame.display.update()

        
        clock.tick()
        print(clock.get_fps())
