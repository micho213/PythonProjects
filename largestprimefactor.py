def factors(x):
    numlist = []
    answer =[]
    wrong = []
    correct = []

    for number in range(1,x+1,1):
        if x/number % 1 == 0:
            #numlist.append(number)
            if number > 1:
                for i in range(2, number):
                    if (number % i) == 0:
                        #print("unlucky",number)
                        wrong.append(number)
                else:
                    answer.append(number)
    #print(numlist)
    #print(wrong)
    #print(answer)
    for num in answer:
        if num not in wrong:
            correct.append(num)

    print(correct)
factors(60085147)


