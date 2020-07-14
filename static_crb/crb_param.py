import numpy as np
from matplotlib import pyplot as plt

xvals = np.linspace(-300, 300)
fwhm = 212
L = 300

gauss1 = np.exp(-4 * np.log(2) * ((xvals - L / 2) / fwhm) ** 2)
gauss2 = np.exp(-4 * np.log(2) * ((xvals + L / 2) / fwhm) ** 2)

frac = (-4 * np.log(2) * xvals * L) / (fwhm ** 2)

param = np.exp(frac) / (2 * np.cosh(frac))

crbparam = (param * (1-param) / np.sqrt(param ** 2 + (1 - param) ** 2))
crbparam_fluo = np.sqrt(param * (1 - param))

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(5, 7))
ax1.plot(xvals, gauss1, color='C0')
ax1.plot(xvals, gauss2, color='C0')

ax2.plot(xvals, param)

ax3.plot(xvals, crbparam)
ax3.plot(xvals, crbparam_fluo)
plt.savefig('../out/crb_param.png')
plt.show()
