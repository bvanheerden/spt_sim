# Simple test script that does 1 simulation run
from matplotlib import pyplot as plt
import numpy as np
from sim_module import TrackingSim

freq = 12.5
ffreq = 3.125
# freq = 3.125

simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                             feedback=ffreq, iscat=False, rin=0.04, bg=0.00125)
# simulation_orb = TrackingSim(numpoints=100000, method='knight', freq=freq, amp=24.0, waist=0.4, tracking=True,
#                              feedback=ffreq, iscat=False, rin=0.3, stage=True, kalman=True)
# simulation_orb = TrackingSim(numpoints=100000, method='minflux', freq=freq, amp=45.0, L=0.05, tracking=True,
#                              feedback=ffreq, rin=0.1, fwhm=0.36)

err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(1e-7)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.0001)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.001)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.01)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.1)

# binnedints = np.zeros(100)
# for i in range(100):
#         binnedints[i] = np.sum(intvals[1000 * i:1000 * (i + 1)])

print(np.mean(intvals))
print('average intensity:', np.sum(intvals) / 100, ' counts/ms')
print('Meas variance:', np.std(measx) ** 2)
print(err)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
ax1.plot(measx[::10])
ax1.plot(truex[::10])
ax2.plot(measy[::10])
ax2.plot(truey[::10])
ax3.plot(intvals[::10])
plt.show()

# plt.plot(binnedints)
# plt.show()
