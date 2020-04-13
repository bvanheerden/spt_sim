# Runs a simulation for different values of D and plots against the error. Fixed bandwidth.
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import joblib
from sim_module import TrackingSim

simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=10, amp=5.0, waist=0.4, tracking=True, feedback=0.5)

diffs = np.logspace(-9, 5, 18)


def parr_func(i, D, method):
    err, measx, truex, measy, truey = simulation_orb.main_tracking(D)
    return err


def fitfunc(D, B, nm):
    return np.sqrt(2 * D / B + (nm ** 2 * B))


errs = joblib.Parallel(n_jobs=6)(joblib.delayed(parr_func)(i, D, 'orb') for i, D in enumerate(diffs))

untracked = np.sqrt(2000 * diffs)
param, pcov = curve_fit(fitfunc, diffs[:7], errs[:7])
print(param[0], param[1])
tracked = fitfunc(diffs, param[0], param[1])

plt.loglog(diffs, errs, '-o')
# plt.loglog(diffs, untracked, '--', 'gray')
plt.loglog(diffs, tracked, '--', 'black')
plt.show()
