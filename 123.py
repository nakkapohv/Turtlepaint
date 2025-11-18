
list_of_people = [

    [1, "Ахмедов"],
    [2, "Белов"],
    [3, "Герасин"],
    [4, "Дублин"],
    [5, "Екимов"],
    [6, "Кондратьев"],
    [7, "Зимин"],
    [8, "Игнашевич"],
    [9, "Никитин"],
    [10, "Похвищев"],
    [11, "Репин"],
    [12, "Северюхин"],
    [13, "Сорокин"],

]


backrooms_people = dict()
earth_people = dict(list_of_people)

print(type(list_of_people))
print(type(earth_people))

#for key, value in earth_people.items():
 #   print(key, value)

for i in range(1, len(earth_people) + 1):
    if i % 2 == 0:
        backrooms_people[i] = earth_people.get(i)

print (backrooms_people)
for key, value in backrooms_people.items():
    print(key, value)