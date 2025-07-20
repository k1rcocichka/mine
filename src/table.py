import random
from pygame.sprite import Group
from .cell import Cell
from .settings import *

class Board:
    """Класс игрового поля"""
    def __init__(self, rows, cols, mines_count):
        self.rows = rows
        self.cols = cols
        self.mines_count = mines_count
        self.grid = [[Cell(i, j) for j in range(cols)] for i in range(rows)]
        self.tiles_group = Group()
        self.first_click = True
        self.game_over = False
        self.win = False
        self.mines_flagged = 0
        
        for row in self.grid:
            for tile in row:
                self.tiles_group.add(tile)
    
    def place_mines(self, safe_row, safe_col):
        """Расставляет мины, избегая безопасной области"""
        positions = [(i, j) for i in range(self.rows) for j in range(self.cols)]
        positions = [
            (i, j) for (i, j) in positions 
            if abs(i - safe_row) > 1 or abs(j - safe_col) > 1
        ]
        
        mine_positions = random.sample(positions, self.mines_count)
        
        for i, j in mine_positions:
            self.grid[i][j].is_mine = True
        
        self.update_neighbors()
    
    def update_neighbors(self):
        """Обновляет количество мин у соседей для всех клеток"""
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.grid[i][j].is_mine:
                    count = 0
                    for di in (-1, 0, 1):
                        for dj in (-1, 0, 1):
                            ni, nj = i + di, j + dj
                            if 0 <= ni < self.rows and 0 <= nj < self.cols:
                                if self.grid[ni][nj].is_mine:
                                    count += 1
                    self.grid[i][j].neighbor_mines = count
                    self.grid[i][j].update_image()
    
    def get_neighbors(self, row, col):
        """Возвращает соседей клетки"""
        neighbors = []
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == 0 and dj == 0:
                    continue
                ni, nj = row + di, col + dj
                if 0 <= ni < self.rows and 0 <= nj < self.cols:
                    neighbors.append(self.grid[ni][nj])
        return neighbors
    
    def open_tile(self, row, col):
        """Открывает указанную клетку"""
        tile = self.grid[row][col]
        
        if self.first_click:
            self.place_mines(row, col)
            self.first_click = False
        
        if tile.state != HIDDEN and tile.state != QUESTION:
            return False
        
        if tile.is_mine:
            tile.open()
            self.game_over = True
            self.reveal_all_mines()
            return 'mine'
        
        opened = tile.open()
        if opened and tile.neighbor_mines == 0:
            self.open_neighbors(row, col)
        
        return opened
    
    def open_neighbors(self, row, col):
        """Рекурсивно открывает соседей для пустых клеток"""
        for neighbor in self.get_neighbors(row, col):
            if neighbor.state == HIDDEN or neighbor.state == QUESTION:
                if not neighbor.is_mine:
                    neighbor.open()
                    if neighbor.neighbor_mines == 0:
                        self.open_neighbors(neighbor.row, neighbor.col)
    
    def toggle_tile_mark(self, row, col):
        """Переключает маркер на клетке"""
        tile = self.grid[row][col]
        if tile.state == OPENED:
            return
        
        prev_state = tile.state
        tile.toggle_mark()
        
        if prev_state == FLAGGED:
            self.mines_flagged -= 1
        elif tile.state == FLAGGED:
            self.mines_flagged += 1
    
    def reveal_all_mines(self):
        """Открывает все мины при проигрыше"""
        for row in self.grid:
            for tile in row:
                if tile.is_mine and tile.state != FLAGGED:
                    tile.state = OPENED
                    tile.update_image()
    
    def check_win(self):
        """Проверяет условия победы"""
        for row in self.grid:
            for tile in row:
                if not tile.is_mine and tile.state != OPENED:
                    return False
                if tile.is_mine and tile.state != FLAGGED:
                    return False
        return True