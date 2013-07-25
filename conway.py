import pygame
import rabbyt
import random
import time


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SPRITE_WIDTH = 32
SPRITE_HEIGHT = 32
GRID_WIDTH = 18
GRID_HEIGHT = 18
WAIT_BETWEEN_STEPS = 0.3
SPRITE_LOCATION = 'dudeguy.png'


# make a random 12 x 12, 2 dimensional array
grid = [[random.randint(0, 1) for x in range(0, GRID_WIDTH)] for y in range(0, GRID_HEIGHT)]

def check_neighbor(grid, row, column):
    try:
        return grid[row][column]
    except IndexError as e:
        # ran into a border, don't count it as a neighbor
        return 0

def step_grid(grid):
    nextgrid = [[0 for x in range(0, GRID_WIDTH)] for y in range(0, GRID_HEIGHT)]
    for rowcount, row in enumerate(grid):
        for count, item in enumerate(row):
                
            neighbors = [ 
                          check_neighbor(grid, rowcount, count + 1),
                          check_neighbor(grid, rowcount, count - 1),
                          check_neighbor(grid, rowcount - 1, count),
                          check_neighbor(grid, rowcount - 1, count - 1),
                          check_neighbor(grid, rowcount - 1, count + 1),
                          check_neighbor(grid, rowcount + 1, count),
                          check_neighbor(grid, rowcount + 1, count - 1),
                          check_neighbor(grid, rowcount + 1, count + 1),
                        ]

            if item == 1:
                if sum(neighbors) < 2 or sum(neighbors) > 3:
                    # overcrowded or undercrowded, dies
                    nextgrid[rowcount][count] = 0

                elif sum(neighbors) is 2 or sum(neighbors) is 3:
                    # just right, live til next generation
                    nextgrid[rowcount][count] = 1
            else:
                if sum(neighbors) is 3:
                    # gave birth!
                    nextgrid[rowcount][count] = 1

    del(grid)
    return nextgrid

def draw_grid(grid):
    renderables = []
    for rowcount, row in enumerate(grid):
        for count, item in enumerate(row):
            if item == 1:
                sprite = rabbyt.Sprite(SPRITE_LOCATION)
                x = (count * SPRITE_WIDTH) - (SCREEN_WIDTH / 2) + SPRITE_WIDTH
                y = (rowcount * SPRITE_HEIGHT) - (SCREEN_HEIGHT / 2) + SPRITE_HEIGHT
                sprite.xy = (x, y)
                renderables.append(sprite)
                
    renderables.reverse()
    for renderable in renderables:
        renderable.render()

    del(renderables)

if __name__ == '__main__':
    rabbyt.init_display((SCREEN_WIDTH, SCREEN_HEIGHT))

    while not pygame.event.get(pygame.QUIT) or max(grid) == 0:
        rabbyt.clear((0., 0., 0., 0.))
        draw_grid(grid)
        pygame.display.flip()
        time.sleep(WAIT_BETWEEN_STEPS)
        grid = step_grid(grid)

