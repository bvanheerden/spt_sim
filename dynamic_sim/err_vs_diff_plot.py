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

formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')
matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

matplotlib.rcParams.update({'font.size': 11})

errs = np.loadtxt('errstemp.txt')
errs_mf = np.loadtxt('errs_mftemp.txt')
errs_kt = np.loadtxt('errs_kttemp.txt')

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

# cutoff1 = 0.03
# cutoff2 = 0.2

# plt.figure(figsize=(4, 3), dpi=150)
fig = formatter.figure(width_ratio=0.8)
plt.loglog(diffs*1000, errs, marker='o', label='Orbital', lw=1)
plt.loglog(diffs*1000, errs_kt, marker='o', label="Knight's Tour", lw=1, color='C2')
plt.loglog(diffs*1000, errs_mf, marker='o', label='MINFLUX', lw=1, color='C1')
# plt.xlabel(r'Diffusiekoëffisient (\textmu m$^2$s$^{-1}$)')
# plt.ylabel(r'Gemiddelde fout (\textmu m)')
plt.xlabel(r'Diffusion coefficient (\textmu m$^2$s$^{-1}$)')
plt.ylabel(r'Average error (\textmu m)')
plt.loglog(diffs*1000, untracked, '--', color='gray')
# plt.loglog(diffs, tracked, '--', color='black')
# plt.axvline(cutoff * 1000)
# plt.axvline(cutoff1 * 1000)
# plt.axvline(cutoff2 * 1000)
# plt.axhline(0.016)
# plt.axhline(0.144)
# plt.axhline(0.166)
plt.legend()
plt.tight_layout()
plt.savefig('../out/err_diff_fluo.pdf')
# plt.savefig('out/poster/err_diff_fluo.pdf')
plt.show()
