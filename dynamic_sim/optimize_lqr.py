# This script is designed to try to optimize the LQR weights by minimizing the error
from matplotlib import pyplot as plt
from sim_module import TrackingSim
import numpy as np
import scipy
import joblib

freq = 12.5
ffreq = 3.125


def minfunc(weights):

    weights = [2.0, weights[0]]
    # weights = [weights[0], 0.0006]
    print(weights)

    simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                                 feedback=ffreq, iscat=False, rin=0.1, r=weights, debug=False)
    # simulation_orb = TrackingSim(numpoints=50000, method='minflux', freq=freq, amp=45.0, L=0.1, tracking=True,
    #                             feedback=ffreq, debug=False, rin=0.001, fwhm=0.36, r=weights)
    # simulation_orb = TrackingSim(numpoints=100000, method='knight', freq=freq, amp=24.0, waist=0.4, tracking=True,
    #                              feedback=ffreq, debug=False, rin=1, r=weights)

    def parr_func(i):
        try:
            err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.000001)
        except:
            raise
            return 10
        return err

    errs = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i) for i in range(8))

    print(np.sum(errs))
    return np.sum(errs)


x = scipy.optimize.brute(minfunc, ranges=[(0.0001, 0.01)], finish=None)
# x = scipy.optimize.brute(minfunc, ranges=[(0.5, 3)], finish=None)
print(x)
