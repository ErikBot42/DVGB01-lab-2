#!/usr/bin/python3

import sys
import operator
import copy

def print_usage():
    print()
    print("Usage:")
    print("./sched.py -f <process information file> -a [FCFS | SJF | RR] [-q <time quantum>]")

#print("num args", len(sys.argv))

algorithms = ["FCFS", "SJF", "RR"]

i = 0
filename = ""
algorithm = algorithms[0]
timeq = 5
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

class Process:
    pid=0
    arrival=0
    time_left=0
    time_total_needed=0

    time_at_last_execute=0 # when last wait started
    waiting_time=0

    start_time=-1

    def turnAroundTime(self):
        return self.time_at_last_execute-self.start_time

    def __init__(self, line):
        vec = line.split(",")
        self.pid = int(vec[0])
        self.arrival = int(vec[1])
        self.time_total_needed = int(vec[2])
        self.time_left = self.time_total_needed
        self.time_at_last_execute = self.arrival

    def print(self):
        print("PID:", self.pid," Arrival time:", self.arrival,"ms  Time left:", self.time_left,"/",self.time_total_needed,"ms") 
        print("    Waiting time:", self.waiting_time,"ms Turaround time:", self.turnAroundTime()) 

    def execute(self, currentTime, executionTime):
        self.waiting_time+=currentTime-self.time_at_last_execute
        self.time_at_last_execute=currentTime+executionTime
        self.time_left-=executionTime
        if self.start_time < 0:
            self.start_time = currentTime

        print("Running PID:", self.pid,"for",executionTime,"ms  at time",currentTime)

processes = []



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
        process.execute(currentTime, executionTime)
        currentTime+=executionTime
elif algorithm == "SJF":
    byBurstTime = sorted(processes, key=operator.attrgetter("time_total_needed"))
    for process in byBurstTime:
        executionTime = process.time_left
        process.execute(currentTime, executionTime)
        currentTime+=executionTime
elif algorithm == "RR":
    processSet = copy.copy(processes)
    while len(processSet)>0:
        for process in processSet:
            executionTime = min(timeq,process.time_left)
            process.execute(currentTime, executionTime)
            currentTime+=executionTime

        processSet = [p for p in processSet if p.time_left>0]

print("-------------------")
for process in processes:
    process.print()
print("-------------------")

sum_wait_time=0
sum_turnaround_time=0
for process in processes:
    sum_wait_time+=process.waiting_time
    sum_turnaround_time+=process.turnAroundTime()

print("Average wait", float(sum_wait_time)/len(processes), "Average turnaround", float(sum_turnaround_time)/len(processes))


