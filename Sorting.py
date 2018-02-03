#117308883
#Michal Wolas

def Print(data):
    print("Name    Age")
    print("------- ---")
    [print("%-7s %3s" % (name, age)) for name, age in data] # -7 signifies 7 spaces to the right , %s is a placeholder
    # for loop comprehension that iterates through data extracting name and age from the list within a list and prints it in the formant
    print("------- ---")

def bubbleSort (data, field):
    #fieldnum check if the user wants to sort by age or name
    fieldnum = 0  # 0 is the position of name in the tuple , e.g x= [("mary",10)] --- print((x[0])[0]) == "mary"
    if field == "age":
        fieldnum = 1

    for iteration in range(len(data)-1): #main iteration of the list
        for index in range(len(data)-1): # this loop goes through each element and compares it with the next one
            if (data[index])[fieldnum] > (data[index+1])[fieldnum]: # compares the iterated element with the next one
                #makes changes , by swapping the iterated element with the next one if it is bigger
                change = (data[index]) # element to be swapped/changed
                data[index] = (data[index +1]) #makes the next element be in the position of the previous one
                data[index + 1] =  change # position of the next element is now swapped with the item to be changed
    return Print(data) # uses the print format from previous function to output the result of the bubblesort

def SelectionSort(data,field):
    #fieldnum check if the user wants to sort by age or name
    fieldnum = 0   # 0 is the position of name in the tuple , e.g x= [("mary",10)] --- print((x[0])[0]) == "mary"
    if field == "age":
        fieldnum = 1

    i = 0 # variable that makes sure when an item is placed at the start it isn't iterated through

    for mainiteration in range(len(data)): # main loop
        largest = data[0]
        index = 0
        for iteration in range(len(data) - i):  # loop to check for largest value judged by field ,  len(data) - i  makes sure it doesn't iterate through already sorted values
                if (data[iteration])[fieldnum] > largest[fieldnum]: #checks for largest value , compared to the first value
                    largest = data[iteration] # overwrites the value untill largest value is saved
                    index = iteration #saves the index of that largest value to make the swap later
        i +=1   # as a change is made to the list and an item is placed at the start , i is increased to avoid that item being iterated through
        #swaps the largest value of this current iteration with the last value,  next time that value is affected by i as the last value is the largest and i changes with each change
        data[index] = data[(len(data) - i)]
        data[(len(data) - i)] = largest
    return Print(data)  # uses the print format from previous function to output the result of the bubblesort


listOfNames = [ ("Ann",23),("Tim",19),("Bob",37),("Ned",51),("jack",67),("John",60),("oldest",70),("Mary",10),("Patrik",34)]

#calls the various functions
Print(listOfNames)
bubbleSort(listOfNames,"age")
SelectionSort(listOfNames,"age")
