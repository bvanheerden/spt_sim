# Plots of the data returned by err_vs_diff.
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from scipy.optimize import curve_fit
import joblib
from sim_module import TrackingSim
import rsmf

formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')
matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

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

# plt.figure(figsize=(8, 5))
fig = formatter.figure(width_ratio=0.8)
plt.loglog(diffs, errs, '-o', label='Orbitaal')
plt.loglog(diffs, errs_mf, '-o', label='MINFLUX')
plt.loglog(diffs, errs_kt, '-o', label="Ruiter se toer")
plt.xlabel(r'Diffusiekoëffisient (\textmu m$^2$s$^{-1}$)')
plt.ylabel(r'Gemiddelde fout (\textmu m)')
# plt.loglog(diffs, untracked, '--', color='gray')
# plt.loglog(diffs, tracked, '--', color='black')
# plt.axvline(cutoff)
# plt.axhline(0.016)
# plt.axhline(0.144)
# plt.axhline(0.166)
plt.legend()
plt.tight_layout()
plt.savefig('out/err_diff_fluo.pdf')
plt.show()
