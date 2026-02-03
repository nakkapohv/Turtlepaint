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
        with open("./__pycache__\Проект Виселица\words.txt.txt", "r", encoding= "UTF-8") as file: 
            #Эта строка автоматические открывает файл и закрывает по завершению выполнения блока кода
            #По заданному нами пути, "r" - мы даём понять что этот файл мы открывает только для чтения
            #encoding= "UTF-8" - кодировка файла, чтобы правильно читать символы
            words = file.read().split("\n") #Читаем всё содержимое файла, как строку и разделяем строку по символу и переносим строки, наши слова становятся списком
            self.secret_word = random.choice(words) #Выбираем случайный элемент из списка, случайное слово из файла
            self.guessed_word = "*" * len(self.secret_word) #Создаём строку состоющую из звёздочек, длиной равной длине из загаданного слова (отображение прогресса)
        
        self.wrong_guesses = [] #Задаём пееменную, в которой храним список неправильных угадываний (букв которые уже названы не правильно)
        self.wrong_guess_count = 0 #Счетчик ошибок
        self.taking_guess = True # #Логическая переменная (Флаг), указывающий, что игра продолжается и можно вводить буквы
        self.running = True #Флаг, который контролирует главный цикл игры, пока он равен True - игра продолжается

        self.background_color = (168, 184, 208) #Задаём цвет фона, в моём случае это кремовый 
        self.gallow_color = (0, 0, 0) #Задаём цвет для виселицы, в моём случае чёртный
        self.body_color = (244, 213, 187) #Задаём цвет человечка, который висит на виселице

        self.font = pygame.font.SysFont("Cascadia", 40) #Задаём шрифт и размер
        self.FPS = pygame.time.Clock() #Создаём объект таймера, который регулирует чистоту обновления экрана(ФПС)


    def _gallow(self): #Функция внутри класса, которая отрисовывать виселицу 
        
        #Отрисовка по координатам x и y (1 и 2 цифры), так же указывает ширину и высоту (3 и 4 цифры)
        stand = pygame.draw.rect(screen, self.gallow_color, pygame.Rect(400, 450, 200, 10)) 
        body = pygame.draw.rect(screen, self.gallow_color, pygame.Rect(495, 180, 10, 280))
        hanger = pygame.draw.rect(screen, self.gallow_color, pygame.Rect(495, 180, 150, 10))
        rope = pygame.draw.rect(screen, self.gallow_color, pygame.Rect(570, 180, 10, 45))


    # Отрисовчка частей человечка (числа в квадратных скобках это коодинаты x и y)
    def _man_pieces(self):
        if self.wrong_guess_count == 1:
            head = pygame.draw.circle(screen, self.body_color, [575, 246], 23, 0)
        elif self.wrong_guess_count == 2:
            body = pygame.draw.rect(screen, self.body_color, pygame.Rect(570, 260, 10, 68))
        elif self.wrong_guess_count == 3:
            r_arm = pygame.draw.line(screen, self.body_color, [546, 321], [571, 280], 8)
        elif self.wrong_guess_count == 4:
            l_arm = pygame.draw.line(screen, self.body_color, [605, 320], [575, 278], 8),
        elif self.wrong_guess_count == 5:
            r_leg = pygame.draw.line(screen, self.body_color, [552, 373], [575, 323], 8),
        elif self.wrong_guess_count == 6:
            l_leg = pygame.draw.line(screen, self.body_color, [597, 370], [572, 320], 8)


    def _right_guess(self, guess_letter): #Эта функция будет вызваться когда пользователь угадал букву
        #Внутри функции мы создаем последовательность индексов букв, перебираем эти индексы
        #Простыми словами если пользователь угадал нужную букву, то она открывается на нужном месте
        index_positions = [index for index, item in enumerate(self.secret_word) if item == guess_letter]
        for i in index_positions: #Перебираем все найденные позиции
            #Далее мы указываем куда встать нашим угаданным буквам по индексам
            self.guessed_word = self.guessed_word[0:i] + guess_letter + self.guessed_word[i+1:] 
        screen.fill(pygame.Color(self.background_color), (10, 500, 390, 20)) 


    def _wrong_guess(self, guess_letter):
        self.wrong_guesses.append(guess_letter)
        self.wrong_guess_count += 1
        self._man_pieces()


    def _guess_taker(self, guess_letter):
        if guess_letter in russian_letters:
            if guess_letter in self.secret_word and guess_letter not in self.guessed_word:
                self._right_guess(guess_letter)
            elif guess_letter not in self.secret_word and guess_letter not in self.wrong_guesses:
                self._wrong_guess(guess_letter)


    def _message(self):
        if self.guessed_word == self.secret_word:
            self.taking_guess = False
            screen.fill(pygame.Color(0,0,79), (40, 218, 320, 30))
            message = self.font.render("Вы победили!!", True, (255,235,0))
            screen.blit(message,(152,224))
            
        elif self.wrong_guess_count == 6:
            self.taking_guess = False
            screen.fill(pygame.Color("grey"), (40, 218, 320, 30))
            message = self.font.render("   Вы проиграли!!", True, (150,0,10))
            screen.blit(message,(78,224))
            # shows the secret word if the player lose
            word = self.font.render(f"слово: {self.secret_word}", True, (255,255,255))
            screen.blit(word,(10,300))

        if not self.taking_guess:
            screen.fill(pygame.Color(self.background_color), (35, 460, 390, 20))


    def main(self):
        screen.fill(self.background_color)
        self._gallow()
        instructions = self.font.render('Введите любую букву', True, (125,0,0))
        screen.blit(instructions,(35,460))

        while self.running:
            guessed_word = self.font.render(f"Слово: {self.guessed_word}", True, (0,0,0))
            screen.blit(guessed_word,(10,370))
            wrong_guesses = self.font.render(f"Ошибки: {' '.join(map(str, self.wrong_guesses))}", True, (0,0,0))
            screen.blit(wrong_guesses,(10,420))

            self._message()
        
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    self.running = False

                elif self.event.type == pygame.KEYDOWN:
                    if self.taking_guess:
                        self._guess_taker(self.event.unicode)

            pygame.display.flip()
            self.FPS.tick(60)

        pygame.quit()


if __name__ =="__main__":
    h = Hangman()
    h.main()