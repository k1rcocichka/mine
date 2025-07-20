import pygame
import sys
from pygame.sprite import Group
from .table import Board
from .settings import *


class Game:
    """Главный класс игры"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Сапёр")
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.board = Board(GRID_HEIGHT, GRID_WIDTH, MINES_COUNT)
        self.reset_button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 15, 
            PANEL_HEIGHT // 2 - 15, 
            30, 30
        )
        self.font = pygame.font.SysFont('Arial', 28)
        self.small_font = pygame.font.SysFont('Arial', 20)
        self.start_time = None
        self.elapsed_time = 0
    
    def reset_game(self):
        """Сбрасывает игру в начальное состояние"""
        self.board = Board(GRID_HEIGHT, GRID_WIDTH, MINES_COUNT)
        self.start_time = None
        self.elapsed_time = 0
    
    def draw_top_panel(self):
        """Рисует верхнюю панель с информацией"""
        panel = pygame.Rect(0, 0, SCREEN_WIDTH, PANEL_HEIGHT)
        pygame.draw.rect(self.screen, DARK_GRAY, panel)
        
        # Счетчик мин
        mines_left = max(0, MINES_COUNT - self.board.mines_flagged)
        mines_text = self.font.render(f'{mines_left:03d}', True, RED)
        self.screen.blit(mines_text, (20, PANEL_HEIGHT // 2 - mines_text.get_height() // 2))
        
        # Кнопка сброса
        pygame.draw.rect(self.screen, LIGHT_BLUE, self.reset_button_rect, border_radius=5)
        pygame.draw.rect(self.screen, BLACK, self.reset_button_rect, 2, border_radius=5)
        
        # Рисуем смайлик
        if self.board.game_over:
            # Грустный смайлик
            pygame.draw.circle(self.screen, BLACK, 
                             (SCREEN_WIDTH // 2, PANEL_HEIGHT // 2), 8)
            pygame.draw.line(self.screen, BLACK, 
                           (SCREEN_WIDTH // 2 - 6, PANEL_HEIGHT // 2 + 5),
                           (SCREEN_WIDTH // 2 + 6, PANEL_HEIGHT // 2 + 5), 2)
        elif self.board.win:
            # Победный смайлик
            pygame.draw.circle(self.screen, BLACK, 
                             (SCREEN_WIDTH // 2, PANEL_HEIGHT // 2), 8)
            pygame.draw.arc(self.screen, BLACK, 
                          (SCREEN_WIDTH // 2 - 6, PANEL_HEIGHT // 2 + 1, 12, 8),
                          0, 3.14, 2)
        else:
            # Обычный смайлик
            pygame.draw.circle(self.screen, BLACK, 
                             (SCREEN_WIDTH // 2, PANEL_HEIGHT // 2), 8)
            pygame.draw.arc(self.screen, BLACK, 
                          (SCREEN_WIDTH // 2 - 6, PANEL_HEIGHT // 2 - 1, 12, 8),
                          3.14, 6.28, 2)
        
        # Таймер
        if self.start_time and not self.board.game_over and not self.board.win:
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        time_text = self.font.render(f'{self.elapsed_time:03d}', True, RED)
        self.screen.blit(time_text, (SCREEN_WIDTH - 70, PANEL_HEIGHT // 2 - time_text.get_height() // 2))
    
    def draw_grid(self):
        """Рисует игровое поле"""
        for tile in self.board.tiles_group:
            rect = tile.rect.move(0, PANEL_HEIGHT)
            self.screen.blit(tile.image, rect)
    
    def draw_instructions(self):
        """Рисует инструкцию внизу экрана"""
        instructions = [
            "ЛКМ - открыть клетку",
            "ПКМ - поставить флаг/вопрос",
            "Средняя кнопка - быстрый доступ"
        ]
        
        for i, text in enumerate(instructions):
            text_surface = self.small_font.render(text, True, BLACK)
            self.screen.blit(text_surface, (20, SCREEN_HEIGHT - 30 - i * 25))
    
    def draw(self):
        """Отрисовывает весь игровой интерфейс"""
        self.screen.fill(BACKGROUND)
        self.draw_top_panel()
        self.draw_grid()
        self.draw_instructions()
        pygame.display.flip()
    
    def handle_events(self):
        """Обрабатывает события игры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Проверка клика на кнопке сброса
                if self.reset_button_rect.collidepoint(mouse_pos):
                    self.reset_game()
                    continue
                
                # Проверка клика на игровом поле
                if mouse_pos[1] > PANEL_HEIGHT:
                    grid_pos = (mouse_pos[0], mouse_pos[1] - PANEL_HEIGHT)
                    row = grid_pos[1] // GRID_SIZE
                    col = grid_pos[0] // GRID_SIZE
                    
                    if 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH:
                        if event.button == 1:  # Левая кнопка мыши
                            if self.start_time is None and not self.board.game_over and not self.board.win:
                                self.start_time = pygame.time.get_ticks()
                            
                            if not self.board.game_over and not self.board.win:
                                result = self.board.open_tile(row, col)
                                if result == 'mine':
                                    self.board.game_over = True
                                elif self.board.check_win():
                                    self.board.win = True
                        
                        elif event.button == 3:  # Правая кнопка мыши
                            if not self.board.game_over and not self.board.win:
                                self.board.toggle_tile_mark(row, col)
                                if self.board.check_win():
                                    self.board.win = True
                        
                        elif event.button == 2:  # Средняя кнопка мыши
                            if not self.board.game_over and not self.board.win:
                                tile = self.board.grid[row][col]
                                if tile.state == OPENED and tile.neighbor_mines > 0:
                                    self.auto_open(row, col)
                                    if self.board.check_win():
                                        self.board.win = True
        
        return True
    
    def auto_open(self, row, col):
        """Автоматически открывает соседей при нажатии средней кнопкой"""
        tile = self.board.grid[row][col]
        if tile.state != OPENED or tile.neighbor_mines == 0:
            return
        
        neighbors = self.board.get_neighbors(row, col)
        flag_count = sum(1 for t in neighbors if t.state == FLAGGED)
        
        if flag_count == tile.neighbor_mines:
            for neighbor in neighbors:
                if neighbor.state != FLAGGED:
                    if neighbor.is_mine:
                        self.board.game_over = True
                        self.board.reveal_all_mines()
                        return
                    neighbor.open()
                    if neighbor.neighbor_mines == 0:
                        self.board.open_neighbors(neighbor.row, neighbor.col)
    
    def run(self):
        """Запускает главный игровой цикл"""
        running = True
        while running:
            running = self.handle_events()
            
            if not self.board.game_over and not self.board.win and self.start_time:
                self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            
            self.draw()
            self.clock.tick(30)
        
        pygame.quit()
        sys.exit()