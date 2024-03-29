# Plots of the data returned by err_vs_diff.
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from scipy.optimize import curve_fit
import joblib
from sim_module import TrackingSim
import rsmf

color_list = ['#1d6996', '#73af48', '#edad08', '#e17c05', '#cc503e', '#94346e', '#6f4070']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

# col_width = 345  # For dissertation I think
col_width = 470  # For journal draft
# col_width = 483.7  # For SPIE paper I think
# col_width = 418  # I don't know anymore

formatter = rsmf.CustomFormatter(columnwidth=col_width * 0.01389, fontsizes=10,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})
matplotlib.rcParams.update({'font.family': 'serif'})
# matplotlib.rcParams.update({'font.size': 11})

errs = np.loadtxt('files/errs_new5.txt')
errs_mf = np.loadtxt('files/errs_mf_new5.txt')
errs_kt = np.loadtxt('files/errs_kt_new5.txt')

# errs = np.concatenate((np.loadtxt('errs8.txt').flatten(), np.loadtxt('errs9.txt').flatten()[:]))
# errs_mf = np.concatenate((np.loadtxt('errs_mf8.txt').flatten(), np.loadtxt('errs_mf9.txt').flatten()[:]))
# errs_kt = np.concatenate((np.loadtxt('errs_kt8.txt').flatten(), np.loadtxt('errs_kt9.txt').flatten()[:]))

diffs = np.logspace(-9, 1, 16)
diffs = np.logspace(-10, -4, 8)
diffs = np.logspace(-9, 0, 16)
# diffs = np.logspace(-4, 0, 16)

untracked = np.sqrt(200 * diffs)
# param, pcov = curve_fit(fitfunc, diffs[:7], errs[:7])
# print(param[0], param[1])
# tracked = fitfunc(diffs, param[0], param[1])

cutoff = np.pi * (0.4 / np.sqrt(2)) ** 2 * 3.125 * 0.001
cutoff1 = np.pi * 0.025 ** 2 * 3.125 * 0.001
cutoff2 = (3.75 * 0.4) ** 2 * 3.125 * 0.001

cutoff1 = 50  # MF
cutoff2 = 566  # Orb
cutoff3 = 1500  # KT

# plt.figure(figsize=(4, 3), dpi=150)
fig = formatter.figure(width_ratio=0.7)
plt.loglog(diffs*1000, errs, marker='o', label='Orbital', lw=1)
plt.loglog(diffs*1000, errs_kt, marker='o', label="Knight's Tour", lw=1, color='C2')
plt.loglog(diffs*1000, errs_mf, marker='o', label='MINFLUX', lw=1, color='C1')
# plt.xlabel(r'Diffusiekoëffisient (\textmu m$^2$s$^{-1}$)')
# plt.ylabel(r'Gemiddelde fout (\textmu m)')
plt.xlabel(r'Diffusion coefficient (\textmu m$^2$s$^{-1}$)')
plt.ylabel(r'Average tracking error (\textmu m)')
plt.loglog(diffs*1000, untracked, '--', color='gray')
# plt.loglog(diffs, tracked, '--', color='black')
# plt.axvline(cutoff1 / 100)
# plt.axvline(cutoff2 / 100)
# plt.axvline(cutoff3 / 100)
# plt.axhline(0.016)
# plt.axhline(0.144)
# plt.axhline(0.166)
plt.legend(framealpha=0.0)
plt.tight_layout()
plt.savefig('../out/err_diff_fluo.pdf')
# plt.savefig('out/poster/err_diff_fluo.pdf')
# plt.show()
