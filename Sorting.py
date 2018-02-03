def Print(data):
    print("Name    Age")
    print("------- ---")
    [print("%-7s %3s" % (name, age)) for name, age in data]


def bubbleSort (data, field):
    for iteration in range(len(data)-1):
        for index in range(len(data)-1):
            if field == "age":
                if (data[index])[1] > (data[index+1])[1]:
                    change = ((data[index])[0],(data[index])[1])
                    data[index] = ((data[index +1])[0],(data[index+1])[1])
                    data[index + 1] =  change
            if field == "name":
                if (data[index])[0] > (data[index+1])[0]:
                    change = ((data[index])[0],(data[index])[1])
                    data[index] = ((data[index +1])[0],(data[index+1])[1])
                    data[index + 1] =  change
    return Print(data)

def SelectionSort(data,field):
    x = -1
    for iteration in range(len(data)):
        for iteration2 in range(len(data)):
            if field == "age":
                if (data[iteration])[1] > (data[iteration2])[1]:
                    largest = ((data[iteration])[0],(data[iteration])[1])
                    y = iteration
    data[x] = largest
    data[y] = ((data[x])[0], (data[x])[1])

    print(data)

"""data[iteration] = ((data[x])[0], (data[x])[1])
            data[x] = largest
            x -= 1"""
x = 3


listOfNames = [ ("Ann",23),("Tim",19),("Bob",37),("Ned",51),("Sue",18)]
print(listOfNames[-1])
#Print(listOfNames)
#bubbleSort(listOfNames,"age")
SelectionSort(listOfNames,"age")
