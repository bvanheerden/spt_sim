import dill
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

dill.settings['recurse'] = True
file_orbital = 'pickles/crb_lambda_orbital_iscat'
file_orbital_fluo = 'pickles/crb_lambda_orbital'

# orbital = Orbital(file_orbital, iscat=True)
# orbital_fluo = Orbital(file_orbital_fluo, iscat=False)
# print('orbital')

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)
fileobject_orbital_fluo = open(file_orbital_fluo, 'rb')
crb_lambda_orbital_fluo = dill.load(fileobject_orbital_fluo)

contrast = 0.01
n = 100
nscat = 1 * n
nsigma = np.sqrt(2 * nscat / contrast)

y = np.linspace(-300, 300, num=100)

nscat_arr = nscat * np.exp(-4 * np.log(2) * ((y / 424) ** 2))
n_arr = n * np.exp(-4 * np.log(2) * ((y / 424) ** 2))

# plt.yscale('log')
# x, y, L, N, w, amp
crb100 = crb_lambda_orbital(0, y, 300, nscat, 212, 1, nsigma)
crb200 = crb_lambda_orbital(0, y, 500, nscat, 353, 1, nsigma)
# crb400 = crb_lambda_orbital(1, y, 300, nscat, 424, 1, nsigma)
crb800 = crb_lambda_orbital(0, y, 700, nscat, 494, 1, nsigma)
# crb800 = crb_lambda_orbital(0, y, 300, nscat, 424, 1, nsigma)
crb1600 = crb_lambda_orbital(0, y, 900, nscat, 636, 1, nsigma)

# crb800 = crb_lambda_orbital_fluo(0, y, 300, n, 424, 1)
# crb800 = [crb_lambda_orbital_fluo(0, yval, 300, n_arr[i], 424, 1) for i, yval in enumerate(y)]


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

# ax4.plot(y, crb100, label='$L=300$ nm')
# ax4.plot(y, crb200, label='$L=500$ nm')
# plt.plot(y, crb400, label='L=564')
# ax4.plot(y, crb800, label='$L=700$ nm')
# ax4.plot(y, crb1600, label='$L=900$ nm')
# ax4.legend(loc='lower right', framealpha=0.7, handlelength=1.0, labelspacing=0.3)
# ax4.set_xlabel('x-position (nm)')
# ax4.set_ylabel('CRB (position) (nm)')

ax1.text(-430, 0.95, 'a', fontsize=12, weight='bold')
ax2.text(-430, 0.95, 'b', fontsize=12, weight='bold')
ax3.text(-430, 0.52, 'c', fontsize=12, weight='bold')
# ax4.text(-430, 100, 'd', fontsize=12, weight='bold')

plt.tight_layout()
plt.savefig('../out/crb_param_art.pdf')
