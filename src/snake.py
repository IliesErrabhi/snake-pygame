import pygame
from .constants import *

class Snake:
    def __init__(self):
        #self.body[0] is the head
        middleX = SCREEN_HEIGHT // 2
        middleY = SCREEN_WIDTH //  2
        self.body = [[middleX,middleY], [middleX - 1, middleY - 1], [middleX - 2, middleY - 2]]
        self.direction = "RIGHT"
        self.grow = False                               # tells whether the snake ate an apple or not

    def move(self):
        '''remove one square from the back and add one to the front'''

        headX,headY = self.body[0]
        
        if   self.direction   == "UP":
            headY -= CELL_SIZE
        elif self.direction == "DOWN":
            headY += CELL_SIZE
        elif self.direction == "RIGHT":
            headX += CELL_SIZE
        else :
            headX -= CELL_SIZE

        self.body.insert(0,[headX,headY])
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def draw(self,surface):
        for bodyPart in self.body:
            pygame.draw.rect(surface,(39, 174, 96),(bodyPart[0],bodyPart[1],
                                                    CELL_SIZE,CELL_SIZE))