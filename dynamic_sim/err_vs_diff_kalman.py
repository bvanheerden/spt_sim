# Runs a simulation for different values of D and plots against the error. Fixed bandwidth.
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import joblib
from sim_module import TrackingSim

numpoints = 100000

freq = 12.5
ffreq = 3.125

simulation_orb = TrackingSim(numpoints=numpoints, method='knight', freq=freq, amp=5.0, waist=0.4, tracking=True,
                             feedback=ffreq, iscat=False, debug=False, rin=0.001)
simulation_orb1 = TrackingSim(numpoints=numpoints, method='knight', freq=freq, amp=5.0, waist=0.4, tracking=True,
                             feedback=ffreq, iscat=False, debug=False, rin=0.01)
simulation_orb2 = TrackingSim(numpoints=numpoints, method='knight', freq=freq, amp=5.0, waist=0.4, tracking=True,
                             feedback=ffreq, iscat=False, debug=False, rin=0.1)
simulation_orb3 = TrackingSim(numpoints=numpoints, method='knight', freq=freq, amp=5.0, waist=0.4, tracking=True,
                              feedback=ffreq, iscat=False, debug=False, rin=1)

numdiffs = 16
numruns = 3

diffs = np.logspace(-9, 1, numdiffs)


def parr_func(i, D, method):
    errsum = 0
    for j in range(numruns):
        print('diff # ', i+1, 'of ', numdiffs)
        print('run # ', j+1, 'of ', numruns)
        if method == '0':
            err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(D)
        elif method == '1':
            err, measx, truex, measy, truey, intvals = simulation_orb1.main_tracking(D)
        elif method == '2':
            err, measx, truex, measy, truey, intvals = simulation_orb2.main_tracking(D)
        elif method == '3':
            err, measx, truex, measy, truey, intvals = simulation_orb3.main_tracking(D)
        errsum += err
    return errsum / numruns


def fitfunc(D, B, nm):
    return np.sqrt(2 * D / B + (nm ** 2 * B))


errs = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, '0') for i, D in enumerate(diffs))
errs_1 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, '1') for i, D in enumerate(diffs))
errs_2 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, '2') for i, D in enumerate(diffs))
errs_3 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, '3') for i, D in enumerate(diffs))

untracked = np.sqrt(2000 * diffs)

cutoff = np.pi * (0.4 / np.sqrt(2)) ** 2 * 0.1
cutoff = np.pi * 0.025 ** 2 * 0.1

plt.loglog(diffs, errs, '-o')
plt.loglog(diffs, errs_1, '-o')
plt.loglog(diffs, errs_2, '-o')
plt.loglog(diffs, errs_3, '-o')
plt.loglog(diffs, untracked, '--', color='gray')
# plt.loglog(diffs, tracked, '--', color='black')
plt.axvline(cutoff)
plt.show()
