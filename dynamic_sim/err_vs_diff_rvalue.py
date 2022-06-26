# Runs a simulation for different values of D and plots against the error. Fixed bandwidth.
import numpy as np
from matplotlib import pyplot as plt
import joblib
from sim_module import TrackingSim

numpoints = 100000

# freq = 12.5
# ffreq = 3.125
# ffreq = 12.5
freq = 8.3333333
ffreq = freq

bg = 0.00125  # (SBR=10)

simulation_orb_r1 = TrackingSim(numpoints=numpoints, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                             feedback=ffreq, iscat=False, debug=False, rin=0.8, bg=bg, kalman=True)
simulation_orb_r2 = TrackingSim(numpoints=numpoints, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                                feedback=ffreq, iscat=False, debug=False, rin=1.0, bg=bg, kalman=True)
simulation_orb_r3 = TrackingSim(numpoints=numpoints, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                                feedback=ffreq, iscat=False, debug=False, rin=1.3, bg=bg, kalman=True)
simulation_orb_r4 = TrackingSim(numpoints=numpoints, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                                feedback=ffreq, iscat=False, debug=False, rin=1.6, bg=bg, kalman=True)

simulation_kt_r1 = TrackingSim(numpoints=numpoints, method='knight', freq=freq, amp=24.0, waist=0.4, tracking=True,
                               feedback=ffreq, debug=False, rin=3.5, bg=bg, kalman=True)
simulation_kt_r2 = TrackingSim(numpoints=numpoints, method='knight', freq=freq, amp=24.0, waist=0.4, tracking=True,
                               feedback=ffreq, debug=False, rin=4.0, bg=bg, kalman=True)
simulation_kt_r3 = TrackingSim(numpoints=numpoints, method='knight', freq=freq, amp=24.0, waist=0.4, tracking=True,
                               feedback=ffreq, debug=False, rin=6.0, bg=bg, kalman=True)
simulation_kt_r4 = TrackingSim(numpoints=numpoints, method='knight', freq=freq, amp=24.0, waist=0.4, tracking=True,
                               feedback=ffreq, debug=False, rin=8.0, bg=bg, kalman=True)

simulation_mf_r1 = TrackingSim(numpoints=numpoints, method='minflux', freq=freq, amp=45.0, L=0.05, tracking=True,
                            feedback=ffreq, debug=False, rin=0.001, fwhm=0.36, bg=bg, kalman=True)
simulation_mf_r2 = TrackingSim(numpoints=numpoints, method='minflux', freq=freq, amp=45.0, L=0.05, tracking=True,
                            feedback=ffreq, debug=False, rin=0.004, fwhm=0.36, bg=bg, kalman=True)
simulation_mf_r3 = TrackingSim(numpoints=numpoints, method='minflux', freq=freq, amp=45.0, L=0.05, tracking=True,
                            feedback=ffreq, debug=False, rin=0.01, fwhm=0.36, bg=bg, kalman=True)
simulation_mf_r4 = TrackingSim(numpoints=numpoints, method='minflux', freq=freq, amp=45.0, L=0.05, tracking=True,
                            feedback=ffreq, debug=False, rin=0.02, fwhm=0.36, bg=bg, kalman=True)

numdiffs = 8
numruns = 10

diffs = np.logspace(-4, 0, numdiffs)


