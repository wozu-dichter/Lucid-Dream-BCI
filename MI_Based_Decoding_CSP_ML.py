# -*- coding: utf-8 -*-
"""
Created on Mon May 18 13:51:06 2020

@author: caghangir
"""

import numpy as np
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import SVC
from sklearn.model_selection import ShuffleSplit, cross_val_score

from mne import Epochs, pick_types, events_from_annotations
from mne.channels import make_standard_montage
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci
from mne.decoding import CSP
import mne
import extremeEEGSignalAnalyzer as chetto_EEG
import os
chetto_EEG = chetto_EEG.extremeEEGSignalAnalyzer()
os.chdir('/home/cagatay/Desktop/PhD/LD_BCI/Progress_Reports/1st_One/All_movements/Real_action')
import gc

# %matplotlib qt #plot in new window
#%% Set parameters and read data

# avoid classification of evoked responses by using epochs that start 1s after
# cue onset.
tmin, tmax = -1., 4.
event_id = dict(hands=2, feet=3)

#=== File Path Concatenator ====
runs_action = [3, 7, 11]  # motor action: left vs. right hand
runs_imagery = [4, 8, 12]  # motor imagery: left vs. right hand
runs_imagery_hf = [6, 10, 14] # motor imagery: hands vs feet

raw_fnames_action = list()
raw_fnames_imagery = list()
raw_fnames_imagery_hf = list()
for subject in range(1, 110):
    temp_raw_fnames = eegbci.load_data(subject, runs_action)
    raw_fnames_action += temp_raw_fnames
    temp_raw_fnames = eegbci.load_data(subject, runs_imagery)
    raw_fnames_imagery += temp_raw_fnames
    temp_raw_fnames = eegbci.load_data(subject, runs_imagery_hf)
    raw_fnames_imagery_hf += temp_raw_fnames

#%%==== Cleaner =======
# Fs_actions = list()    
# cals_actions = list()
# for i in range(len(raw_fnames_action)):
#     temp_raw = read_raw_edf(input_fname=raw_fnames_action[i], preload=True)
#     Fs_actions.append(temp_raw.info['sfreq'])
#     cals_actions.append(temp_raw._cals[0])
# plt.plot(Fs_actions)
# plt.plot(cals_actions)

# Fs_actions=np.array(Fs_actions)
# cals_actions = np.array(cals_actions)    
# to_delete_Fs = np.where(Fs_actions==128)[0]
#==== Cleaner =======

#============= Clean Data ===========
raw_fnames_action.pop(261)
raw_fnames_action.pop(261)
raw_fnames_action.pop(261)
raw_fnames_action.pop(261)
raw_fnames_action.pop(261)
raw_fnames_action.pop(261)
raw_fnames_action.pop(267)
raw_fnames_action.pop(267)
raw_fnames_action.pop(267)
raw_fnames_action.pop(288)
raw_fnames_action.pop(288)
raw_fnames_action.pop(288)

raw_fnames_imagery.pop(261)
raw_fnames_imagery.pop(261)
raw_fnames_imagery.pop(261)
raw_fnames_imagery.pop(261)
raw_fnames_imagery.pop(261)
raw_fnames_imagery.pop(261)
raw_fnames_imagery.pop(267)
raw_fnames_imagery.pop(267)
raw_fnames_imagery.pop(267)
raw_fnames_imagery.pop(288)
raw_fnames_imagery.pop(288)
raw_fnames_imagery.pop(288)

raw_fnames_imagery_hf.pop(261)
raw_fnames_imagery_hf.pop(261)
raw_fnames_imagery_hf.pop(261)
raw_fnames_imagery_hf.pop(261)
raw_fnames_imagery_hf.pop(261)
raw_fnames_imagery_hf.pop(261)
raw_fnames_imagery_hf.pop(267)
raw_fnames_imagery_hf.pop(267)
raw_fnames_imagery_hf.pop(267)
raw_fnames_imagery_hf.pop(288)
raw_fnames_imagery_hf.pop(288)
raw_fnames_imagery_hf.pop(288)
#============= Clean Data ===========
#=== File Path Concatenator ====

# #==== One file 87  ======
# raw_6 = read_raw_edf(input_fname=raw_fnames_action[267], preload=True)
# Fs = raw_6.info['sfreq']
# raw_6_data = raw_6.get_data()
# ch_names = raw_6.info['ch_names']
# length_of_raw_6 = np.size(raw_6.get_data(), 1) / Fs #125 sec
# #==== One file ======

