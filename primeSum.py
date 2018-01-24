
def check_prime(number):
    return all(number % i for i in range(2, number))

x = 1
answer = 0
while x < 2000000:
    x+=1
    if check_prime(x):
        answer+=x
print(answer)