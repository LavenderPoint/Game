import pygame
import sys
import random
import math
import os
from pygame.locals import *

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Определение размеров экрана
if pygame.display.get_driver() == 'android':
    # Режим для телефона
    info = pygame.display.Info()
    SCREEN_WIDTH = info.current_w
    SCREEN_HEIGHT = info.current_h
    IS_MOBILE = True
else:
    # Режим для компьютера
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    IS_MOBILE = False

# Константы
BACKGROUND_COLOR = (255, 255, 200)
TEXT_COLOR = (80, 50, 50)
BUTTON_COLOR = (255, 182, 193)
BUTTON_HOVER_COLOR = (255, 105, 180)
PANEL_COLOR = (255, 250, 240)
CATEGORY_COLORS = [
    (255, 182, 193), (173, 216, 230), 
    (144, 238, 144), (255, 99, 71)
]

# Создание экрана
if IS_MOBILE:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Подарочек")

# Адаптивные размеры шрифтов
title_size = int(SCREEN_WIDTH * 0.04) if IS_MOBILE else 48
header_size = int(SCREEN_WIDTH * 0.03) if IS_MOBILE else 32
normal_size = int(SCREEN_WIDTH * 0.025) if IS_MOBILE else 24
small_size = int(SCREEN_WIDTH * 0.02) if IS_MOBILE else 20

