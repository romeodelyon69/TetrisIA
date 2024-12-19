import pygame

# Dimensions de la fenêtre
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 1000
CELL_SIZE = 30  # Taille d'une case
COLUMNS = 10
ROWS = 18
GRIDPOS = [50, 100]
NEXTPIECEPOS = [400, 120]


# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Bleu
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Jaune
    (0, 255, 0),    # Vert
    (128, 0, 128),  # Violet
    (255, 0, 0),    # Rouge
]

def game_loop(tetris, display, clock, speed, graphicsON, player):
    time_keeper = 0
    while tetris.running:
        tetris.get_next_states()
        time_keeper += 1
        
        if(time_keeper == 5):
            
            tetris.update()
            time_keeper = 0
                

        if(player == None):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tetris.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        tetris.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        tetris.move_piece(1, 0)
                    elif event.key == pygame.K_DOWN:
                        tetris.move_piece(0, 1)
                    elif event.key == pygame.K_UP:
                        tetris.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        while(True):
                            pass
            
            
        else:                       #le jeu est controllé par l'IA du coup
            action = player.predict(tetris.output())
            
            #print(action)
            if action == 1:
                tetris.move_piece(-1, 0)
            if action == 2:
                tetris.move_piece(1, 0)
            if action == 3:
                tetris.move_piece(0, 1)
            if action == 4:
                tetris.rotate_piece()

            if(time_keeper == 5):
                tetris.update()
                time_keeper = 0
            

        if(graphicsON):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tetris.running = False
            clock.tick(speed)
            # Dessiner la grille et la pièce actuelle
            display.fill(BLACK)
            tetris.draw(display)
            pygame.display.flip()

    return tetris.score