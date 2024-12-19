import pygame
import random
import numpy as np
import time 
import constant
from copy import deepcopy

TETROMINOS = {
        0: { # I
            0: [(0,0), (1,0), (2,0), (3,0)],
            90: [(1,0), (1,1), (1,2), (1,3)],
            180: [(3,0), (2,0), (1,0), (0,0)],
            270: [(1,3), (1,2), (1,1), (1,0)],
        },
        1: { # T
            0: [(1,0), (0,1), (1,1), (2,1)],
            90: [(0,1), (1,2), (1,1), (1,0)],
            180: [(1,2), (2,1), (1,1), (0,1)],
            270: [(2,1), (1,0), (1,1), (1,2)],
        },
        2: { # L
            0: [(1,0), (1,1), (1,2), (2,2)],
            90: [(0,1), (1,1), (2,1), (2,0)],
            180: [(1,2), (1,1), (1,0), (0,0)],
            270: [(2,1), (1,1), (0,1), (0,2)],
        },
        3: { # J
            0: [(1,0), (1,1), (1,2), (0,2)],
            90: [(0,1), (1,1), (2,1), (2,2)],
            180: [(1,2), (1,1), (1,0), (2,0)],
            270: [(2,1), (1,1), (0,1), (0,0)],
        },
        4: { # Z
            0: [(0,0), (1,0), (1,1), (2,1)],
            90: [(0,2), (0,1), (1,1), (1,0)],
            180: [(2,1), (1,1), (1,0), (0,0)],
            270: [(1,0), (1,1), (0,1), (0,2)],
        },
        5: { # S
            0: [(2,0), (1,0), (1,1), (0,1)],
            90: [(0,0), (0,1), (1,1), (1,2)],
            180: [(0,1), (1,1), (1,0), (2,0)],
            270: [(1,2), (1,1), (0,1), (0,0)],
        },
        6: { # O
            0: [(1,0), (2,0), (1,1), (2,1)],
            90: [(1,0), (2,0), (1,1), (2,1)],
            180: [(1,0), (2,0), (1,1), (2,1)],
            270: [(1,0), (2,0), (1,1), (2,1)],
        }
    }



class Tetrominos:
    def __init__(self):
        self.shape = 0
        self.color = 0
        self.rotation = 0                           #0 up, 1 left, 2 down, 3 right (trigonometric order )

        
    def new_piece(self):
        self.shape = TETROMINOS[random.randint(0, 6)]
        self.color = random.choice(constant.COLORS)
    
    def rotate(self):
        # Rotation de la pièce en transposant la matrice et en inversant les colonnes
        self.rotation = (self.rotation+90)%360
        
