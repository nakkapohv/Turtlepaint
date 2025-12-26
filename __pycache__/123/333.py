
try: 
    a = int(input("Введите превое число: "))
    b = int(input("Введите второе число: "))
    result = a/b

except (ZeroDivisionError, ValueError):
    print("Ошибка")

else:
    print(result)