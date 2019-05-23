
squareNum = 0
squareSum = 0
for x in range(1,101):
    squareNum += x**2
    squareSum += x

squareSum = squareSum**2

print(squareSum - squareNum)



