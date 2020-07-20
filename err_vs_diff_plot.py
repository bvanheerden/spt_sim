# Plots of the data returned by err_vs_diff.
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from scipy.optimize import curve_fit
import joblib
from sim_module import TrackingSim

matplotlib.rcParams.update({'font.size': 14})

errs = np.loadtxt('errs.txt')
errs_mf = np.loadtxt('errs_mf.txt')
errs_kt = np.loadtxt('errs_kt.txt')

# diffs = np.logspace(-12, 0, 12)
diffs = np.logspace(-14, 5, 18)

# untracked = np.sqrt(2000 * diffs)
# param, pcov = curve_fit(fitfunc, diffs[:7], errs[:7])
# print(param[0], param[1])
# tracked = fitfunc(diffs, param[0], param[1])

cutoff = np.pi * (0.4 / np.sqrt(2)) ** 2 * 0.1
cutoff = np.pi * 0.025 ** 2 * 12.5

plt.figure(figsize=(8, 5))
plt.loglog(diffs, errs, '-o', label='Orbital')
plt.loglog(diffs, errs_mf, '-o', label='MINFLUX')
plt.loglog(diffs, errs_kt, '-o', label="Knight's Tour")
plt.xlabel(r'Diffusion Coefficient (\textmu m$^2$s$^{-1}$)')
plt.ylabel(r'Average error (\textmu m)')
# plt.loglog(diffs, untracked, '--', color='gray')
# plt.loglog(diffs, tracked, '--', color='black')
# plt.axvline(cutoff)
plt.axhline(0.016)
plt.axhline(0.144)
plt.axhline(0.166)
plt.legend()
# plt.savefig('./out/err_diff_fluo.png')
plt.show()
