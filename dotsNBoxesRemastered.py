import numpy as np
import pygame



class lineButton:
    def __init__(self, x, y, dimensions, gameDisplay):
        self.rect = pygame.Rect((x,y), dimensions) 
        # creates a pygame rectangle, passed values of (x,y) and dimensions (a tuple containing (length, width))
        # determine location of topleft of rectangle and shape
        self.display = gameDisplay
        self.clicked = False
    
    def draw(self):
        # draws the rectangle
        pygame.draw.rect(self.display, "black", self.rect)

    # # Testing function    
    # def __str__(self):
    #     return f"Button at {self.rect.topleft}"

# StartupSequence sets up the playing board and returns an array of buttons that represent the possible player moves.
def startupSequence(rows, cols, size, display):
    # numpy's linspace used to split the playing area evenly.
    rowArray = np.linspace(0, size[1], num = (rows + 2))
    rowArray = rowArray[1:-1] # These lines remove the edges of the linspace equation
    colArray = np.linspace(0, size[0], num = (cols + 2))
    colArray = colArray[1:-1]
    buttonArrayHoriz = []
    buttonArrayVert = []
    gameButtons = []

    # Fills the display with white, then draws the dots onto the screen
    display.fill("white")
    [[pygame.draw.circle(display, "black", (dotCol, dotRow), 10) for dotCol in colArray] for dotRow in rowArray]
    # pygame.draw.circle(surface, color, (center location in tuple), radius)

    for i in range(cols):
        for b in range(rows - 1):
            buttonArrayHoriz.append(lineButton(colArray[b] , rowArray[i] - 3, (colArray[b + 1] - colArray[b], 5), display))
            # colArray[b + 1] - colArray[b] determines rectangle length, "5" is just the width I chose based on the circle's radius
            # Must be careful, coordinates go (x,y) but matrices go (row, col) which is (y,x)
            # display is just the game screen

    for j in range(cols):
        for k in range(rows - 1):
            buttonArrayVert.append(lineButton(colArray[j] - 3, rowArray[k], (5, rowArray[k + 1] - rowArray[k]), display))

    
    # # Testing function
    # for z in buttonArrayVert:
    #     z.draw()
    # for o in buttonArrayHoriz:
    #     o.draw() 


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
