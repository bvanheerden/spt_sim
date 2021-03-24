# Runs a simulation for different values of D and plots against the error. Fixed bandwidth.
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import joblib
from sim_module import TrackingSim

freq = 12.5
ffreq = 3.125

numpoints = 10000

# intfactor = 1.4e6  # HIV-QD
intfactor = 33  # PB
# intfactor = 48  # LHCII
# intfactor = 213  # LHCII-mic
# intfactor = 84  # GFP

# contrast = 0.057  # HIV-QD
contrast = 4.2e-4  # PB
# contrast = 1.02e-5  # LHCII
# contrast = 4.47e-5  # LHCII-mic
# contrast = 1.08e-6  # GFP

simulation_orb = TrackingSim(numpoints=numpoints, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                             feedback=ffreq, iscat=False, debug=False, rin=1)
simulation_orb_iscat = TrackingSim(numpoints=numpoints, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                                   feedback=ffreq, iscat=True, debug=False, rin=1, intfactor=intfactor, contrast=contrast)

diffs = np.logspace(-19, 2, 18)
# diffs = np.logspace(-4, 2, 12)
diffs = np.logspace(-15, 1, 8)


def parr_func(i, D, method, sim):
    print('run ', i, 'of 18')
    errsum = 0
    for j in range(1):
        err, measx, truex, measy, truey, intvals = sim.main_tracking(D)
        errsum += err
    return errsum / 1


def fitfunc(D, B, nm):
    return np.sqrt(2 * D / B + (nm ** 2 * B))


errs = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'orb', simulation_orb) for i, D in enumerate(diffs))
errs_iscat = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'orb', simulation_orb_iscat) for i, D in enumerate(diffs))

# untracked = np.sqrt(2000 * diffs)
# param, pcov = curve_fit(fitfunc, diffs[:7], errs[:7])
# print(param[0], param[1])
# tracked = fitfunc(diffs, param[0], param[1])

cutoff = np.pi * (0.4 / np.sqrt(2)) ** 2 * 0.1
cutoff = np.pi * 0.025 ** 2 * 0.1

# np.savetxt('errs_fluo_gfp1.txt', errs)
# np.savetxt('errs_iscat_pb1.txt', errs_iscat)

plt.loglog(diffs, errs, '-o')
plt.loglog(diffs, errs_iscat, '-o')
# plt.loglog(diffs, untracked, '--', color='gray')
# plt.loglog(diffs, tracked, '--', color='black')
plt.axvline(cutoff)
plt.show()
