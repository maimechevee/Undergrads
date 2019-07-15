# This is Sakshi's draft

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