import turtle

screen = turtle.Screen()
screen.bgcolor("sky blue")

def pencolorandsize(t, color,size):
    if size < 1:
       print ("Размер не может быть меньше одного")
       return(0)
    t.color(color)
    t.pensize(size) #Смена цевета и размера пера

def teleport(t, x, y):
   t.penup()
   t.goto(x, y)
   t.pendown()  #Телепорт пера (чтобы фигуры были в разных местах)

def square(t, x, y, size):
 if size < 1:
    print ("Размер не может быть меньше одного")
    return(0)
 teleport (t, x, y)
 for _ in range(4):
    t.forward(size)
    t.left(90)
  
def triangle(t, x, y, size):
   teleport (t, x, y)
   for _ in range(3):
     t.left(360 / 3)
     t.forward(size) #Функция Отрисовки равностороннего треугольника

def hexagon10(t, x, y, size):
   teleport(t, x, y)
   for i in range(10):
    t.forward(size)
    t.right(360 / 8) #Функция отрисовки многоугольника (в данном случае 8-угольника)

def rectangle(t, x, y, size, size2):
 if size < 1:
    print ("Размер не может быть меньше одного")
    return(0)
 teleport(t, x, y)
 for i in range(2):
    t.forward(size)
    t.left(90)
    t.forward(size2)
    t.left(90) 
  
def circle(t):
   for i in range(370):
     t.forward(1)
     t.right(1) #Открисовка круга #Функция отрисовки круга
