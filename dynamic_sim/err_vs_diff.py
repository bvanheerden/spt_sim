# Runs a simulation for different values of D and plots against the error. Fixed bandwidth.
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import joblib
from sim_module import TrackingSim

numpoints = 100000
# numpoints = 500000

freq = 12.5
# freq = 3.125
ffreq = 3.125
# ffreq = 12.5

simulation_orb = TrackingSim(numpoints=numpoints, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                             feedback=ffreq, iscat=False, debug=False, rin=1, r=[2.0, 0.003])
simulation_mf = TrackingSim(numpoints=numpoints, method='minflux', freq=freq, amp=45.0, L=0.1, tracking=True,
                            feedback=ffreq, debug=False, rin=0.001, fwhm=0.36, r=[2.0, 0.0006])
simulation_kt = TrackingSim(numpoints=numpoints, method='knight', freq=freq, amp=24.0, waist=0.4, tracking=True,
                            feedback=ffreq, debug=False, rin=1, r=[2.1, 0.15])

numdiffs = 16
numruns = 3

# diffs = np.logspace(-14, 5, 16)
diffs = np.logspace(-9, 1, 16)
# diffs = np.logspace(-12, 6, 18)
# diffs = np.logspace(-3, 5, 18)
# diffs = [1e-10]


def parr_func(i, D, method):
    errsum = 0
    for j in range(numruns):
        print('diff # ', i+1, 'of ', numdiffs)
        print('run # ', j+1, 'of ', numruns)
        if method == 'orb':
            err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(D)
        elif method == 'mf':
            err, measx, truex, measy, truey, intvals = simulation_mf.main_tracking(D)
        elif method == 'kt':
            err, measx, truex, measy, truey, intvals = simulation_kt.main_tracking(D)
        errsum += err
        # print('average int: ', np.mean(intvals))
    return errsum / numruns


def fitfunc(D, B, nm):
    return np.sqrt(2 * D / B + (nm ** 2 * B))


# errs = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'orb') for i, D in enumerate(diffs))
errs_mf = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'mf') for i, D in enumerate(diffs))
# errs_kt = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'kt') for i, D in enumerate(diffs))

# np.savetxt('errs2.txt', errs)
np.savetxt('errs_mf2.txt', errs_mf)
# np.savetxt('errs_kt2.txt', errs_kt)

untracked = np.sqrt(2000 * diffs)
# param, pcov = curve_fit(fitfunc, diffs[:7], errs[:7])
# print(param[0], param[1])
# tracked = fitfunc(diffs, param[0], param[1])

cutoff = np.pi * (0.4 / np.sqrt(2)) ** 2 * 0.1
cutoff = np.pi * 0.025 ** 2 * 0.1

# plt.loglog(diffs, errs, '-o')
plt.loglog(diffs, errs_mf, '-o')
# plt.loglog(diffs, errs_kt, '-o')
plt.loglog(diffs, untracked, '--', color='gray')
# plt.loglog(diffs, tracked, '--', color='black')
plt.axvline(cutoff)
plt.show()
