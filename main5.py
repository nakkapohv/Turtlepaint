a = 0
b = 1
c = 0

i = 0
k = []

k.append(a)
k.append(b)

for i in range(144):
    k.append(a+b)
    c = b
    b = a + b
    a = c 

q = int(input("Введите число: "))

if k.count(q) > 0:
    print(k.index(q) + 1)

else:
    print("Не найдено")

