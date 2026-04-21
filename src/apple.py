import pygame
from random import randint
from .constants import SCREEN_WIDTH,SCREEN_HEIGHT,CELL_SIZE

class Apple:
    def __init__(self):
        self.position = [0,0]
        self.randomizePosition()

    def randomizePosition(self,snakeBody=None):
        nbColumns = SCREEN_WIDTH  // CELL_SIZE
        nbLines   = SCREEN_HEIGHT // CELL_SIZE

        while True:
                                #numéro de case           #bonne coordonnée
            self.position[0] = randint(0,nbColumns - 1) * CELL_SIZE
            self.position[1] = randint(0,nbLines   - 1) * CELL_SIZE
            if snakeBody is None or self.position not in snakeBody:
                break

    
    def draw(self,surface):
        pygame.draw.rect(surface,(192, 57, 43),pygame.Rect(self.position[0],self.position[1],
                                                CELL_SIZE,CELL_SIZE))