# #==== One file 88  ======
# raw_7 = read_raw_edf(input_fname=raw_fnames_action[263], preload=True)
# Fs_1 = raw_7.info['sfreq']
# raw_6_data = raw_6.get_data()
# ch_names = raw_6.info['ch_names']
# length_of_raw_6 = np.size(raw_6.get_data(), 1) / Fs #125 sec
# #==== One file ======
# del temp_raw, Fs_actions, cals_actions
#%% ====== Reading Raw =========
raw_action = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames_action]) #concatenate
# raw_imagery = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames_imagery]) #concatenate
#%% Standardize ====
eegbci.standardize(raw_action)  # set channel names
ch_names_new = raw_action.info['ch_names']
#=== Name Standardize ====

montage = make_standard_montage('standard_1005')
raw_action.set_montage(montage)

# strip channel names of "." characters
raw_action.rename_channels(lambda x: x.strip('.'))
ch_names_new_2 = raw_action.info['ch_names']

# Apply band-pass filter
raw_action.filter(8., 30., fir_design='firwin', skip_by_annotation='edge')
#%% ==== Event / Epoching / Train Data ==========
events, _ = events_from_annotations(raw_action, event_id=dict(T1=2, T2=3))

picks = pick_types(raw_action.info, meg=False, eeg=True, stim=False, eog=False,
                   exclude='bads')

# Read epochs (train will be done only between 1 and 2s)
# Testing will be done with a running classifier
epochs = Epochs(raw_action, events, event_id, tmin=0, tmax=4, proj=True, picks=picks,
                baseline=None, preload=True)
# epochs_train = epochs.copy().crop(tmin=1., tmax=5.)
labels = epochs.events[:, -1] - 2
#%% ========== Classification with linear discrimant analysis ==================
scores = []
epochs_data_train = epochs.get_data()
# epochs_data_train = epochs_train.get_data()
cv = ShuffleSplit(10, test_size=0.2, random_state=42)
cv_split = cv.split(epochs_data_train)

# ==== Assemble a classifier ========
lda = LinearDiscriminantAnalysis()
lda_shrinkage = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')
svc = SVC(gamma='auto')


csp = CSP(n_components=4, reg=None, log=True, norm_trace=False)

# Use scikit-learn Pipeline with cross_val_score function
clf = Pipeline([('CSP', csp), ('LDA', lda)])
scores_lda = cross_val_score(clf, epochs_data_train, labels, cv=cv, n_jobs=1)
mean_scores_lda, std_scores_lda = np.mean(scores_lda), np.std(scores_lda)
clf = Pipeline([('CSP', csp), ('LDA', lda_shrinkage)])
scores_ldashrinkage = cross_val_score(clf, epochs_data_train, labels, cv=cv, n_jobs=1)
mean_scores_ldashrinkage, std_scores_ldashrinkage = np.mean(scores_ldashrinkage), np.std(scores_ldashrinkage)
clf = Pipeline([('CSP', csp), ('SVC', svc)])
scores_svc = cross_val_score(clf, epochs_data_train, labels, cv=cv, n_jobs=1)
mean_scores_svc, std_scores_svc = np.mean(scores_svc), np.std(scores_svc)

# Printing the results
class_balance = np.mean(labels == labels[0])
class_balance = max(class_balance, 1. - class_balance)
print("Classification accuracy: %f / Chance level: %f" % (np.mean(scores),
                                                          class_balance))

# plot CSP patterns estimated on full data for visualization
csp.fit_transform(epochs_data_train, labels)

csp.plot_patterns(epochs.info, ch_type='eeg', units='Patterns (AU)', size=1.5)
#%% =========== Individual Subject training ========
subject_acc = np.zeros((105,3)) #lda, ldashrinkage, svc
subject_acc_crossval = np.zeros((105,5)) #lda, ldashrinkage, svc
subject_f1 = np.zeros((105,3))

subject_acc_std = np.zeros((105,3))
subject_f1_std = np.zeros((105,3))
event_id = dict(T1=2, T2=3)

