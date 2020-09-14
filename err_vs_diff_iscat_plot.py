# Plots of the data returned by err_vs_diff.
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from scipy.optimize import curve_fit
import joblib
from sim_module import TrackingSim

matplotlib.rcParams.update({'font.size': 14})

errs = np.loadtxt('errs_fluo_gfp.txt')
errs_gfp = np.loadtxt('errs_iscat_gfp.txt')
errs_hiv = np.loadtxt('errs_iscat_hiv.txt')
errs_lhcii = np.loadtxt('errs_iscat_lhcii.txt')
errs_lhcii_mic = np.loadtxt('errs_iscat_lhcii-mic.txt')
errs_pb = np.loadtxt('errs_iscat_pb.txt')

# diffs = np.logspace(-12, 0, 12)
diffs = np.logspace(-19, 2, 18)

# untracked = np.sqrt(2000 * diffs)
# param, pcov = curve_fit(fitfunc, diffs[:7], errs[:7])
# print(param[0], param[1])
# tracked = fitfunc(diffs, param[0], param[1])

cutoff = np.pi * (0.4 / np.sqrt(2)) ** 2 * 0.1
cutoff = np.pi * 0.025 ** 2 * 12.5

plt.figure(figsize=(8, 5))
plt.loglog(diffs, errs, '-o', label='Fluorescence')
plt.loglog(diffs, errs_gfp, '-o', label='GFP')
plt.loglog(diffs, errs_lhcii, '-o', label="LHCII")
plt.loglog(diffs, errs_pb, '-o', label="PB")
plt.loglog(diffs, errs_lhcii_mic, '-o', label="LHCII-Micelle")
plt.loglog(diffs, errs_hiv, '-o', label="HIV-QD")
plt.xlabel(r'Diffusion Coefficient (\textmu m$^2$s$^{-1}$)')
plt.ylabel(r'Average error (\textmu m)')
# plt.loglog(diffs, untracked, '--', color='gray')
# plt.loglog(diffs, tracked, '--', color='black')
# plt.axvline(cutoff)
plt.legend()
plt.savefig('./out/err_diff_iscat.png')
plt.show()
