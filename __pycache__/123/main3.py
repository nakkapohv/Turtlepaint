class cat_Node:

#Через ключевое солнце self объявляются поля клаccfб т.е переменные, которые будут принадлежать его экземпляру 
    def __init__(self, name = None):

        self.prev = None
        self.next = None
        self.name = name 
    
    def __str__(self):
        return self.name 

class cat_linkedlist:

    def __init__(self):
        self.head = None
        self.tail = None
    
    def __str__(self):
        cats = ""
        current = self.head
        if current is None:
            print("Список пуст.")
            return
        while current is not None:
            cats += current.name + " "
            current = current.next
        return cats
    
    def add(self, cat_name):
        
        #Мы создаём переменную в которой будем хранить сылку на новый созданный узел
        #При его создании мы передаём информацию - имя кота
        newCat = cat_Node(cat_name)
        pass
       
       #Если указатель head для списка - пустой
       #то мы указываем нашу ссылку newCat = в качестве указателя (строки 25, 26)
        if self.head is None:
            self.head = newCat
        
        #Иначе, если указатель уже есть, мы объевляем переменную current и храним
        #В нём ссылку на (голову) нашего списка. Затем перебираем все элементы
        #списка до тех пор, пока указатель на следующий элемент не станет пустым.
        #И добовляем в качестве пустого ссылку на новый элемент.

        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next=newCat


CATS = cat_linkedlist()

CATS.add("Барсик")
CATS.add("Соня")
CATS.add("Гуманоид")
CATS.add("Ирокез")
CATS.add("Добрый")

print(CATS)