tmin, tmax = -1, 4
for i in range(105):
    temp_raw = raw_fnames_action[i*3:i*3+3]
    raw = concatenate_raws([read_raw_edf(f, preload=True) for f in temp_raw]) #concatenate
    
    # ========= Standardize =============
    eegbci.standardize(raw)  # set channel names
    ch_names_new = raw.info['ch_names']
    #=== Name Standardize ====
    
    montage = make_standard_montage('standard_1005')
    raw.set_montage(montage)
    
    # strip channel names of "." characters
    raw.rename_channels(lambda x: x.strip('.'))
    ch_names_new_2 = raw.info['ch_names']
    
    # Apply band-pass filter
    raw.filter(8., 30., fir_design='firwin', skip_by_annotation='edge')
    # ========= Standardize =============
    
    # ========= Event / Epoching / Train Data ==========
    events, _ = events_from_annotations(raw, event_id=event_id)
    
    picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                       exclude='bads')
    
    # Read epochs (train will be done only between 1 and 2s)
    # Testing will be done with a running classifier
    epochs = Epochs(raw, events, event_id, tmin=tmin, tmax=tmax, proj=True, picks=picks,
                    baseline=(-0.5,0), preload=True)
    epochs_train = epochs.copy().crop(tmin=0., tmax=4.)
    labels = epochs.events[:, -1] - 2
    # ========= Event / Epoching / Train Data ==========
    
    # ========== Classification with linear discrimant analysis ==================
    scores = []
    epochs_data_train = epochs_train.get_data()
    cv = ShuffleSplit(5, test_size=0.2, random_state=42)
    cv_split = cv.split(epochs_data_train)
    
    # ==== Assemble a classifier ========
    lda = LinearDiscriminantAnalysis()
    lda_shrinkage = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')
    svc = SVC(gamma='auto')
    # ==== Assemble a classifier ========
    
    csp = CSP(n_components=4, reg=None, log=True, norm_trace=False)
    
    #=== Classification ===
    clf = Pipeline([('CSP', csp), ('LDA', lda)])
    temp_acc_lda = cross_val_score(clf, epochs_data_train, labels, cv=cv, n_jobs=-1)
    temp_f1score_lda = cross_val_score(clf, epochs_data_train, labels, cv=cv, scoring='f1_macro', n_jobs=-1)
    
    # clf = Pipeline([('CSP', csp), ('LDA', lda_shrinkage)])
    # temp_acc_ldashrinkage = cross_val_score(clf, epochs_data_train, labels, cv=cv, n_jobs=-1)
    # temp_f1score_ldashrinkage = cross_val_score(clf, epochs_data_train, labels, cv=cv, scoring='f1_macro', n_jobs=-1)
    
    # clf = Pipeline([('CSP', csp), ('SVC', svc)])
    # temp_acc_svc = cross_val_score(clf, epochs_data_train, labels, cv=cv, n_jobs=-1)
    # temp_f1score_svc = cross_val_score(clf, epochs_data_train, labels, cv=cv, scoring='f1_macro', n_jobs=-1)
    #=== Classification ===
    
    subject_acc[i,0], subject_acc_std[i,0] = np.mean(temp_acc_lda), np.std(temp_acc_lda) * 2
    # subject_acc[i,1], subject_acc_std[i,1] = np.mean(temp_acc_ldashrinkage), np.std(temp_acc_ldashrinkage) * 2
    # subject_acc[i,2], subject_acc_std[i,2] = np.mean(temp_acc_svc), np.std(temp_acc_svc) * 2
    
    subject_acc_crossval[i] = temp_acc_lda
    
    subject_f1[i,0], subject_f1_std[i,0] = np.mean(temp_f1score_lda), np.std(temp_f1score_lda) * 2
    # subject_f1[i,1], subject_f1_std[i,1] = np.mean(temp_f1score_ldashrinkage), np.std(temp_f1score_ldashrinkage) * 2
    # subject_f1[i,2], subject_f1_std[i,2] = np.mean(temp_f1score_svc), np.std(temp_f1score_svc) * 2
    
    print('Evaluation subject no : %s is completed' % i)
    # ========== Classification with linear discrimant analysis ==================
    
#==== AVGs =====
subject_acc_avgs = np.mean(subject_acc, axis=0)
subject_f1_avgs = np.mean(subject_f1, axis=0)

subject_acc_std_avgs = np.mean(subject_acc_std, axis=0)
subject_f1_avgs_std = np.mean(subject_f1_std, axis=0)

del epochs, epochs_train, epochs_data_train
gc.collect()

sorted_indexes = np.argsort(-1 * subject_acc[:,0])
subject_acc_crossval_sorted = subject_acc_crossval[sorted_indexes]
#%% ========= Box plot Cross-val ========
chetto_EEG.sorted_boxplot_scores(results=subject_acc_crossval, title='Hand Clench Classification Cross-validation accuracy of Each subject', \
                                 xlabel='Subject no', ylabel='Mean Cross-validation acc [%]')

