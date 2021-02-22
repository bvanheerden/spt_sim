# This script seems to not have been a good idea
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import joblib
from sim_module import TrackingSim

feedbacks = np.logspace(-1, 5, 12)
errs2d = np.zeros((12, 12))
for i, feedback in enumerate(feedbacks):
    print(i)
    simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=10, amp=5.0, waist=0.4, tracking=True,
                                 feedback=10)

    diffs = np.logspace(-5, 2, 12)


    def parr_func(i, D, method):
        err, measx, truex, measy, truey = simulation_orb.main_tracking(D)
        return err


    errs = joblib.Parallel(n_jobs=6)(joblib.delayed(parr_func)(i, D, 'orb') for i, D in enumerate(diffs))
    errs2d[:, i] = errs

print(errs2d)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# ax.set_xscale('log')
# ax.set_yscale('log')
ax.set_zscale('log')
X, Y = np.meshgrid(feedbacks, diffs)
ax.plot_surface(X, Y, errs2d)

plt.show()
