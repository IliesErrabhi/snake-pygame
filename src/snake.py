import pygame
from .constants import *

class Snake:
    def __init__(self):
        #self.body[0] is the head
        gridX = (SCREEN_WIDTH // 2) // CELL_SIZE 
        gridY = (SCREEN_HEIGHT //  2) // CELL_SIZE 

        startX = gridX * CELL_SIZE
        startY = gridY * CELL_SIZE
        self.body = [[startX ,startY], [startX - CELL_SIZE, startY], [startX - 2 * CELL_SIZE, startY]]
        self.direction = "RIGHT"
        self.grow = False                               # tells whether the snake ate an apple or not

        
        #Pour les images, au lieu de se coltiner 15 images différentes on va en prendre quelques unes et les tourner

        # --- 1. CHARGEMENT DES IMAGES DE BASE ---
        head_img          = pygame.image.load("assets/head_right.png").convert_alpha()
        tail_img          = pygame.image.load("assets/tail_left.png").convert_alpha()
        body_img = pygame.image.load("assets/body_horizontal.png").convert_alpha()

        # Redimensionnement pour correspondre à la grille
        self.head_img = pygame.transform.scale(head_img, (CELL_SIZE, CELL_SIZE))
        self.tail_img = pygame.transform.scale(tail_img, (CELL_SIZE, CELL_SIZE))
        self.body_img = pygame.transform.scale(body_img, (CELL_SIZE, CELL_SIZE))

        # TÊTE (Image de base = Regarde à DROITE)
        self.head_right = self.head_img
        self.head_up    = pygame.transform.rotate(self.head_img, 90)   # Tourne d'1/4 de tour vers le haut
        self.head_left  = pygame.transform.rotate(self.head_img, 180)  # Demi-tour
        self.head_down  = pygame.transform.rotate(self.head_img, -90)  # Tourne d'1/4 de tour vers le bas
 
        # QUEUE (Image de base DROITE)
        self.tail_right = self.tail_img
        self.tail_up    = pygame.transform.rotate(self.tail_img, 90)
        self.tail_left  = pygame.transform.rotate(self.tail_img, 180)
        self.tail_down  = pygame.transform.rotate(self.tail_img, -90)

        # CORPS (Image de base DROITE)
        self.body_h = self.body_img
        self.body_v = pygame.transform.rotate(self.body_h, 90)

        # Image de base : virage qui vient du BAS et va vers la DROITE (ou vice-versa)
        curve_img = pygame.image.load("assets/body_bottomleft.png").convert_alpha()
        self.curve = pygame.transform.scale(curve_img, (CELL_SIZE, CELL_SIZE))

        # Les 4 rotations possibles
        self.body_bl = self.curve                          # Bottom-Left (Bas -> Gauche)
        self.body_br = pygame.transform.rotate(self.curve, 90)   # Bottom-Right
        self.body_tr = pygame.transform.rotate(self.curve, 180)  # Top-Right
        self.body_tl = pygame.transform.rotate(self.curve, 270)  # Top-Left


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

    def draw(self, surface):
        for index, block in enumerate(self.body):
            x, y = block[0], block[1]
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            # 1. HEAD
            if index == 0:
                if self.direction == "UP":
                    surface.blit(self.head_up, rect)
                elif self.direction == "DOWN":
                    surface.blit(self.head_down, rect)
                elif self.direction == "LEFT":
                    surface.blit(self.head_left, rect)
                elif self.direction == "RIGHT":
                    surface.blit(self.head_right, rect)

            # 2. TAIL
            elif index == len(self.body) - 1:
                # On regarde le segment juste avant pour savoir où pointe la queue
                prev_block = self.body[index - 1]
                diff_x = prev_block[0] - x
                diff_y = prev_block[1] - y

                if diff_x > 0:   surface.blit(self.tail_right, rect) # RIGHT
                elif diff_x < 0: surface.blit(self.tail_left, rect)  # LEFT
                elif diff_y > 0: surface.blit(self.tail_down, rect)  # DOWN
                elif diff_y < 0: surface.blit(self.tail_up, rect)    # UP

            # 3. BODY
            else:
                prev = self.body[index - 1]
                next = self.body[index + 1]

                # --- LIGNES DROITES ---
                if prev[0] == next[0]:                               # Aligné verticalement
                    surface.blit(self.body_v, rect)
                elif prev[1] == next[1]:                             # Aligné horizontalement
                    surface.blit(self.body_h, rect)

                # --- VIRAGES (CORNERS) ---
                else:
                    p_x, p_y = prev[0] - x, prev[1] - y
                    n_x, n_y = next[0] - x, next[1] - y

                    # On teste les 4 combinaisons de virages
                    if p_x == -CELL_SIZE and n_y == -CELL_SIZE or n_x == -CELL_SIZE and p_y == -CELL_SIZE:
                        surface.blit(self.body_tl, rect) # Top-Left
                    elif p_x == -CELL_SIZE and n_y == CELL_SIZE or n_x == -CELL_SIZE and p_y == CELL_SIZE:
                        surface.blit(self.body_bl, rect) # Bottom-Left
                    elif p_x == CELL_SIZE and n_y == -CELL_SIZE or n_x == CELL_SIZE and p_y == -CELL_SIZE:
                        surface.blit(self.body_tr, rect) # Top-Right
                    elif p_x == CELL_SIZE and n_y == CELL_SIZE or n_x == CELL_SIZE and p_y == CELL_SIZE:
                        surface.blit(self.body_br, rect) # Bottom-Right