# green_diamond = dict(markerfacecolor='g', marker='D')
# fig1, ax1 = plt.subplots()
# ax1.set_title('Basic Plot')
# ax1.boxplot(subject_acc_crossval, showfliers=False)
# plt.plot(subject_acc[sorted_indexes,0], linewidth=4, color='blue')
# plt.plot(np.arange(1,106), np.ones(105)*0.5, ls='--', linewidth=4, color='black')
# ax1.set_title('Cross-validation accuracy of Each subject', size=25)
# ax1.set_xlabel(xlabel='Subject no', size=20)
# ax1.set_ylabel(ylabel='Mean Cross-validation acc [%]', size=20)
# ax1.tick_params(labelsize=10) #chnage size of tick parameters on x and y axes  
#%% =============== Explore Event-Related Dynamics for Specific Frequency Bands ========

#======= We create average power time courses for each frequency band ========
# set epoching parameters
tmin, tmax = -1., 4.
event_id = dict(T1=2, T2=3)
baseline = None
picks = ['C5', 'C3', 'C4', 'Cz', 'C1', 'C2', 'C6']
saving_directory = '/home/cagatay/Desktop/PhD/LD_BCI/Progress_Reports/1st_One/All_movements/MI_Action/GFP'

#==== Data Selection =====
# all_raw = list()
# for i in sorted_indexes[95:]:
#     temp_raw = raw_fnames_imagery[i*3:i*3+3]
#     all_raw += temp_raw
i=sorted_indexes[1]
temp_raw = raw_fnames_imagery[i*3:i*3+3]
#==== Data Selection =====

raw = concatenate_raws([read_raw_edf(f, preload=True) for f in temp_raw]) #concatenate
# ========= Read Data =============
eegbci.standardize(raw)  # set channel names
#=== Name Standardize ====
montage = make_standard_montage('standard_1005')
raw.set_montage(montage)
raw.rename_channels(lambda x: x.strip('.'))
# ========= Read Data =============
events, _ = events_from_annotations(raw, event_id=event_id)

chetto_EEG.plt_GFP(raw=raw, picks=picks, saving_directory=saving_directory, events=events, event_id=event_id, \
                   explanation='MI Successful Subject 2', tmin=-1, tmax=4)

#%% ========== Epochs to Evokes =======
tmin, tmax = -1., 4.
event_id = dict(T1=2, T2=3)
baseline = None
# picks = ['C5', 'C3', 'C4', 'Cz', 'C1', 'C2', 'C6']

saving_directory = '/home/cagatay/Desktop/PhD/LD_BCI/Progress_Reports/1st_One/All_movements/Real_action'
frequency_map = list()

#==== Data Selection =====
# all_raw = list()
# for i in sorted_indexes[0:10]:
#     temp_raw = raw_fnames_imagery[i*3:i*3+3]
#     all_raw += temp_raw
i=sorted_indexes[60]
temp_raw = raw_fnames_imagery[i*3:i*3+3]
#==== Data Selection =====

# ========= Read Data =============
raw = concatenate_raws([read_raw_edf(f, preload=True) for f in temp_raw]) #concatenate
eegbci.standardize(raw)  # set channel names
#=== Name Standardize ====
montage = make_standard_montage('standard_1005')
raw.set_montage(montage)
raw.rename_channels(lambda x: x.strip('.'))

# raw = chetto_EEG.CSD(raw)
# ========= Read Data =============
picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                    exclude='bads')
# picks='csd'

events, _ = events_from_annotations(raw, event_id=event_id)

# (re)load the data to save memory
raw.load_data()

chetto_EEG.plt_evoked_response(raw=raw, explanation='Random Accuracy MI Action Evoked Response \n of All Channels', \
                               picks=picks, events=events, event_id=event_id, tmin=-1, tmax=4)
gc.collect()
#%% ========== Plot evoked topomaps ==========
tmin, tmax = -1., 4.
# event_id = dict(T1=2, T2=3)
event_id = dict(T2=3)
baseline = None
explanation = 'All Subjects'
times=np.array([-1,0,1,2,3,4])
saving_directory = '/home/cagatay/Desktop/PhD/LD_BCI/Progress_Reports/1st_One/All_movements/Real_action/Topo Maps'
frequency_map = list()

#==== Data Selection =====
# all_raw = list()
# for i in sorted_indexes[0:15]:
#     temp_raw = raw_fnames_action[i*3:i*3+3]
#     all_raw += temp_raw
i=sorted_indexes[0]
temp_raw = raw_fnames_imagery[i*3:i*3+3]

# temp_raw = raw_fnames_action
#==== Data Selection =====

