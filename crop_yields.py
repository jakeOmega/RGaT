# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 13:41:46 2020

@author: jakef
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

freq = 12
warmup_time = 10 * freq
time = 12000
roll_range = 0.3
kernal = np.array([[0,1,0],[1,0,1],[0,1,0]])/4

state = np.random.uniform(-roll_range, roll_range, (25,25))
rolls = np.random.uniform(-roll_range, roll_range)
state_history = []
for i in range(0, time):
    state_history += [state]
    rolls = np.random.uniform(-roll_range, roll_range, (25,25)) + 0.9 * rolls
    neighbor_avg = convolve(state, kernal, mode='reflect')
    state = 0.99 * neighbor_avg + rolls
    
q = np.array(state_history).flatten()
print(len(np.where((q<-1.5) & (q>-2.5))[0])/len(q))
print(len(np.where(q<-2.5)[0])/len(q))
plt.imshow(state_history[time-1])
plt.show()
plt.scatter(x=[state_history[i][10][10] for i in range(warmup_time, time, freq)], y=[state_history[i][10][11] for i in range(warmup_time, time, freq)])
plt.show()
plt.scatter(x=[state_history[i][10][10] for i in range(warmup_time, time, freq)], y=[state_history[i][10][20] for i in range(warmup_time, time, freq)])
plt.show()
print(np.corrcoef(x=[state_history[i][10][10] for i in range(warmup_time, time, freq)], y=[state_history[i][10][11] for i in range(warmup_time, time, freq)])[0][1])
print(np.corrcoef(x=[state_history[i-freq][10][10] for i in range(warmup_time, time, freq)], y=[state_history[i][10][10] for i in range(warmup_time, time, freq)])[0][1])
print(np.corrcoef(x=[state_history[i-10*freq][10][10] for i in range(warmup_time, time, freq)], y=[state_history[i][10][10] for i in range(warmup_time, time, freq)])[0][1])
print(np.corrcoef(x=[state_history[i][10][10] for i in range(warmup_time, time, freq)], y=[state_history[i][10][20] for i in range(warmup_time, time, freq)])[0][1])