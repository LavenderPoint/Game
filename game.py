import pygame
import sys
import random

# Проверка на веб-среду
WEB_MODE = 'pygame_web' in sys.modules

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Настройки экрана
SCREEN_WIDTH = 360
SCREEN_HEIGHT = 640
BACKGROUND_COLOR = (255, 255, 200)
TEXT_COLOR = (80, 50, 50)
BUTTON_COLOR = (255, 182, 193)
BUTTON_HOVER_COLOR = (255, 105, 180)

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Подарочек")

# Шрифты (веб-совместимые)
try:
    title_font = pygame.font.Font(None, 48)
    normal_font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 24)
except:
    title_font = pygame.font.SysFont("Arial", 48)
    normal_font = pygame.font.SysFont("Arial", 32)
    small_font = pygame.font.SysFont("Arial", 24)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=10)
        
        text_surf = normal_font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

def draw_main_menu():
    screen.fill(BACKGROUND_COLOR)
    
    # Заголовок
    title = title_font.render("Подарочек", True, (220, 20, 60))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
    
    # Подзаголовок
    subtitle = normal_font.render("Игра для компании", True, TEXT_COLOR)
    screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 180))
    
    # Кнопка
    button = Button(SCREEN_WIDTH // 2 - 100, 300, 200, 60, "Начать игру")
    button.draw(screen)
    
    # Инструкция
    instruction = small_font.render("Нажмите кнопку, чтобы начать", True, TEXT_COLOR)
    screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 400))
    
    return button

def main():
    clock = pygame.time.Clock()
    running = True
    
    # Создаем кнопку
    start_button = draw_main_menu()
    
    try:
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Проверка клика по кнопке
                if start_button.is_clicked(mouse_pos, event):
                    print("Игра начата!")
            
            # Обновление состояния кнопки
            start_button.check_hover(mouse_pos)
            
            # Отрисовка
            draw_main_menu()
            
            pygame.display.flip()
            clock.tick(60)
            
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        if WEB_MODE:
            # В веб-режиме выводим сообщение на экран
            screen.fill((0, 0, 0))
            error_font = pygame.font.Font(None, 36)
            error_text = error_font.render("Произошла ошибка", True, (255, 0, 0))
            screen.blit(error_text, (SCREEN_WIDTH//2 - error_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
            pygame.display.flip()
            pygame.time.delay(5000)
        else:
            raise e
            
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
