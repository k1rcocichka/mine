import pygame
from .mines import Cell
from .settings import *


class Mineswapper():
    def __init__(self):
        self.name = "mineswapper"

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(DISPLAY)
        screen.fill("GREY")
        run = True

        all_cells = pygame.sprite.Group()

        x, y = 0, 0

        for i in range(8):
            for j in range(8):
                cell = Cell(x, y)
                all_cells.add(cell)
                x = x + 10
                print(x, y)
            x = 0
            y = y + 10

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            all_cells.draw(screen)
            

            pygame.display.flip()