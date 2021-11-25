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

errs = np.loadtxt('files/errs_nokalman.txt')
errs_mf = np.loadtxt('files/errs_mf_nokalman.txt')
errs_kt = np.loadtxt('files/errs_kt_nokalman.txt')

diffs = np.logspace(-9, 0, 16)

untracked = np.sqrt(200 * diffs)
# param, pcov = curve_fit(fitfunc, diffs[:7], errs[:7])
# print(param[0], param[1])
# tracked = fitfunc(diffs, param[0], param[1])

fig = formatter.figure(width_ratio=0.6)
plt.loglog(diffs*1000, errs, marker='o', label='Orbital', lw=1)
plt.loglog(diffs*1000, errs_kt, marker='o', label="Knight's Tour", lw=1, color='C2')
plt.loglog(diffs*1000, errs_mf, marker='o', label='MINFLUX', lw=1, color='C1')
plt.xlabel(r'Diffusion coefficient (\textmu m$^2$s$^{-1}$)')
plt.ylabel(r'Average error (\textmu m)')
plt.loglog(diffs*1000, untracked, '--', color='gray')
plt.ylim((0.01, None))
# plt.axhline(0.016)
# plt.axhline(0.144)
# plt.axhline(0.166)
plt.legend(framealpha=0)
plt.tight_layout()
plt.savefig('../out/err_diff_nokalman.pdf')
plt.show()
