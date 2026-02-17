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
        with open("Project-individual\Проект Виселица\words.txt.txt", "r", encoding= "UTF-8") as file: 
            #Эта строка автоматические открывает файл и закрывает по завершению выполнения блока кода
            #По заданному нами пути, "r" - мы даём понять что этот файл мы открывает только для чтения
            #encoding= "UTF-8" - кодировка файла, чтобы правильно читать символы
            words = file.read().split("\n") #Читаем всё содержимое файла, как строку и разделяем строку по символу и переносим строки, наши слова становятся списком
            self.secret_word = random.choice(words) #Выбираем случайный элемент из списка, случайное слово из файла
            self.guessed_word = "_" * len(self.secret_word) #Создаём строку состоющую из звёздочек, длиной равной длине из загаданного слова (отображение прогресса)
        
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
        if self.wrong_guess_count == 1:
            head = pygame.draw.circle(screen, self.body_color, [343, 200], 40, 0)
        elif self.wrong_guess_count == 2:
            body = pygame.draw.rect(screen, self.body_color, pygame.Rect(335, 230, 17, 160))
        elif self.wrong_guess_count == 3:
            r_arm = pygame.draw.line(screen, self.body_color, [290, 360], [338, 252], 15)
        elif self.wrong_guess_count == 4:
            l_arm = pygame.draw.line(screen, self.body_color, [400, 360], [348, 252], 15),
        elif self.wrong_guess_count == 5:
            r_leg = pygame.draw.line(screen, self.body_color, [405, 500], [344, 385], 16),
        elif self.wrong_guess_count == 6:
            l_leg = pygame.draw.line(screen, self.body_color, [283,503], [340, 385], 16)


    def _right_guess(self, guess_letter): #Эта функция будет вызваться когда пользователь угадал букву
        #Внутри функции мы создаем последовательность индексов букв, перебираем эти индексы
        #Простыми словами если пользователь угадал нужную букву, то она открывается на нужном месте
        index_positions = [index for index, item in enumerate(self.secret_word) if item == guess_letter]
        for i in index_positions: #Перебираем все найденные позиции
            #Далее мы указываем куда встать нашим угаданным буквам 
            self.guessed_word = self.guessed_word[0:i] + guess_letter + self.guessed_word[i+1:] 
        #screen.fill(pygame.Color(self.background_color), (10, 370, 390, 20)) 


    def _wrong_guess(self, guess_letter): #Эта функция будет вызывать когда пользователь не угадал букву
        self.wrong_guesses.append(guess_letter) #Список который будет хранить буквы, которые не правильно угаданы
        self.wrong_guess_count += 1 #Переменная которая считает, сколько неправильных догадок 
        self._man_pieces() #Вызываем отрисовку человечка


    def _guess_taker(self, guess_letter): #Эта функкция будет вызваться когда мы вводим букву
        if guess_letter in russian_letters: #Говорим что используем русскую кириллицу 
            if guess_letter in self.secret_word and guess_letter not in self.guessed_word:#Если все условия соблюдены 
                self._right_guess(guess_letter) #Вызываем появление угаданной буквы
            elif guess_letter not in self.secret_word and guess_letter not in self.wrong_guesses: #Проверка, если буквы нет в слове или не была ли она добавлена в список не правильных
                self._wrong_guess(guess_letter)


    def _message(self): #Проверка состояния игры и отрабражения слова
        if self.guessed_word == self.secret_word: #Проверка выиграл ли игрок
            self.taking_guess = False #Если проиграл, то прекращает игру
            screen.fill(pygame.Color(0,0,79), (40, 218, 320, 30))
            message = self.font.render("Вы победили!!", True, (255,235,0))
            screen.blit(message,(152,224)) #Отрисовка сообщения о том что мы выиграли
            
        elif self.wrong_guess_count == 6:
            self.taking_guess = False #Есл мы 6 раз ответили неверно, то игра заканчивается
            #screen.fill(pygame.Color("grey"), (40, 218, 320, 30))
            message = self.font.render("   Вы проиграли!!", True, (150,0,10))
            screen.blit(message,(78,224)) #Отрисовка сообщения о том что мы проиграли

            word = self.font.render(f"слово: {self.secret_word}", True, (255,255,255))
            screen.blit(word,(10,300)) #Отрисовка с загаданным словом, появляется когда мы проиграли

        #if not self.taking_guess: #Срабатывает когда мы выиграли или проиграли
            #screen.fill(pygame.Color(self.background_color), (35, 460, 390, 20))


    def main(self):
        screen.fill(self.background_color) #Заливаем весь экран заданный нами цветом
        self._gallow() #Риуем висилицу 
        instructions = self.font.render('Введите любую букву', True, (125,0,0)) #Выводим текст на экран (Введите любую букву)
        screen.blit(instructions,(680,150)) #Ставляем нужный нам текст по координатам

        while self.running: #Запуска цикл
            guessed_word = self.font.render(f"Слово: {self.guessed_word}", True, (0,0,0)) 
            screen.blit(guessed_word,(680,200)) #Создаем изображение строки с текущим состоянием угаданного слова
            wrong_guesses = self.font.render(f"Ошибки: {' '.join(map(str, self.wrong_guesses))}", True, (0,0,0))
            screen.blit(wrong_guesses,(680,300)) #Создаём строку с перечнем неправильных букв

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