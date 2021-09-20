#!/usr/bin/python3

import sys
import operator

def print_usage():
    print()
    print("Usage:")
    print("./sched.py -f <process information file> -a [FCFS | SJF | RR] [-q <time quantum>]")

print("num args", len(sys.argv))

algorithms = ["FCFS", "SJF", "RR"]

i = 0
filename = ""
algorithm = algorithms[0]
timeq = 10
while i<len(sys.argv):
    curr = sys.argv[i];i+=1
    if curr == "-f":
        filename = sys.argv[i];i+=1
    if curr == "-a":
        algorithm = sys.argv[i];i+=1
    if curr == "-q":
        timeq = sys.argv[i];i+=1

if filename=="" or not algorithm in algorithms:
    print_usage()
    exit(1)

print("Algorithm:",algorithm)

class Process:
    pid=0
    arrival=0
    time_left=0
    time_total_needed=0

    time_at_last_execute=0
    waiting_time=0

    def __init__(self, line):
        vec = line.split(",")
        self.pid = int(vec[0])
        self.arrival = int(vec[1])
        self.time_total_needed = int(vec[2])
        self.time_left = self.time_total_needed

    def __lt__(self, other):
        self.arrival<other.arrival

    def print(self):
        print("PID:", self.pid," Arrival time:", self.arrival,"ms  Time left:", self.time_left) 

    def execute(currentTime, executionTime):
        waiting_time+=currentTime-time_at_last_execute
        time_at_last_execute=currentTime+executionTime
        time_left-=executionTime

processes = []

with open(filename) as file:
    lines = file.readlines()
    for line in lines:
        processes.append(Process(line))


#processes = sorted(processes, key=operator.attrgetter("arrival"))

for process in processes:
    process.print()


