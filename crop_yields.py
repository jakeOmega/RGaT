# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 13:41:46 2020

@author: jakef
"""
import numpy as np
import matplotlib.pyplot as plt
from itertools import groupby

freq = 12
warmup_time = 10 * freq
time = 12000
roll_range = 0.10

f = open("F:\\Libraries\\Documents\\Paradox Interactive\\Imperator\\mod\\Realistic_Growth\\debug.log")
lines_neighbors = [line.split(':')[7] for line in f.readlines() if ("Region neighbors" in line)]
adj_dict = {}
for line in lines_neighbors:
    _, first, second = line.strip().split('-')
    first, second = first.strip(), second.strip()
    if first not in adj_dict.keys():
        adj_dict[first] = [second]
    if second not in adj_dict.keys():
        adj_dict[second] = [first]
    if second not in adj_dict[first]:
        adj_dict[first] += [second]
    if first not in adj_dict[second]:
        adj_dict[second] += [first]

state = {}
for prov in adj_dict.keys():
    state[prov] = 0
roll = {}
for prov in adj_dict.keys():
    roll[prov] = 0
state_history = []
for i in range(0, time):
    state_history += [state]
    next_state = {}
    for prov in adj_dict.keys():
        roll[prov] = 0.996 * roll[prov] + np.random.uniform(-roll_range, roll_range)
        neighbor_count = 0
        neighbor_sum = 0
        for neighbor in adj_dict[prov]:
            neighbor_count += 1
            neighbor_sum += state[neighbor]
        next_state[prov] = 0.8 * neighbor_sum/neighbor_count + roll[prov]
    state = next_state
    
q = np.array([list(state_history[i].values()) for i in range(0, len(state_history), freq)]).flatten()
print(len(np.where((q<0.5) & (q>-0.5))[0])/len(q))
print(len(np.where((q<-0.5) & (q>-1.5))[0])/len(q))
print(len(np.where((q<-1.5) & (q>-2.5))[0])/len(q))
print(len(np.where(q<-2.5)[0])/len(q))
print(len([1 for q in state_history if np.quantile(list(q.values()), 0.95) < 2.5 and np.quantile(list(q.values()), 0.05) > -2.5])/time)
plt.scatter(x=[state_history[i]['Alalia'] for i in range(warmup_time, time, freq)], y=[state_history[i]['Qapara'] for i in range(warmup_time, time, freq)])
plt.show()
plt.scatter(x=[state_history[i]['Alalia'] for i in range(warmup_time, time, freq)], y=[state_history[i]['Qapara'] for i in range(warmup_time, time, freq)])
plt.xlim(-0.5, 0.5)
plt.show()
plt.scatter(x=[state_history[i]['Alalia'] for i in range(warmup_time, time, freq)], y=[state_history[i]['Gujjar'] for i in range(warmup_time, time, freq)])
plt.show()
plt.hist(q, bins = [x/4 + 0.5 for x in range(-16, 15)], density=True)
plt.show()
print('neighbor corr: ', np.corrcoef(x=[state_history[i]['Alalia'] for i in range(warmup_time, time, freq)], y=[state_history[i]['Qapara'] for i in range(warmup_time, time, freq)])[0][1])
print('1 year autocorrelation: ', np.corrcoef(x=[state_history[i-freq]['Alalia'] for i in range(warmup_time, time, freq)], y=[state_history[i]['Alalia'] for i in range(warmup_time, time, freq)])[0][1])
print('10 year autocorrelation: ', np.corrcoef(x=[state_history[i-10*freq]['Alalia'] for i in range(warmup_time, time, freq)], y=[state_history[i]['Alalia'] for i in range(warmup_time, time, freq)])[0][1])
print('distant region corr: ', np.corrcoef(x=[state_history[i]['Alalia'] for i in range(warmup_time, time, freq)], y=[state_history[i]['Gujjar'] for i in range(warmup_time, time, freq)])[0][1])

famine = q < -2.5
famine_lengths = [sum(1 for x in v if x) for k,v in groupby(famine)]
famine_lengths = [x for x in famine_lengths if x > 0]
plt.hist(famine_lengths, bins = [i for i in range(1, 21)], density=True)
plt.show()

bad_times = q < -0.5
bad_times_lengths = [sum(1 for x in v if x) for k,v in groupby(bad_times)]
bad_times_lengths = [x for x in bad_times_lengths if x > 0]
plt.hist(bad_times_lengths, bins = [i for i in range(1, 21)], density=True)
plt.show()