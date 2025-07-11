import pygame


class Cell(pygame.sprite.Sprite):
    """Класс клетки"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(("GREEN"))
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y