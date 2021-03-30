# Simple test script that does 1 simulation run
from matplotlib import pyplot as plt
import numpy as np
from sim_module import TrackingSim

freq = 12.5
ffreq = 3.125
# freq = 3.125

simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                             feedback=ffreq, iscat=False, rin=1, r=[1.8, 0.0037])
# simulation_orb = TrackingSim(numpoints=100000, method='knight', freq=freq, amp=24.0, waist=0.4, tracking=True,
#                              feedback=ffreq, iscat=False, rin=10)
# simulation_orb = TrackingSim(numpoints=10000, method='minflux', freq=freq, amp=320.0, L=0.05, tracking=True,
#                              feedback=ffreq, rin=1, fwhm=0.36)

# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.00007)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.003)
err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.1)

print('average intensity:', np.mean(intvals))
print('Meas variance:', np.std(measx) ** 2)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
ax1.plot(measx[::10])
ax1.plot(truex[::10])
ax2.plot(measy[::10])
ax2.plot(truey[::10])
ax3.plot(intvals[::10])
plt.show()
