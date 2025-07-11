import pygame
from .mines import Cell
from .settings import *


class Mineswapper():
    """Класс основного приложнеия"""
    def __init__(self):
        self.name = "mineswapper"

    def reset_game(self):
        pass

    def revel(self):
        pass

    def check_win(self):
        pass

    def toggle_flag(self):
        pass

    def draw(self):
        pygame.init()
        screen = pygame.display.set_mode(DISPLAY)
        screen.fill("GREY")
        run = True

        all_cells = pygame.sprite.Group()

        x, y = 10, 10

        for i in range(GRID_SIZES):
            for j in range(GRID_SIZES):
                cell = Cell(x, y)
                all_cells.add(cell)
                x = x + 35
            x = 10
            y = y + 35

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        clicked_sprites = [s for s in all_cells if s.rect.collidepoint(mouse_pos)]
                        for sprite in clicked_sprites:
                            sprite.image.fill("RED")
                

            all_cells.draw(screen)
            pygame.display.flip()