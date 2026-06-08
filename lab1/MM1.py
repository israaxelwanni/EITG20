import heapq
import random
import matplotlib.pyplot as plt
import numpy as np
from queue import Queue

import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plt

signalList = []
def send(signalType, evTime, destination, info):
    heapq.heappush(signalList, (evTime, signalType, destination, info))

GENERATE = 1
ARRIVAL = 2
MEASUREMENT = 3
DEPARTURE = 4

simTime = 0.0
stopTime = 10000.0 
# 3.7
# stopTime = 50.0 # 50 simulated seconds
# stopTime = 3000.0 # 3000 simulated seconds
# 3.8
stopTime = 1000.0


class larger():
    def __gt__(self, other):
        return False

class generator(larger):
    def __init__(self, sendTo,lmbda):
        self.sendTo = sendTo
        self.lmbda = lmbda
        self.arrivalTimes = []
    def arrivalTime(self):
        return simTime + random.expovariate(self.lmbda)
    def treatSignal(self, x, info):
        if x == GENERATE:
            send(ARRIVAL, simTime, self.sendTo, simTime)  #Send new cusomer to queue
            send(GENERATE, self.arrivalTime(), self, [])  #Schedule next arrival
            self.arrivalTimes.append(simTime)


class queue(larger):
    def __init__(self, mu, sendTo):
        self.numberInQueue = 0
        self.sumMeasurements = 0
        self.numberOfMeasurements = 0
        self.measuredValues = []
        self.buffer = Queue(maxsize=7)
        self.mu = mu 
        self.sendTo = sendTo
        self.numberarrived = 0
        self.numberblocked = 0
    # M/M/1
    def serviceTime(self):
        return simTime + random.expovariate(self.mu) 
    # M/U/1
    # def serviceTime(self):
    #     return simTime + random.uniform(0, 2*(1/self.mu)) 
    # M/D/1
    # def serviceTime(self):
    #     return simTime + 1/self.mu 
    # M/H^2/1
    # def serviceTime(self):
    #     if random.random() < 0.25:
    #         return simTime + random.expovariate(2*100) 
    #     else:
    #         return simTime + random.expovariate(0.5*(1/0.13))
    def treatSignal(self, x, info):
        if x == ARRIVAL:
            self.numberarrived = self.numberarrived + 1
            if self.buffer.full(): 
                self.numberblocked += 1
            else: 
                if self.numberInQueue == 0:
                    send(DEPARTURE,self.serviceTime() , self, []) #Schedule  a departure for the arrival customer if queue is empty
                self.numberInQueue = self.numberInQueue + 1
                self.buffer.put(info)
        elif x == DEPARTURE:
            self.numberInQueue = self.numberInQueue - 1
            if self.numberInQueue > 0:
                send(DEPARTURE, self.serviceTime(), self, [])  # Schedule  a departure for next customer in queue
            send(ARRIVAL, simTime, self.sendTo, self.buffer.get())
        elif x == MEASUREMENT:
            self.measuredValues.append(self.numberInQueue)
            self.sumMeasurements = self.sumMeasurements + self.numberInQueue
            self.numberOfMeasurements = self.numberOfMeasurements + 1
            send(MEASUREMENT, simTime + random.expovariate(1), self, [])



class sink(larger):
    def __init__(self):
        self.numberArrived = 0
        self.departureTimes = []
        self.totalTime = 0
        self.T = []
    def treatSignal(self, x, info):
        self.numberArrived = self.numberArrived + 1
        self.departureTimes.append(info)
        self.totalTime = self.totalTime + simTime - info
        self.T.append(simTime - info)

          
  ###################################################
  #
  # Add code to create a queuing system  here
  #
  ###################################################

## 4.1
s = sink()
q = queue(mu = 10, sendTo=s)
gen = generator(lmbda = 7, sendTo=q)

send(GENERATE, 0, gen, [])
send(MEASUREMENT, 1, q, [])

while simTime < stopTime:
    [simTime, signalType, dest, info] = heapq.heappop(signalList)
    dest.treatSignal(signalType, info)

# 5.2
block_prob = q.numberblocked / q.numberarrived
print('Blocking probability: ', block_prob)

