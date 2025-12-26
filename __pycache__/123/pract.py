for x in [0,1]:
    for y in [0,1]: #Работает как с 2 в скобках так и с 0, 1 это одно и тоже
        for z in [0,1]:
            for w in [0,1]:
                if ((x or y) and not (y == z) and not (w)) == 1:
                 print(x,y,z,w)
