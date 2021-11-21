# Runs a simulation for different values of D and plots against the error. Fixed bandwidth.
import numpy as np
from matplotlib import pyplot as plt
import joblib
from sim_module import TrackingSim

numpoints = 100000

freq = 12.5
ffreq = 3.125

simulation_orb = TrackingSim(numpoints=numpoints, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                             feedback=ffreq, iscat=False, debug=False, rin=0.04)
simulation_mf = TrackingSim(numpoints=numpoints, method='minflux', freq=freq, amp=45.0, L=0.05, tracking=True,
                            feedback=ffreq, debug=False, rin=0.004, fwhm=0.36)
simulation_kt = TrackingSim(numpoints=numpoints, method='knight', freq=freq, amp=24.0, waist=0.4, tracking=True,
                            feedback=ffreq, debug=False, rin=0.3)

numdiffs = 16
numruns = 6

# diffs = np.logspace(-11, 1, numdiffs)
# diffs = np.logspace(-4, 0, numdiffs)
# diffs = np.logspace(-10, -4, numdiffs)
diffs = np.logspace(-9, 0, numdiffs)


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
    return errsum / numruns


errs = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'orb') for i, D in enumerate(diffs))
errs_mf = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'mf') for i, D in enumerate(diffs))
errs_kt = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'kt') for i, D in enumerate(diffs))

np.savetxt('files/errstemp.txt', errs)
np.savetxt('files/errs_mftemp.txt', errs_mf)
np.savetxt('files/errs_kttemp.txt', errs_kt)

untracked = np.sqrt(200 * diffs)

# cutoff = np.pi * (0.4 / np.sqrt(2)) ** 2 * 0.1
# cutoff = np.pi * 0.025 ** 2 * 0.1

plt.loglog(diffs, errs, '-o')
plt.loglog(diffs, errs_mf, '-o')
plt.loglog(diffs, errs_kt, '-o')
plt.loglog(diffs, untracked, '--', color='gray')
# plt.axvline(cutoff)
plt.show()
