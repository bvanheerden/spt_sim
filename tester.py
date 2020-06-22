# Simple test script that does 1 simulation run
from matplotlib import pyplot as plt
from sim_module import TrackingSim
import numpy as np

simulation_orb = TrackingSim(numpoints=10000, method='orbital', freq=12.5, amp=5.0, waist=0.4, tracking=True,
                             feedback=12.5, iscat=False, kalman=True, lqr=True, rin=0.1, weights=[0.1, 10, 1.3, 10])
# simulation_orb = TrackingSim(numpoints=100000, method='minflux', freq=12.5, amp=80.0, L=0.05, tracking=True, feedback=1)

err, measx, truex, kalmx, stagex, measy, truey, kalmy, stagey, intvals = simulation_orb.main_tracking(0.09)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
ax1.plot(measx[::10])
ax1.plot(kalmx[::10])
ax1.plot(truex[::10])
ax2.plot(measy[::10])
ax2.plot(truey[::10])
ax3.plot(intvals[::10])
plt.show()

print(np.sum(err))
# plt.figure(figsize=(9, 3))
# plt.plot(truex[::100])
plt.plot(measx[::10])
plt.plot(kalmx[::10])
# plt.plot(stagex[::100])
# plt.show()
