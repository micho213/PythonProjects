"""
Michal Wolas    117308883


What is the difference between mergesort and quicksort?
    - both algorithms recursively split the list and sort it.
     however, quicksort does its sorting during the splitting by comparing it with the pivot.
     In merge sort the sorting part is done on the way up when two lists are merged back together.

What is the worst case complexity of mergesort?
    - O(n log n)

What is the space complexity of standard mergesort on an array, and bottom-up mergesort on an array?
    -  O (n log n) for standard
    - O(n) for bottom up , as we just need 1 extra list.


Assignment Analyisis:

    as expected, the times for sorting a list for each algorithm (excluding python's timsort)  in order were :
        1. Quicksort 2. mergesort 3. heapsort 4. Insertion sort ( any basic sort )

    Without the need of shuffling the list before QuickSort , As its worst-case is O(n^2) on sorted lists.
    Quicksort performs much better. When adding the shuffling, it also beats mergesort but not by a lot.
    On bigger lists heapsort tends to be about 25-60% worse than quick and merge sort. e.g for 100000 item list
    heapsort took 1s, where as quicksort took 0.38s. There was also a significant advantage with having heapsort done
    iteratively rather than recursively , I found about 20% increase in efficiency on the lists sizes I could test

    Basic sorting algorithm ( insertion sort) was almost pointless to run on bigger lists. However during my testing,
    I accidentally didn't shuffle the list for insertion sort, and it sorted it faster than python sort. Which left me
    confused but lead me to a discovery of how Timsort operates ( before being tol in the lecture)

"""

import random
from time import perf_counter
import math


def quicksort(list, left, right):
    if left < right:
        # get pivot, while sorting the sublists (inplace)
        pivot = sortSubList(list, left, right)

        quicksort(list, left, pivot)  # recursive call to sort left side
        quicksort(list, pivot + 1, right)  # recursive call to sort left side
        return list


def sortSubList(list, left, right):
    pivot = list[left]  # the first element of the sublist as pivot
    while True:
        # search to the left until you get a bigger item
        while list[left] < pivot:
            left += 1
        # search to the right until you get a smaller item
        while list[right] > pivot:
            right -= 1
        if left >= right:  # if the searches have crossed
            return right  # this is the pivot for the next sub lists
        # if the searches did not cross, swap the found items
        list[left], list[right] = list[right], list[left]
        left += 1
        right -= 1


def bubbleUp(l, item, quit=False):
    parent = (item - 1) // 2  # the parent of the item being bubbled up
    if parent < 0 or quit:  # if we went outside the list range
        return
    # only compare with item's parent, and swap if its bigger
    if l[item] > l[parent]:
        l[parent], l[item] = l[item], l[parent]
        bubbleUp(l, parent)  # recursively call, to see if more changes are needed
    return


def bubbleDown(l, item, end):
    # iterative version about 20% faster than recursive
    while (item * 2 + 1) < end:
        # if it ever enters the loop then left child exits, position is left child, position +1 is rightchild
        position = (2 * item) + 1
        lchild = l[position]

        # if right child exists compare left with right and decide
        if end > position:
            rchild = l[position + 1]  # right child exists
            if lchild >= rchild:
                if l[item] < lchild:  # if the item we are bubbling is smaller swap
                    l[position], l[item] = l[item], l[position]
                    item = position  # position updated for the next loop iteration
                else:  # the item isn't smaller its in the right place so break out
                    break
            else:  # same as above but for rightchild
                if l[item] < rchild:
                    l[position + 1], l[item] = l[item], l[position + 1]
                    item = position + 1
                else:
                    break
        # if there isn't a rightchild, only check left child
        else:
            if l[item] < lchild:
                l[position], l[item] = l[item], l[position]
                item = position
            else:
                break  # must be in the right position so break out


def bubbleDownRecursive(l, item, end):
    # left and right  child of the item we are bubbling down
    left = (2 * item) + 1
    right = left + 1

    # variable end represents the end of the Max heap
    # as we are removing the max and placing it at the end progressively
    if right > end:  # if we went outside the range
        return

    # now choose the correct child to swap with
    # left side
    if l[left] >= l[right]:
        if l[item] < l[left]:  # if the item in question is smaller swap
            l[left], l[item] = l[item], l[left]
            bubbleDown(l, left, end)  # keep checking if the item is in the correct place

    # right side
    elif l[right] >= l[left]:
        if l[item] < l[right]:  # if the item in question is smaller swap
            l[right], l[item] = l[item], l[right]
            bubbleDown(l, right, end)  # keep checking if the item is in the correct place
    return  # this means the item is in the correct place already


