
def check_prime(number):
    return all(number % i for i in range(2, number))
answer = []
x = 0

while len(answer) <10001:
    x += 1
    prime = check_prime(x)
    if prime:
        answer.append(x)
print(answer)



'''
true = True
x = 2
i = 2
answer = []
y= 0

while len(answer)<10001:
    lol = 0
    if x % 2 == 0:
        y += 1
    else:
        for num in range (2,x):
            for num2 in range(2,x):
                if x/num2 % 1 == 0:
                    lol+=1
            if lol == 0:
                if x in answer:
                    y += 1
                else:
                    answer.append(x)
    x += 1

print(answer)
print(len(answer))
'''
