i = [ ]
x = 0
answer = 0
while x != 999:
    x += 1
    if x%3 == 0 or x%5 == 0:
        answer += x
print(answer)
