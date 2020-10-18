import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import rsmf

formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

xvals = np.linspace(-300, 300, num=100)
fwhm = 212
L = 300

gauss1 = np.exp(-4 * np.log(2) * ((xvals - L / 2) / fwhm) ** 2)
gauss2 = np.exp(-4 * np.log(2) * ((xvals + L / 2) / fwhm) ** 2)

frac = (-4 * np.log(2) * xvals * L) / (fwhm ** 2)

param = np.exp(frac) / (2 * np.cosh(frac))

crbparam = (param * (1-param) / np.sqrt(param ** 2 + (1 - param) ** 2))
crbparam_fluo = np.sqrt(param * (1 - param))

fig = formatter.figure(width_ratio=0.6, aspect_ratio=1.5)
ax1, ax2, ax3 = fig.subplots(3, 1, sharex=True)
ax1.plot(xvals, gauss1, color='C0')
ax1.plot(xvals, gauss2, color='C0')

ax2.plot(xvals, param)

ax3.plot(xvals, crbparam, label='iSCAT')
ax3.plot(xvals, crbparam_fluo, label='Fluoressensie')

ax1.set_ylabel('Intensiteit')
ax2.set_ylabel('Parameter')
ax3.set_ylabel('CRB (parameter)')
ax3.set_xlabel('x-posisie (nm)')

ax3.legend()

plt.savefig('../out/crb_param.pdf')
plt.show()