# Шрифты
title_font = pygame.font.SysFont("Arial", title_size, bold=True)
header_font = pygame.font.SysFont("Arial", header_size, bold=True)
normal_font = pygame.font.SysFont("Arial", normal_size)
small_font = pygame.font.SysFont("Arial", small_size)

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        self.avatar = self.generate_avatar()
        
    def add_score(self, points):
        self.score += points
        
    def generate_avatar(self):
        avatar_size = int(SCREEN_WIDTH * 0.07) if IS_MOBILE else 80
        avatar = pygame.Surface((avatar_size, avatar_size), pygame.SRCALPHA)
        pygame.draw.circle(avatar, self.color, (avatar_size//2, avatar_size//2), avatar_size//2)
        initials = "".join([n[0] for n in self.name.split()]).upper()[:2]
        text = header_font.render(initials, True, (255, 255, 255))
        avatar.blit(text, (avatar_size//2 - text.get_width()//2, avatar_size//2 - text.get_height()//2))
        return avatar

class Game:
    def __init__(self):
        self.players = []
        self.current_player_idx = 0
        self.state = "SETUP"
        self.tasks_per_category = 20
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
        self.task_data = self.load_tasks()
        
    def load_tasks(self):
        """Загрузка заданий из файлов"""
        tasks = {
            "riddles": [],
            "creativity": [],
            "words": [],
            "physical": []
        }
        
        try:
            # Загадки
            with open(os.path.join("data", "riddles.txt"), "r", encoding="utf-8") as f:
                tasks["riddles"] = [line.strip() for line in f.readlines() if line.strip()]
            
            # Творческие задания
            with open(os.path.join("data", "creativity.txt"), "r", encoding="utf-8") as f:
                tasks["creativity"] = [line.strip() for line in f.readlines() if line.strip()]
            
            # Словесные задания
            with open(os.path.join("data", "words.txt"), "r", encoding="utf-8") as f:
                tasks["words"] = [line.strip() for line in f.readlines() if line.strip()]
            
            # Физические задания
            with open(os.path.join("data", "physical.txt"), "r", encoding="utf-8") as f:
                tasks["physical"] = [line.strip() for line in f.readlines() if line.strip()]
        except Exception as e:
            print(f"Ошибка загрузки заданий: {e}")
            # Резервные задания
            tasks = {
                "riddles": ["Загадка 1", "Загадка 2"],
                "creativity": ["Творческое задание 1", "Творческое задание 2"],
                "words": ["Словесное задание 1", "Словесное задание 2"],
                "physical": ["Физическое задание 1", "Физическое задание 2"]
            }
        
        return tasks
    
    def setup_tasks(self):
        self.categories = ["Загадки", "Творчество", "Слова", "Физподготовка"]
        
        # Создание структуры для хранения состояния заданий
        self.tasks = []
        for cat_idx in range(4):
            category_tasks = []
            available_tasks = []
            
            # Выбор правильного набора заданий
            if cat_idx == 0:
                available_tasks = self.task_data["riddles"]
            elif cat_idx == 1:
                available_tasks = self.task_data["creativity"]
            elif cat_idx == 2:
                available_tasks = self.task_data["words"]
            else:
                available_tasks = self.task_data["physical"]
            
            # Перемешиваем задания для случайного порядка
            random.shuffle(available_tasks)
            
            # Берем не более 50 заданий
            tasks_to_use = available_tasks[:min(len(available_tasks), 50)]
            
            for j in range(min(self.tasks_per_category, len(tasks_to_use))):
                task = {
                    "description": tasks_to_use[j],
                    "completed": False,
                    "difficulty": j + 1,
                    "answer": self.get_answer(cat_idx, j) if cat_idx == 0 else ""
                }
                category_tasks.append(task)
            self.tasks.append(category_tasks)
        
        self.total_tasks = 4 * min(self.tasks_per_category, 50)
        self.tasks_remaining = self.total_tasks
    
    def get_answer(self, category, difficulty):
        if category == 0:
            return self.generate_answer(category, difficulty)
        return ""
    
    def generate_answer(self, category, difficulty):
        # В реальном приложении здесь должна быть логика получения ответов
        return f"Ответ на загадку {difficulty + 1}"
    
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
    
    def select_task(self, category, difficulty):
        if not self.task_window_open and 0 <= category < 4 and 0 <= difficulty < len(self.tasks[category]):
            task = self.tasks[category][difficulty]
            if not task["completed"]:
                self.selected_category = category
                self.selected_difficulty = difficulty
                self.task_window_open = True
                self.show_answer = False
                return True
        return False
    
    def complete_task(self, success):
        if self.selected_category is not None and self.selected_difficulty is not None:
            task = self.tasks[self.selected_category][self.selected_difficulty]
            if not task["completed"]:
                task["completed"] = True
                self.completed_tasks += 1
                self.tasks_remaining -= 1
                
                if success:
                    points = task["difficulty"]
                    self.players[self.current_player_idx].add_score(points)
                    
                self.task_window_open = False
                self.next_player()
                return True
        return False

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

class InputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.active = False
        
    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        
        if event.type == KEYDOWN and self.active:
            if event.key == K_RETURN:
                return True
            elif event.key == K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        return False
        
    def draw(self, surface):
        color = (100, 160, 210) if self.active else (200, 200, 200)
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        pygame.draw.rect(surface, color, self.rect, 2)
        
        text_surf = normal_font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))
        
        if self.active:
            cursor_pos = text_surf.get_rect().width + 5
            pygame.draw.line(surface, (0, 0, 0), 
                            (self.rect.x + cursor_pos, self.rect.y + 5),
                            (self.rect.x + cursor_pos, self.rect.y + self.rect.height - 5), 2)

def draw_setup_screen(game):
    screen.fill(BACKGROUND_COLOR)
    
    # Заголовок
    title = title_font.render("Подарочек", True, (220, 20, 60))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT * 0.05))
    
    # Декоративные элементы
    circle_size = SCREEN_WIDTH * 0.07
    pygame.draw.circle(screen, (255, 182, 193), (SCREEN_WIDTH * 0.17, SCREEN_HEIGHT * 0.19), circle_size)
    pygame.draw.circle(screen, (173, 216, 230), (SCREEN_WIDTH * 0.83, SCREEN_HEIGHT * 0.19), circle_size)
    pygame.draw.circle(screen, (144, 238, 144), (SCREEN_WIDTH * 0.17, SCREEN_HEIGHT * 0.81), circle_size)
    pygame.draw.circle(screen, (255, 99, 71), (SCREEN_WIDTH * 0.83, SCREEN_HEIGHT * 0.81), circle_size)
    
    # Панель настройки
    panel_rect = pygame.Rect(SCREEN_WIDTH * 0.08, SCREEN_HEIGHT * 0.19, SCREEN_WIDTH * 0.84, SCREEN_HEIGHT * 0.62)
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect, border_radius=20)
    pygame.draw.rect(screen, TEXT_COLOR, panel_rect, 2, border_radius=20)
    
    # Заголовок панели
    setup_title = header_font.render("Настройка игры", True, TEXT_COLOR)
    screen.blit(setup_title, (SCREEN_WIDTH // 2 - setup_title.get_width() // 2, SCREEN_HEIGHT * 0.22))
    
    # Ввод количества заданий
    tasks_label = normal_font.render("Количество заданий в категории (5-50):", True, TEXT_COLOR)
    screen.blit(tasks_label, (SCREEN_WIDTH * 0.17, SCREEN_HEIGHT * 0.31))
    
    # Ввод имени игрока
    player_label = normal_font.render("Имя игрока:", True, TEXT_COLOR)
    screen.blit(player_label, (SCREEN_WIDTH * 0.17, SCREEN_HEIGHT * 0.40))
    
    # Информация об игроках
    players_label = normal_font.render("Добавленные игроки:", True, TEXT_COLOR)
    screen.blit(players_label, (SCREEN_WIDTH * 0.17, SCREEN_HEIGHT * 0.52))
    
    # Список игроков
    for i, player in enumerate(game.players):
        player_text = small_font.render(f"{i+1}. {player.name}", True, TEXT_COLOR)
        screen.blit(player_text, (SCREEN_WIDTH * 0.18, SCREEN_HEIGHT * 0.57 + i * SCREEN_HEIGHT * 0.04))
    
    # Отрисовка полей ввода
    tasks_input.draw(screen)
    player_input.draw(screen)
    
    # Кнопки
    start_btn.draw(screen)
    add_player_btn.draw(screen)

def draw_game_screen(game):
    screen.fill(BACKGROUND_COLOR)
    
    # Декоративные элементы
    for i in range(20):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        pygame.draw.circle(screen, CATEGORY_COLORS[i % 4], (x, y), 5)
    
    # Заголовок
    title = title_font.render("Подарочек", True, (220, 20, 60))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT * 0.02))
    
    # Информация о раунде
    round_text = header_font.render(f"Раунд: {game.round_counter}", True, TEXT_COLOR)
    screen.blit(round_text, (SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.02))
    
    # Прогресс выполнения
    progress = game.completed_tasks / game.total_tasks if game.total_tasks > 0 else 0
    pygame.draw.rect(screen, (200, 200, 200), (SCREEN_WIDTH * 0.04, SCREEN_HEIGHT * 0.10, SCREEN_WIDTH * 0.92, SCREEN_HEIGHT * 0.025))
    pygame.draw.rect(screen, (0, 150, 0), (SCREEN_WIDTH * 0.04, SCREEN_HEIGHT * 0.10, SCREEN_WIDTH * 0.92 * progress, SCREEN_HEIGHT * 0.025))
    progress_text = small_font.render(f"Выполнено: {game.completed_tasks}/{game.total_tasks} ({int(progress*100)}%)", True, TEXT_COLOR)
    screen.blit(progress_text, (SCREEN_WIDTH // 2 - progress_text.get_width() // 2, SCREEN_HEIGHT * 0.102))
    
    # Информация о текущем игроке
    if game.players:
        current_player = game.players[game.current_player_idx]
        player_text = header_font.render(f"Текущий игрок: {current_player.name}", True, current_player.color)
        screen.blit(player_text, (SCREEN_WIDTH * 0.04, SCREEN_HEIGHT * 0.14))
    
    # Панель категорий
    category_width = (SCREEN_WIDTH - SCREEN_WIDTH * 0.08) // 4 - 10
    for i, category in enumerate(game.categories):
        x = SCREEN_WIDTH * 0.04 + i * (category_width + 10)
        y = SCREEN_HEIGHT * 0.19
        height = SCREEN_HEIGHT * 0.75
        
        pygame.draw.rect(screen, CATEGORY_COLORS[i], (x, y, category_width, height), border_radius=15)
        pygame.draw.rect(screen, TEXT_COLOR, (x, y, category_width, height), 2, border_radius=15)
        
        # Название категории
        cat_text = header_font.render(category, True, TEXT_COLOR)
        screen.blit(cat_text, (x + category_width // 2 - cat_text.get_width() // 2, y + SCREEN_HEIGHT * 0.02))
        
        # Задания (кружочки)
        tasks_per_row = 5
        task_size = SCREEN_WIDTH * 0.025 if IS_MOBILE else 30
        spacing = SCREEN_WIDTH * 0.01
        start_y = y + SCREEN_HEIGHT * 0.10
        
        # Рассчитаем общую ширину всех кружков в ряду
        total_width = tasks_per_row * task_size + (tasks_per_row - 1) * spacing
        start_x = x + (category_width - total_width) // 2
        
        # Определяем количество строк
        rows = min(10, (game.tasks_per_category + tasks_per_row - 1) // tasks_per_row)
        
        for j in range(min(game.tasks_per_category, 50)):
            row = j // tasks_per_row
            col = j % tasks_per_row
            
            # Пропускаем если больше 10 строк (для мобильных)
            if row >= rows:
                continue
                
            task_x = start_x + col * (task_size + spacing)
            task_y = start_y + row * (task_size + spacing)
            
            task = game.tasks[i][j]
            color = (100, 200, 100) if task["completed"] else CATEGORY_COLORS[i]
            pygame.draw.circle(screen, color, (task_x, task_y), task_size // 2)
            pygame.draw.circle(screen, TEXT_COLOR, (task_x, task_y), task_size // 2, 2)
            
            # Номер задания
            num_text = small_font.render(str(j+1), True, TEXT_COLOR)
            screen.blit(num_text, (task_x - num_text.get_width() // 2, task_y - num_text.get_height() // 2))

def draw_task_window(game):
    if not game.task_window_open:
        return
    
    # Затемнение фона
    s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    s.fill((0, 0, 0, 150))
    screen.blit(s, (0, 0))
    
    # Окно задания
    window_width = SCREEN_WIDTH * 0.8 if IS_MOBILE else 800
    window_height = SCREEN_HEIGHT * 0.6 if IS_MOBILE else 500
    window_x = (SCREEN_WIDTH - window_width) // 2
    window_y = (SCREEN_HEIGHT - window_height) // 2
    
    pygame.draw.rect(screen, PANEL_COLOR, (window_x, window_y, window_width, window_height), border_radius=20)
    pygame.draw.rect(screen, TEXT_COLOR, (window_x, window_y, window_width, window_height), 3, border_radius=20)
    
    # Заголовок
    cat_idx = game.selected_category
    task = game.tasks[cat_idx][game.selected_difficulty]
    title = header_font.render(f"Задание: Уровень {task['difficulty']}", True, TEXT_COLOR)
    screen.blit(title, (window_x + window_width // 2 - title.get_width() // 2, window_y + SCREEN_HEIGHT * 0.03))
    
    # Категория
    cat_text = normal_font.render(f"Категория: {game.categories[cat_idx]}", True, CATEGORY_COLORS[cat_idx])
    screen.blit(cat_text, (window_x + SCREEN_WIDTH * 0.04, window_y + SCREEN_HEIGHT * 0.08))
    
    # Описание задания
    desc_text = normal_font.render("Задание:", True, TEXT_COLOR)
    screen.blit(desc_text, (window_x + SCREEN_WIDTH * 0.04, window_y + SCREEN_HEIGHT * 0.13))
    
    # Разбиение описания на строки
    description = task["description"]
    words = description.split()
    lines = []
    current_line = ""
    max_width = window_width - SCREEN_WIDTH * 0.08
    
    for word in words:
        test_line = current_line + word + " "
        if normal_font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    
    # Ограничение количества строк для мобильных
    max_lines = 5 if IS_MOBILE else 10
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][:min(len(lines[-1]), 30)] + "..."  # Обрезаем последнюю строку
    
    for i, line in enumerate(lines):
        line_surf = normal_font.render(line, True, TEXT_COLOR)
        screen.blit(line_surf, (window_x + SCREEN_WIDTH * 0.06, window_y + SCREEN_HEIGHT * 0.16 + i * SCREEN_HEIGHT * 0.05))
    
    # Показываем ответ только если нажали кнопку "Показать ответ"
    y_pos = window_y + SCREEN_HEIGHT * 0.16 + len(lines) * SCREEN_HEIGHT * 0.05
    button_width = SCREEN_WIDTH * 0.15 if IS_MOBILE else 180
    button_height = SCREEN_HEIGHT * 0.06 if IS_MOBILE else 50
    button_spacing = SCREEN_WIDTH * 0.02
    
    if cat_idx == 0:  # Загадки
        if game.show_answer:
            # Показываем ответ
            ans_text = normal_font.render(f"Правильный ответ: {task['answer']}", True, (0, 100, 0))
            screen.blit(ans_text, (window_x + SCREEN_WIDTH * 0.06, y_pos))
            y_pos += SCREEN_HEIGHT * 0.07
            
            # Кнопки принятия/отклонения
            accept_btn.rect = pygame.Rect(
                window_x + window_width // 2 - button_width - button_spacing // 2,
                y_pos,
                button_width,
                button_height
            )
            accept_btn.draw(screen)
            
            reject_btn.rect = pygame.Rect(
                window_x + window_width // 2 + button_spacing // 2,
                y_pos,
                button_width,
                button_height
            )
            reject_btn.draw(screen)
        else:
            # Кнопка "Показать ответ"
            show_answer_btn.rect = pygame.Rect(
                window_x + window_width // 2 - button_width // 2,
                y_pos,
                button_width,
                button_height
            )
            show_answer_btn.draw(screen)
    else:
        # Для остальных категорий сразу показываем кнопки "Принять" и "Отклонить"
        accept_btn.rect = pygame.Rect(
            window_x + window_width // 2 - button_width - button_spacing // 2,
            y_pos,
            button_width,
            button_height
        )
        accept_btn.draw(screen)
        
        reject_btn.rect = pygame.Rect(
            window_x + window_width // 2 + button_spacing // 2,
            y_pos,
            button_width,
            button_height
        )
        reject_btn.draw(screen)

def draw_intermediate_results(game):
    screen.fill(BACKGROUND_COLOR)
    
    # Заголовок
    title = title_font.render(f"Промежуточные результаты: Раунд {game.round_counter}", True, (220, 20, 60))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT * 0.06))
    
    # Информация о прогрессе
    progress = game.completed_tasks / game.total_tasks if game.total_tasks > 0 else 0
    progress_text = header_font.render(f"Выполнено заданий: {game.completed_tasks}/{game.total_tasks} ({int(progress*100)}%)", True, TEXT_COLOR)
    screen.blit(progress_text, (SCREEN_WIDTH // 2 - progress_text.get_width() // 2, SCREEN_HEIGHT * 0.15))
    
    # Таблица результатов
    pygame.draw.rect(screen, PANEL_COLOR, (SCREEN_WIDTH * 0.08, SCREEN_HEIGHT * 0.22, SCREEN_WIDTH * 0.84, SCREEN_HEIGHT * 0.65), border_radius=20)
    pygame.draw.rect(screen, TEXT_COLOR, (SCREEN_WIDTH * 0.08, SCREEN_HEIGHT * 0.22, SCREEN_WIDTH * 0.84, SCREEN_HEIGHT * 0.65), 2, border_radius=20)
    
    # Заголовок таблицы
    results_title = header_font.render("Результаты игроков", True, TEXT_COLOR)
    screen.blit(results_title, (SCREEN_WIDTH // 2 - results_title.get_width() // 2, SCREEN_HEIGHT * 0.25))
    
    # Список всех игроков
    sorted_players = sorted(game.players, key=lambda p: p.score, reverse=True)
    avatar_size = int(SCREEN_WIDTH * 0.07) if IS_MOBILE else 80
    
    for i, player in enumerate(sorted_players):
        y_pos = SCREEN_HEIGHT * 0.32 + i * SCREEN_HEIGHT * 0.10
        
        # Аватар
        scaled_avatar = pygame.transform.scale(player.avatar, (avatar_size, avatar_size))
        screen.blit(scaled_avatar, (SCREEN_WIDTH * 0.12, y_pos - avatar_size//2))
        
        # Имя и очки
        name_text = normal_font.render(f"{i+1}. {player.name}", True, player.color)
        screen.blit(name_text, (SCREEN_WIDTH * 0.21, y_pos - name_text.get_height()//2))
        
        score_text = header_font.render(f"{player.score} очков", True, TEXT_COLOR)
        screen.blit(score_text, (SCREEN_WIDTH * 0.75 - score_text.get_width()//2, y_pos - score_text.get_height()//2))
    
    # Кнопка продолжения
    continue_btn.rect = pygame.Rect(
        SCREEN_WIDTH // 2 - SCREEN_WIDTH * 0.15,
        SCREEN_HEIGHT * 0.85,
        SCREEN_WIDTH * 0.30,
        SCREEN_HEIGHT * 0.07
    )
    continue_btn.draw(screen)

def draw_game_over_screen(game):
    screen.fill(BACKGROUND_COLOR)
    
    # Заголовок
    title = title_font.render("Игра завершена! Финальные результаты", True, (220, 20, 60))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT * 0.06))
    
    # Информация о количестве раундов
    rounds_text = header_font.render(f"Всего раундов: {game.round_counter}", True, TEXT_COLOR)
    screen.blit(rounds_text, (SCREEN_WIDTH // 2 - rounds_text.get_width() // 2, SCREEN_HEIGHT * 0.15))
    
    # Пьедестал для топ-3
    podium_height = SCREEN_HEIGHT * 0.25
    podium_width = SCREEN_WIDTH * 0.84
    podium_x = SCREEN_WIDTH * 0.08
    podium_y = SCREEN_HEIGHT * 0.25
    
    # Основание пьедестала
    pygame.draw.rect(screen, (180, 180, 180), (podium_x, podium_y + podium_height - SCREEN_HEIGHT * 0.025, podium_width, SCREEN_HEIGHT * 0.025))
    
    # Ступени пьедестала
    step_width = podium_width // 3
    step_height = podium_height // 3
    
    # Цвета для пьедестала
    podium_color_1 = (255, 215, 0)  # Золотой
    podium_color_2 = (192, 192, 192)  # Серебряный
    podium_color_3 = (205, 127, 50)   # Бронзовый
    
    # 1 место (золото)
    pygame.draw.rect(screen, podium_color_1, 
                    (podium_x + step_width, podium_y, 
                     step_width, podium_height - step_height))
    
    # 2 место (серебро)
    pygame.draw.rect(screen, podium_color_2, 
                    (podium_x, podium_y + step_height, 
                     step_width, podium_height - step_height))
    
    # 3 место (бронза)
    pygame.draw.rect(screen, podium_color_3, 
                    (podium_x + 2 * step_width, podium_y + step_height, 
                     step_width, podium_height - step_height))
    
    # Список всех игроков
    sorted_players = sorted(game.players, key=lambda p: p.score, reverse=True)
    avatar_size = int(SCREEN_WIDTH * 0.10) if IS_MOBILE else 120
    
    # Отображение топ-3 на пьедестале
    for i, player in enumerate(sorted_players[:3]):
        if i == 0:  # 1 место
            x_pos = podium_x + step_width + step_width // 2
            y_pos = podium_y + podium_height * 0.15
            place_color = podium_color_1
        elif i == 1:  # 2 место
            x_pos = podium_x + step_width // 2
            y_pos = podium_y + podium_height * 0.35
            place_color = podium_color_2
        else:  # 3 место
            x_pos = podium_x + 2 * step_width + step_width // 2
            y_pos = podium_y + podium_height * 0.35
            place_color = podium_color_3
        
        # Увеличиваем аватар для топ-3
        scaled_avatar = pygame.transform.scale(player.avatar, (avatar_size, avatar_size))
        avatar_rect = scaled_avatar.get_rect(center=(x_pos, y_pos - SCREEN_HEIGHT * 0.05))
        screen.blit(scaled_avatar, avatar_rect)
        
        # Место
        place_text = header_font.render(f"{i+1} МЕСТО", True, place_color)
        screen.blit(place_text, (x_pos - place_text.get_width() // 2, y_pos + SCREEN_HEIGHT * 0.03))
        
        # Имя
        name_text = normal_font.render(player.name, True, player.color)
        screen.blit(name_text, (x_pos - name_text.get_width() // 2, y_pos + SCREEN_HEIGHT * 0.06))
        
        # Очки
        score_text = normal_font.render(f"{player.score} очков", True, TEXT_COLOR)
        screen.blit(score_text, (x_pos - score_text.get_width() // 2, y_pos + SCREEN_HEIGHT * 0.09))
    
    # Таблица для остальных игроков
    if len(sorted_players) > 3:
        other_rect = pygame.Rect(
            SCREEN_WIDTH * 0.08,
            podium_y + podium_height + SCREEN_HEIGHT * 0.05,
            SCREEN_WIDTH * 0.84,
            SCREEN_HEIGHT * 0.25
        )
        pygame.draw.rect(screen, PANEL_COLOR, other_rect, border_radius=20)
        pygame.draw.rect(screen, TEXT_COLOR, other_rect, 2, border_radius=20)
        
        other_title = header_font.render("Остальные участники", True, TEXT_COLOR)
        screen.blit(other_title, (SCREEN_WIDTH // 2 - other_title.get_width() // 2, other_rect.y + SCREEN_HEIGHT * 0.02))
        
        # Отображение остальных игроков
        small_avatar_size = int(SCREEN_WIDTH * 0.05) if IS_MOBILE else 40
        
        for i, player in enumerate(sorted_players[3:]):
            idx = i + 4
            y_pos = other_rect.y + SCREEN_HEIGHT * 0.08 + i * SCREEN_HEIGHT * 0.05
            
            # Аватар
            scaled_avatar = pygame.transform.scale(player.avatar, (small_avatar_size, small_avatar_size))
            screen.blit(scaled_avatar, (SCREEN_WIDTH * 0.12, y_pos - small_avatar_size//2))
            
            # Имя и очки
            player_text = normal_font.render(f"{idx}. {player.name}: {player.score} очков", True, player.color)
            screen.blit(player_text, (SCREEN_WIDTH * 0.17, y_pos - player_text.get_height()//2))
    
    # Кнопка новой игры
    new_game_btn.rect = pygame.Rect(
        SCREEN_WIDTH // 2 - SCREEN_WIDTH * 0.15,
        SCREEN_HEIGHT * 0.85,
        SCREEN_WIDTH * 0.30,
        SCREEN_HEIGHT * 0.07
    )
    new_game_btn.draw(screen)

# Создание объектов игры и UI
game = Game()

# Кнопки для экрана настройки
start_btn = Button(
    SCREEN_WIDTH // 2 - SCREEN_WIDTH * 0.10,
    SCREEN_HEIGHT * 0.75,
    SCREEN_WIDTH * 0.20,
    SCREEN_HEIGHT * 0.07,
    "Начать игру"
)

add_player_btn = Button(
    SCREEN_WIDTH // 2 - SCREEN_WIDTH * 0.10,
    SCREEN_HEIGHT * 0.65,
    SCREEN_WIDTH * 0.20,
    SCREEN_HEIGHT * 0.07,
    "Добавить игрока"
)

# Поля ввода
tasks_input = InputBox(
    SCREEN_WIDTH * 0.50,
    SCREEN_HEIGHT * 0.31,
    SCREEN_WIDTH * 0.17,
    SCREEN_HEIGHT * 0.05
)

player_input = InputBox(
    SCREEN_WIDTH * 0.50,
    SCREEN_HEIGHT * 0.40,
    SCREEN_WIDTH * 0.17,
    SCREEN_HEIGHT * 0.05
)

# Кнопки для окна задания
show_answer_btn = Button(0, 0, 0, 0, "Показать ответ")
accept_btn = Button(0, 0, 0, 0, "Принять", (144, 238, 144))
reject_btn = Button(0, 0, 0, 0, "Отклонить", (255, 99, 71))

# Кнопки для других экранов
continue_btn = Button(0, 0, 0, 0, "Продолжить игру")
new_game_btn = Button(0, 0, 0, 0, "Новая игра")

# Главный цикл игры
clock = pygame.time.Clock()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        # Обработка касаний на мобильных
        if IS_MOBILE and event.type == FINGERDOWN:
            # Преобразование координат касания
            touch_x = event.x * SCREEN_WIDTH
            touch_y = event.y * SCREEN_HEIGHT
            mouse_pos = (touch_x, touch_y)
            # Эмулируем событие клика мыши
            mouse_event = pygame.event.Event(MOUSEBUTTONDOWN, {
                'pos': mouse_pos,
                'button': 1
            })
            pygame.event.post(mouse_event)
        
        if game.state == "SETUP":
            # Обработка ввода
            tasks_input.handle_event(event)
            player_input.handle_event(event)
            
            # Обработка кнопок
            if add_player_btn.is_clicked(mouse_pos, event):
                if game.add_player(player_input.text):
                    player_input.text = ""
            
            if start_btn.is_clicked(mouse_pos, event):
                game.tasks_count_input = tasks_input.text
                if game.start_game():
                    pass
        
        elif game.state == "PLAYING":
            if not game.task_window_open:
                # Обработка выбора задания
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # Проверяем, было ли нажатие на задание
                    category_width = (SCREEN_WIDTH - SCREEN_WIDTH * 0.08) // 4 - 10
                    tasks_per_row = 5
                    
                    for i in range(4):
                        cat_x = SCREEN_WIDTH * 0.04 + i * (category_width + 10)
                        
                        # Рассчитаем общую ширину всех кружков в ряду
                        task_size = SCREEN_WIDTH * 0.025 if IS_MOBILE else 30
                        spacing = SCREEN_WIDTH * 0.01
                        total_width = tasks_per_row * task_size + (tasks_per_row - 1) * spacing
                        start_x = cat_x + (category_width - total_width) // 2
                        
                        # Определяем количество строк
                        rows = min(10, (game.tasks_per_category + tasks_per_row - 1) // tasks_per_row)
                        
                        for j in range(min(game.tasks_per_category, 50)):
                            row = j // tasks_per_row
                            col = j % tasks_per_row
                            
                            # Пропускаем если больше 10 строк (для мобильных)
                            if row >= rows:
                                continue
                                
                            task_x = start_x + col * (task_size + spacing)
                            task_y = SCREEN_HEIGHT * 0.19 + SCREEN_HEIGHT * 0.10 + row * (task_size + spacing)
                            
                            # Проверка расстояния до центра кружка
                            dx = mouse_pos[0] - task_x
                            dy = mouse_pos[1] - task_y
                            distance = math.sqrt(dx*dx + dy*dy)
                            
                            if distance <= task_size // 2:
                                game.select_task(i, j)
                                break
            
            else:  # Если открыто окно задания
                # Обработка кнопок
                if show_answer_btn.is_clicked(mouse_pos, event):
                    game.show_answer = True
                
                if accept_btn.is_clicked(mouse_pos, event):
                    game.complete_task(True)
                
                if reject_btn.is_clicked(mouse_pos, event):
                    game.complete_task(False)
        
        elif game.state == "INTERMEDIATE_RESULTS":
            if continue_btn.is_clicked(mouse_pos, event):
                game.state = "PLAYING"
        
        elif game.state == "GAME_OVER":
            if new_game_btn.is_clicked(mouse_pos, event):
                # Перезапуск игры
                game = Game()
                tasks_input.text = str(game.tasks_per_category)
    
    # Обновление состояния кнопок
    start_btn.check_hover(mouse_pos)
    add_player_btn.check_hover(mouse_pos)
    show_answer_btn.check_hover(mouse_pos)
    accept_btn.check_hover(mouse_pos)
    reject_btn.check_hover(mouse_pos)
    continue_btn.check_hover(mouse_pos)
    new_game_btn.check_hover(mouse_pos)
    
    # Отрисовка
    if game.state == "SETUP":
        draw_setup_screen(game)
    elif game.state == "PLAYING":
        draw_game_screen(game)
        draw_task_window(game)
    elif game.state == "INTERMEDIATE_RESULTS":
        draw_intermediate_results(game)
    elif game.state == "GAME_OVER":
        draw_game_over_screen(game)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
