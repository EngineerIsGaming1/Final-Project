import numpy as np
import pygame
from pygame.locals import *
 
class App:
    def __init__(self):
        pygame.init() #pygame.init initializes game module
        self._running = True
        self._display_surf = None
        self.size = (840, 600)
        self.rows = 4
        self.cols = 4
        self.clock = pygame.time.Clock()


    def playerOneAction(self):
        actionOne = True
        actionTwo = True

        # while actionOne:
        #     for event in pygame.event.get():
        #         if event.type == 
        # https://stackoverflow.com/questions/67778032/drawing-a-rectangle-on-mouse-position-in-python-using-pygame
        # https://www.youtube.com/watch?v=yKcupTojOek
        pass

    def playerTwoAction(self):
        pass

    def on_cleanup(self):
        pygame.quit()
    
    def startupSequence(self):
        rowArray = np.linspace(0, self.size[1], num = (self.rows + 2))
        colArray = np.linspace(0, self.size[0], num = (self.cols + 2))

        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        # https://stackoverflow.com/questions/29135147/what-do-hwsurface-and-doublebuf-do
        # HWSURFACE -> hardware acceleration. DOUBLEBUF -> reduces artifacting by saving to vram
        self._display_surf.fill("white")
        [[pygame.draw.circle(self._display_surf, "black", (dotCol, dotRow), 10) for dotCol in colArray[1:-1]] for dotRow in rowArray[1:-1]]
        pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
 
    def on_execute(self):
        self.startupSequence()

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.playerOneAction()
            self.playerTwoAction()
            # for event in pygame.event.get():
            #     # print(event)
            #     self.on_event(event)
            
            # self.on_loop()
            # self.on_render()
            self.clock.tick(60)
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()



# Citations:
# http://pygametutorials.wikidot.com/tutorials-basic
# https://www.pygame.org/docs/
# https://www.youtube.com/watch?v=FKv5KBzFW_s
#   these are the rules that I'm going to program
