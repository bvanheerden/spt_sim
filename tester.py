# Simple test script that does 1 simulation run
from matplotlib import pyplot as plt
from sim_module import TrackingSim

simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=10, amp=5.0, waist=0.4, tracking=True, feedback=1)
err, measx, truex, measy, truey = simulation_orb.main_tracking(0.001)

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1.plot(measx)
ax1.plot(truex)
ax2.plot(measy)
ax2.plot(truey)
plt.show()
