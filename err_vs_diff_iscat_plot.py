# Plots of the data returned by err_vs_diff.
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from scipy.optimize import curve_fit
import joblib
from sim_module import TrackingSim
import rsmf

formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=10,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

errs = np.loadtxt('errs_fluo_gfp1.txt')
errs_gfp = np.loadtxt('errs_iscat_gfp1.txt')
errs_hiv = np.loadtxt('errs_iscat_hiv1.txt')
errs_lhcii = np.loadtxt('errs_iscat_lhcii1.txt')
errs_lhcii_mic = np.loadtxt('errs_iscat_lhcii-mic1.txt')
errs_pb = np.loadtxt('errs_iscat_pb1.txt')

# diffs = np.logspace(-12, 0, 12)
diffs = np.logspace(-19, 2, 18)
diffs = np.logspace(-15, 1, 12)

# untracked = np.sqrt(2000 * diffs)
# param, pcov = curve_fit(fitfunc, diffs[:7], errs[:7])
# print(param[0], param[1])
# tracked = fitfunc(diffs, param[0], param[1])

cutoff = np.pi * (0.4 / np.sqrt(2)) ** 2 * 0.1
cutoff = np.pi * 0.025 ** 2 * 12.5

# plt.figure(figsize=(8, 5))
fig = formatter.figure(width_ratio=0.8)
plt.loglog(diffs*1000, errs, '-o', label='Fluorescence')
plt.loglog(diffs*1000, errs_gfp, '-o', label='GFP')
plt.loglog(diffs*1000, errs_lhcii, '-o', label="LHCII")
plt.loglog(diffs*1000, errs_pb, '-o', label="FB")
plt.loglog(diffs*1000, errs_lhcii_mic, '-o', label="LHCII-Micelle")
plt.loglog(diffs*1000, errs_hiv, '-o', label="HIV-QD")
plt.xlabel(r'Diffusion coefficient (\textmu m$^2$s$^{-1}$)')
plt.ylabel(r'Average error (\textmu m)')
# plt.loglog(diffs, untracked, '--', color='gray')
# plt.loglog(diffs, tracked, '--', color='black')
# plt.axvline(cutoff)
plt.legend(framealpha=0.7)
plt.tight_layout()
plt.savefig('./out/err_diff_iscat_art.pdf')
