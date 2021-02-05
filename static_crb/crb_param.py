import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import rsmf

formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=10,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})
matplotlib.rcParams.update({'font.family': 'serif'})

xvals = np.linspace(-300, 300, num=100)
fwhm = 212
L = 300

gauss1 = np.exp(-4 * np.log(2) * ((xvals - L / 2) / fwhm) ** 2)
gauss2 = np.exp(-4 * np.log(2) * ((xvals + L / 2) / fwhm) ** 2)

frac = (-4 * np.log(2) * xvals * L) / (fwhm ** 2)

param = np.exp(frac) / (2 * np.cosh(frac))

crbparam = (param * (1-param) / np.sqrt(param ** 2 + (1 - param) ** 2))
crbparam_fluo = np.sqrt(param * (1 - param))

fig = formatter.figure(width_ratio=0.6, aspect_ratio=1.7)
ax1, ax2, ax3 = fig.subplots(3, 1, sharex=True)
ax1.plot(xvals[25:], gauss1[25:], color='C0')
ax1.plot(xvals[:75], gauss2[:75], color='C0')

ax1.fill_between(xvals[25:], 0, gauss1[25:], color='#8FBBD9')
ax1.fill_between(xvals[:75], 0, gauss2[:75], color='#8FBBD9')

ax2.plot(xvals, param)

ax3.plot(xvals, crbparam, label='iSCAT')
ax3.plot(xvals, crbparam_fluo, label='Fluorescence')

ax1.set_ylabel('Intensity (a.u.)')
ax2.set_ylabel('Parameter (a.u.)')
ax3.set_ylabel('CRB (param.) (a.u.)')
ax3.set_xlabel('x-position (nm)')

ax3.legend(framealpha=0.7)

ax1.text(-430, 0.95, 'a', fontsize=12, weight='bold')
ax2.text(-430, 0.95, 'b', fontsize=12, weight='bold')
ax3.text(-430, 0.52, 'c', fontsize=12, weight='bold')

plt.savefig('../out/crb_param_art.pdf')
