import turtle
t = turtle.Turtle()
t.shape("turtle")
t.speed(500)
screen = turtle.Screen()
screen.bgcolor("sky blue")

def pencolorandsize(t, color,size):
   t.color(color)
   t.pensize(size) #Смена цевета и размера пера

def teleport(t, x, y):
   t.penup()
   t.goto(x, y)
   t.pendown()  #Телепорт пера (чтобы фигуры были в разных местах)

def square(t):
   for i in range(4):
     t.forward(70)
     t.right(90)  #Функция отрисовки квадрата
  
def triangle(t):
   t.forward(80)
   for i in range(3):
     t.left(360 / 3)
     t.forward(80) #Функция Отрисовки равностороннего треугольника

def hexagon10(t):
   for i in range(10):
      t.forward(30)
      t.right(360 / 8) #Функция отрисовки многоугольника (в данном случае 8-угольника)

def rectangle(t):
   for i in range(2):
     t.forward(50)
     t.left(90)
     t.forward(100)
     t.left(90) #Функция отрисовки прямоугольника (как бонус)
  
def circle(t):
   for i in range(370):
     t.forward(1)
     t.right(1) #Открисовка круга #Функция отрисовки круга

pencolorandsize(t, "red", 5) #выбираем цвет и размер пера
teleport(t, -180, 175) #Телепорт для того чтобы высставить фигуры в ряд
square(t) #Вызываем функцию для отрисовки квадрата
teleport(t, -40, 105) #Телепорт для того чтобы высставить фигуры в ряд
triangle(t) #Вызываем функцию для отрисовки треугольника
teleport(t, 120, 180) #Телепорт для того чтобы высставить фигуры в ряд
hexagon10(t) #Вызываем функцию для отрисовки многоугольника
teleport(t, -190, 40) #Телепорт для того чтобы высставить фигуры
rectangle(t)
teleport(t, 0, 40)
circle(t)


