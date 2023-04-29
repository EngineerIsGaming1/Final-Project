import numpy as np
import pygame
import time



class lineButton:
    def __init__(self, x, y, dimensions, gameDisplay):
        self.rect = pygame.Rect((x,y), dimensions) 
        # creates a pygame rectangle, passed values of (x,y) and dimensions (a tuple containing (length, width))
        # determine location of topleft of rectangle and shape
        self.display = gameDisplay
        self.clicked = False
    
    def draw(self, color):
        # draws the rectangle
        pygame.draw.rect(self.display, color, self.rect)
        pygame.display.flip()

    # # Testing function    
    # def __str__(self):
    #     return f"Button at {self.rect.topleft}"

def checkQuit(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running == False
    
    return(running)

def checkBox(inputBox):
    clickedBox = []
    [clickedBox.append(curLine.clicked) for curLine in inputBox]

    return(all(clickedBox))
    
def checkPoints(line, boxes):
    score = 0

    for curBox in boxes:
        if line in curBox:
            score += checkBox(curBox)

    return(score)



def playerAction(boxes, color):
    action = True
    
    while action:
        # This quit action has to be in any while loop or else pygame gets mad and crashes
        # Idk why, and I don't really know how to fix it, so it's just going to be here
        # This line also returns an error since the main gameloop wasn't stoppped before the
        # pygame.quit() line was called, but it has to be here for the program to work :////
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cleanupSequence()

        mousePos = pygame.mouse.get_pos() # gets mouse position using get_pos()
        
        # Nested for loop that indexes through individual elements of the list of boxes
        for curBox in boxes:
            for curLine in curBox:
                # "rect" object has an attribute "collidepoint" that returns true or false based on the coordinates given
                if curLine.rect.collidepoint(mousePos):
                    # if mouse is clicked and the clicked line hasn't been clicked yet, draw it and end player action 
                    if pygame.mouse.get_pressed()[0] == 1 and curLine.clicked == False:
                        curLine.clicked = True
                        curLine.draw(color)
                        points = checkPoints(curLine, boxes)
                        action = False
                        time.sleep(.25)

    return(points)

# StartupSequence sets up the playing board and returns an array of buttons that represent the possible player moves.
def startupSequence(rows, cols, size, display):
    # numpy's linspace used to split the playing area evenly.
    rowArray = np.linspace(0, size[1], num = (rows + 2))
    rowArray = rowArray[1:-1] # These lines remove the edges of the linspace equation
    colArray = np.linspace(0, size[0], num = (cols + 2))
    colArray = colArray[1:-1]
    buttonArrayHoriz = []
    buttonArrayVert = []
    boxList = []

    # Fills the display with white, then draws the dots onto the screen
    display.fill("white")
    [[pygame.draw.circle(display, "black", (dotCol, dotRow), 10) for dotCol in colArray] for dotRow in rowArray]
    # how function works -> pygame.draw.circle(surface, color, (center location in tuple), radius)

    # creates a list of horizontal buttons. Indexes like matlab when only 1 dimension is given
    [[buttonArrayHoriz.append(lineButton(colArray[b] , rowArray[i] - 3, (colArray[b + 1] - colArray[b], 9), display)) \
      for b in range(cols - 1)] for i in range(rows)]
            # colArray[b + 1] - colArray[b] determines rectangle length, "9" is just the width I chose
            # Must be careful, coordinates go (x,y) but matrices go (row, col) which is (y,x)
            # display is just the game screen

    # creates a list of vertical buttons. Indexes like matlab when only 1 dimension is given
    [[buttonArrayVert.append(lineButton(colArray[k] - 3, rowArray[j], (9, rowArray[j + 1] - rowArray[j]), display)) \
      for k in range(cols)] for j in range(rows - 1)]
    
    # creates a list of lists of all boxes in the playing area
    for z in range((rows - 1) * (cols - 1)):
        boxList.append([buttonArrayHoriz[z], buttonArrayVert[z + 1 + (z//cols)],\
                        buttonArrayHoriz[z + (cols - 1)], buttonArrayVert[z + (z//cols)]])

    
    # Testing function
    # for z in buttonArrayVert:
    #     z.draw("black")
    # for o in buttonArrayHoriz:
    #     o.draw("black") 


    pygame.display.flip()

    return(boxList)

def cleanupSequence():
    print("Quitting game\n")
    pygame.quit()

pygame.init() #pygame.init initializes game module
gameRunning = True
screenSize = (840, 600)
gameDisplay = pygame.display.set_mode(screenSize, pygame.HWSURFACE | pygame.DOUBLEBUF)
    # https://stackoverflow.com/questions/29135147/what-do-hwsurface-and-doublebuf-do
    # HWSURFACE -> hardware acceleration. DOUBLEBUF -> reduces artifacting by saving to vram

# Can cange numRows and numCols without anything breaking (probably)
# Keeping it static for the sake of the project to stay consistent with game rules given by wikihow
# Basically have to have a square playing field or else person who goes first has an unfair advantage
numRows = 4
numCols = 4
totalMoves = 0
gameClock = pygame.time.Clock()
playerOneScore = 0
playerTwoScore = 0

boxList = startupSequence(numRows,numCols,screenSize, gameDisplay)

while gameRunning:
    gameRunning = checkQuit(gameRunning)

    # Passing blue and red signifies the two different players' actions
    playerOneScore += playerAction(boxList, "Blue")
    print(playerOneScore)
    playerTwoScore += playerAction(boxList, "Red")
    print(playerTwoScore)


    
    totalMoves += 2
    # print(totalMoves)

    # this equation I got by doing algebra and then simplifying
    # rows*(col-1) + cols*(rows-1)
    # This equation is used to find how many total moves there are, and end the gameloop
    # once all possible moves have been made
    if (totalMoves >= (2 * (numRows * numCols) - numRows - numCols)):
        gameRunning = False
    
    # print(gameRunning)
    gameClock.tick(60)

cleanupSequence()
