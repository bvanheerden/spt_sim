# Script for making plot for dissertation cover.
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from sim_module import TrackingSim
matplotlib.rcParams['text.usetex'] = False

freq = 12.5
ffreq = 3.125

simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                             feedback=ffreq, iscat=False, rin=0.04, bg=0)

err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.001)

fig, ax1 = plt.subplots(1, 1, sharex=True, figsize=(25, 10), dpi=300)
fig.patch.set_visible(False)
ax1.patch.set_visible(False)
ax1.axis('off')
ax1.plot(measx[::20], color='#808080', lw='7')
ax1.plot(truex[::20], color='#ecc03a', lw='4')
plt.tight_layout()
plt.savefig('/home/bertus/Pictures/voorblad_grafiek.png', transparent=True)
plt.show()

