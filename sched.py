#!/usr/bin/python3


import sys
import operator
import copy

def print_usage():
    print()
    print("Usage:")
    print("./sched.py -f <process information file> -a [FCFS | SJF | RR] [-q <time quantum>]")

algorithms = ["FCFS", "SJF", "RR"]

# read CLI arguments
filename = ""
algorithm = algorithms[0]
timeq = 5
i = 0
while i<len(sys.argv):
    curr = sys.argv[i];i+=1
    if curr == "-f":
        filename = sys.argv[i];i+=1
    if curr == "-a":
        algorithm = sys.argv[i];i+=1
    if curr == "-q":
        timeq = int(sys.argv[i]);i+=1

if filename=="" or not algorithm in algorithms:
    print_usage()
    exit(1)

print("-------------------")
print("Algorithm:",algorithm)
print("Time quanta:",timeq)
print("-------------------")

# waiting time = turnaround - execute time

# pad number
def num_format(number):
    return '{0: <2}'.format(str(number))

class Process:
    pid=0
    arrival=0
    time_left=0
    time_total_needed=0
   
    time_at_done=0 # time at last stopped processing
    waiting_time=0

    # turnaround = from arrival to done
    def turnAroundTime(self):
        return self.time_at_done-self.arrival

    def __init__(self, line):
        vec = line.split(",")
        self.pid = int(vec[0]) # input file is pid, arrival, time needed
        self.arrival = int(vec[1])
        self.time_total_needed = int(vec[2])
        self.time_left = self.time_total_needed
        self.time_at_done = self.arrival

    def print(self):
        RED = '\033[91m'
        BOLD = '\033[1m'
        END = '\033[0m'
        print("PID:", num_format(self.pid)," Arrival time:", num_format(self.arrival),"ms  Time left:", num_format(self.time_left),"/",num_format(self.time_total_needed),"ms") 
        print(BOLD,"    Waiting time:",RED, num_format(self.waiting_time),"ms",END,BOLD,"Turaround time:",RED, num_format(self.turnAroundTime()),"ms",END) 
        print()

    def execute(self, currentTime, executionTime):
        self.waiting_time+=currentTime-self.time_at_done
        self.time_at_done=currentTime+executionTime
        self.time_left-=executionTime

        print("Running PID:", self.pid,"for",executionTime,"ms  at time",currentTime)

processes = []

def process_wait(targetTime, currentTime):
    time = targetTime-currentTime
    print("Waiting until", targetTime, "ms  for", time, "ms  at time",currentTime)
    return time+currentTime

def too_late(process):
    print("PID", process.pid,"arrived too late to be run")

# read file to process objects
with open(filename) as file:
    lines = file.readlines()
    for line in lines:
        processes.append(Process(line))

# processes should be sorted by arrival time.
processes = sorted(processes, key=operator.attrgetter("arrival"))

# Execute algorithm:
currentTime = 0
if algorithm == "FCFS":
    byArrivalTime= sorted(processes, key=operator.attrgetter("arrival"))
    for process in byArrivalTime:
        executionTime = process.time_left
        if process.arrival>currentTime:
            currentTime = process_wait(process.arrival, currentTime)
        process.execute(currentTime, executionTime)
        currentTime+=executionTime

elif algorithm == "SJF":
    byBurstTime = sorted(processes, key=operator.attrgetter("time_total_needed"))
    processSet = copy.copy(byBurstTime)
    while len(processSet)>0:
        for process in processSet:
            if process.arrival>currentTime:
                too_late(process)
            else:
                executionTime = process.time_left
                process.execute(currentTime, executionTime)
                currentTime+=executionTime
                break
        processSet = [p for p in processSet if p.time_left>0]

elif algorithm == "RR":
    processSet = copy.copy(processes)
    while len(processSet)>0:
        for process in processSet:
            if process.arrival>currentTime:
                continue
            executionTime = min(timeq,process.time_left)
            process.execute(currentTime, executionTime)
            currentTime+=executionTime

        processSet = [p for p in processSet if p.time_left>0]

print("-------------------")
print()
for process in processes:
    process.print()
print("-------------------")

# calc average and print averages
sum_wait_time=0
sum_turnaround_time=0
for process in processes:
    sum_wait_time+=process.waiting_time
    sum_turnaround_time+=process.turnAroundTime()

print("Average wait", float(sum_wait_time)/len(processes), "Average turnaround", float(sum_turnaround_time)/len(processes))


