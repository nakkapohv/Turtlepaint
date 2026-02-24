import pygame
from pygame.locals import *

import random #имортируем библиотеку random

pygame.init() #Инициализация библиотеки PyGame, настраиваем систему отображения 
pygame.font.init() #инициализируем модуль шрифтов

screen = pygame.display.set_mode((1000, 700)) #Задаём размеры нашему окну
pygame.display.set_caption("Hangman") #Задаём название окна
russian_letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ' \
                  'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


class Hangman():
    def __init__(self): #Создаём основной класс и функцию, который будет отвечать за логику игры
        with open("Project-individual\\Проект Виселица\\words.txt.txt", "r", encoding="UTF-8") as file:
            words = [w.strip() for w in file.read().split("\n") if w.strip()]
            self.secret_word = random.choice(words)

            # NEW — первая буква всегда заглавная
            if self.secret_word:
                self.secret_word = self.secret_word[0].upper() + self.secret_word[1:]

            # хранить угаданное слово как список символов (по одному элементу на позицию)
            self.guessed_word = [" "] * len(self.secret_word)
        
        self.wrong_guesses = [] #Задаём пееменную, в которой храним список неправильных угадываний (букв которые уже названы не правильно)
        self.wrong_guess_count = 0 #Счетчик ошибок
        self.taking_guess = True # #Логическая переменная (Флаг), указывающий, что игра продолжается и можно вводить буквы
        self.running = True #Флаг, который контролирует главный цикл игры, пока он равен True - игра продолжается

        self.background_color = (168, 184, 208) #Задаём цвет фона, в моём случае это кремовый 
        self.gallow_color = (0, 0, 0) #Задаём цвет для виселицы, в моём случае чёртный
        self.body_color = (244, 213, 187) #Задаём цвет человечка, который висит на виселице

        self.font = pygame.font.SysFont("Cascadia", 50) #Задаём шрифт и размер
        self.FPS = pygame.time.Clock() #Создаём объект таймера, который регулирует чистоту обновления экрана(ФПС)


    def _gallow(self): #Функция внутри класса, которая отрисовывать виселицу 
        
        #Отрисовка по координатам x и y (1 и 2 цифры), так же указывает ширину и высоту (3 и 4 цифры)
        stand = pygame.draw.rect(screen, self.gallow_color, pygame.Rect(100, 600, 260, 15)) 
        body = pygame.draw.rect(screen, self.gallow_color, pygame.Rect(225, 100, 13, 500))
        hanger = pygame.draw.rect(screen, self.gallow_color, pygame.Rect(230, 100, 220, 11))
        rope = pygame.draw.rect(screen, self.gallow_color, pygame.Rect(338, 110, 10, 50))


    # Отрисовчка частей человечка (числа в квадратных скобках это коодинаты x и y)
    def _man_pieces(self):
        # Рисуем на каждом кадре те части, которые уже открыты (>=), чтобы не полагаться на вызов в момент ошибки
        if self.wrong_guess_count >= 1:
            pygame.draw.circle(screen, self.body_color, [343, 200], 40, 0)
        if self.wrong_guess_count >= 2:
            pygame.draw.rect(screen, self.body_color, pygame.Rect(335, 230, 17, 160))
        if self.wrong_guess_count >= 3:
            pygame.draw.line(screen, self.body_color, [290, 360], [338, 252], 15)
        if self.wrong_guess_count >= 4:
            pygame.draw.line(screen, self.body_color, [400, 360], [348, 252], 15)
        if self.wrong_guess_count >= 5:
            pygame.draw.line(screen, self.body_color, [405, 500], [344, 385], 16)
        if self.wrong_guess_count >= 6:
            pygame.draw.line(screen, self.body_color, [283,503], [340, 385], 16)


    def _right_guess(self, guess_letter): #Эта функция будет вызваться когда пользователь угадал букву
        # NEW — сравнение без учёта регистра
        index_positions = [
            index for index, item in enumerate(self.secret_word)
            if item.lower() == guess_letter.lower()
        ]

        for i in index_positions: #Перебираем все найденные позиции
            # вставляем оригинальную букву (с правильным регистром)
            self.guessed_word[i] = self.secret_word[i]


    def _wrong_guess(self, guess_letter): #Эта функция будет вызывать когда пользователь не угадал букву
        self.wrong_guesses.append(guess_letter.lower()) # NEW — сохраняем в одном регистре
        self.wrong_guess_count += 1 #Переменная которая считает, сколько неправильных догадок 


    def _guess_taker(self, guess_letter): #Эта функкция будет вызваться когда мы вводим букву
        if not guess_letter or len(guess_letter) != 1:
            return

        if guess_letter in russian_letters: #Говорим что используем русскую кириллицу 

            # NEW — сравнение без учёта регистра
            gl = guess_letter.lower()
            secret_lower = [c.lower() for c in self.secret_word]
            guessed_lower = [c.lower() for c in self.guessed_word]
            wrong_lower = [c.lower() for c in self.wrong_guesses]

            if gl in secret_lower and gl not in guessed_lower:
                self._right_guess(guess_letter)
            elif gl not in secret_lower and gl not in wrong_lower:
                self._wrong_guess(guess_letter)


    def _message(self): #Проверка состояния игры и отрабражения слова
        # сравниваем собранную строку (без пробелов) с секретным словом
        if ''.join(self.guessed_word) == self.secret_word: #Проверка выиграл ли игрок
            self.taking_guess = False #Если выиграл, то прекращает ввод
            screen.fill(pygame.Color(0,0,79), (40, 218, 320, 30))
            message = self.font.render("Вы победили!!", True, (255,235,0))
            screen.blit(message,(152,224)) #Отрисовка сообщения о том что мы выиграли
            
        elif self.wrong_guess_count == 6:
             self.taking_guess = False
             self._dark_souls_lose_screen()

    def _dark_souls_lose_screen(self):
    # Создаём полупрозрачную поверхность размером с экран
    
        overlay = pygame.Surface((1000, 700))
        overlay.set_alpha(180)  # Прозрачность (0-255). 180 = сильное затемнение
        overlay.fill((0, 0, 0))  # Чёрный цвет

    # Накладываем затемнение
        screen.blit(overlay, (0, 0))

    # Большой шрифт для надписи
        big_font = pygame.font.SysFont("Cascadia", 100)

        lose_text = big_font.render("ВЫ ПРОИГРАЛИ", True, (180, 0, 0))
        word_text = self.font.render(f"Правильное слово: {self.secret_word}", True, (255, 255, 255))

    # Центрируем текст
        lose_rect = lose_text.get_rect(center=(500, 300))
        word_rect = word_text.get_rect(center=(500, 420))

        screen.blit(lose_text, lose_rect)
        screen.blit(word_text, word_rect)


    def main(self):
        screen.fill(self.background_color) #Заливаем весь экран заданный нами цвет
        self._gallow() #Риуем висилицу 
        instructions = self.font.render('Введите любую букву', True, (36, 1, 69)) #Выводим текст на экран (Введите любую букву)
        screen.blit(instructions,(680,150)) #Ставляем нужный нам текст по координатам

        while self.running: #Запуска цикл
            # рисуем виселицу и уже набранные части (на каждый кадр)
            self._gallow()
            self._man_pieces()

            # отображаем слово с пробелами между буквами/подчёркиваниями (координаты не менял)
            guessed_word_s = ' '.join(self.guessed_word)
            guessed_word = self.font.render(f"Слово: {guessed_word_s}", True, (0, 8, 62))
            screen.blit(guessed_word,(680,200)) #КОГДА: координата сохранена как (680, 200)

            # отображаем ошибки (также без изменений координат)
            wrong_guesses = self.font.render(f"Ошибки: {' '.join(self.wrong_guesses)}", True, (0, 8, 62))
            screen.blit(wrong_guesses,(680,300)) #КОГДА: координата сохранена как (680, 300)

            self._message() #Вызываем при допольнительный сообщениях (О победе, о поражениях)
        
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    self.running = False #Выход из программы и цикла, завершить игру в любой момент

                elif self.event.type == pygame.KEYDOWN: #Вызывается когда мы нажимаем любую клавишу на клавиатуры
                    if self.taking_guess: #Контролирует можно ли сейчас вводить буквы
                        self._guess_taker(self.event.unicode) #Делаем так чтобы заглавные и строчные буквы подходили в любом случае

            pygame.display.flip() #Обновляет весь экран целиком, используется для отобрежния измененй
            self.FPS.tick(60) #ставил лок и контроль частоты кадров (ФПС)

        pygame.quit() #Заверашем работу(выходим)


if __name__ =="__main__": #Запущен ли скрипт напрямую (а не импортирован как модуль)
    h = Hangman() #Класс самой игры, вызывается
    h.main() #Вызываем саму игру, запускаем