# 5.3
# number of times the system is full
fullCount = q.measuredValues.count(7)
# number of times the system is full / number of messurments = probability that the system is full
full_prob = fullCount/len(q.measuredValues)
print(f"Probability system is full: {full_prob}")
a = list(range(0, 8))
plt.hist(q.measuredValues, density=True, bins=a)
plt.xlabel('Number in system')
plt.ylabel('Estimated steady-state probability')
plt.title('Steady-state distribution of queue length')
plt.show()

# 3.3
# print('Mean number in queue: ', np.mean(q.measuredValues))
# print('Mean time in queue: ', np.mean(s.T))

# 3.9
# gen = generator(lmbda = 11, sendTo = q)
# gen = generator(lmbda = 7, sendTo = q)

# 3.12
# gen = generator(lmbda = 2.5, sendTo = q)
# gen = generator(lmbda = 9, sendTo = q)

# send(GENERATE, 0, gen, [])
# send(MEASUREMENT, 1, q, [])

# while simTime < stopTime:
#     [simTime, signalType, dest, info] = heapq.heappop(signalList)
#     dest.treatSignal(signalType, info)

# # 3.12
# plt.scatter(s.T[2:101], s.T[1:100])
# plt.show()

# 3.11
# append mean response time for each lambda to T
# T = []
# for lmbda in [2.5, 5, 7, 9, 10, 11]:
#     gen = generator(lmbda = lmbda, sendTo = q)

#     signalList.clear()
#     simTime = 0

#     send(GENERATE, 0, gen, [])
#     send(MEASUREMENT, 1, q, [])

#     while simTime < stopTime:
#         [simTime, signalType, dest, info] = heapq.heappop(signalList)
#         dest.treatSignal(signalType, info)
#     # 3.10
#     print(f"lambda: {gen.lmbda}, mu: {q.mu}, T: {np.mean(s.T)}")

#     T.append(np.mean(s.T))

# # 3.11
# # Plot the mean response time, T , for the investigated ρ-values
# plt.plot(T, marker = '*')
# plt.xlabel('Time')
# plt.ylabel('Response Time')
# plt.title(f'MM1 Queueing System with lambdas = {[2.5, 5, 7, 9, 10, 11]} and mu = {q.mu}')
# plt.show()



  ###################################################
  #
  # Add code to print final result
  #
  ###################################################

# # 3.1 
# plot the number of jobs in the system at the
# instant of a measurement even
# plt.plot(q.measuredValues)
# plt.xlabel('Time')
# plt.ylabel('Number of Customers in Queue')
# plt.title('MM1 Queueing System')
# plt.show()

# #3.2 
# # Calculate the average number of jobs in the system, E[N ], 
# # from the simulation results.
# average_jobs = np.mean(q.measuredValues)
# print(f"Average number of jobs in the system: {average_jobs}")


# #3.4
# # Make a histogram over the obtained measurements for N 
# # What does the histogram show?
# # answer: The histogram shows a distribution of the number of 
# # calls in the system at a given measurement instance. 
# #3.5
# # normalize the histogram
# # same as previous only with density = True
# a = list(range(0, 15))
# # 3.4
# # plt.hist(q.measuredValues, density=False, bins=a)
# # 3.5
# from pkMM1 import pk
# plt.hist(q.measuredValues, density=True, bins=a)
# # 3.6
# # Plot the steady state distribution in the same diagram as the histogram
# # how have they been obtained?
# # answer: it plots the steady state distribution of the number of calls 
# # in the system, calculated using pk from pkMM1. 
# plt.plot(pk)
# plt.xlabel('Number of Customers in Queue')
# plt.ylabel('Density')
# plt.title('Histogram of Jobs in MM1 Queueing System')
# plt.show()

# 3.8
# Calculate the mean response time, T 
# T = np.mean(s.T)
# print(f"Mean response time: {T}")

# 3.9
# Plot the number of jobs at the instant of a measurement of different lambda
# plt.plot(q.measuredValues) # lambda changed with gen
# plt.xlabel('Time')
# plt.ylabel('mean number of jobs in the system')
# plt.title(f'MM1 Queueing System with lambda = {gen.lmbda}')
# plt.show()
