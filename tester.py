# Simple test script that does 1 simulation run
from matplotlib import pyplot as plt
import matplotlib
from sim_module import TrackingSim
import numpy as np
import scipy.signal
# import rsmf
#
# formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
#                                  pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')
#
# matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=12.5, amp=4.0, waist=0.4, tracking=True,
                             feedback=12.5, iscat=False, kalman=True, lqr=True, rin=1000, weights=[1, 1, 1, 1])
# simulation_orb = TrackingSim(numpoints=10000, method='minflux', freq=12.5, amp=80.0, L=0.05, tracking=True,
#                              feedback=12.5, iscat=False, kalman=True, lqr=False)#, rin=0.1, weights=[0.1, 1, 1, 1])
# simulation_orb = TrackingSim(numpoints=100000, method='minflux', freq=12.5, amp=80.0, L=0.05, tracking=True, feedback=12.5, kalman=False, lqr=False)

good = False
if good:
    # err, measx, truex, kalmx, stagex, measy, truey, kalmy, stagey, intvals = simulation_orb.main_tracking(0.0001)
    err, measx, truex, kalmx, stagex, measy, truey, kalmy, stagey, intvals = simulation_orb.main_tracking(0.001)
    filename = 'out/good_tracking.pdf'
else:
    err, measx, truex, kalmx, stagex, measy, truey, kalmy, stagey, intvals = simulation_orb.main_tracking(0.03)
    # err, measx, truex, kalmx, stagex, measy, truey, kalmy, stagey, intvals = simulation_orb.main_tracking(0.01)
    filename = 'out/bad_tracking.pdf'

tvals = np.linspace(0, 100, 1000)
# tvals = np.linspace(0, 10, 1000)

# fig = formatter.figure(width_ratio=0.9, aspect_ratio=0.7)
fig = plt.figure()
ax1, ax2, ax3 = fig.subplots(3, 1, sharex=True)
# ax1.plot(measx[::10])
ax1.plot(tvals, truex[::100])
ax1.plot(tvals, stagex[::100])
# ax1.plot(tvals, kalmx[::100])
# ax2.plot(measy[::10])
ax2.plot(tvals, truey[::100])
ax2.plot(tvals, stagey[::100])
# ax3.plot(tvals, intvals[::100])
# tvals = np.linspace(0, 100, 100000)
intvals = scipy.signal.resample(intvals, 1000)  # resample intvals so it's per millisecond
intvals = intvals * 1000  # times 1000 since timestep is 0.001 ms
ax3.plot(tvals, intvals)
# ax3.axhline(np.mean(intvals))

ax3.set_xlabel('Tyd (ms)')
ax1.set_ylabel(r'X Posisie (\textmu m)')
ax2.set_ylabel(r'Y Posisie (\textmu m)')
ax3.set_ylabel(r'Intensiteit (tellings/ms)')
fig.align_ylabels()

print(np.mean(intvals))

plt.tight_layout()
# plt.savefig(filename)

plt.show()

# print(np.sum(err))
# plt.figure(figsize=(9, 3))
# plt.plot(truex[::])
# # plt.plot(measx[::10])
# # plt.plot(kalmx[::10])
# plt.plot(stagex[::])
# plt.show()
