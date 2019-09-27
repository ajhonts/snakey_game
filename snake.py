import pygame
import sys
import time
import random

from pygame.locals import *

FPS = 5
pygame.init()
fpsClock=pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((255,255,255))
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 40)

GRIDSIZE=10
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)
    
screen.blit(surface, (0,0))

def draw_box(surf, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRIDSIZE, GRIDSIZE))
    pygame.draw.rect(surf, color, r)

class Snake(object):
    def __init__(self):
        self.lose()
        self.color = (0,0,0)
        self.move_snake = False

    def get_head_position(self):
        return self.positions[0]

    def lose(self):
        self.length = 1
        self.positions =  [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def point(self, pt):
        if self.length > 1 and (pt[0] * -1, pt[1] * -1) == self.direction:
            return
        else:
            self.direction = pt

    def move(self,other_snake):
        if self.move_snake == True:
            cur = self.positions[0]
            x, y = self.direction
            new = (((cur[0]+(x*GRIDSIZE)) % SCREEN_WIDTH), (cur[1]+(y*GRIDSIZE)) % SCREEN_HEIGHT)
            if len(self.positions) > 2 and new in self.positions[2:]:
                self.lose()
            elif len(self.positions) > 2 and new in other_snake.positions[:]:
                self.lose()
            else:
                self.positions.insert(0, new)
                if len(self.positions) > self.length:
                    self.positions.pop()
    
    def draw(self, surf):
        for p in self.positions:
            draw_box(surf, self.color, p)

class Apple(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (255,0,0)
        self.randomize()

    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRIDSIZE, random.randint(0, GRID_HEIGHT-1) * GRIDSIZE)

    def draw(self, surf):
        draw_box(surf, self.color, self.position)

def check_eat(snake, apple):
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize()

if __name__ == '__main__':
    snake = Snake()
    snake2 = Snake()
    apple = Apple()
    
    while True:
        a = False
        b = False
        while a == False:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        snake.move_snake = True
                        snake.point(UP)
                        a = True
                    elif event.key == K_DOWN:
                        snake.move_snake = True
                        snake.point(DOWN)
                        a = True
                    elif event.key == K_LEFT:
                        snake.move_snake = True
                        snake.point(LEFT)
                        a = True
                    elif event.key == K_RIGHT:
                        snake.move_snake = True
                        snake.point(RIGHT)
                        a = True
                    elif event.key == K_SPACE:
                        snake.move_snake = False
                        a = True
        while b == False:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_w:
                        snake2.move_snake = True
                        snake2.point(UP)
                        b = True
                    elif event.key == K_s:
                        snake2.move_snake = True
                        snake2.point(DOWN)
                        b = True
                    elif event.key == K_a:
                        snake2.move_snake = True
                        snake2.point(LEFT)
                        b = True
                    elif event.key == K_d:
                        snake2.move_snake = True
                        snake2.point(RIGHT)
                        b = True
                    elif event.key == K_SPACE:
                        snake2.move_snake = False
                        b = True


        surface.fill((255,255,255))
        snake.move(snake2)
        snake2.move(snake)
        check_eat(snake, apple)
        check_eat(snake2, apple)
        snake.draw(surface)
        snake2.draw(surface)
        apple.draw(surface)
        font = pygame.font.Font(None, 36)
        text = font.render(str(snake.length), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = 20
        surface.blit(text, textpos)
        screen.blit(surface, (0,0))

        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(FPS + snake.length/3)
        print(snake.positions)
