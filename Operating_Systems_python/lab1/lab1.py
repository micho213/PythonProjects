import time
import sched


class Process:
    def __init__(self, id, name, execTime):
        self.id = id
        self.name = name
        self.execTime = execTime
        # self.state = state

    def __str__(self):
        return str(self.name)
class Scheduler:
    def __init__(self):
        self.readyQueue = []
        self.blockedQueue = []
        self.currentlyRunning = [None]
        self.idle = Process("idle" , "idle", 100)
        self.interruptProcess = Process("Interuption","interuption",1)

    def addReadyProcess(self, process):
        self.readyQueue.append(process)
        print("process ' %s ' added to the queue of %d " %(process.name,len(self.readyQueue)))

    def addBlockedProcess(self, process):
        self.blockedQueue.append(process)
        self.runProcess()

    def AddSuspendedProcess(self, process):
        newInterruption =self.interruptProcess
        self.currentlyRunning[0] = newInterruption
        self.readyQueue.insert(0,process)

    def preemptProcess(self, process):
        # take the blocked process from the queue, as the I/O arrives back
        for x in range(self.blockedQueue):
            if self.blockedQueue[x].id == process.id:
                self.readyQueue.append(self.blockedQueue[x])
                self.blockedQueue.pop(x)

    def runProcess(self):
        if len(self.readyQueue) == 0:
            self.currentlyRunning[0] = self.idle
        self.currentlyRunning[0] = self.readyQueue.pop(0)

    def schedule(self):
        if len(self.currentlyRunning) != 0 and self.currentlyRunning[0] != None:
            self.currentlyRunning[0].execTime -= 1
            if self.currentlyRunning[0].execTime != 0:
                self.readyQueue.append(self.currentlyRunning[0])

            self.runProcess()
            print("currently running: %s" % (self.currentlyRunning[0].id) )
        else:
            self.runProcess()
            print("currently running: %s" % (self.currentlyRunning[0].id) )


processA = Process("123","first Process",3)
processB = Process("456","second Process",4)
scheduler = Scheduler()
scheduler.addReadyProcess(processA)
scheduler.addReadyProcess(processB)


timeSlice = sched.scheduler(time.time,time.sleep)
while True:
    timeSlice.enter(2,1,scheduler.schedule,())
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
