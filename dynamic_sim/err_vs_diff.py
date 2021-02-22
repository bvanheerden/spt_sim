# Runs a simulation for different values of D and plots against the error. Fixed bandwidth.
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import joblib
from sim_module import TrackingSim

simulation_orb = TrackingSim(numpoints=1000000, method='orbital', freq=12.5, amp=4.0, waist=0.4, tracking=True,
                             feedback=12.5, iscat=False)#, rin=0.1, weights=[0.1, 1, 1, 1])
simulation_mf = TrackingSim(numpoints=1000000, method='minflux', freq=12.5, amp=80.0, L=0.05, tracking=True,
                             feedback=12.5, iscat=False)#, rin=0.1, weights=[0.1, 1, 1, 1])

diffs = np.logspace(-11, 0, 12)


def parr_func(i, D, method):
    if method == 'orb':
        retvals = simulation_orb.main_tracking(D)
    elif method == 'mf':
        retvals = simulation_mf.main_tracking(D)
    return retvals[0]


def fitfunc(D, B, nm):
    return np.sqrt(2 * D / B + (nm ** 2 * B))


errs = joblib.Parallel(n_jobs=6)(joblib.delayed(parr_func)(i, D, 'orb') for i, D in enumerate(diffs))
errs_mf = joblib.Parallel(n_jobs=6)(joblib.delayed(parr_func)(i, D, 'mf') for i, D in enumerate(diffs))

# untracked = np.sqrt(2000 * diffs)
# param, pcov = curve_fit(fitfunc, diffs[:7], errs[:7])
# print(param[0], param[1])
# tracked = fitfunc(diffs, param[0], param[1])

cutoff = np.pi * (0.4 / np.sqrt(2)) ** 2 * 0.1
cutoff = np.pi * 0.025 ** 2 * 0.1

plt.loglog(diffs, errs, '-o')
plt.loglog(diffs, errs_mf, '-o')
# plt.loglog(diffs, untracked, '--', color='gray')
# plt.loglog(diffs, tracked, '--', color='black')
plt.axvline(cutoff)
plt.show()
