# This script is designed to try to optimize the LQR weights by minimizing the error
from matplotlib import pyplot as plt
from sim_module import TrackingSim
import numpy as np
import scipy
import joblib

freq = 12.5
ffreq = 3.125


def minfunc(weights):

    weights = 10 ** weights
    # weights = [1.0, weights[0]]
    weights = [weights[0], 0.001]
    print(weights)

    simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                                 feedback=ffreq, iscat=False, rin=0.04, r=weights, debug=False)
    # simulation_orb = TrackingSim(numpoints=100000, method='minflux', freq=freq, amp=45.0, L=0.1, tracking=True,
    #                             feedback=ffreq, debug=False, rin=weights, fwhm=0.36)
    # simulation_orb = TrackingSim(numpoints=100000, method='knight', freq=freq, amp=24.0, waist=0.4, tracking=True,
    #                              feedback=ffreq, debug=False, rin=0.3, r=weights)

    def parr_func(i):
        try:
            # err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.000001)
            # err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.01)  # KT
            err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.001)  # orb
            # err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.0001)  # mf
            # err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(1e-5)  # mf slow
        except:
            raise
            return 10
        return err

    errs = joblib.Parallel(n_jobs=8)(joblib.delayed(parr_func)(i) for i in range(8))

    print(np.sum(errs))
    return np.sum(errs)


# x = scipy.optimize.brute(minfunc, ranges=[(0.01, 1)], finish=None)  # kalman filter orb
# x = scipy.optimize.brute(minfunc, ranges=[(0.005, 0.05)], finish=None)  # kalman filter mf
# x = scipy.optimize.brute(minfunc, ranges=[(-4, -1)], finish=None)  # kalman filter mf slow exp
# x = scipy.optimize.brute(minfunc, ranges=[(-2, 0)], finish=None)  # kalman filter KT exp
# x = scipy.optimize.brute(minfunc, ranges=[(-4, -2)], finish=None)  # i gain exp
x = scipy.optimize.brute(minfunc, ranges=[(-0.3, 0.5)], finish=None)  # p gain exp
print(x)
