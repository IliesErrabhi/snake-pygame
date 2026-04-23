import pygame
from src.constants import *
from src.snake import *
from src.apple import *

# initialisation de tous les sous-modules de Pygame(vidéo,son,joystick)
pygame.init()

# création de la fenêtre de jeu (largeur,hauteur) en pixels
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # surface principale
pygame.display.set_caption("Snake 🐍")
# s'assure que le jeu de tourne pas trop vite
clock = pygame.time.Clock()
running = True

def show_game_over_menu(surface):
    font = pygame.font.SysFont("Arial", 45)
    font_small = pygame.font.SysFont("Arial", 20)
    
    # Textes
    title = font.render("GAME OVER :(", True, "red")
    retry_txt = font_small.render("Press R to try again", True, "white")
    quit_txt = font_small.render("Press Q to leave", True, "white")
    
    # Affichage
    surface.fill("black")

    # 4. Draw of the screen
    surface.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)))
    surface.blit(retry_txt, retry_txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30)))
    surface.blit(quit_txt, quit_txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70)))
    pygame.display.flip()

    # Boucle d'attente spécifique au menu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "RETRY"
                if event.key == pygame.K_q:
                    return "QUIT"


def show_pause_menu(surface):
    font = pygame.font.SysFont("Arial", 60)
    text = font.render("PAUSE - Press P to resume", True, "white")
    surface.blit(text, text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
    pygame.display.flip()

    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    paused = False


def show_you_won_menu(surface):
    font = pygame.font.SysFont("Arial", 50)
    font_small = pygame.font.SysFont("Arial", 30)
    
    # Textes
    title = font.render("YOU WON :)", True, "green")
    retry_txt = font_small.render("Press R to try again", True, "white")
    quit_txt = font_small.render("Press Q to leave", True, "white")
    
    # Affichage
    surface.fill("black")

    # 4. Draw of the screen
    surface.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)))
    surface.blit(retry_txt, retry_txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30)))
    surface.blit(quit_txt, quit_txt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70)))
    pygame.display.flip()

    # Boucle d'attente spécifique au menu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "RETRY"
                if event.key == pygame.K_q:
                    return "QUIT"



def resetGame():
    return Snake(),Apple()


snake,apple = resetGame()
while running:
    # poll for events
    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                show_pause_menu(screen)
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT  and snake.direction != "RIGHT":
                snake.direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                snake.direction = "RIGHT"
            elif event.key == pygame.K_UP    and snake.direction != "DOWN":
                snake.direction = "UP"
            elif event.key == pygame.K_DOWN  and snake.direction != "UP":
                snake.direction = "DOWN"

    # UPDATE
    snake.move()
    head = snake.body[0]

    # Collisions handling
    if (head[0] < 0 or head[0] >= SCREEN_WIDTH) or (head[1] < 0 or head[1] >= SCREEN_HEIGHT) or head in snake.body[1:]:
        choice = show_game_over_menu(screen)
        if choice == "RETRY":
            snake, apple = resetGame()
            continue
        else:
            running = False # On quitte

    if len(snake.body) == ((SCREEN_HEIGHT // CELL_SIZE) * (SCREEN_WIDTH //CELL_SIZE)):
        choice = show_you_won_menu(screen)
        if choice == "RETRY":
            snake, apple = resetGame()
            continue
        else:
            running = False # On quitte

    # Check if the snake eats the apple
    if head == apple.position:
        snake.grow = True
        apple.randomizePosition(snake.body)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("pink")

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