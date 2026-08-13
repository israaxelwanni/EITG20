import heapq

import random

import numpy as np

from queue import Queue

import time



import matplotlib as mpl

mpl.use('tkagg')

import matplotlib.pyplot as plt





MaxM = max(0,int(input('Maximum value of M: ')))

serv = 1

beta = 0.2



while MaxM > 0:

     mu=1/serv

     M =  np.array([i for i in range(1,MaxM)])

     P=np.ones([len(M),4])



     # !!! Här har jag ändrat !!!

     P[:,1] = M  * beta * P[:,0] /mu

     P[:,2] =  (M-1) * beta * P[:,1]/ (2*mu);

     P[:,3] =  (M-2) * beta * P[:,2]/ (3*mu);



     P[P<0] = 0



     P0 = np.zeros(len(M))

     for i in range(len(M)):

         P0[i] = 1/np.sum(P[i,:])





     E = np.zeros(len(M))

     B = np.zeros(len(M))  #blocking probability



     E = P[:,3] * P0   #P3



     B= (M-3) * P[:,3] / (M *P[:,0] + (M-1) * P[:,1] + (M-2) * P[:,2] + (M-3) * P[:,3])





     plt.plot(M,E,'-',M,B,'x')



     plt.grid(True)

     plt.xlabel('Number of customers, M')

     plt.ylabel('Loss probability')

    # added for the labb, exercise 3.1.1
    # E is the probability that the system if full.
    # B is the blocking probability.
     plt.legend([f'E = P(full)', f'B = P(block)']) 

    # exercise 3.1.2:
    # there is only one server, as serv = 1

    # exercise 3.1.3:
    # when the number of customers M is very large, the system is almost always full, so E approaches 1. 
    # The blocking probability B also approaches 1, because almost all arriving customers will be blocked 
    # when the system is full.

     plt.show()



     MaxM=0

