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

users = {"Dima", "Vova"}
for user in users:
    print(user)