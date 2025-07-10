import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(("GREEN"))
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y