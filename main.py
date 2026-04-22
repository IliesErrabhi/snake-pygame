import pygame
from src.constants import *
from src.snake import *
from src.apple import *

# initialisation de tous les sous-modules de Pygame(vidéo,son,joystick)
pygame.init()

# création de la fenêtre de jeu (largeur,hauteur) en pixels
screen = pygame.display.set_mode((1280, 720)) # surface principale

# s'assure que le jeu de tourne pas trop vite
clock = pygame.time.Clock()
running = True
snake = Snake()
apple = Apple()


def gameover(surface):
    # 1. font cration                  #size
    font = pygame.font.SysFont("Arial", 60)
    
    # 2. image creation 
    text_surface = font.render("Game over hahaha", True, (255, 255, 255))
    
    # 3. Center the message
    text_rect = text_surface.get_rect(center=(1280 // 2, 720 // 2))
    
    # 4. Draw of the screen
    surface.blit(text_surface, text_rect)
    pygame.display.flip()
    
    # 5. Wait 3 sec before leaving
    pygame.time.wait(3000)


while running:
    # poll for events
    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT  and snake.direction != "RIGHT":
                print("LEFT")
                snake.direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                print("RIGHT")
                snake.direction = "RIGHT"
            elif event.key == pygame.K_UP    and snake.direction != "DOWN":
                print("UP")
                snake.direction = "UP"
            elif event.key == pygame.K_DOWN  and snake.direction != "UP":
                print("DOWN")
                snake.direction = "DOWN"

    # UPDATE
    snake.move()
    head = snake.body[0]

    # Collisions handling
    if (head[0] < 0 or head[0] >= SCREEN_WIDTH) or (head[1] < 0 or head[1] >= SCREEN_HEIGHT) or head in snake.body[1:]:
        gameover(screen)
        running = False

    # Check if the snake eats the apple
    if head == apple.position:
        snake.grow = True
        apple.randomizePosition(snake.body)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # drawing of the apple
    apple.draw(screen)
    # drawing of the snake
    snake.draw(screen)
    


    # RENDER YOUR GAME HERE
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)      #pygame s'assure que le jeu ne dépasse pas le nombre d'FPS établi


# on éteint le moteur pygame et on ferme la fenêtre
pygame.quit()