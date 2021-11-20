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

# col_width = 345  # For dissertation I think
col_width = 470  # For journal draft
# col_width = 483.7  # For SPIE paper I think
# col_width = 418  # I don't know anymore
formatter = rsmf.CustomFormatter(columnwidth=col_width * 0.01389, fontsizes=10,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

# matplotlib.rcParams.update({'font.size': 10})

errs = np.loadtxt('files/errs_fluo1.txt')
# errs_gfp = np.loadtxt('files/errs_iscat_gfp2.txt')
# errs_hiv = np.loadtxt('files/errs_iscat_hiv-qd2.txt')
# errs_lhcii = np.loadtxt('files/errs_iscat_lhcii2.txt')
# errs_lhcii_mic = np.loadtxt('files/errs_iscat_lhcii-mic2.txt')
# errs_pb = np.loadtxt('files/errs_iscat_pb2.txt')

errs_gfp = np.loadtxt('files/errs_iscat_gfp_adjust3.txt')
errs_lhcii = np.loadtxt('files/errs_iscat_lhcii_adjust3.txt')
errs_lhcii_mic = np.loadtxt('files/errs_iscat_lhcii-mic_adjust3.txt')
errs_pb = np.loadtxt('files/errs_iscat_pb_adjust3.txt')
errs_hiv = np.loadtxt('files/errs_iscat_hiv-qd_adjust3.txt')

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
fig = formatter.figure(width_ratio=0.53, aspect_ratio=0.7)
fluo, = plt.loglog(diffs*1000, errs, '-o', label='Fluorescence')
lhcii, = plt.loglog(diffs*1000, errs_lhcii, '-o', label="LHCII")
mic, = plt.loglog(diffs*1000, errs_lhcii_mic, '-o', label="LHCII-Micelle")
pb, = plt.loglog(diffs*1000, errs_pb, '-o', label="PB")
gfp, = plt.loglog(diffs*1000, errs_gfp, '-o', label='GFP')
hiv, = plt.loglog(diffs*1000, errs_hiv, '-o', label="HIV-QD")
plt.xlabel(r'Diffusion coefficient (\textmu m$^2$s$^{-1}$)')
plt.ylabel(r'Average tracking error (\textmu m)')
plt.loglog(diffs*1000, untracked, '--', color='gray')
# plt.loglog(diffs, tracked, '--', color='black')
# plt.axvline(cutoff)
legend1 = plt.legend([fluo, lhcii, mic], ['Fluorescence', 'LHCII', 'LHCII-micelle'], ncol=1)
plt.legend([pb, gfp, hiv], ['PB', 'GFP', 'HIV-QD'], ncol=1, loc='lower right')
plt.gca().add_artist(legend1)
plt.tight_layout()
plt.savefig('../out/err_diff_iscat_adjust.pdf')
# plt.savefig('../out/err_diff_iscat.pdf')
plt.show()
