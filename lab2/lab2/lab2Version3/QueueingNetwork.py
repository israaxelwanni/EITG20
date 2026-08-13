import heapq
import random
import numpy as np
from queue import Queue

signalList = []

def send(signalType, evTime, destination, info):
    heapq.heappush(signalList, (evTime, signalType, destination, info))

GENERATE = 1
ARRIVAL = 2
MEASUREMENT = 3
DEPARTURE = 4

simTime = 0.0
# stopTime = 100000.0
# stopTime = 1000000.0
stopTime = 1000.0
        

class larger():
    def __gt__(self, other):
        return False


class generator(larger):
    def __init__(self, lambda1):
        self.lambda1 = lambda1
        send(GENERATE, self.arrivalTime(), self, None)
    def arrivalTime(self):
        return simTime + random.expovariate(self.lambda1)
    def treatSignal(self, x, info):
        if x == GENERATE:
            send(ARRIVAL, simTime, sendTo(self), simTime)
            send(GENERATE, self.arrivalTime(), self, None)



class queue(larger):
    # Added code for Home assignment exercise 5
    def __init__(self, mu):
        self.measuredValues = []
        self.buffer = Queue(maxsize=0)
        self.mu = mu 
        self.Nq = [] # added list to save nbr customers in queue
        self.Ts = [] # added list to save service times
        send(MEASUREMENT, simTime + random.expovariate(1), self, None)
    def serviceTime(self):
        # return simTime + random.expovariate(self.mu)
        # st = random.expovariate(self.mu)
        
        # st = 1/self.mu # change for exercise 4.1.1

        ## exercise 4.1.2 ##
        alpha = 1/1.5
        mu_1 = self.mu * 2
        mu_2 = self.mu /2
        if random.random() < alpha:
            st = random.expovariate(mu_1)
        else:
            st = random.expovariate(mu_2)
        ## exercise 4.1.2 ##
        
        self.Ts.append(st) # save service time 
        return simTime + st
    def treatSignal(self, x, info):
        if x == ARRIVAL: 
            if self.buffer.empty():
                send(DEPARTURE, self.serviceTime(), self, None) 
            self.buffer.put(info)
        elif x == DEPARTURE:
            tid = self.buffer.get()
            send(ARRIVAL, simTime, sendTo(self), tid)
            if not self.buffer.empty():
                send(DEPARTURE,  self.serviceTime(), self, None)  
        elif x == MEASUREMENT:
            # self.measuredValues.append(self.buffer.qsize())
            # send(MEASUREMENT, simTime + random.expovariate(1), self, [])
            n = self.buffer.qsize()
            self.measuredValues.append(n) # customers in system
            # self.Nq.append(n) # customers in queue
            if n > 0 :
                self.Nq.append(n - 1)     # one customer is being served
            else:
                self.Nq.append(n)         # no customers in system, so no customers in queue
            send(MEASUREMENT, simTime + random.expovariate(1), self, None)

            
class sink(larger):
    def __init__(self):
        self.T = [] 
    def treatSignal(self, x, info):
        self.T.append(simTime - info)

# Below the queueing network is set up. 

# A vector where q[i] is node i is created. The first position in the list is not 
# used so that q[i] correspondst to node number i, for convenience.  
q = [None, queue(10), queue(14), queue(22), queue(9), queue(11)] 

# Sinks and generators are created.
sink1 = sink()
sink2 = sink()
gen1 = generator(7.5)
gen2 = generator(10)
# gen2 = generator(12) # changed for exercise 4.0.3

# The function sendTo(source) gives the routing in the queueing network
def sendTo(source):
    if source == q[1]:
        return q[3]
    elif source == q[2]:
        return q[3]
    elif source == q[3]:
        if random.random() < 0.4:
            return q[4]
        else:
            return q[5]
    elif source == q[4]:
        return sink1
    elif source == q[5]:
        return sink2
    elif source == gen1:
        return q[1]
    elif source == gen2:
        return q[2]


# The main simulation loop
while simTime < stopTime:
    [simTime, signalType, dest, info] = heapq.heappop(signalList)
    dest.treatSignal(signalType, info)

# The mean number of customers in each node i printed:  
print('Mean number of customers in each node: ')
for i in range(1,6):
    print(i, ': ', np.mean(q[i].measuredValues))
    

print('Result from home assignment exercise 5 (and 6):')
print('Mean number of customers in buffer and mean service time for each node: ')
for i in range(1,6):
    print(f"Node {i}:")
    print("  E[Nq] =", np.mean(q[i].Nq))
    print("  E[Ts] =", np.mean(q[i].Ts))

#E[N1q] ≈ 1,85 and E[N3q] ≈ 3,30 
# E(T3s) ≈ 0,046 and E(T4s) ≈ 0,11 (the numbers are slightly of however they are around what we want)

### verifying little's theorem: exercise 4.0.2 ###
### for exercise 4.0.3, we changed the generator(10), to generator(12), for gen2
# find W, the average time a customer spends in the system
T_all = sink1.T + sink2.T
E_T = np.mean(T_all)

print()
print("Mean time in system =", E_T)

# find lambda_eff, the effective arrival rate to the system
lambda_eff = len(T_all) / simTime
print("Effective arrival rate =", lambda_eff)
print()

# find L, the average number of customers in the system
L_sim = sum([np.mean(q[i].measuredValues) for i in range(1,6)])
print(f"lambda_eff * E_T = {lambda_eff * E_T}")
print(f"L_sim = {L_sim}")
print("Little's theorem holds approximately, as lambda_eff * E_T is close to L_sim")

