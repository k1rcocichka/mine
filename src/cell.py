import pygame
from pygame.sprite import Sprite
from .settings import *

class Cell(Sprite):
    """Класс для представления клетки на игровом поле"""
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.is_mine = False
        self.state = HIDDEN
        self.neighbor_mines = 0
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        self.update_image()
    
    def update_image(self):
        """Обновляет изображение клетки в зависимости от состояния"""
        self.image.fill(BACKGROUND)
        
        if self.state == HIDDEN:
            pygame.draw.rect(self.image, DARK_GRAY, (0, 0, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(self.image, WHITE, (0, 0, GRID_SIZE, GRID_SIZE), 2)
        elif self.state == OPENED:
            pygame.draw.rect(self.image, GRAY, (0, 0, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(self.image, DARK_GRAY, (0, 0, GRID_SIZE, GRID_SIZE), 1)
            
            if self.is_mine:
                pygame.draw.circle(self.image, BLACK, 
                                  (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//3)
            elif self.neighbor_mines > 0:
                font = pygame.font.SysFont('Arial', 24)
                color = NUMBER_COLORS.get(self.neighbor_mines, BLACK)
                text = font.render(str(self.neighbor_mines), True, color)
                text_rect = text.get_rect(center=(GRID_SIZE//2, GRID_SIZE//2))
                self.image.blit(text, text_rect)
        elif self.state == FLAGGED:
            pygame.draw.rect(self.image, DARK_GRAY, (0, 0, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(self.image, WHITE, (0, 0, GRID_SIZE, GRID_SIZE), 2)
            
            # Рисуем флаг
            pygame.draw.rect(self.image, RED, (10, 8, 4, 14))
            pygame.draw.polygon(self.image, RED, [
                (14, 8), (22, 12), (14, 16)
            ])
        elif self.state == QUESTION:
            pygame.draw.rect(self.image, DARK_GRAY, (0, 0, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(self.image, WHITE, (0, 0, GRID_SIZE, GRID_SIZE), 2)
            
            font = pygame.font.SysFont('Arial', 24)
            text = font.render('?', True, BLUE)
            text_rect = text.get_rect(center=(GRID_SIZE//2, GRID_SIZE//2))
            self.image.blit(text, text_rect)
    
    def open(self):
        """Открывает клетку"""
        if self.state != OPENED:
            self.state = OPENED
            self.update_image()
            return True
        return False
    
    def toggle_mark(self):
        """Переключает состояние маркера (флаг/вопрос/нет)"""
        if self.state == HIDDEN:
            self.state = FLAGGED
        elif self.state == FLAGGED:
            self.state = QUESTION
        elif self.state == QUESTION:
            self.state = HIDDEN
        self.update_image()