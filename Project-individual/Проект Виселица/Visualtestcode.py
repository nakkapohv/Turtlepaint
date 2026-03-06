import pygame
from pygame.locals import *

import random

pygame.init()
pygame.font.init()

# Константы экрана
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hangman")

# Цвета
BACKGROUND_COLOR = (167, 199, 231)        # нежно-голубой для игры
MENU_BG_COLOR = (80, 45, 20)               # тёмный шоколадный
BUTTON_COLOR = (0, 150, 0)                 # зелёный
BUTTON_HOVER_COLOR = (0, 200, 0)           # ярче при наведении
BUTTON_TEXT_COLOR = (255, 255, 255)        # белый
GALLOW_COLOR = (0, 0, 0)                   # чёрный для виселицы
GALLOW_WOOD_COLOR = (101, 67, 33)          # коричневый для текстуры дерева

russian_letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' \
                  'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.border_radius = 25

    def draw(self, surface, alpha=255):
        color = self.hover_color if self.is_hovered else self.color
        # Создаём временную поверхность для кнопки, чтобы применить альфа-канал
        button_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surf, (*color, alpha), button_surf.get_rect(), border_radius=self.border_radius)
        # Текст
        text_surf = self.font.render(self.text, True, self.text_color)
        text_surf.set_alpha(alpha)
        text_rect = text_surf.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        button_surf.blit(text_surf, text_rect)
        surface.blit(button_surf, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial Black", 70)          # для кнопок
        self.small_font = pygame.font.SysFont("Arial", 20)         # для подписи
        self.clock = pygame.time.Clock()
        self.running = True

        # Кнопки
        button_width = 450
        button_height = 140
        center_x = SCREEN_WIDTH // 2
        first_button_center_y = SCREEN_HEIGHT // 2 - 80
        second_button_center_y = SCREEN_HEIGHT // 2 + 80

        self.play_button = Button(
            center_x - button_width // 2, first_button_center_y - button_height // 2,
            button_width, button_height,
            "Играть", self.font, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR
        )
        self.exit_button = Button(
            center_x - button_width // 2, second_button_center_y - button_height // 2,
            button_width, button_height,
            "Выход", self.font, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR
        )

    def fade_out(self):
        """Плавное затемнение экрана (переход)"""
        fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade_surface.fill((0, 0, 0))
        for alpha in range(0, 255, 5):
            fade_surface.set_alpha(alpha)
            self.screen.fill(MENU_BG_COLOR)
            self.play_button.draw(self.screen)
            self.exit_button.draw(self.screen)
            signature = self.small_font.render("Created by Nakka", True, (255, 215, 0))
            signature_rect = signature.get_rect(bottomright=(980, 680))
            self.screen.blit(signature, signature_rect)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "exit"
                if self.play_button.handle_event(event):
                    self.fade_out()
                    self.running = False
                    return "play"
                if self.exit_button.handle_event(event):
                    self.running = False
                    return "exit"

            self.screen.fill(MENU_BG_COLOR)
            self.play_button.draw(self.screen)
            self.exit_button.draw(self.screen)

            signature = self.small_font.render("Created by Nakka", True, (255, 215, 0))
            signature_rect = signature.get_rect(bottomright=(980, 680))
            self.screen.blit(signature, signature_rect)

            pygame.display.flip()
            self.clock.tick(60)

        return "exit"


class Hangman():
    def __init__(self):
        with open("words.txt", "r", encoding="UTF-8") as file:
            words = [w.strip() for w in file.read().split("\n") if w.strip()]
            self.secret_word = random.choice(words)

            if self.secret_word:
                self.secret_word = self.secret_word[0].upper() + self.secret_word[1:]

            self.guessed_word = ["_"] * len(self.secret_word)

        self.wrong_guesses = []
        self.wrong_guess_count = 0
        self.taking_guess = True
        self.running = True
        self.game_over = False    # флаг окончания игры
        self.win = False          # True если победа, False если поражение

        self.background_color = BACKGROUND_COLOR
        self.body_color = (244, 213, 187)
        self.tongue_color = (255, 0, 0)

        self.font = pygame.font.SysFont("Arial Black", 35)
        self.big_font = pygame.font.SysFont("Arial Black", 100)
        self.small_font = pygame.font.SysFont("Arial", 20)
        self.FPS = pygame.time.Clock()

    def _draw_fancy_gallow(self):
        """Отрисовка виселицы в игровом стиле (скруглённые углы + текстура дерева)"""
        # Основание
        pygame.draw.rect(screen, GALLOW_COLOR, pygame.Rect(100, 600, 260, 15), border_radius=7)
        # Вертикальная стойка
        pygame.draw.rect(screen, GALLOW_COLOR, pygame.Rect(225, 100, 13, 500), border_radius=6)
        # Горизонтальная перекладина
        pygame.draw.rect(screen, GALLOW_COLOR, pygame.Rect(230, 100, 220, 11), border_radius=5)
        # Верёвка
        pygame.draw.rect(screen, GALLOW_COLOR, pygame.Rect(338, 110, 10, 50), border_radius=3)

        # Текстура дерева
        wood_color = GALLOW_WOOD_COLOR
        for y in range(150, 550, 30):
            pygame.draw.line(screen, wood_color, (230, y), (233, y), 2)
        for x in range(240, 430, 30):
            pygame.draw.line(screen, wood_color, (x, 105), (x, 108), 2)

    def _man_pieces(self):
        if self.win and self.wrong_guess_count > 0 and self.game_over:
            # Улыбающееся лицо при победе (если были ошибки)
            pygame.draw.circle(screen, self.body_color, [343, 200], 40, 0)
            pygame.draw.circle(screen, GALLOW_COLOR, [330, 190], 7, 0)
            pygame.draw.circle(screen, GALLOW_COLOR, [356, 190], 7, 0)
            pygame.draw.arc(screen, GALLOW_COLOR, [328, 210, 30, 20], 3.14, 0, 3)  # улыбка
        else:
            if self.wrong_guess_count >= 1:
                pygame.draw.circle(screen, self.body_color, [343, 200], 40, 0)

                if self.wrong_guess_count == 6:
                    # Мёртвые глаза
                    pygame.draw.line(screen, GALLOW_COLOR, [325, 185], [335, 195], 3)
                    pygame.draw.line(screen, GALLOW_COLOR, [335, 185], [325, 195], 3)
                    pygame.draw.line(screen, GALLOW_COLOR, [351, 185], [361, 195], 3)
                    pygame.draw.line(screen, GALLOW_COLOR, [361, 185], [351, 195], 3)
                    # Рот с языком
                    pygame.draw.ellipse(screen, (200, 0, 0), [328, 215, 30, 20])
                    pygame.draw.ellipse(screen, self.tongue_color, [338, 225, 10, 15])
                    pygame.draw.ellipse(screen, GALLOW_COLOR, [328, 215, 30, 20], 2)
                else:
                    # Живые глаза
                    pygame.draw.circle(screen, GALLOW_COLOR, [330, 190], 7, 0)
                    pygame.draw.circle(screen, GALLOW_COLOR, [356, 190], 7, 0)
                    # Нейтральный рот
                    pygame.draw.line(screen, GALLOW_COLOR, [333, 220], [353, 220], 3)

            if self.wrong_guess_count >= 2:
                pygame.draw.rect(screen, self.body_color, pygame.Rect(335, 230, 17, 160))
            if self.wrong_guess_count >= 3:
                pygame.draw.line(screen, self.body_color, [290, 360], [338, 252], 15)
            if self.wrong_guess_count >= 4:
                pygame.draw.line(screen, self.body_color, [400, 360], [348, 252], 15)
            if self.wrong_guess_count >= 5:
                pygame.draw.line(screen, self.body_color, [405, 500], [344, 385], 16)
            if self.wrong_guess_count >= 6:
                pygame.draw.line(screen, self.body_color, [283, 503], [340, 385], 16)

    def _right_guess(self, guess_letter):
        indices = [i for i, ch in enumerate(self.secret_word) if ch.lower() == guess_letter.lower()]
        for i in indices:
            self.guessed_word[i] = self.secret_word[i]

    def _wrong_guess(self, guess_letter):
        self.wrong_guesses.append(guess_letter.lower())
        self.wrong_guess_count += 1

    def _guess_taker(self, guess_letter):
        if not guess_letter or len(guess_letter) != 1:
            return
        if guess_letter in russian_letters:
            gl = guess_letter.lower()
            secret_lower = [c.lower() for c in self.secret_word]
            guessed_lower = [c.lower() for c in self.guessed_word]
            wrong_lower = [c.lower() for c in self.wrong_guesses]

            if gl in secret_lower and gl not in guessed_lower:
                self._right_guess(guess_letter)
            elif gl not in secret_lower and gl not in wrong_lower:
                self._wrong_guess(guess_letter)

    def _message(self):
        if ''.join(self.guessed_word) == self.secret_word:
            self.taking_guess = False
            self.game_over = True
            self.win = True
        elif self.wrong_guess_count == 6:
            self.taking_guess = False
            self.game_over = True
            self.win = False

    def _show_end_screen(self):
        """Отображает финальный экран с плавно появляющимися горизонтальными кнопками."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))

        # Текст результата
        if self.win:
            result_text = self.big_font.render("ВЫ ПОБЕДИЛИ", True, (50, 205, 50))
        else:
            result_text = self.big_font.render("ВЫ ПРОИГРАЛИ", True, (180, 0, 0))
        word_text = self.font.render(f"Слово: {self.secret_word}", True, (255, 255, 255))

        # Кнопки (горизонтально) с шириной 300
        button_font = pygame.font.SysFont("Arial Black", 40)
        button_width = 300
        button_height = 70
        spacing = 30
        total_width = 2 * button_width + spacing
        start_x = (SCREEN_WIDTH - total_width) // 2

        continue_button = Button(
            start_x, 420, button_width, button_height,
            "Продолжить", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR
        )
        exit_button = Button(
            start_x + button_width + spacing, 420, button_width, button_height,
            "Выход", button_font, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR
        )

        clock = pygame.time.Clock()
        alpha = 0
        # Анимация появления кнопок
        while alpha < 255:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
            # Перерисовываем игровой фон
            screen.fill(self.background_color)
            self._draw_fancy_gallow()
            self._man_pieces()
            signature = self.small_font.render("Created by Nakka", True, (255, 215, 0))
            signature_rect = signature.get_rect(bottomright=(980, 680))
            screen.blit(signature, signature_rect)
            # Затемнение
            screen.blit(overlay, (0, 0))
            # Текст результата
            result_rect = result_text.get_rect(center=(500, 300))
            screen.blit(result_text, result_rect)
            word_rect = word_text.get_rect(center=(500, 380))
            screen.blit(word_text, word_rect)
            # Рисуем кнопки с текущей прозрачностью
            continue_button.draw(screen, alpha)
            exit_button.draw(screen, alpha)

            pygame.display.flip()
            alpha += 5
            clock.tick(60)

        # После анимации ждём нажатия
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if continue_button.handle_event(event):
                    return "menu"
                if exit_button.handle_event(event):
                    return "exit"

            # Перерисовываем всё так же
            screen.fill(self.background_color)
            self._draw_fancy_gallow()
            self._man_pieces()
            signature = self.small_font.render("Created by Nakka", True, (255, 215, 0))
            signature_rect = signature.get_rect(bottomright=(980, 680))
            screen.blit(signature, signature_rect)
            screen.blit(overlay, (0, 0))
            result_rect = result_text.get_rect(center=(500, 300))
            screen.blit(result_text, result_rect)
            word_rect = word_text.get_rect(center=(500, 380))
            screen.blit(word_text, word_rect)
            continue_button.draw(screen)
            exit_button.draw(screen)

            pygame.display.flip()
            clock.tick(60)

        return "menu"

    def run(self):
        screen.fill(self.background_color)
        self._draw_fancy_gallow()
        instructions = self.font.render('Введите любую букву', True, (255, 255, 255))
        instr_rect = instructions.get_rect(center=(720, 200))
        screen.blit(instructions, instr_rect)
        pygame.display.flip()

        while self.running:
            screen.fill(self.background_color)
            self._draw_fancy_gallow()
            screen.blit(instructions, instr_rect)
            self._man_pieces()

            display_word = ' '.join(self.guessed_word)
            guessed_word = self.font.render(f"Слово: {display_word}", True, (0, 0, 139))
            word_rect = guessed_word.get_rect(center=(720, 300))
            screen.blit(guessed_word, word_rect)

            if self.wrong_guesses:
                wrong_display = ' '.join(self.wrong_guesses)
            else:
                wrong_display = ''
            wrong_guesses = self.font.render(f"Ошибки: {wrong_display}", True, (200, 0, 0))
            wrong_rect = wrong_guesses.get_rect(center=(720, 400))
            screen.blit(wrong_guesses, wrong_rect)

            signature = self.small_font.render("Created by Nakka", True, (255, 215, 0))
            signature_rect = signature.get_rect(bottomright=(980, 680))
            screen.blit(signature, signature_rect)

            self._message()

            if self.game_over:
                result = self._show_end_screen()
                return result

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "exit"
                elif event.type == pygame.KEYDOWN and self.taking_guess:
                    self._guess_taker(event.unicode)

            pygame.display.flip()
            self.FPS.tick(60)

        return "menu"


def main():
    while True:
        menu = Menu(screen)
        choice = menu.run()
        if choice == "exit":
            break
        elif choice == "play":
            game = Hangman()
            result = game.run()
            if result == "exit":
                break
            # иначе (result == "menu") возвращаемся в меню

    pygame.quit()


if __name__ == "__main__":
    main()