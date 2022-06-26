# Simple test script that does 1 simulation run
import joblib
from matplotlib import pyplot as plt
import numpy as np
from sim_module import TrackingSim

freq = 8.3333333
ffreq = 8.3333333

rvals = [0.1, 0.2, 0.3, 0.5, 0.7, 1., 1.2, 1.5]
# rvals = [1.0, 1.5, 1.7, 2., 2.2, 2.5, 3.0, 3.3]  # knigths tour
# rvals = [0.001, 0.002, 0.005, 0.007, 0.01, 0.02, 0.05, 0.07]  # minflux

D = 0.02
# D = 1e-5  # minflux


def parr_func(rval):
    simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                                 feedback=ffreq, iscat=False, rin=rval, bg=0, kalman=True)#.00125)
    # simulation_orb = TrackingSim(numpoints=100000, method='knight',freq=freq, amp=24.0, waist=0.4, tracking=True,
    #                              feedback=ffreq, iscat=False, rin=rval, stage=True, kalman=True)
    # simulation_orb = TrackingSim(numpoints=100000, method='minflux', freq=freq, amp=45.0, L=0.05, tracking=True,
    #                              feedback=ffreq, rin=rval, fwhm=0.36)
    err1, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(D)
    print('1')
    err2, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(D)
    print('2')
    err3, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(D)
    print('3')
    err4, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(D)
    print('4')
    err5, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(D)
    print('5')
    err = np.mean([err1, err2, err3, err4, err5])
    print(rval, err)
    return err


errs = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(rval) for rval in rvals)

plt.plot(rvals, errs)
plt.show()
