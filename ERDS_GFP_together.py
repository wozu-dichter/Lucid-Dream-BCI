#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 16:48:42 2020

@author: caghangir
"""

import numpy as np
import matplotlib.pyplot as plt
import mne
from mne.datasets import eegbci
from mne.io import concatenate_raws, read_raw_edf
from mne.time_frequency import tfr_multitaper
from mne.stats import permutation_cluster_1samp_test as pcluster_test
from mne.viz.utils import center_cmap
from mne.preprocessing import ICA
from mne.channels import make_standard_montage
import extremeEEGSignalAnalyzer as chetto_EEG
chetto_EEG = chetto_EEG.extremeEEGSignalAnalyzer()
from mne.preprocessing import  (ICA, create_eog_epochs, create_ecg_epochs, corrmap)
from mne.stats import bootstrap_confidence_interval
from mne.baseline import rescale
from lspopt.lsp import spectrogram_lspopt
from mne.stats import permutation_cluster_1samp_test as pcluster_test
from matplotlib.colors import LinearSegmentedColormap
from mne.viz.utils import center_cmap

# %matplotlib qt #plot in new window
#%% =========== Mapping ===========
mapping = {
    'Fc5.': 'FC5', 'Fc3.': 'FC3', 'Fc1.': 'FC1', 'Fcz.': 'FCz', 'Fc2.': 'FC2',
    'Fc4.': 'FC4', 'Fc6.': 'FC6', 'C5..': 'C5', 'C3..': 'C3', 'C1..': 'C1',
    'Cz..': 'Cz', 'C2..': 'C2', 'C4..': 'C4', 'C6..': 'C6', 'Cp5.': 'CP5',
    'Cp3.': 'CP3', 'Cp1.': 'CP1', 'Cpz.': 'CPz', 'Cp2.': 'CP2', 'Cp4.': 'CP4',
    'Cp6.': 'CP6', 'Fp1.': 'Fp1', 'Fpz.': 'Fpz', 'Fp2.': 'Fp2', 'Af7.': 'AF7',
    'Af3.': 'AF3', 'Afz.': 'AFz', 'Af4.': 'AF4', 'Af8.': 'AF8', 'F7..': 'F7',
    'F5..': 'F5', 'F3..': 'F3', 'F1..': 'F1', 'Fz..': 'Fz', 'F2..': 'F2',
    'F4..': 'F4', 'F6..': 'F6', 'F8..': 'F8', 'Ft7.': 'FT7', 'Ft8.': 'FT8',
    'T7..': 'T7', 'T8..': 'T8', 'T9..': 'T9', 'T10.': 'T10', 'Tp7.': 'TP7',
    'Tp8.': 'TP8', 'P7..': 'P7', 'P5..': 'P5', 'P3..': 'P3', 'P1..': 'P1',
    'Pz..': 'Pz', 'P2..': 'P2', 'P4..': 'P4', 'P6..': 'P6', 'P8..': 'P8',
    'Po7.': 'PO7', 'Po3.': 'PO3', 'Poz.': 'POz', 'Po4.': 'PO4', 'Po8.': 'PO8',
    'O1..': 'O1', 'Oz..': 'Oz', 'O2..': 'O2', 'Iz..': 'Iz'
}

#%% ========== Load and Preprocess ======
subject = 1  # use data from subject 1
# runs_imagery = [4, 8, 12]  # motor imagery: left vs. right hand
runs_action = [3, 7, 11]  # motor action: left vs. right hand

fnames = eegbci.load_data(subject, runs_action)
raws = [read_raw_edf(f, preload=True) for f in fnames]
raw = concatenate_raws(raws)

raw.rename_channels(mapping)
raw.set_montage('standard_1005')

raw.rename_channels(lambda x: x.strip('.'))  # remove dots from channel names

events_actions, _ = mne.events_from_annotations(raw, event_id=dict(T1=2, T2=3))
events_rest, _ = mne.events_from_annotations(raw, event_id=dict(T0=1))
events_all, _ = mne.events_from_annotations(raw, event_id=dict(T0=1, T1=2, T2=3))

#%% ============== Preprocess =================
# raw.filter(l_freq=0.1)

ica = ICA(n_components=30, random_state=97)
ica.fit(raw)
eog_inds, eog_scores = ica.find_bads_eog(raw, ch_name='Fp1')
# ica.plot_sources(raw) #delete 1st one
ica.exclude = [0]

ica.apply(raw)

# selected_channels = ["C3", "Cz", "C4"]
# selected_channels = ["C5", "C3", "C1", "Cz", "C2", "C4", "C6"]
selected_channels = ["FC5", "FC3", "FC1", "FCz", "FC2", "FC4", "FC6", "C5", "C3", "C1", "Cz", "C2", "C4", "C6",\
                      "CP5", "CP3", "CP1", "CPz", "CP2", "CP4", "CP6"]
raw.pick_channels(selected_channels)

raw._data = raw._data[:,0:8000]
raw._times = raw._times[0:8000]

raw_data = raw.get_data()
#%% ======== Non-epoching MNE ========
event_id = {'Whole_data':0}
events =  np.zeros(shape=(1,3)).astype(int)

time_second = np.size(raw.get_data(),1) / raw.info['sfreq'] - 1 / raw.info['sfreq']

#Deletion
raw.del_proj()
raw.set_annotations(None)

epochs = mne.Epochs(raw, events, event_id, tmin=0., tmax=time_second, baseline=None, preload=True, reject=None, \
                    reject_by_annotation=None)
    
print(epochs.drop_log)
#%% ================== Permutation Cluster Preparation Among Non-averaged Channel ERDS Maps =====================
freqs = np.arange(2, 36, 0.1)  # frequencies from 2-35Hz
n_cycles = freqs  # use constant t/f resolution
vmin, vmax = -1, 1.5  # set min and max ERDS values in plot
baseline_period = 672 / raw.info['sfreq'] #second
kwargs = dict(n_permutations=100, step_down_p=0.05, seed=1, buffer_size=100, out_type='mask', n_jobs=8)  # for cluster test
cmap = center_cmap(plt.cm.Reds, vmin=vmin, vmax=vmax)  # zero maps to white

#%% ========== Focus to ERD ==========
#best combination
n_cycles = freqs * 2  # use constant t/f resolution
power = tfr_multitaper(epochs, freqs=freqs, n_cycles=n_cycles, use_fft=True, return_itc=False, time_bandwidth = 8.0, decim=2)
power_data = power._data
baseline_period = 672 / epochs.info['sfreq'] #second
power.apply_baseline([0, baseline_period], mode='percent')

#%%======= Focus to ERD ==========
power_data = power._data

# power_data = power_data[:,:,0:4000]
# power.times = power.times[0:4000]

power_data[power_data > 0] = 0
power_data[power_data < 0] *= -1 
power._data = power_data
#%% ======== Permutation Clustering by Windowing Power Spectrogram for Memory Saving ===========
window_size = int(epochs.info['sfreq'] * 5)
window_amount = int(np.size(power_data,2) / window_size) #1 minute data

total_mask = np.zeros((np.size(power_data,1),np.size(power_data,2)), dtype=bool)
for i in range(window_amount):
    # positive clusters
    _, c1, p1, _ = pcluster_test(power_data[:,:,i*window_size:(i+1)*window_size], tail=1, **kwargs)
    # negative clusters
    # _, c2, p2, _ = pcluster_test(power_data[:,:,i*window_size:(i+1)*window_size], tail=-1, **kwargs)

    # c = np.stack(c1 + c2, axis=2)  # combined clusters
    c = np.stack(c1, axis=2)
    # p = np.concatenate((p1, p2))  # combined p-values

    mask = c[..., p1 <= 0.01].any(axis=-1)
    print(np.sum(mask))
    total_mask[:,i*window_size:(i+1)*window_size] = mask
#%%averaging 
avg_power = np.mean(power._data, 0)
power._data = np.expand_dims(avg_power, axis=0) #expand dimension from axis=0 [1,x,y]
#%% =============== ERD Plotting ==============
freq_thesholds = np.array([4,8,12,30])

fig, ax = plt.subplots(1, 2, figsize=(12, 4), gridspec_kw={"width_ratios": [10, 1]})
power.plot([0], vmin=np.min(avg_power), vmax=np.max(avg_power), cmap=(cmap, False), axes=ax[0], colorbar=False, show=False)

ax[0].axvline(0, linewidth=1, color="black", linestyle=":")  # event
ax[0].vlines(x=events_actions[:,0]/160, ymin=0, ymax=36, colors='purple', ls='--', lw=3, label='Action Onsets')
ax[0].hlines(y=freq_thesholds, xmin=0, xmax=time_second, colors='black', ls='--', lw=3, label='Brain waves')
ax[0].legend(fontsize=15)
fig.colorbar(ax[0].images[-1], cax=ax[-1])

ax[0].text(-13,3, 'Delta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,6, 'Theta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,10, 'Alpha', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,24, 'Beta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,33, 'Gamma', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')

# ax[0].set_xlim(0, 100)
plt.title('ERD Color Spectrum', fontsize=13)
plt.suptitle("Average Multitaper Spectrogram of Central 21 Channels", fontsize=20)
fig.show()
#%% =============== ERD Plotting with Permutation Cluster ==============
freq_thesholds = np.array([4,8,12,30])

fig, ax = plt.subplots(1, 2, figsize=(12, 4), gridspec_kw={"width_ratios": [10, 1]})
power.plot([0], vmin=np.min(avg_power), vmax=np.max(avg_power), cmap=(cmap, False), axes=ax[0], colorbar=False, show=False, mask=total_mask, mask_style="mask")

ax[0].axvline(0, linewidth=1, color="black", linestyle=":")  # event
ax[0].vlines(x=events_actions[:,0]/160, ymin=0, ymax=36, colors='purple', ls='--', lw=3, label='Action Onsets')
ax[0].hlines(y=freq_thesholds, xmin=0, xmax=time_second, colors='black', ls='--', lw=3, label='Brain waves')
ax[0].legend(fontsize=15)
fig.colorbar(ax[0].images[-1], cax=ax[-1])

ax[0].text(-13,3, 'Delta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,6, 'Theta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,10, 'Alpha', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,24, 'Beta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,33, 'Gamma', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')

# ax[0].set_xlim(0, 100)
plt.title('ERD Color Spectrum', fontsize=13)
plt.suptitle("ERD Permutation Clustered Multitaper Spectrogram Among Central 21 Channels", fontsize=20)
fig.show()
#%% ========== ERD Relative Difference Envelope ===========
# erd_rel_diff = np.zeros(np.size(avg_power, axis=1))
# for i in range(len(erd_rel_diff)-1):
#     erd_rel_diff[i+1] = np.sum(avg_power[:,i+1]) - np.sum(avg_power[:,i])

# plt.figure()
# plt.plot(erd_rel_diff)
# plt.title('ERD Relative Difference From Neighbour')
#%% ========== GFP ==============
time_second = np.size(raw.get_data(),1) / raw.info['sfreq']

iter_freqs = [
            ('Theta', 4, 7),
            ('Alpha', 8, 12),
            ('Beta', 13, 30),
            ('Gamma', 30, 45)
            ]
frequency_map = list()

for band, fmin, fmax in iter_freqs:
    # (re)load the data to save memory
    raw_copy = raw.copy()
    raw_copy.load_data()

    # bandpass filter
    raw_copy.filter(fmin, fmax, n_jobs=1,  # use more jobs to speed up.
               l_trans_bandwidth=1,  # make sure filter params are the same
               h_trans_bandwidth=1)  # in each band and skip "auto" option.
   
    # get analytic signal (envelope)
    raw_copy.apply_hilbert(envelope=True)
    frequency_map.append(((band, fmin, fmax), raw_copy))

#%% ========= GFP with Sav-gol Filter Per Brainwave ==========
Fs = int(raw.info['sfreq'])
titles = ['theta', 'alpha', 'beta', 'gamma']
gfp_envelopes = list()
# plt.figure()
# ax = plt.axes()
for i in range(4):
    hilbert_raw = frequency_map[i][1]
    times = hilbert_raw.times * 1e3
    gfp = np.sum(hilbert_raw.get_data() ** 2, axis=0)
    gfp = mne.baseline.rescale(gfp, times, baseline=(0, baseline_period), mode="percent")
    gfp_envelope = chetto_EEG.envelopeCreator(gfp, degree=3, intervalLength=Fs+1)
    gfp_envelopes.append(gfp_envelope)

#     ax.plot(np.arange(0,8000)/Fs,gfp_envelope, label=titles[i])
# ax.legend(loc='upper right', prop={"size":20})

#%% ============== Plot GFP ============
# Plot one freq bin one
# titles = ['theta', 'alpha', 'beta', 'gamma']
# colors = plt.get_cmap('winter_r')(np.linspace(0, 1, 5))
# for ((freq_name, fmin, fmax), average), color, title in zip(
#     frequency_map, colors[0:4], titles):

#     times = average.times * 1e3
#     gfp = np.sum(average.get_data() ** 2, axis=0)
#     gfp = mne.baseline.rescale(gfp, times, baseline=(0, baseline_period), mode="percent")
#     # gfp = gfp / np.max(gfp)
#     gfp_envelope = chetto_EEG.envelopeCreator(gfp, degree=3, intervalLength=161)
    
#     plt.figure()
#     ax = plt.axes()
#     ax.plot(np.arange(0,8000)/Fs, gfp, label=freq_name, color=color, linewidth=2.5)
#     ax.plot(np.arange(0,8000)/Fs, gfp_envelope, color='cyan', linewidth=2)

#     ax.axhline(0, linestyle='--', color='grey', linewidth=2)
    
#     # ci_low, ci_up = bootstrap_confidence_interval(average.get_data(), random_state=0,
#     #                                               stat_fun=chetto_EEG.stat_fun)
#     # ci_low = rescale(ci_low, np.arange(0,len(times)), baseline=(None, 0))
#     # ci_up = rescale(ci_up, np.arange(0,len(times)), baseline=(None, 0))

#     # ax.fill_between(np.arange(0,len(times)), gfp + ci_up, gfp - ci_low, color=color, alpha=0.3)
#     ax.grid(False)
#     ax.set_ylabel('GFP', size=20)
#     ax.set_xlabel('Time [Sec]', size=20)
#     ax.set_title('Global Field Power of Event-related Dynamics (' + title + ')' , size=25)
    
#     ax.vlines(x=events_actions[0:6,0]/Fs, ymin=0, ymax=max(gfp), colors='purple', ls='--', lw=2, label='Action Onsets')
#%% ========== GFP Affection to ERD ==================
# plt.figure()
# plt.plot(gfp_envelopes[1])
from scipy import signal

gfp_new_envelopes = gfp_envelopes.copy()
    
for i in range(4):
    gfp_new_envelopes[i] = signal.resample(gfp_new_envelopes[i], 4000)
    minimum = np.min(gfp_new_envelopes[i])
    if(minimum < 0 ):
        gfp_new_envelopes[i] += np.abs(minimum)
        gfp_new_envelopes[i] += 2 #min will be 2
        
    gfp_new_envelopes[i] = np.log2(gfp_new_envelopes[i])
    
alphabeta_mean_gfp = (gfp_new_envelopes[1] + gfp_new_envelopes[2]) / 2

# plt.plot(gfp_new_envelopes[1])

# print(np.max(gfp_new_envelopes[1]))
# print(np.min(gfp_new_envelopes[1]))

#GFP Filtering
new_avg_power = avg_power.copy()
# for i in range(np.size(new_avg_power,1)):
# new_avg_power[60:100,:] = new_avg_power[60:100,:] / gfp_new_envelopes[1] 
# new_avg_power[100:280,:] = new_avg_power[100:280,:] / gfp_new_envelopes[2] 
# new_avg_power[280:,:] = new_avg_power[280:,:] / gfp_new_envelopes[3] 
# new_avg_power[0:60,:] = new_avg_power[0:60,:] / gfp_new_envelopes[0] 
new_avg_power = new_avg_power / alphabeta_mean_gfp

print(np.min(new_avg_power))
print(np.max(new_avg_power))

#New power object creation
gfpfiltered_power = power.copy()
gfpfiltered_power._data = np.expand_dims(new_avg_power, axis=0)

#Plot
fig, ax = plt.subplots(1, 2, figsize=(12, 4), gridspec_kw={"width_ratios": [10, 1]})
gfpfiltered_power.plot([0], vmin=np.min(new_avg_power), vmax=np.max(new_avg_power), cmap=(cmap, False), axes=ax[0], colorbar=False, \
                       show=False, mask=total_mask, mask_style="mask")
ax[0].axvline(0, linewidth=1, color="black", linestyle=":")  # event
ax[0].vlines(x=events_actions[:,0]/160, ymin=0, ymax=36, colors='purple', ls='--', lw=3, label='Action Onsets')
ax[0].hlines(y=freq_thesholds, xmin=0, xmax=time_second, colors='black', ls='--', lw=3, label='Brain waves')
ax[0].legend(fontsize=15)
fig.colorbar(ax[0].images[-1], cax=ax[-1])

ax[0].text(-13,3, 'Delta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,6, 'Theta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,10, 'Alpha', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,24, 'Beta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,33, 'Gamma', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')

# ax[0].set_xlim(0, 100)
plt.title('ERD Color Spectrum', fontsize=13)
plt.suptitle("Global Field Power Enhanced ERD Permutation Clustered Multitaper Spectrogram", fontsize=20)
#%% ============ Final v.01 Amplification of ERD Algorithms ==================

#sharpening
# filt_avgpower = ndimage.gaussian_filter(avg_power, 1)
# alpha = 30
# sharpened = avg_power + alpha * (avg_power - filt_avgpower)

#%%==== unsharp mask =======
from skimage.filters import unsharp_mask
unsharped = unsharp_mask(new_avg_power, radius=5, amount=2)

copy_power = power.copy()
copy_power._data = np.expand_dims(unsharped, axis=0)

# new_mask = unsharped > unsharped.mean() + 0.1
unsharped[unsharped < unsharped.mean() + 0.2] = 0

fig, ax = plt.subplots(1, 2, figsize=(12, 4), gridspec_kw={"width_ratios": [10, 1]})
copy_power.plot([0], vmin=np.min(unsharped), vmax=np.max(unsharped), cmap=(cmap, False), axes=ax[0], colorbar=False, show=False, \
                mask=total_mask, mask_style="mask")

ax[0].axvline(0, linewidth=1, color="black", linestyle=":")  # event
ax[0].vlines(x=events_actions[:,0]/160, ymin=0, ymax=36, colors='purple', ls='--', lw=3, label='Action Onsets')
ax[0].hlines(y=freq_thesholds, xmin=0, xmax=time_second, colors='black', ls='--', lw=3, label='Brain waves')
ax[0].legend(fontsize=15)
fig.colorbar(ax[0].images[-1], cax=ax[-1])

ax[0].text(-13,3, 'Delta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,6, 'Theta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,10, 'Alpha', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,24, 'Beta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,33, 'Gamma', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')

# ax[0].set_xlim(0, 100)
plt.title('ERD Color Spectrum', fontsize=13)
plt.suptitle("Unsharp Masked of Global Field Power Enhanced ERD Permutation Clustered Multitaper Spectrogram", fontsize=20)
#==== unsharp mask =======

#%%================= edge detection =================
from scipy import ndimage

sx = ndimage.sobel(unsharped, axis=0, mode='constant')
sy = ndimage.sobel(unsharped, axis=1, mode='constant')
sob = np.hypot(sx, sy)

copy_power = power.copy()
copy_power._data = np.expand_dims(sob, axis=0)

fig, ax = plt.subplots(1, 2, figsize=(12, 4), gridspec_kw={"width_ratios": [10, 1]})
copy_power.plot([0], vmin=np.min(sob), vmax=np.max(sob), cmap=(cmap, False), axes=ax[0], colorbar=False, show=False, mask=total_mask, mask_style="mask")

ax[0].axvline(0, linewidth=1, color="black", linestyle=":")  # event
ax[0].vlines(x=events_actions[:,0]/160, ymin=0, ymax=36, colors='purple', ls='--', lw=3, label='Action Onsets')
ax[0].hlines(y=freq_thesholds, xmin=0, xmax=time_second, colors='black', ls='--', lw=3, label='Brain waves')
ax[0].legend(fontsize=15)
fig.colorbar(ax[0].images[-1], cax=ax[-1])

ax[0].text(-13,3, 'Delta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,6, 'Theta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,10, 'Alpha', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,24, 'Beta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,33, 'Gamma', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')

# ax[0].set_xlim(0, 100)
plt.title('ERD Color Spectrum', fontsize=13)
plt.suptitle("Unsharp Mask + Sobel Filtered of Global Field Power Enhanced ERD Permutation Clustered Multitaper Spectrogram", fontsize=20)
#================= edge detection =================

#%%============= Contrasting ================
# from skimage import exposure
# contrasted = exposure.equalize_hist(sob)
# # new_mask = contrasted > contrasted.max() * 0.9

# copy_power = power.copy()
# copy_power._data = np.expand_dims(contrasted, axis=0)

# fig, ax = plt.subplots(1, 2, figsize=(12, 4), gridspec_kw={"width_ratios": [10, 1]})
# copy_power.plot([0], vmin=np.min(contrasted), vmax=np.max(contrasted), cmap=(cmap, False), axes=ax[0], colorbar=False, show=False, mask=total_mask, mask_style="mask")
# # ax[0].contour(sob, [0.02], linewidth=2, colors='r')

# ax[0].axvline(0, linewidth=1, color="black", linestyle=":")  # event
# ax[0].vlines(x=events_actions[:,0]/160, ymin=0, ymax=36, colors='purple', ls='--', lw=3, label='Action Onsets')
# ax[0].hlines(y=freq_thesholds, xmin=0, xmax=time_second, colors='black', ls='--', lw=3, label='Brain waves')
# ax[0].legend(fontsize=15)
# fig.colorbar(ax[0].images[-1], cax=ax[-1])
# #============= Contrasting ================

# #Local Equalize
# # from skimage.filters import rank
# # from skimage.morphology import disk
# # selem = disk(30)
# # sob2 = (sob/np.max(sob) - 0.5) * 2
# # img_eq = rank.equalize(sob2, selem=selem)
# # img_eq = img_eq / np.max(img_eq)
#%% ========= Nearest =========
# nearest = plt.imshow(unsharped, interpolation='nearest', cmap=cmap).get_array()

# copy_power = power.copy()
# copy_power._data = np.expand_dims(nearest, axis=0)

# # new_mask = unsharped > unsharped.max() * 0.9

# fig, ax = plt.subplots(1, 2, figsize=(12, 4), gridspec_kw={"width_ratios": [10, 1]})
# copy_power.plot([0], vmin=np.min(unsharped), vmax=np.max(unsharped), cmap=(cmap, False), axes=ax[0], colorbar=False, show=False, mask=total_mask, mask_style="mask")

# ax[0].axvline(0, linewidth=1, color="black", linestyle=":")  # event
# ax[0].vlines(x=events_actions[:,0]/160, ymin=0, ymax=36, colors='purple', ls='--', lw=3, label='Action Onsets')
# ax[0].hlines(y=freq_thesholds, xmin=0, xmax=time_second, colors='black', ls='--', lw=3, label='Brain waves')
# ax[0].legend(fontsize=15)
# fig.colorbar(ax[0].images[-1], cax=ax[-1])
# #==== unsharp mask =======


# plt.figure()
# plt.imshow(unsharped, interpolation='nearest', cmap=cmap).get_array()

#%% ============ Area 51 ===========

#============== Interpolation ================
# methods = [None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
#            'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
#            'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']
# # Fixing random state for reproducibility
# np.random.seed(19680801)

# fig, axs = plt.subplots(nrows=3, ncols=6, figsize=(9, 6),
#                         subplot_kw={'xticks': [], 'yticks': []})

# for ax, interp_method in zip(axs.flat, methods):
#     ax.imshow(unsharped[:,1000:1500], interpolation=interp_method, cmap=cmap)
#     ax.set_title(str(interp_method))

# plt.tight_layout()
# plt.show()
#============== Interpolation ================

#%%============== K-means =================
# from sklearn.cluster import KMeans
# kmeans = KMeans(n_clusters=9, random_state=0).fit(unsharped)
# kmeans_pic = kmeans.cluster_centers_[kmeans.labels_]

# plt.figure()
# plt.imshow(kmeans_pic)

# copy_power = power.copy()
# copy_power._data = np.expand_dims(kmeans_pic, axis=0)

# fig, ax = plt.subplots(1, 2, figsize=(12, 4), gridspec_kw={"width_ratios": [10, 1]})
# copy_power.plot([0], vmin=np.min(contrasted), vmax=np.max(contrasted), cmap=(cmap, False), axes=ax[0], colorbar=False, show=False, mask=total_mask, mask_style="mask")
# # ax[0].contour(sob, [0.02], linewidth=2, colors='r')

# ax[0].axvline(0, linewidth=1, color="black", linestyle=":")  # event
# ax[0].vlines(x=events_actions[:,0]/160, ymin=0, ymax=36, colors='purple', ls='--', lw=3, label='Action Onsets')
# ax[0].hlines(y=freq_thesholds, xmin=0, xmax=time_second, colors='black', ls='--', lw=3, label='Brain waves')
# ax[0].legend(fontsize=15)
# fig.colorbar(ax[0].images[-1], cax=ax[-1])
#============== K-means =================
#%% ============== Deep Learning Segmentation ==========
# import pixellib
# from pixellib.semantic import semantic_segmentation
# from pixellib.instance import instance_segmentation
# import time
# import os
# from PIL import Image
# import gc


# os.chdir('/home/caghangir/Desktop/PhD/LD_BCI/Codes/Segmentation Deep Learning Model')

# #====== Array to Image ======
# # plt.figure()
# # plt.imshow(unsharped)
# # plt.savefig('unsharped.jpg', pad_inches=1, bbox_inches='tight', dpi=400)
# # print('Figure has saved successfully!')
# # plt.close()
# unsharped_3d = np.array(Image.fromarray(contrasted, mode="RGB").convert('L'))
# unsharped_3d = np.stack((unsharped_3d,)*3, axis=-1)
# # unsharped_3d = np.expand_dims(unsharped_3d, axis=2)

# # plt.figure()
# # plt.imshow(unsharped_3d)

# # unsharped_3d.shape
# # x=Image.open('unsharped.jpg')   

# # image = np.array(Image.open('unsharped.jpg'))    
# #====== Array to Image ======

# %% Semantic Segmentation Pascal
# segment_image = semantic_segmentation()
# # segment_image.load_pascalvoc_model("pascal.h5")
# segment_image.load_pascalvoc_model("deeplabv3_xception_tf_dim_ordering_tf_kernels.h5") 

# start = time.time()
# segment_image.segmentAsPascalvoc(image_path=unsharped_3d, arrayinput=True, overlay=True, \
#                                  output_image_name="pascal_semantic_segmented_output_contrasted.jpg.jpg")
# end = time.time()
# print(f"Inference Time: {end-start:.2f}seconds")

# gc.collect()
# del segment_image
# %% Instance Segmentation Ade20k Model
# segment_image = semantic_segmentation()
# # segment_image.load_pascalvoc_model("pascal.h5")
# segment_image.load_ade20k_model("deeplabv3_xception65_ade20k.h5") 

# start = time.time()
# segment_image.segmentAsAde20k(image_path=unsharped_3d, arrayinput=True, output_image_name="ade20k_instance_segmented_output_contrasted.jpg", overlay=True)
# end = time.time()
# print(f"Inference Time: {end-start:.2f}seconds")

# gc.collect()
# %% Instance Segmentation Mask RCNN
# segment_image = instance_segmentation()
# segment_image.load_model("mask_rcnn_coco.h5") 

# start = time.time()
# segment_image.segmentImage(image_path=unsharped_3d, arrayinput=True, output_image_name = "maskrcnn_instance_segmented_output_contrasted.jpg")
# end = time.time()
# print(f"Inference Time: {end-start:.2f}seconds")

# gc.collect()
# del segment_image

# from streamlit import caching
# caching.clear_cache()
#%% ========== Morphologic Snakes ========
from skimage import data, img_as_float
from skimage.segmentation import (morphological_chan_vese,
                                  morphological_geodesic_active_contour,
                                  inverse_gaussian_gradient,
                                  checkerboard_level_set)
import numpy as np
import matplotlib.pyplot as plt

def store_evolution_in(lst):
    """Returns a callback function to store the evolution of the level sets in
    the given list.
    """

    def _store(x):
        lst.append(np.copy(x))

    return _store

# methods = [avg_power, new_avg_power, unsharped, sob, contrasted]
# method_names = ['avg_power', 'new_avg_power', 'unsharped', 'edge detected', 'contrasted']
# fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(9, 6), subplot_kw={'xticks': [], 'yticks': []})
# for ax, method, method_name in zip(axs.flat, methods, method_names):
#     # Morphological GAC
#     image = img_as_float(method)
#     gimage = inverse_gaussian_gradient(image)
    
#     init_ls = np.zeros(image.shape, dtype=np.int8)
#     init_ls[10:-10, 10:-10] = 1
    
#     evolution = []
#     callback = store_evolution_in(evolution)
#     ls = morphological_geodesic_active_contour(gimage, 230, init_ls,
#                                                smoothing=1, balloon=-1,
#                                                threshold=0.69,
#                                                iter_callback=callback)
#     ax.imshow(image)
#     ax.contour(ls, colors='r')
    # ax.set_title(method_name, size=15)

#%% ======== Edge Detection Morphologic Snake =====
image = img_as_float(sob)
gimage = inverse_gaussian_gradient(sob)

init_ls = np.zeros(image.shape, dtype=np.int8)
init_ls[10:-10, 10:-10] = 1
evolution = []
callback = store_evolution_in(evolution)
ls = morphological_geodesic_active_contour(gimage, 330, init_ls,
                                            smoothing=1, balloon=-1,
                                            threshold=0.69,
                                            iter_callback=callback)

copy_power = power.copy()
copy_power._data = np.expand_dims(sob, axis=0)

fig, ax = plt.subplots(1, 2, figsize=(12, 4), gridspec_kw={"width_ratios": [10, 1]})
copy_power.plot([0], vmin=np.min(sob), vmax=np.max(sob), cmap=(cmap, False), axes=ax[0], colorbar=False, show=False, \
                mask=ls, mask_style="contour")
ax[0].axvline(0, linewidth=1, color="black", linestyle=":")  # event
ax[0].vlines(x=events_actions[:,0]/160, ymin=0, ymax=36, colors='purple', ls='--', lw=3, label='Action Onsets')
ax[0].hlines(y=freq_thesholds, xmin=0, xmax=time_second, colors='black', ls='--', lw=3, label='Brain waves')
ax[0].legend(fontsize=15)
fig.colorbar(ax[0].images[-1], cax=ax[-1])

ax[0].text(-13,3, 'Delta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,6, 'Theta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,10, 'Alpha', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,24, 'Beta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,33, 'Gamma', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')

# ax[0].set_xlim(0, 100)
plt.title('ERD Color Spectrum', fontsize=13)
plt.suptitle("Filter Iterated ERD Permutation Clustered Multitaper Spectrogram with Morphology Snake Contours", fontsize=20)
#================= edge detection =================

#%% ============ Morphology Snake Contour Ordering ===========
contour_indexes = np.where(ls==1)
ls_boolean = np.array(ls == 1, dtype='bool')

import cv2
ls_image = ls.copy()
ls_image = ls_image.astype(np.uint8)
ls_image[ls_image == 1] = 255

# ======= Find Contour Area Size ===========
idx = cv2.findContours(ls_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
areas = np.zeros(len(idx))
for i in range(len(idx)):
    areas[i] = cv2.contourArea(idx[i])
# ======= Find Contour Area Size ===========

# ===== 3D to 2D =======
# idx_new = list()
# for i in range(len(idx)):
#     idx_new.append(np.reshape(idx[i], (np.size(idx[i], 0), np.size(idx[i], 2))))
# ===== 3D to 2D =======
    
#=== Sort Cluster Area Indexes =====
sorted_area_idx = np.argsort(areas * -1)
idx_sorted = list()
for i in range(len(idx)):
    idx_sorted.append(idx[sorted_area_idx[i]])
#=== Sort Cluster Area Indexes =====

#%% ========= Select only Big Contours ===========
new_mask = np.zeros_like(sob)
contours = idx_sorted[0:10]

#==== Corners of contours =====
left_right_corners_ofcontours = np.zeros((10,2))
for i in range(10):
    left_right_corners_ofcontours[i,0], left_right_corners_ofcontours[i,1] = np.min(contours[i][:,:,0]), np.max(contours[i][:,:,0])
#==== Corners of contours =====

cv2.drawContours(new_mask, contours, -1, (1),1)

# ========== Plot Power Data ==============
copy_power = power.copy()
copy_power._data = np.expand_dims(sob, axis=0)

fig, ax = plt.subplots(1, 2, figsize=(12, 4), gridspec_kw={"width_ratios": [10, 1]})
copy_power.plot([0], vmin=np.min(sob), vmax=np.max(sob), cmap=(cmap, False), axes=ax[0], colorbar=False, show=False, \
                mask=new_mask, mask_style="contour")
ax[0].axvline(0, linewidth=1, color="black", linestyle=":")  # event
ax[0].vlines(x=events_actions[:,0]/160, ymin=0, ymax=36, colors='purple', ls='--', lw=3, label='Action Onsets')
ax[0].vlines(x=left_right_corners_ofcontours[:,0]*2/160, ymin=0, ymax=36, colors='blue', ls=':', lw=4, label='Contour Points')
ax[0].hlines(y=freq_thesholds, xmin=0, xmax=time_second, colors='black', ls='--', lw=3, label='Brain waves')
ax[0].legend(fontsize=15)
fig.colorbar(ax[0].images[-1], cax=ax[-1])

ax[0].text(-13,3, 'Delta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,6, 'Theta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,10, 'Alpha', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,24, 'Beta', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')
ax[0].text(-13,33, 'Gamma', horizontalalignment='center', verticalalignment='center', fontsize=15, color='Black')

# ax[0].set_xlim(0, 100)
plt.title('ERD Color Spectrum', fontsize=13)
plt.suptitle("Filter Iterated ERD Permutation Clustered Multitaper Spectrogram with Largest Morphology Snake Contours", fontsize=20)
# ========== Plot Power Data ==============

#%% =============== Spectrogram to 1-D Line ================
freq_low_threshold_index = np.where(freqs > 8)[0][0]
freq_high_threshold_index = np.where(freqs <= 30)[0][-1]
sob_interval = np.sum(sob[freq_low_threshold_index:freq_high_threshold_index], axis=0)

plt.figure()
x_axis = np.linspace(0,len(sob_interval)*2/Fs, len(sob_interval))
plt.plot(x_axis, sob_interval)
all_vlines = events_actions[:,0]/160
plt.vlines(x=all_vlines[0:6], ymin=0, ymax=max(sob_interval), colors='purple', ls='--', lw=3, label='Action Onsets')

plt.xlabel('Time (s)')
plt.ylabel('Sum Power')