import random
import math
import time


# represents a page, owned by a block. Has id and size
class Page:
    def __init__(self, id):
        self.size = 4
        self.id = id

    def __str__(self):
        return str(self.id)


# Block class owns Pages of variable sizes, The main memory Owns the blocks and stores them in a data structure
class Block:
    def __init__(self, id, numberOfPages):
        self.id = id
        self.numberOfPages = numberOfPages
        self.allocatedbit = None
        self.accessbit = None
        self.pages = []

    # returns the number of pages this block owns
    def size(self):
        return self.numberOfPages

    # returns the KBs this block can store
    def KB(self):
        return self.numberOfPages * 4

    # Boolean checker, whether the block was accessed or not ( used by Second chance algorithm )
    def accessed(self):
        if self.accessbit == 1:
            return True
        return False

    # Returns a string showing the pages it has, to show the main memory structure ( part of mainMemory create method )
    def getPages(self):
        pagesList = ""
        for i in self.pages:
            pagesList += str(i) + ", "

        return pagesList[:-2]

    def __str__(self):
        return str(self.id)

    # populates the block with instances of pages
    def populate(self):
        for page in range(self.numberOfPages):
            self.pages += [Page(str(self.id) + "." + str(page))]


class MainMemory:
    def __init__(self):
        # dictionary where keys are the number of pages a block has
        # value is a list of blocks all of which have the same number of pages
        self._free = {2: [], 4: [], 6: [], 8: [], 10: []}

        # round-robin style list, items are appended at the end, and taken out the front
        self._taken = []

    # creates all the necessary instances of blocks building up self._free structure
    def create(self):
        # creates 8 blocks of different predefined sizes
        for block in range(8):
            new_block4 = Block("four." + str(block), 4)
            new_block4.populate()
            self._free[4].append(new_block4)

            new_block6 = Block("six." + str(block), 6)
            new_block6.populate()
            self._free[6].append(new_block6)

            new_block8 = Block("eight." + str(block), 8)
            new_block8.populate()
            self._free[8].append(new_block8)

            new_block10 = Block("ten." + str(block), 10)
            new_block10.populate()
            self._free[10].append(new_block10)

        # creates 16 blocks of 2 pages, this is for increased best fit algorithm precision
        for block in range(16):
            new_block2 = Block("two." + str(block), 2)
            new_block2.populate()
            self._free[2].append(new_block2)

        self.represent()

    # prints all the blocks ( and pages inside the blocks ) that the main memory has
    def represent(self):
        for x in self._free:
            for y in self._free[x]:
                print("block: ", y, " has pages: ", y.getPages())

        print(self)
        print()

    # call issued by kernel allocate method
    # Updates the blocks allocated bit and appends it to the taken list
    def addtoTaken(self, block):
        block.allocatedbit = 1
        self._taken.append(block)

    # issued by the kernel secondChance method
    # Updates the blocks allocated bit and appends it to the free dictionary accordingly
    def addtoFree(self, block):
        block.allocatedbit = 0
        self._free[block.size()].append(block)

    # reports the of free KBs left in the main memory
    def freeKBs(self):
        total = 0
        for k in self._free:
            for block in self._free[k]:
                total += block.KB()
        return total

    # report True if the main memory is almost full, false otherwise
    def filledUp(self):
        if self.freeKBs() <= 30:  # considering 30kbs as already filled up , as i chose process size to be 2KBs - 40KBss
            return True
        return False

    # check how many blocks of a particular size are left
    def freeBlocksofSize(self, size):
        return len(self._free[size])

    # returns a list of free KEYS that can be allocated
    # by keys i mean the block of a certain size
    # if freeblock() returns  [2,6,8] -> this mean that only blocks of size 2, 6 and 8 are available

    def freeBlocks(self):
        free = []
        for k in self._free:
            if len(self._free[k]) > 0:
                free += [k]
        return free

    def __str__(self):
        free = self.freeKBs()
        description = "Main Memory size:  1024KB \tavailable: " + str(free) + "KB"
        return description


class Process:
    # process has, id, the size it will require in KBs
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.blocks = []  # the blocks this process was allocated

    def __str__(self):
        return str(self.id)

    # called by kernel allocate method
    # Process requests a block and is allocated a block
    def allocateBlock(self, block):
        self.blocks += [block]
        # each time it has 70% chance to write to the  block making it accessed
        self.accessTheBlock(block)

    # 70% chance ( chosen arbitrarily ) of a block being accessed by the process
    def accessTheBlock(self, block):
        x = random.randint(1, 10)

        if x <= 7:
            block.accessbit = 1  # update the blocks access bit


