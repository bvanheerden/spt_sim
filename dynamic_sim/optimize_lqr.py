# This script is designed to try to optimize the LQR weights by minimizing the error
from matplotlib import pyplot as plt
from sim_module import TrackingSim
import numpy as np
import scipy
import joblib


def minfunc(weights):
    print(weights)

    simulation_orb = TrackingSim(numpoints=10000, method='orbital', freq=12.5, amp=5.0, waist=0.4, tracking=True,
                                 feedback=12.5, iscat=False, kalman=True, lqr=True, rin=0.1,
                                 weights=np.insert(weights, 0, 0.0145))

    def parr_func(i):
        try:
            err, measx, truex, kalmx, stagex, measy, truey, kalmy, stagey, intvals = simulation_orb.main_tracking(0.05)
        except:
            return 10
        return err

    errs = joblib.Parallel(n_jobs=6)(joblib.delayed(parr_func)(i) for i in range(18))

    # try:
    #     err1, measx, truex, kalmx, stagex, measy, truey, kalmy, stagey, intvals = simulation_orb.main_tracking(0.05)
    #     err2, measx, truex, kalmx, stagex, measy, truey, kalmy, stagey, intvals = simulation_orb.main_tracking(0.05)
    #     err3, measx, truex, kalmx, stagex, measy, truey, kalmy, stagey, intvals = simulation_orb.main_tracking(0.05)
    #     err4, measx, truex, kalmx, stagex, measy, truey, kalmy, stagey, intvals = simulation_orb.main_tracking(0.05)
    #     err5, measx, truex, kalmx, stagex, measy, truey, kalmy, stagey, intvals = simulation_orb.main_tracking(0.05)
    # except:
    #     return 5
    #
    # print(np.sum(err1) + np.sum(err2) + np.sum(err3) + np.sum(err4) + np.sum(err5))
    # return np.sum(err1) + np.sum(err2) + np.sum(err3) + np.sum(err4) + np.sum(err5)
    print(np.sum(errs))
    return np.sum(errs)


# res = scipy.optimize.minimize(minfunc, [0.007, 1, 1, 1], bounds=[(0.005, 0.01), (0, 2), (0, 2), (0, 2)])
# print(res.x)
# res = scipy.optimize.minimize(minfunc, 0.008, bounds=[(0.001, 0.01)])
# print(res.x)

# res = scipy.optimize.basinhopping(minfunc, [0.007, 1, 1, 1], stepsize=1, T=10)
# print(res.x)
res = scipy.optimize.dual_annealing(minfunc, bounds=[(0, 10), (0, 10), (0, 10)])
print(res.x)
# res = scipy.optimize.dual_annealing(minfunc, bounds=[(0, 0.1)])
# print(res.x)

# x0 = scipy.optimize.brute(minfunc, ranges=((0.005, 0.01), (0, 10), (0, 10), (0, 10)), Ns=5, finish=None)
# print(x0)
