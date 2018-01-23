x = True
term1 = 1
term2 = 2
nextterm = term1 + term2
answer = []
while x:
    if nextterm > 4000000:
        x = False
    term1 = term2
    term2 = nextterm
    nextterm = term1 + term2
    answer.append(nextterm)

answer1 = 2
for number in answer:
    if number%2 == 0:
        answer1 += number

print(answer1)  #correct answer of sum of even numbers
print(answer)
