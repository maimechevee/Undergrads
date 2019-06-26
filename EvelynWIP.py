# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 12:00:44 2019

@author: Brown Lab
"""

#This is Evelyn's work in progress

#Recreate column '-1to3sec_25msecbins_StimAligned'
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
data_folder = Path('Z:\\Maxime Chevee\Maxime 3\Analysis\Analysis OptoTagged 20180411')
file_to_open = data_folder / "master_log_lite.pkl"
with open(file_to_open, 'rb') as f:
    master_log = pickle.load(f, encoding='latin1')

#Length specific to time interval (-1to3sec25msecbins)
bins_num = int((3-(-1))/(25/1000)-1)
new_col = np.zeros(bins_num)
pos = np.arange(-1,3,0.025)

#Claustrum For-Loop ~183268
#Create empty dictionary to collect all stimulus-aligned columns
#Checking needed
D = {}
for num in range(1,len(master_log.loc[:,'mouse_name'])+1):
    for i in range(0,len(master_log.loc[num,'spike_times'])):
        for j in range(0,bins_num-1):
            if (pos[j] <= float(master_log.loc[num,'spike_times'][i])-float(master_log.loc[num,'stim_onset'])) and (pos[j+1] >= float(master_log.loc[num,'spike_times'][i])-float(master_log.loc[num,'stim_onset'])):
                new_col[j]+=1
    D[str(num)] = new_col
    new_col = np.zeros(bins_num)
C = pd.Series(D)
C


#Claustrum 1
for i in range(0,len(master_log.loc[1,'spike_times'])):
    for j in range(0,bins_num-1):
        if (pos[j] <= float(master_log.loc[1,'spike_times'][i])-float(master_log.loc[1,'stim_onset'])) and (pos[j+1] >= float(master_log.loc[1,'spike_times'][i])-float(master_log.loc[1,'stim_onset'])):
            new_col[j]+=1
C1 = new_col

#Claustrum 2
new_col = np.zeros(bins_num)
for i in range(0,len(master_log.loc[2,'spike_times'])):
    for j in range(0,bins_num-1):
        if (pos[j] <= float(master_log.loc[2,'spike_times'][i])-float(master_log.loc[2,'stim_onset'])) and (pos[j+1] >= float(master_log.loc[2,'spike_times'][i])-float(master_log.loc[2,'stim_onset'])):
            new_col[j]+=1
C2 = new_col

#June 26: Rewrite code for histogram frequency
#Checking needed
#Recreate column '-1to3sec_25msecbins_StimAligned'
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
data_folder = Path('Z:\\Maxime Chevee\Maxime 3\Analysis\Analysis OptoTagged 20180411')
file_to_open = data_folder / "master_log_lite.pkl"
with open(file_to_open, 'rb') as f:
    master_log = pickle.load(f, encoding='latin1')
L = []
for num in range(1, len(master_log.loc[:,'mouse_name'])+1):
    adjusted_spike_times = master_log.loc[num,'spike_times']-float(master_log.loc[num,'stim_onset'])
    histogram = adjusted_spike_times.hist(bins=int((3-(-1))/0.025-1))
    L.append(histogram)
master_log['-1to3sec_25msecbins_StimAligned'] = L

#Draft 2: June 26
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
data_folder = Path('Z:\\Maxime Chevee\Maxime 3\Analysis\Analysis OptoTagged 20180411')
file_to_open = data_folder / "master_log_lite.pkl"
with open(file_to_open, 'rb') as f:
    master_log = pickle.load(f, encoding='latin1')
L=[]
for num in range(1,len(master_log.loc[:,'mouse_name']+1):
                 adjusted_spike_times=master_log.loc[num,'spike_times']-float(master_log.loc[num,'stim_onset'])
                 hist=np.histogram(adjusted_spike_times,bins=int((3-(-1))/0.025-1))
                 L.append(hist)
master_log['-1to3sec_25msecbins_StimAligned']=L
#June 26: Create raster for one neuron
import matplotlib.pyplot as plt