def heapsortRecursive(toSort):
    for x in range(len(toSort)):  # loop to build the max heap sort
        bubbleUp(toSort, x)

    last = len(toSort) - 1
    for y in range(len(toSort)):  # this loop removes the biggest item and places it at the end of the list accordingly
        toSort[last], toSort[0] = toSort[0], toSort[last]
        last -= 1
        bubbleDownRecursive(toSort, 0, last)  # makes sure the swapped item is in the correct place

    # Sometimes the loop goes 1 too many times, and mixes up 0 and 1 index
    if toSort[0] > toSort[1]:
        toSort[0], toSort[1] = toSort[1], toSort[0]
    return toSort


def heapsort(toSort):
    # the other version where you bubble items down  instead of bubbling them up.
    end = len(toSort) - 1
    for x in range(len(toSort) - 1 - math.ceil(len(toSort) / 2), -1, -1):  # loop to build the max heap sort
        bubbleDown(toSort, x, end)

    last = len(toSort) - 1
    for y in range(len(toSort)):  # this loop removes the biggest item and places it at the end of the list accordingly
        toSort[last], toSort[0] = toSort[0], toSort[last]
        last -= 1
        bubbleDown(toSort, 0, last)  # makes sure the swapped item is in the correct place

    # Sometimes the loop goes 1 too many times, and mixes up 0 and 1 index
    if toSort[0] > toSort[1]:
        toSort[0], toSort[1] = toSort[1], toSort[0]

    return toSort


def heapsortRecursiveBubbleDown(toSort):
    # the other version where you bubble items down  instead of bubbling them up.
    end = len(toSort) - 1
    for x in range(len(toSort) - 1 - math.ceil(len(toSort) / 2), -1, -1):  # loop to build the max heap sort
        bubbleDownRecursive(toSort, x, end)

    last = len(toSort) - 1
    for y in range(len(toSort)):  # this loop removes the biggest item and places it at the end of the list accordingly
        toSort[last], toSort[0] = toSort[0], toSort[last]
        last -= 1
        bubbleDownRecursive(toSort, 0, last)  # makes sure the swapped item is in the correct place

    # Sometimes the loop goes 1 too many times, and mixes up 0 and 1 index
    if toSort[0] > toSort[1]:
        toSort[0], toSort[1] = toSort[1], toSort[0]

    return toSort


def mergeTwoLists(mergedLists, firstList, secondList):
    i1 = 0
    i2 = 0

    # save them in variables rather than calculating them all the time
    lenFirst = len(firstList)
    lenSecond = len(secondList)

    # as long as i1 and i2 are not outside their index range
    # merge them together accordingly
    while i1 < lenFirst and i2 < lenSecond:
        if secondList[i2] >= firstList[i1]:
            mergedLists += [firstList[i1]]
            i1 += 1
        else:
            mergedLists += [secondList[i2]]
            i2 += 1

    # if either of the lists were not fully added to the merged lists check and add them
    if i1 < lenFirst:
        mergedLists += firstList[i1:]  # add the remaining of the list to the merged result
    if i2 < lenSecond:
        mergedLists += secondList[i2:]  # add the remaining of the list to the merged result
    return mergedLists


def mergeSort(list):
    if len(list) <= 1:
        return list

    midPoint = len(list) // 2  # calculate the middle of the list
    firstList = list[:midPoint]
    secondList = list[midPoint:]

    # recursive call to break it down untill its a single length list
    firstList = mergeSort(firstList)
    secondList = mergeSort(secondList)

    mergedLists = []  # where the result will be stored
    return mergeTwoLists(mergedLists, firstList, secondList)


def insertionSort(list):
    # iterating left to right, try to place each item in its correct place
    for index in range(1, len(list)):
        to_insert = list[index]  # element to be inserted in the list
        j = index
        # find a correct place for the element
        # looking right to left from the index itself
        # esentially building the sorted list
        while list[j - 1] > to_insert and j > 0:
            # keep switching it until you find the right spot
            list[j] = list[j - 1]
            j -= 1
        list[j] = to_insert  # place the item in the right spot we just found
    return list


# each of the runXXX function, returns the time took for completing it, and the list itself
def runInsertSort(l):
    t1 = perf_counter()
    sortedInsert = insertionSort(l)
    t2 = perf_counter()
    return (t2 - t1), sortedInsert


def runHeapRecursive(l):
    t1 = perf_counter()
    sortedHeap = heapsortRecursive(l)
    t2 = perf_counter()
    return (t2 - t1), sortedHeap


def runHeapRecursiveBubbleDown(l):
    t1 = perf_counter()
    sortedHeap = heapsortRecursiveBubbleDown(l)
    t2 = perf_counter()
    return (t2 - t1), sortedHeap


