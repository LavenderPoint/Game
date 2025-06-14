import pygame
import sys
import random
import math
import os
from pygame.locals import *

# Флаг для определения веб-среды
WEB_MODE = 'pygame_web' in sys.modules or 'emscripten' in sys.modules

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Адаптация констант для веб-среды
if WEB_MODE:
    SCREEN_WIDTH = 360
    SCREEN_HEIGHT = 640
    IS_MOBILE = True
    TASKS_PER_CATEGORY = 10
    
    # Упрощенные шрифты
    def get_font(size, bold=False):
        try:
            return pygame.font.Font(None, size)
        except:
            return pygame.font.SysFont("Arial", size, bold=bold)
    
    title_font = get_font(36, True)
    header_font = get_font(28, True)
    normal_font = get_font(20)
    small_font = get_font(16)
    
    # Упрощенный класс Player
    class Player:
        def __init__(self, name):
            self.name = name
            self.score = 0
            self.color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            self.avatar = self.generate_avatar()
            
        def generate_avatar(self):
            size = 40
            avatar = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(avatar, self.color, (size//2, size//2), size//2)
            return avatar
else:
    # Константы для локального запуска
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    IS_MOBILE = False
    TASKS_PER_CATEGORY = 20
    
    # Шрифты
    title_font = pygame.font.SysFont("Arial", 48, bold=True)
    header_font = pygame.font.SysFont("Arial", 32, bold=True)
    normal_font = pygame.font.SysFont("Arial", 24)
    small_font = pygame.font.SysFont("Arial", 20)
    
    # Класс Player
    class Player:
        def __init__(self, name):
            self.name = name
            self.score = 0
            self.color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            self.avatar = self.generate_avatar()
            
        def generate_avatar(self):
            size = 60 if IS_MOBILE else 80
            avatar = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(avatar, self.color, (size//2, size//2), size//2)
            initials = "".join([n[0] for n in self.name.split()]).upper()[:2]
            font_size = header_font.size if IS_MOBILE else HEADER_FONT_SIZE
            font = pygame.font.SysFont("Arial", font_size, bold=True)
            text = font.render(initials, True, (255, 255, 255))
            avatar.blit(text, (size//2 - text.get_width()//2, size//2 - text.get_height()//2))
            return avatar

# Общие константы
BACKGROUND_COLOR = (255, 255, 200)
TEXT_COLOR = (80, 50, 50)
BUTTON_COLOR = (255, 182, 193)
BUTTON_HOVER_COLOR = (255, 105, 180)
PANEL_COLOR = (255, 250, 240)
CATEGORY_COLORS = [
    (255, 182, 193),  # Розовый
    (173, 216, 230),  # Голубой
    (144, 238, 144),  # Зеленый
    (255, 99, 71)     # Красный
]

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Подарочек")

# Класс Game (упрощенный)
class Game:
    def __init__(self):
        self.players = []
        self.current_player_idx = 0
        self.state = "SETUP"
        self.tasks_per_category = TASKS_PER_CATEGORY
        self.setup_tasks()
        self.selected_category = None
        self.selected_difficulty = None
        self.task_window_open = False
        self.task_result = None
        self.tasks_count_input = str(self.tasks_per_category)
        self.show_answer = False
        self.round_counter = 0
        self.completed_tasks = 0
        self.total_tasks = 0
        self.tasks_remaining = 0
        self.category_scroll = [0, 0, 0, 0]
        self.active_category = None
        self.scroll_start_x = 0
        
    def setup_tasks(self):
        self.categories = ["Загадки", "Творчество", "Слова", "Физподготовка"]
        self.tasks = []
        for cat_idx in range(4):
            category_tasks = []
            for diff in range(self.tasks_per_category):
                task = {
                    "description": f"Задание {diff+1} в категории {self.categories[cat_idx]}",
                    "completed": False,
                    "difficulty": diff + 1,
                    "answer": f"Ответ на задание {diff+1}"
                }
                category_tasks.append(task)
            self.tasks.append(category_tasks)
        
        self.total_tasks = 4 * self.tasks_per_category
        self.tasks_remaining = self.total_tasks
    
    def start_game(self):
        if len(self.players) < 2:
            return False
        try:
            count = int(self.tasks_count_input)
            if count < 5 or count > 50:
                return False
            self.tasks_per_category = count
            self.setup_tasks()
            self.state = "PLAYING"
            self.round_counter = 0
            self.completed_tasks = 0
            return True
        except:
            return False
    
    def add_player(self, name):
        if name and len(self.players) < 15:
            self.players.append(Player(name))
            return True
        return False
    
    def next_player(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        if self.current_player_idx == 0:
            self.round_counter += 1
            if self.tasks_remaining < len(self.players):
                self.state = "GAME_OVER"
            else:
                self.state = "INTERMEDIATE_RESULTS"
    
    # Остальные методы класса Game...

# Класс Button
class Button:
    def __init__(self, x, y, width, height, text, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (50, 50, 80), self.rect, 2, border_radius=10)
        text_surf = normal_font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

# Главная функция игры
def main():
    game = Game()
    
    # Создание кнопок и элементов UI...
    
    clock = pygame.time.Clock()
    running = True
    
    try:
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                # Обработка событий игры...
            
            # Отрисовка игры...
            
            pygame.display.flip()
            clock.tick(60)
            
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        if WEB_MODE:
            # Показать сообщение об ошибке в веб-версии
            error_surface = title_font.render("Произошла ошибка", True, (255, 0, 0))
            screen.fill((0, 0, 0))
            screen.blit(error_surface, (SCREEN_WIDTH//2 - error_surface.get_width()//2, SCREEN_HEIGHT//2 - 50))
            pygame.display.flip()
            pygame.time.delay(5000)
        else:
            raise e
            
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
