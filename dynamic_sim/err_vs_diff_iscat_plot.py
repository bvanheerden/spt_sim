# Plots of the data returned by err_vs_diff.
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from scipy.optimize import curve_fit
import joblib
from sim_module import TrackingSim
import rsmf
import os

color_list = ['#1d6996', '#73af48', '#edad08', '#e17c05', '#cc503e', '#94346e', '#6f4070']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

# matplotlib.rcParams.update({'font.size': 13})

errs = np.loadtxt('files/errs_fluo1.txt')
errs_gfp = np.loadtxt('files/errs_iscat_gfp2.txt')
errs_hiv = np.loadtxt('files/errs_iscat_hiv-qd2.txt')
errs_lhcii = np.loadtxt('files/errs_iscat_lhcii2.txt')
errs_lhcii_mic = np.loadtxt('files/errs_iscat_lhcii-mic2.txt')
errs_pb = np.loadtxt('files/errs_iscat_pb2.txt')

# errs_gfp = np.loadtxt('files/errs_iscat_gfp_adjust2.txt')
# errs_lhcii = np.loadtxt('files/errs_iscat_lhcii_adjust2.txt')
# errs_lhcii_mic = np.loadtxt('files/errs_iscat_lhcii-mic_adjust2.txt')
# errs_pb = np.loadtxt('files/errs_iscat_pb_adjust2.txt')
# errs_hiv = np.loadtxt('files/errs_iscat_hiv-qd_adjust2.txt')

# diffs = np.logspace(-12, 0, 12)
# diffs = np.logspace(-19, 2, 18)
diffs = np.logspace(-9, 0, 16)
# diffs = np.logspace(-13, -5, 8)

untracked = np.sqrt(200 * diffs)
# param, pcov = curve_fit(fitfunc, diffs[:7], errs[:7])
# print(param[0], param[1])
# tracked = fitfunc(diffs, param[0], param[1])

cutoff = np.pi * (0.4 / np.sqrt(2)) ** 2 * 0.1
cutoff = np.pi * 0.025 ** 2 * 12.5

# plt.figure(figsize=(6, 4), dpi=150)
fig = formatter.figure(width_ratio=0.8)
plt.loglog(diffs*1000, errs, '-o', label='Fluorescence')
plt.loglog(diffs*1000, errs_lhcii, '-o', label="LHCII")
plt.loglog(diffs*1000, errs_lhcii_mic, '-o', label="LHCII-Micelle")
plt.loglog(diffs*1000, errs_pb, '-o', label="PB")
plt.loglog(diffs*1000, errs_gfp, '-o', label='GFP')
plt.loglog(diffs*1000, errs_hiv, '-o', label="HIV-QD")
plt.xlabel(r'Diffusion coefficient (\textmu m$^2$s$^{-1}$)')
plt.ylabel(r'Average tracking error (\textmu m)')
plt.loglog(diffs*1000, untracked, '--', color='gray')
# plt.loglog(diffs, tracked, '--', color='black')
# plt.axvline(cutoff)
plt.legend(ncol=2)
plt.tight_layout()
# plt.savefig('../out/err_diff_iscat_adjust.pdf')
plt.savefig('../out/err_diff_iscat.pdf')
plt.show()