class KernelServices:

    def __init__(self):
        # create and populate the main memory
        self.mainMemory = MainMemory()
        self.mainMemory.create()

    # Best fit algorithm , It is asked to allocate blocks to a process
    # it returns a list of blocks sizes e.g
    # [4] , this tells "def allocate" that the process is best fitted for 1 block of 4
    # if memory is scare it might return something like [2,2,2] , meaning 3 blocks of 2.
    def bestFit(self, process):
        # given a process it returns a list of blocks sizes best suited for the process size
        size = process.size

        # turns size into minimum number of pages required
        numPages = math.ceil(size / 4)
        freeBlocks = self.mainMemory.freeBlocks()
        blocks = []
        while numPages > 0:
            # if the requested size is available in perfectly
            if numPages in freeBlocks:
                blocks += [numPages]
                return blocks

            # if the size is greater than or equal to the max block size
            elif numPages >= 10 and 10 in freeBlocks:
                blocks += [10]
                numPages -= 10
            else:
                try:
                    # tries to assign the correct block
                    # examples
                    #y = 4 , if request for 3 pages is made
                    # if request for 7 pages was made, y = 8
                    y = min(filter(lambda x: x > numPages, freeBlocks))
                    numPages -= y
                    blocks += [y]
                except: # this exception occurs when y failed to match a block
                    # this could happen if 7 pages was requested and 10 and 8 sized blocks are taken
                    # in that case any block is added ,as this happens only towards the end, about the last 50KBs or so
                    if self.mainMemory.freeKBs() >= process.size:
                        # to make sure that we are not allocating too many blocks of one size than there are available
                        # for example, to prevent trying to allocate 3 blocks of 2, if we only have 2 blocks of 2
                        if not blocks.count(freeBlocks[0]) > (self.mainMemory.freeBlocksofSize(freeBlocks[0])) + 1:
                            numPages -= freeBlocks[0]
                            blocks += [freeBlocks[0]]
                    else: # safety measure to ensure correct flow of execution
                        return self.secondChance(process.size, process)
        return blocks

    # allocates memory to a process, uses Best fit and Second Chance
    def allocate(self, process):
        # allocate block/s to the process
        print("------- NEW PROCESS REQUESTS BLOCKS --------")
        print("Process ID: ", str(process), "Current: ", self.mainMemory.freeKBs(), "KBs Needed : ", process.size,
              "KBs\n")

        bestFit = []
        if self.mainMemory.freeKBs() < process.size:
            bestFit = self.secondChance(process.size, process)
        else:
        # the array of blocks that the process needs to be allocated based on best fit
            bestFit = self.bestFit(process)

        for i in bestFit:
            blockToBeAllocated = self.mainMemory._free[i].pop() # removes the block from free
            process.allocateBlock(blockToBeAllocated) # allocates the block to a process
            self.mainMemory.addtoTaken(blockToBeAllocated) # adds process to taken list

    # Page replacement algorithm , Second Chance
    # triggered when a process requests memory and the main memory is full
    def secondChance(self, toFree, process):

        print("\n--------- Page replacement ( second chance ) -------------")
        print("Current free Kbs: ", self.mainMemory.freeKBs(), " Need : ", toFree, "Kbs")

        x = 0
        freed = 0

        # frees up enough space to allow the process to be allocated memory
        while freed < toFree:
            # checks if an allocated memory, (round robin style), has been accessed
            if not self.mainMemory._taken[0].accessed():
                # frees up that page
                self.mainMemory.addtoFree(self.mainMemory._taken[0])
                freed += self.mainMemory._taken[0].KB()
                self.mainMemory._taken.pop(0)
                x += 1

            else: # if it has been accessed it is given a second chance
                giveSecondChance = self.mainMemory._taken.pop(0)
                giveSecondChance.accessbit = 0
                self.mainMemory._taken.append(giveSecondChance)

        print(freed, " KBs have been freed, by de-allocating ", x, " block/s\n")

        # allow best fit to give the correct blocks to a process
        return self.bestFit(process)

    # reports if the main memory is full or not
    def full(self):
        return self.mainMemory.filledUp()

    # report information about the main memory
    def info(self):
        return str(self.mainMemory)


#
kernel = KernelServices()

i = 0
processList = []
 # fill up the memory untill its full
while not kernel.full():
    i += 1
    process = Process(str(i), random.randint(2, 50))
    processList += [process]
    # print(process.size)
    kernel.allocate(process)

print()
print(len(processList), " processes have been allocated so far , filling up the memory to about 30KBs remaining")
print()

# add processes to show page replacement algorithm
while True:
    i += 1
    process = Process(str(i), random.randint(2, 50))
    processList += [process]
    # print(process.size)
    time.sleep(1)
    kernel.allocate(process)