class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(constant.COLUMNS)] for _ in range(constant.ROWS)]


        self.current_piece = Tetrominos()
        self.current_piece.new_piece()
        self.current_piece_pos = [0, 0]

        self.next_piece = Tetrominos()
        self.next_piece.new_piece()

        self.score = 0

        self.running = True
        self.next_states = self.get_next_states()

    def reset(self):
        self.grid = [[0 for _ in range(constant.COLUMNS)] for _ in range(constant.ROWS)]
        self.current_piece = Tetrominos()
        self.current_piece.new_piece()
        self.current_piece_pos = [0, 0]
        self.next_piece = Tetrominos()
        self.next_piece.new_piece()
        self.score = 0
        self.running = True
        self.next_states = self.get_next_states()

        return self.get_grid_prop()
        
    def draw(self, display):
        self.draw_grid(display)
        self.draw_piece(display)
        self.draw_score(display)
        self.draw_next_pice(display)

    def draw_grid(self, display):
        for row in range(constant.ROWS):
            for col in range(constant.COLUMNS):
                rect = pygame.Rect(col * constant.CELL_SIZE + constant.GRIDPOS[0], row * constant.CELL_SIZE + constant.GRIDPOS[1], constant.CELL_SIZE, constant.CELL_SIZE)
                if self.grid[row][col] == 0:
                    pygame.draw.rect(display, constant.WHITE, rect, 1)
                else:
                    pygame.draw.rect(display, constant.COLORS[self.grid[row][col]], rect)

    def draw_piece(self,  display):
        shape = self.current_piece.shape[self.current_piece.rotation]
        for (row, col) in shape:
            rect = pygame.Rect(
                (self.current_piece_pos[0] + col) * constant.CELL_SIZE + constant.GRIDPOS[0],
                (self.current_piece_pos[1] + row) * constant.CELL_SIZE + constant.GRIDPOS[1],
                constant.CELL_SIZE,
                constant.CELL_SIZE,
                )
            pygame.draw.rect(display, self.current_piece.color, rect)
    
    def draw_next_pice(self, display):
        shape = self.next_piece.shape[self.next_piece.rotation]
        for (row, col) in shape:
            rect = pygame.Rect(
                col* constant.CELL_SIZE + constant.NEXTPIECEPOS[0],
                row* constant.CELL_SIZE + constant.NEXTPIECEPOS[1],
                constant.CELL_SIZE,
                constant.CELL_SIZE,
            )
            pygame.draw.rect(display, self.next_piece.color, rect)

    def draw_score(self, display):
        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {self.score}", True, constant.WHITE)
        display.blit(score_text, (10, 10))
        
    def next_collision(self, dx, dy):         #return 0 si pas de collision, 1 si collision sur le coté et 2 si collision vers le bas -> il faut fixer la pièce à la grille
        res = 0
        shape = self.current_piece.shape[self.current_piece.rotation]
        for (row, col) in shape:
            x = self.current_piece_pos[0] + col + dx
            y = self.current_piece_pos[1] + row + dy

            # Vérification des collisions avec les bords des côtés
            if x < 0 or x >= constant.COLUMNS:
                res = 1
                continue

            # Vérification des collisions avec la grille existante ou le bas de la grille 
            if y >= constant.ROWS or (y >= 0 and self.grid[y][x] != 0):
                if(dy == 0):
                    return 1
                else:
                    return 2
        return res
    
    def collision(self, piece, pos):            #renvoie 1 si il y a une collision avec la pièce à la position donnée et 0 sinon
        for (row, col) in piece:
            x = pos[0] + col
            y = pos[1] + row 

            # Vérification des collisions avec les bords des côtés
            if x < 0 or x >= constant.COLUMNS:
                return True

            # Vérification des collisions avec la grille existante ou le bas de la grille 
            if y >= constant.ROWS or (y >= 0 and self.grid[y][x] != 0):
                    return True
    
        return False
    
    
    def attache_piece_to_grid(self):
        shape = self.current_piece.shape[self.current_piece.rotation]
        for (row, col) in shape:
            x = self.current_piece_pos[0] + col
            y = self.current_piece_pos[1] + row

            #self.grid[y][x] = self.current_piece.color
            self.grid[y][x] = 1

        self.complete_line_check()

        self.current_piece = self.next_piece
        self.current_piece_pos = [0, 0]

        self.next_piece = Tetrominos()
        self.next_piece.new_piece()

        self.next_states = self.get_next_states()
        if(self.is_over() or self.next_states == {}):
            self.running = False
            self.score -= 2
            #print("you Lose, score : ", self.score)
        
        self.score += 1

    def attache_piece_to_grid_pos_and_shape(self, shape, pos):
        for (row, col) in shape:
            x = pos[0] + col
            y = pos[1] + row

            #self.grid[y][x] = self.current_piece.color
            self.grid[y][x] = 1
        
        
    def is_over(self):
        return any(self.grid[0])
    
    def complete_line_check(self):
        full_lines = [row for row in range(constant.ROWS) if all(self.grid[row])]
        for line in full_lines:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(constant.COLUMNS)])

        self.score += len(full_lines)**2*10
        
        return len(full_lines)
    
    def move_piece(self, dx, dy):
        collision = self.next_collision(dx, dy)
        if (collision == 0):
            self.current_piece_pos[0] += dx
            self.current_piece_pos[1] += dy
            return True
        elif collision == 2:
            self.attache_piece_to_grid()
        
        return False

    def play(self, x, rotation, render=False, display = None, render_delay=None):
        '''Makes a play given a position and a rotation, returning the reward and if the game is over'''
        self.current_piece_pos = [x, 0]
        self.current_piece.rotation = rotation

        previous_score = self.score

        # Drop piece
        while True:
            if render:
                display.fill(constant.BLACK)
                self.draw(display)
                pygame.display.flip()
                time.sleep(0.01)
            if(not self.move_piece(0, 1)):
                break
            
        return (self.score - previous_score), not self.running

    def rotate_piece(self):
        backup = self.current_piece.rotation
        self.current_piece.rotate()

        if self.next_collision(0, 0):            #il y a une collision d'une quelconque nature, il faut annuler la rotation (on peut tourner trois fois pour ça, pas ouf mais ça fait le taffe)
            self.current_piece.rotation = backup

    def get_grid_prop(self):
        '''Get properties of the board'''
        lines = self.complete_line_check()
        holes = self.number_of_holes()
        total_bumpiness, max_bumpiness = self.bumpiness()
        sum_height, max_height, min_height = self.height()
        return [lines, holes, total_bumpiness, sum_height, max_height]
    
    def number_of_holes(self):
        '''Number of holes in the board (empty sqquare with at least one block above it)'''
        holes = 0

        for col in zip(*self.grid):
            i = 0
            while i < constant.ROWS and col[i] != 1:
                i += 1
            holes += len([x for x in col[i+1:] if x == 0])

        return holes


    def bumpiness(self):
        '''Sum of the differences of heights between pair of columns'''
        total_bumpiness = 0
        max_bumpiness = 0
        min_ys = []

        for col in zip(*self.grid):
            i = 0
            while i < constant.ROWS and col[i] != 1:
                i += 1
            min_ys.append(i)
        
        for i in range(len(min_ys) - 1):
            bumpiness = abs(min_ys[i] - min_ys[i+1])
            max_bumpiness = max(bumpiness, max_bumpiness)
            total_bumpiness += abs(min_ys[i] - min_ys[i+1])

        return total_bumpiness, max_bumpiness


    def height(self):
        '''Sum and maximum height of the board'''
        sum_height = 0
        max_height = 0
        min_height = constant.ROWS

        for col in zip(*self.grid):
            i = 0
            while i < constant.ROWS and col[i] == 0:
                i += 1
            height = constant.ROWS - i
            sum_height += height
            if height > max_height:
                max_height = height
            elif height < min_height:
                min_height = height

        return sum_height, max_height, min_height

    def update(self):
        self.move_piece(0, 1)
        self.score += 0

    def get_state_size(self):
        '''Size of the state'''
        return len(self.get_grid_prop())

    def get_next_states(self):
        '''Get all possible next states'''
        states = {}

        rotations = [0, 90, 180, 270]

        # For all rotations
        for rotation in rotations:
            piece = self.current_piece.shape[rotation]
            min_x = min([p[1] for p in piece])
            max_x = max([p[1] for p in piece])

            # For all positions
            for x in range(-min_x, constant.COLUMNS - max_x):
                pos = [x, 0]

                # Drop piece
                while not self.collision(piece, pos):
                    pos[1] += 1
                pos[1] -= 1

                # Valid move
                if pos[1] >= 0:
                    backup_grid = deepcopy(self.grid)
                    backup_score = self.score
                    self.attache_piece_to_grid_pos_and_shape(piece, pos)
                    states[(x, rotation)] = self.get_grid_prop()
                    self.grid = backup_grid
                    self.score = backup_score

        
        #print(states)
        return states


