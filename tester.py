# Simple test script that does 1 simulation run
from matplotlib import pyplot as plt
import matplotlib
from sim_module import TrackingSim
import numpy as np

matplotlib.rcParams.update({'font.size': 12})

simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=12.5, amp=4.0, waist=0.4, tracking=True,
                             feedback=12.5, iscat=False, kalman=True, lqr=True)#, rin=0.1, weights=[0.1, 1, 1, 1])
# simulation_orb = TrackingSim(numpoints=10000, method='minflux', freq=12.5, amp=80.0, L=0.05, tracking=True,
#                              feedback=12.5, iscat=False, kalman=True, lqr=False)#, rin=0.1, weights=[0.1, 1, 1, 1])
# simulation_orb = TrackingSim(numpoints=100000, method='minflux', freq=12.5, amp=80.0, L=0.05, tracking=True, feedback=12.5, kalman=False, lqr=False)

err, measx, truex, kalmx, stagex, measy, truey, kalmy, stagey, intvals = simulation_orb.main_tracking(0.0001)

tvals = np.linspace(0, 100, 1000)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(8, 5), dpi=150)
# ax1.plot(measx[::10])
ax1.plot(tvals, truex[::100])
ax1.plot(tvals, stagex[::100])
# ax1.plot(kalmx[::10])
# ax2.plot(measy[::10])
ax2.plot(tvals, truey[::100])
ax2.plot(tvals, stagey[::100])
ax3.plot(tvals, intvals[::100])
# ax3.axhline(np.mean(intvals))

ax3.set_xlabel('Time (ms)')
ax1.set_ylabel(r'X Position (\textmu m)')
ax2.set_ylabel(r'Y Position (\textmu m)')
ax3.set_ylabel(r'Intensity (counts/ms)')
fig.align_ylabels()

print(np.mean(intvals))
plt.show()

# print(np.sum(err))
# plt.figure(figsize=(9, 3))
# plt.plot(truex[::])
# # plt.plot(measx[::10])
# # plt.plot(kalmx[::10])
# plt.plot(stagex[::])
# plt.show()
