import tetris2
import pygame
import neuralNetwork
import gameLoop
import constant

def playTetris(graphicsON = False, speed = 100 , player = None):
    #init : 
    #initialisation du jeu
    tetris = tetris2.Tetris()
    if(graphicsON):
        # Initialisation de pygame
        clock = pygame.time.Clock()
        pygame.init()
        display = pygame.display.set_mode((constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
    else:
        display = None
        clock = None
    
    score = gameLoop.game_loop(tetris, display, clock, speed, graphicsON, player)

    if(graphicsON):
        pygame.quit()
    
    return score


playTetris(True, 35, None)