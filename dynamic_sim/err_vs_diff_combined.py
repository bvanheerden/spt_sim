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
matplotlib.rcParams.update({'font.family': 'serif'})

# matplotlib.rcParams.update({'font.size': 10})

errs = np.loadtxt('files/errs_fluo1.txt')
errs_mf = np.loadtxt('files/errs_mftemp.txt')
errs_kt = np.loadtxt('files/errs_kttemp.txt')

errs_nk = np.loadtxt('files/errs_nokalman_high.txt')
errs_mf_nk = np.loadtxt('files/errs_mf_nokalman_high.txt')
errs_kt_nk = np.loadtxt('files/errs_kt_nokalman_high.txt')

errs_gfp = np.loadtxt('files/errs_iscat_gfp2.txt')
errs_hiv = np.loadtxt('files/errs_iscat_hiv-qd2.txt')
errs_lhcii = np.loadtxt('files/errs_iscat_lhcii2.txt')
errs_lhcii_mic = np.loadtxt('files/errs_iscat_lhcii-mic2.txt')
errs_pb = np.loadtxt('files/errs_iscat_pb2.txt')
#
errs_gfp_adj = np.loadtxt('files/errs_iscat_gfp_adjust3.txt')
errs_lhcii_adj = np.loadtxt('files/errs_iscat_lhcii_adjust3.txt')
errs_lhcii_mic_adj = np.loadtxt('files/errs_iscat_lhcii-mic_adjust3.txt')
errs_pb_adj = np.loadtxt('files/errs_iscat_pb_adjust3.txt')
errs_hiv_adj = np.loadtxt('files/errs_iscat_hiv-qd_adjust3.txt')

# diffs = np.logspace(-12, 0, 12)
# diffs = np.logspace(-19, 2, 18)
diffs = np.logspace(-9, 0, 16)
# diffs = np.logspace(-13, -5, 8)

untracked = np.sqrt(200 * diffs)
# param, pcov = curve_fit(fitfunc, diffs[:7], errs[:7])
# print(param[0], param[1])
# tracked = fitfunc(diffs, param[0], param[1])

# cutoff = np.pi * (0.4 / np.sqrt(2)) ** 2 * 0.1
# cutoff = np.pi * 0.025 ** 2 * 12.5

# plt.figure(figsize=(6, 4), dpi=150)
fig = formatter.figure(width_ratio=1.0, aspect_ratio=0.7)
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222, sharey=ax1)
ax3 = fig.add_subplot(223, sharex=ax1)
ax4 = fig.add_subplot(224, sharex=ax2, sharey=ax3)

ax1.loglog(diffs*1000, errs, label='Orbital', lw=1)
ax1.loglog(diffs*1000, errs_kt, label="Knight's Tour", lw=1, color='C2')
ax1.loglog(diffs*1000, errs_mf, label='MINFLUX', lw=1, color='C1')
ax1.set_ylabel(r'Average tracking error (\textmu m)')
ax1.loglog(diffs*1000, untracked, '--', color='gray', label='Untracked')
ax1.legend(loc='upper left', framealpha=0)

ax2.loglog(diffs*1000, errs_nk, label='Orbital', lw=1)
ax2.loglog(diffs*1000, errs_kt_nk, label="Knight's Tour", lw=1, color='C2')
ax2.loglog(diffs*1000, errs_mf_nk, label='MINFLUX', lw=1, color='C1')
ax2.loglog(diffs*1000, untracked, '--', color='gray', label='Untracked')
ax2.legend(loc='upper left', framealpha=0)

fluo, = ax3.loglog(diffs * 1000, errs, '-', label='Fluorescence')
lhcii, = ax3.loglog(diffs * 1000, errs_lhcii, '-', label="LHCII")
mic, = ax3.loglog(diffs * 1000, errs_lhcii_mic, '-', label="LHCII-Micelle")
pb, = ax3.loglog(diffs * 1000, errs_pb, '-', label="PB")
gfp, = ax3.loglog(diffs * 1000, errs_gfp, '-', label='GFP')
hiv, = ax3.loglog(diffs * 1000, errs_hiv, '-', label="HIV-QD")
ax3.set_xlabel(r'Diffusion coefficient (\textmu m$^2$s$^{-1}$)')
ax3.set_ylabel(r'Average tracking error (\textmu m)')
untracked_plot, = ax3.loglog(diffs * 1000, untracked, '--', color='gray')
leg1 = ax3.legend(loc='upper left', framealpha=0, handles=[gfp, lhcii])
ax3.legend(loc='lower right', framealpha=0, handles=[pb, mic, fluo, hiv, untracked_plot])
ax3.add_artist(leg1)

fluo_adj, = ax4.loglog(diffs * 1000, errs, '-', label='Fluorescence')
lhcii_adj, = ax4.loglog(diffs * 1000, errs_lhcii_adj, '-', label="LHCII")
mic_adj, = ax4.loglog(diffs * 1000, errs_lhcii_mic_adj, '-', label="LHCII-Micelle")
pb_adj, = ax4.loglog(diffs * 1000, errs_pb_adj, '-', label="PB")
gfp_adj, = ax4.loglog(diffs * 1000, errs_gfp_adj, '-', label='GFP')
hiv_adj, = ax4.loglog(diffs * 1000, errs_hiv_adj, '-', label="HIV-QD")
untracked_plot, = ax4.loglog(diffs * 1000, untracked, '--', color='gray', label='Untracked')
ax4.set_xlabel(r'Diffusion coefficient (\textmu m$^2$s$^{-1}$)')
leg1 = ax4.legend(loc='upper left', framealpha=0, handles=[gfp_adj, fluo_adj, lhcii_adj, mic_adj])
ax4.legend(loc='lower right', framealpha=0, handles=[pb_adj, hiv_adj, untracked_plot])
ax4.add_artist(leg1)

ax1.set_xlim((np.min(diffs*1000), np.max(diffs*1000)))
ax2.set_xlim((np.min(diffs*1000), np.max(diffs*1000)))

for ax in fig.get_axes():
    for line in ax.lines:
        line.set_lw(1.5)

plt.tight_layout()
plt.savefig('../out/err_diff_combined.pdf')
plt.show()
