import pygame
import spriteSheet
swidth = 960
sheight = 640
screen = pygame.display.set_mode((swidth,sheight))

playerBaseDim = 24
playerScale = 4

# right facing player sprites
playerSpriteImg = pygame.image.load("doux.png").convert_alpha()
playerSpriteSheet = spriteSheet.SpriteSheet(playerSpriteImg)

playerFrames = []
for x in range(0,23):
    playerFrames.append(
        playerSpriteSheet.get_image(
            x, playerBaseDim, playerBaseDim, playerScale, (0,0,0)
        )
    )

# left facing player sprites (inverted)
playerSpriteInv = pygame.transform.flip(playerSpriteImg, True, False)
playerSpriteInvSheet = spriteSheet.SpriteSheet(playerSpriteInv)

playerInvFrames = []
for x in range(23,-1,-1):
    playerInvFrames.append(
        playerSpriteInvSheet.get_image(
            x, playerBaseDim, playerBaseDim, playerScale, (0,0,0)
        )
    )

# tile square assets for map
tileScale = int((3/2)*playerScale)
tileDim = 16
tileSprites = []
tileSprites.append(pygame.image.load("MapAssets/Tiles/tile_0000.png")) # 0
tileSprites.append(pygame.image.load("MapAssets/Tiles/tile_0001.png")) # 1
tileSprites.append(pygame.image.load("MapAssets/Tiles/tile_0002.png")) # 2
tileSprites.append(pygame.image.load("MapAssets/Tiles/tile_0036.png")) # 3
tileSprites.append(pygame.image.load("MapAssets/Tiles/tile_0037.png")) # 4
tileSprites.append(pygame.image.load("MapAssets/Tiles/tile_0038.png")) # 5
tileSprites.append(pygame.image.load("MapAssets/Tiles/tile_0039.png")) # 6
tileSprites.append(pygame.image.load("MapAssets/Tiles/tile_0040.png")) # 7
tileSprites.append(pygame.image.load("MapAssets/Tiles/tile_0041.png")) # 8
tileSprites.append(pygame.image.load("MapAssets/Tiles/tile_0042.png")) # 9

tileList = []
for x in range(10):
    tileList.append(spriteSheet.SpriteSheet(tileSprites[x]).get_image(0, tileDim, tileDim, tileScale, (0,0,0)))