def parr_func(i, D, method):
    errsum = 0
    for j in range(numruns):
        print('diff # ', i+1, 'of ', numdiffs)
        print('run # ', j+1, 'of ', numruns)
        if method == 'orb1':
            err, measx, truex, measy, truey, intvals = simulation_orb_r1.main_tracking(D)
        elif method == 'orb2':
            err, measx, truex, measy, truey, intvals = simulation_orb_r2.main_tracking(D)
        elif method == 'orb3':
            err, measx, truex, measy, truey, intvals = simulation_orb_r2.main_tracking(D)
        elif method == 'orb4':
            err, measx, truex, measy, truey, intvals = simulation_orb_r4.main_tracking(D)
        elif method == 'kt1':
            err, measx, truex, measy, truey, intvals = simulation_kt_r1.main_tracking(D)
        elif method == 'kt2':
            err, measx, truex, measy, truey, intvals = simulation_kt_r2.main_tracking(D)
        elif method == 'kt3':
            err, measx, truex, measy, truey, intvals = simulation_kt_r2.main_tracking(D)
        elif method == 'kt4':
            err, measx, truex, measy, truey, intvals = simulation_kt_r4.main_tracking(D)
        elif method == 'mf1':
            err, measx, truex, measy, truey, intvals = simulation_mf_r1.main_tracking(D)
        elif method == 'mf2':
            err, measx, truex, measy, truey, intvals = simulation_mf_r2.main_tracking(D)
        elif method == 'mf3':
            err, measx, truex, measy, truey, intvals = simulation_mf_r3.main_tracking(D)
        elif method == 'mf4':
            err, measx, truex, measy, truey, intvals = simulation_mf_r4.main_tracking(D)
        errsum += err
    return errsum / numruns


# errs_orb1 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'orb1') for i, D in enumerate(diffs))
# errs_orb2 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'orb2') for i, D in enumerate(diffs))
# errs_orb3 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'orb3') for i, D in enumerate(diffs))
# errs_orb4 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'orb4') for i, D in enumerate(diffs))
errs_kt1 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'kt1') for i, D in enumerate(diffs))
errs_kt2 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'kt2') for i, D in enumerate(diffs))
errs_kt3 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'kt3') for i, D in enumerate(diffs))
errs_kt4 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'kt4') for i, D in enumerate(diffs))
# errs_mf1 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'mf1') for i, D in enumerate(diffs))
# errs_mf2 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'mf2') for i, D in enumerate(diffs))
# errs_mf3 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'mf3') for i, D in enumerate(diffs))
# errs_mf4 = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'mf4') for i, D in enumerate(diffs))

# errs_mf = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'mf') for i, D in enumerate(diffs))
# errs_kt = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i, D, 'kt') for i, D in enumerate(diffs))
# np.savetxt('files/errs_orb_r1.txt', errs_orb1)
# np.savetxt('files/errs_orb_r2.txt', errs_orb2)
# np.savetxt('files/errs_orb_r3.txt', errs_orb3)
# np.savetxt('files/errs_orb_r4.txt', errs_orb4)
# np.savetxt('files/errs_kt_r1.txt', errs_kt1)
# np.savetxt('files/errs_kt_r2.txt', errs_kt2)
# np.savetxt('files/errs_kt_r3.txt', errs_kt3)
# np.savetxt('files/errs_kt_r4.txt', errs_kt4)
np.savetxt('files/errs_kt_r1.txt', errs_mf1)
np.savetxt('files/errs_kt_r2.txt', errs_mf2)
np.savetxt('files/errs_kt_r3.txt', errs_mf3)
np.savetxt('files/errs_kt_r4.txt', errs_mf4)

untracked = np.sqrt(200 * diffs)

# cutoff = np.pi * (0.4 / np.sqrt(2)) ** 2 * 0.1
# cutoff = np.pi * 0.025 ** 2 * 0.1

plt.loglog(diffs, errs_mf1, '-o', label='r=0.001')
plt.loglog(diffs, errs_mf2, '-o', label='r=0.004')
plt.loglog(diffs, errs_mf3, '-o', label='r=0.01')
plt.loglog(diffs, errs_mf4, '-o', label='r=0.02')

# plt.loglog(diffs, errs, '-o')
# plt.loglog(diffs, errs_mf, '-o')
# plt.loglog(diffs, errs_kt, '-o')
# plt.loglog(diffs, untracked, '--', color='gray')
# plt.axvline(cutoff)
plt.legend()
plt.show()
