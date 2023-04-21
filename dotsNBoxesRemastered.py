import numpy as np
import pygame



class lineButton:
    def __init__(self, x, y, orientation):
        self.x

def startupSequence(rows, cols, size, display):
    rowArray = np.linspace(0, size[1], num = (rows + 2))
    colArray = np.linspace(0, size[0], num = (cols + 2))

    display.fill("white")
    [[pygame.draw.circle(display, "black", (dotCol, dotRow), 10) for dotCol in colArray[1:-1]] for dotRow in rowArray[1:-1]]
    pygame.display.flip()

def cleanupSequence():
    print("Quitting game\n")
    pygame.quit()

pygame.init() #pygame.init initializes game module
gameRunning = True
screenSize = (840, 600)
gameDisplay = pygame.display.set_mode(screenSize, pygame.HWSURFACE | pygame.DOUBLEBUF)
    # https://stackoverflow.com/questions/29135147/what-do-hwsurface-and-doublebuf-do
    # HWSURFACE -> hardware acceleration. DOUBLEBUF -> reduces artifacting by saving to vram
numRows = 4
numCols = 4
gameClock = pygame.time.Clock()

startupSequence(numRows,numCols,screenSize, gameDisplay)

while gameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
    
    gameClock.tick(60)

cleanupSequence()
