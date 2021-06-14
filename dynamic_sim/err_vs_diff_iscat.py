# Runs a simulation for different values of D and plots against the error. Fixed bandwidth.
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import joblib
from sim_module import TrackingSim
import os

freq = 12.5
ffreq = 3.125

numpoints = 100000

samples = ['lhcii', 'lhcii-mic', 'pb', 'gfp', 'hiv-qd']
rvals = [0.02, 0.005, 0.002, 0.05, 0.001]
rvals = [0.008, 0.001, 0.0005, 0.1, 0.0005]
sample = 3

adjusted = False

if adjusted:
    intfactors = [0.91, 4.0, 1.3, 2.0, 88548]
    contrasts = [4.75e-5, 2.09e-4, 4.00e-3, 6.36e-6, 0.90]
else:
    intfactors = [3.1, 13.5, 2.1, 5.3, 88548]
    contrasts = [1.61e-4, 7.07e-4, 6.53e-3, 1.71e-5, 0.90]

intfactor = intfactors[sample]
contrast = contrasts[sample]
rval = rvals[sample]

simulation_orb = TrackingSim(numpoints=numpoints, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                             feedback=ffreq, iscat=False, debug=False, rin=0.04)
if adjusted:
    simulation_orb_iscat = TrackingSim(numpoints=numpoints, method='orbital', freq=freq, amp=5.0, waist=0.4,
                                       tracking=True, feedback=ffreq, iscat=True, debug=False, rin=rval,
                                       intfactor=intfactor, contrast=contrast, adjustment=1000, avint=0.0125)
else:
    simulation_orb_iscat = TrackingSim(numpoints=numpoints, method='orbital', freq=freq, amp=5.0, waist=0.4,
                                       tracking=True, feedback=ffreq, iscat=True, debug=False, rin=0.04,
                                       intfactor=intfactor, contrast=contrast, avint=0.0125)

diffs = np.logspace(-9, 0, 16)
# diffs = np.logspace(-13, -5, 8)


def parr_func(i, D, method, sim):
    print('run ', i, 'of 18')
    errsum = 0
    for j in range(200):
        if j % 20 == 0:
            print(j)
        err, measx, truex, measy, truey, intvals = sim.main_tracking(D)
        errsum += err
    return errsum / 200


def fitfunc(D, B, nm):
    return np.sqrt(2 * D / B + (nm ** 2 * B))


# errs = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'orb', simulation_orb) for i, D in enumerate(diffs))
errs_iscat = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'orb', simulation_orb_iscat) for i, D in enumerate(diffs))

duration = 1  # seconds
freq = 440  # Hz
os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))

# untracked = np.sqrt(2000 * diffs)
# param, pcov = curve_fit(fitfunc, diffs[:7], errs[:7])
# print(param[0], param[1])
# tracked = fitfunc(diffs, param[0], param[1])

cutoff = np.pi * (0.4 / np.sqrt(2)) ** 2 * 0.1
cutoff = np.pi * 0.025 ** 2 * 0.1

# np.savetxt('files/errs_fluo1.txt', errs)

if adjusted:
    np.savetxt('files/errs_iscat_' + samples[sample] + '_adjust2.txt', errs_iscat)
else:
    np.savetxt('files/errs_iscat_' + samples[sample] + '2.txt', errs_iscat)

# plt.loglog(diffs, errs, '-o')
plt.loglog(diffs, errs_iscat, '-o')
# plt.loglog(diffs, untracked, '--', color='gray')
# plt.loglog(diffs, tracked, '--', color='black')
plt.axvline(cutoff)
plt.show()
