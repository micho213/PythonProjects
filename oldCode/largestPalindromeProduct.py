x = 900
y = 820

pali = str(x * y)
i = 1
lol =[]
lol1 = []
lol2 = []
while x < 1000:
    pali = str(x * y)
    if pali[i-1] == pali[-i]:
        i+=1
        if i == len(pali):
            print(pali,x,y)
            lol.append(pali)
            lol1.append(x)
            lol2.append(y)
            x+=1
            y += 1
            i = 1

    else:
       x+=1
       y +=1
       i = 1


print(lol)
print(lol1)
print(lol2)