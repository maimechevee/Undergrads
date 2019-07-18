# 

import pandas as pd
import numpy as np

import pickle
from pathlib import Path
data_folder = Path('Z:\\Maxime Chevee\Maxime 3\Analysis\Analysis OptoTagged 20180411')
file_to_open = data_folder / "master_log_lite.pkl"
with open(file_to_open, 'rb') as f:
   master_log = pickle.load(f, encoding='latin1')
   
modified_spike_times = master_log.spike_times - master_log.stim_onset
L=[]
for i in range(0,len(master_log.spike_times)):
    hist = np.histogram(modified_spike_times[i], bins=159, range = (-1,3))[0]
    L.append(hist)
L

# Final code for individual neuron rasters

import pandas as pd
import numpy as np

import pickle
from pathlib import Path
data_folder = Path('Z:\\Maxime Chevee\Maxime 3\Analysis\Analysis OptoTagged 20180411')
file_to_open = data_folder / "master_log_lite.pkl"
with open(file_to_open, 'rb') as f:
   master_log = pickle.load(f, encoding='latin1')

import matplotlib.pyplot as plt
neurons_list = np.unique(master_log[master_log.Category == 'OptoTag'].unit_name)
for k in neurons_list:
    neuron_name = 'Neuron'+' '+k+' '+' Raster Plot'
    selected_neuron = master_log[master_log.unit_name == k]
    modified_spike = selected_neuron.spike_times - selected_neuron.stim_onset
    yvar = selected_neuron.trial_num
    for i in range(0,len(modified_spike)):
        x = modified_spike[modified_spike.index[i]]
        y = np.tile(int(yvar[yvar.index[i]]), len(x))
        plt.scatter(x, y, color = 'salmon', s = 0.5)
    plt.xlim(-1,3)
    plt.axvline(x=0, color = 'black')
    plt.title(neuron_name)
    plt.xlabel('Time (s)')
    plt.ylabel('Trials')
    plt.savefig(neuron_name + '.pdf')
    plt.figure()
    
# 
