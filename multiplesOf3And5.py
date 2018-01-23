i = [ ]
x = 0
three = 0
while x != 999:
    x += 1
    if x%3 == 0 or x%5 == 0:
        three += x
        print(three)
