# Runs a simulation for different values of D and plots against the error. Fixed bandwidth.
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import joblib
from sim_module import TrackingSim

simulation_orb = TrackingSim(numpoints=500000, method='orbital', freq=12.5, amp=5.0, waist=0.4, tracking=True,
                             feedback=3.125, iscat=False, kalman=True, rin=0.01)
simulation_orb_kalm = TrackingSim(numpoints=500000, method='orbital', freq=12.5, amp=5.0, waist=0.4, tracking=True,
                                   feedback=3.125, iscat=False, kalman=True, rin=0.1)

diffs = np.logspace(-7, 1, 16)


def parr_func(i, D, method, sim):
    err, measx, truex, measy, truey, intvals = sim.main_tracking(D)
    return err


def fitfunc(D, B, nm):
    return np.sqrt(2 * D / B + (nm ** 2 * B))


errs = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'orb', simulation_orb) for i, D in enumerate(diffs))
errs_kalm = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'orb', simulation_orb_kalm) for i, D in enumerate(diffs))

# untracked = np.sqrt(2000 * diffs)
# param, pcov = curve_fit(fitfunc, diffs[:7], errs[:7])
# print(param[0], param[1])
# tracked = fitfunc(diffs, param[0], param[1])

cutoff = np.pi * (0.4 / np.sqrt(2)) ** 2 * 0.1
cutoff = np.pi * 0.025 ** 2 * 0.1

plt.loglog(diffs, errs, '-o', label='Fluorescence')
plt.loglog(diffs, errs_kalm, '-o', label='iScat')
# plt.loglog(diffs, untracked, '--', color='gray')
# plt.loglog(diffs, tracked, '--', color='black')
# plt.axvline(cutoff)
plt.legend()
plt.show()
