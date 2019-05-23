import time
import sched


class Process:
    def __init__(self, id, name, execTime,numOfIOs):
        self.id = id
        self.name = name
        self.execTime = execTime
        # self.state = state
        self.numOfIOs = numOfIOs

    def __str__(self):
        return str(self.name)


class Scheduler:
    def __init__(self):
        self.readyQueue = []
        self.blockedQueue = []
        self.currentlyRunning = [None]
        self.idle = Process("idle" , "idle", 100,0)
        self.interruptProcess = Process("Interuption","interuption",1,0)

    def addReadyProcess(self, process):
        self.readyQueue.append(process)
        print("process ' %s ' added to the queue of %d " %(process.name,len(self.readyQueue)))

    def addBlockedProcess(self, process):
        self.blockedQueue.append(process)
        self.currentlyRunning[0] = None
        print("\t\tProcess %s has been blocked due to I/O" %(process.name))
        print("Resuming:")
        self.schedule()
        # time.sleep(0.5)
        self.preemptProcess(process)

    def AddSuspendedProcess(self, process):
        newInterruption =self.interruptProcess
        self.currentlyRunning[0] = newInterruption
        self.readyQueue.insert(0,process)

    def preemptProcess(self, process):
        # take the blocked process from the queue, as the I/O arrives back
        for x in range(len(self.blockedQueue)):
            if self.blockedQueue[x].id == process.id:
                self.addReadyProcess(self.blockedQueue[x])
                self.blockedQueue.pop(x)

    def runProcess(self):
        if len(self.readyQueue) == 0:
            self.currentlyRunning[0] = self.idle
        else:
            self.currentlyRunning[0] = self.readyQueue.pop(0)

    def schedule(self):
        if len(self.currentlyRunning) != 0:
            self.runProcess()
            print("current process running: %s" % (self.currentlyRunning[0].name) )
            # check if process has I/O
            if self.currentlyRunning[0].numOfIOs != 0:
                self.currentlyRunning[0].numOfIOs -=1
                self.addBlockedProcess(self.currentlyRunning[0])
            # reduce the execution time required for the process
            self.currentlyRunning[0].execTime -= 1
            if self.currentlyRunning[0].execTime != 0:
                self.readyQueue.append(self.currentlyRunning[0])




        # first time or resuming after I/O, starting up currentlyRunning == None
        # else:
        #     self.runProcess()
        #     print("current process running: %s" % (self.currentlyRunning[0].name) )


processA = Process("123","A",3,0)
processB = Process("456","B",4,1)
processC = Process("789","C",2,3)
scheduler = Scheduler()
scheduler.addReadyProcess(processA)
scheduler.addReadyProcess(processB)
scheduler.addReadyProcess(processC)


timeSlice = sched.scheduler(time.time,time.sleep)
while True:
    timeSlice.enter(1,1,scheduler.schedule,())
    timeSlice.run()



# scheduler =sched.scheduler(time.time,time.sleep)
#
# def x(name):
#     print ( "EVENT: ", time.time(),name )
#
# print("START: ", time.time() )
# scheduler.enter(2,1,x,("first",))
# scheduler.enter(3,1,x,("second",))
# scheduler.run()