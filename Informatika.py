users = {"Dima", "Vova", "Kolya"}
print(users)    # {"Dima", "Vova", "Kolya"}

people = ["Dima", "Vova"]
users = set(people)
print (users) 

user = set() #Пустон множество

users = {"Dima", "Vova"}
print (len(users)) #Длина множества

users = set()
user.add("Dima") #Для добовления одиночного элемента
print(users)

users = {"Dima", "Vova"}
user = "Dima"
if user in users:
    users.remove(user) #Для удаления одного элемента из множества
print(users)

users = {"Dima", "Vova"}
users.discard("kolya") #переменной kolya нет и метод ничего не делает
print(users)
users.discard("Dima") #переменная Dima есть и метод удаляет этот элеминет
print(users)

users.clear() #Для удаления всех переменных 

users = {"Dima", "Vova"} #Для перебора множеств, используется цикл for:
for user in users:
    print(user)

users = {"Dima", "Vova"}
students = users.copy() #Копирование содержимое одного множества в другую переменную
print(students)

users = {"Dima", "Vova"}
users2 = {"Kolya", "Roma"}
users3 = users.union(users2) #Для объеденение нескольких множеств в одно
print(users3)

users = {"Dima", "Vova", "Kolya"}
users2 = {"Roma", "Dima", "Andrey"}
users3 = users.intersection(users2) #выдаёт только повторяющиеся элементы во множествах
print(users3)

users = {"Dima", "Vova", "Kolya"}
users2 = {"Roma", "Dima", "Andrey"}
users.intersection_update(users2) #Заменяет пересеченными элементами первое множество
print(users)

users = {"Dima", "Vova", "Kolya"}
users2 = {"Roma", "Dima", "Andrey"}
users3 = users.difference(users2) #Разность множеств, возращает те элементы которые есть в первом множестве, но нет во 2 
print(users3)

users = {"Dima", "Vova", "Kolya"}
users2 = {"Roma", "Dima", "Andrey"}
users3 = users.symmetric_difference(users2) #Возвращает все элементы обоих множеств, за исключением одинаковых
print(users3)

users = {"Dima", "Vova", "Kolya"}
superusers = {"Oleg", "Dima", "Vova", "Kolya", "Andrey"}
print(users.issubset(superusers)) #Является ли одно множество частью другого множества
print(superusers.issubset(users))

users = {"Dima", "Vova", "Kolya"}
superusers = {"Oleg", "Dima", "Vova", "Kolya", "Andrey"}
print(users.issuperset(superusers)) #Не являет ли одно множество частью другого множества
print(superusers.issuperset(users))

users = frozenset ({"Dima", "Vova", "Kolya"}) #Не может быть изменено

#В функцию frozenset передается набор элементов - список, кортеж, другое множество.

#В такое множество мы не можем добавить новые элементы, как и удалить из него уже имеющиеся. Собственно поэтому frozen set поддерживает ограниченный набор операций:

#len(s): возвращает длину множества

#x in s: возвращает True, если элемент x присутствует в множестве s

#x not in s: возвращает True, если элемент x отсутствует в множестве s

#s.issubset(t): возвращает True, если t содержит множество s

#s.issuperset(t): возвращает True, если t содержится в множестве s

#s.union(t)

#: возвращает объединение множеств s и t
#s.intersection(t): возвращает пересечение множеств s и t

#s.difference(t): возвращает разность множеств s и t

#s.copy(): возвращает копию множества s