def runHeap(l):
    t1 = perf_counter()
    sortedHeap2 = heapsort(l)
    t2 = perf_counter()
    return (t2 - t1), sortedHeap2


def runMerge(l):
    t1 = perf_counter()
    sortedMerge = mergeSort(l)
    t2 = perf_counter()
    return (t2 - t1), sortedMerge


def runQuick(l):
    t1 = perf_counter()
    # "randomising" of the list included in the time it takes to run QuickSort.
    random.shuffle(l) # shuffle the list regardless, to avoid sorting a sorted list.
    sortedQuick = quicksort(l, 0, len(l) - 1)
    t2 = perf_counter()
    return (t2 - t1), sortedQuick


def runPython(l):
    t1 = perf_counter()
    sortedPython = sorted(l)
    t2 = perf_counter()
    return (t2 - t1), sortedPython


def evaluateall(n, k):
    if k > n:
        return False
    myList = []
    for i in range(n - k):
        myList += [i]
    for x in range(k):
        duplicate = myList[random.randint(0, n - k - 1)]
        myList += [duplicate]

    print("n: %d k: %d len(mylist): %d \n" % (n, k, len(myList)))

    # shuffle and copy the lists
    random.shuffle(myList)
    heap, heapRecursive, heapRecursiveBD, python, merge, quick, insert = myList.copy(), myList.copy(), myList.copy(), myList.copy(), myList.copy(), myList.copy(), myList.copy()

    avgP, avgH, avgHR, avgHRBD, avgQ, avgM, avgI = 0, 0, 0, 0, 0, 0, 0
    timeInsert = 0
    numOfTimesToRun = 10

    for i in range(numOfTimesToRun):
        timePython, python = runPython(python)
        timeHeap, heap = runHeap(heap)
        timeMerge, merge = runMerge(merge)
        timeQuick, quick = runQuick(quick)

        if not n > 10000:
            timeInsert, insert = runInsertSort(insert)
            if insert != python:
                print("One of the lists didn't sort properly")
                break
        # testing other versions of heap
        timeHeap2, heapRecursive = runHeapRecursive(heapRecursive)
        timeHeap3, heapRecursiveBD = runHeapRecursiveBubbleDown(heapRecursiveBD)

        # testing on the basis that python sort will do it correctly
        if python != heap or python != quick or python != merge or heapRecursive != python or heapRecursiveBD != python:
            print("One of the lists didn't sort properly")
            break
        avgP += timePython
        avgH += timeHeap
        avgM += timeMerge
        avgQ += timeQuick
        avgI += timeInsert

        # other versions of heap
        avgHR += timeHeap2
        avgHRBD += timeHeap3

        # shuffle the original list again, and make copies
        random.shuffle(myList)
        heap, heapRecursive, heapRecursiveBD, python, merge, quick, insert = myList.copy(), myList.copy(), myList.copy(), myList.copy(), myList.copy(), myList.copy(), myList.copy()

    avgH = avgH / numOfTimesToRun
    avgP = avgP / numOfTimesToRun
    avgQ = avgQ / numOfTimesToRun
    avgM = avgM / numOfTimesToRun
    avgI = avgI / numOfTimesToRun

    avgHR = avgHR / numOfTimesToRun
    avgHRBD = avgHRBD / numOfTimesToRun

    print("Avarage times for  sorting a lists %d times" % (numOfTimesToRun))
    print("heap sort took: %.5f" % (avgH))
    print("mergesort took: %.5f" % (avgM))
    print("quicksort took: %.5f" % (avgQ))
    print("python sort took: %.5f" % (avgP))
    if avgI == 0:
        print("INSERTION SORT DID NOT EXECUTE BECAUSE LIST IS TOO BIG")
    else:
        print("Insertion sort took: %.5f " % (avgI))

    print("\nother versions of heap")
    print("heap Recursively with bubble up took: %.5f" % (avgHR))
    print("heap Recursively with bubble down only took: %.5f" % (avgHRBD))
    print("-----------------------------(%d, %d)  completed-----------------------------------\n" % (n, k))


def evaluate():
    evaluateall(100, 0)
    evaluateall(1000, 0)
    evaluateall(10000, 0)
    evaluateall(100000, 0)
    evaluateall(100, 20)
    evaluateall(1000, 200)
    evaluateall(10000, 2000)
    evaluateall(100000, 20000)
    evaluateall(100, 70)
    evaluateall(1000, 700)
    evaluateall(10000, 7000)
    evaluateall(100000, 70000)


evaluate()
