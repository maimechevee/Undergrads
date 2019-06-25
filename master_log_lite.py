#Script used to generate the master_log_lite for Python practice analysis 2090618

#First, load master_log from Master_log_and_ROC.py


import pickle
from pathlib import Path
data_folder = Path('Z:\\Maxime Chevee\Maxime 3\Analysis\Analysis OptoTagged 20180411')
file_to_open = data_folder / "master_log_lite.pkl"
with open(file_to_open, 'rb') as f:
   master_log = pickle.load(f, encoding='latin1')
   
list(master_log)
#master_log_lite=master_log[['mouse_name',
# 'date',
# 'block_type',
# 'trial_type',
# 'touch_stimulus',
# 'vis_stimulus',
# 'response',
# 'trial_num',
# 'stim_onset',
# 'stim_offset',
# 'licks_right',
# 'licks_left',
# 'spike_times',
# 'cluster_name',
# '-0.5to2.0sec_25msecbins_StimAligned',
# 'Category',
# '-1to3sec_25msecbins_StimAligned',
#  'Stim/Block/Response',
# 'Reward',
# 'rewarded_licks',
# 'non_rewarded_licks',
# 'unit_name',
# 'LeftFirstLick',
# 'RightFirstLick',
# 'FirstLick',
# '-1to3sec_25msecbins_LickAligned',
#  'LickALigned_spike_times']]

# 1) Recreate column  '-1to3sec_25msecbins_StimAligned'
# 2) plot a stim aligned raster for one neuron, for each trial type 
