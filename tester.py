# Simple test script that does 1 simulation run
from matplotlib import pyplot as plt
from sim_module import TrackingSim

simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=12.5, amp=5.0, waist=0.4, tracking=True,
                             feedback=1, iscat=True)
# simulation_orb = TrackingSim(numpoints=100000, method='minflux', freq=12.5, amp=80.0, L=0.05, tracking=True, feedback=1)

err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.00001)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
ax1.plot(measx[::10])
ax1.plot(truex[::10])
ax2.plot(measy[::10])
ax2.plot(truey[::10])
ax3.plot(intvals[::10])
plt.show()