#===== Function ======
epochs, events, picks = chetto_EEG.raw_file_to_epochs(raw_file_list=temp_raw, event_id=event_id, tmin=-1, tmax=4, \
                                                      l_pass=8., h_pass=30., CSD=False)

chetto_EEG.plt_evoked_topomap(raw=epochs, times=np.array([-1,0,0.2,0.3,0.4,1,4]), explanation='Successful Subject \n Right Hand Clench Action Based\n Scalp Topomap', \
                              events=events, performance_mode=True,\
                              event_id=event_id, tmin=-1, tmax=4, picks=picks, CSD=False, saving_directory=saving_directory)
# del raw, events
gc.collect()
#===== Function ======
#%% ======== Area 51 ========
subject_acc = np.zeros((10,3)) #lda, ldashrinkage, svc
subject_acc_std = np.zeros((10,3))
event_id = dict(T1=2, T2=3)

tmin, tmax, n_components = -1, 4, 4
for i in range(10):
    temp_raw = raw_fnames_action[i*3:i*3+3]
    raw = concatenate_raws([read_raw_edf(f, preload=True) for f in temp_raw]) #concatenate
    
    # ========= Standardize =============
    eegbci.standardize(raw)  # set channel names
    #=== Name Standardize ====
    
    montage = make_standard_montage('standard_1005')
    raw.set_montage(montage)
    
    # strip channel names of "." characters
    raw.rename_channels(lambda x: x.strip('.'))
    
    #==== Preprocess =====
    raw.filter(8., 30., fir_design='firwin', skip_by_annotation='edge')    # Apply band-pass filter
    # raw = chetto_EEG.CSD(raw)
    #==== Preprocess =====
    # ========= Standardize =============
    
    # ========= Event / Epoching / Train Data ==========
    events, _ = events_from_annotations(raw, event_id=dict(T1=2, T2=3))
    
    picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False,
                        exclude='bads')
    # picks = 'csd'
    # picks = ['C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6']
    
    # Read epochs (train will be done only between 1 and 2s)
    # Testing will be done with a running classifier
    epochs = Epochs(raw, events, event_id, tmin=tmin, tmax=tmax, proj=True, picks=picks,
                    baseline=(-0.5,0), preload=True)
    epochs = epochs.copy().crop(tmin=0., tmax=4.)
    # remove evoked response
    epochs.subtract_evoked()

    labels = epochs.events[:, -1] - 2
    # ========= Event / Epoching / Train Data ==========
    
    # ========== Classification with linear discrimant analysis ==================
    scores = []
    epochs_data_train = epochs.get_data()
    # R = np.mean(epochs_data_train[:,:,], axis=0)
    cv = ShuffleSplit(5, test_size=0.2, random_state=42)
    cv_split = cv.split(epochs_data_train)
    
    # ==== Assemble a classifier ========
    lda = LinearDiscriminantAnalysis()
    # lda_shrinkage = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto')
    # svc = SVC(gamma='auto')
    # ==== Assemble a classifier ========
    
    csp = CSP(n_components=n_components, reg=None, log=True, norm_trace=False, transform_into='average_power')
    
    #=== Classification ===
    clf = Pipeline([('CSP', csp), ('LDA', lda)])
    temp_acc_lda = cross_val_score(clf, epochs_data_train, labels, cv=cv, n_jobs=-1)
    
    # clf = Pipeline([('CSP', csp), ('LDA', lda_shrinkage)])
    # temp_acc_ldashrinkage = cross_val_score(clf, epochs_data_train, labels, cv=cv, n_jobs=-1)
    
    # clf = Pipeline([('CSP', csp), ('SVC', svc)])
    # temp_acc_svc = cross_val_score(clf, epochs_data_train, labels, cv=cv, n_jobs=-1)
    #=== Classification ===
    
    subject_acc[i,0], subject_acc_std[i,0] = np.mean(temp_acc_lda), np.std(temp_acc_lda) * 2
    # subject_acc[i,1], subject_acc_std[i,1] = np.mean(temp_acc_ldashrinkage), np.std(temp_acc_ldashrinkage) * 2
    # subject_acc[i,2], subject_acc_std[i,2] = np.mean(temp_acc_svc), np.std(temp_acc_svc) * 2
    
    print('Evaluation subject no : %s is completed' % i)
    # ========== Classification with linear discrimant analysis ==================
    
#==== AVGs =====
subject_acc_avgs = np.mean(subject_acc, axis=0)
subject_acc_std_avgs = np.mean(subject_acc_std, axis=0)
print('ACC : %s' % subject_acc_avgs)
print('ACC std : %s' % subject_acc_std_avgs)
gc.collect()