# Simple test script that does 1 simulation run
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
from sim_module import TrackingSim
import scipy.signal
import rsmf

formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=10,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')
matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

freq = 12.5
ffreq = 12.5
ffreq = 3.125
# freq = 3.125

# simulation_orb = TrackingSim(numpoints=100000, method='knight', freq=freq, amp=24.0, waist=0.4, tracking=True,
#                              feedback=ffreq, iscat=False, rin=10)
# simulation_orb = TrackingSim(numpoints=10000, method='minflux', freq=freq, amp=320.0, L=0.05, tracking=True,
#                              feedback=ffreq, rin=1, fwhm=0.36)

good_tracking = True

if good_tracking:
    simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                                 feedback=ffreq, iscat=False, rin=500, lqr=True, weights=[10, 1, 1, 1])
    # err, measx, truex, measy, truey, intvals, stagex, stagey = simulation_orb.main_tracking(0.00001)
    err, measx, truex, measy, truey, intvals, stagex, stagey = simulation_orb.main_tracking(0.001)
    filename = 'out/good_tracking_art.pdf'
else:
    simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                                 feedback=ffreq, iscat=False, rin=10, lqr=True, weights=[1, 1, 1, 1])
    err, measx, truex, measy, truey, intvals, stagex, stagey = simulation_orb.main_tracking(0.02)
    # err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.1)
    filename = 'out/bad_tracking_art.pdf'

print('average intensity:', np.mean(intvals))

fig = formatter.figure(width_ratio=0.9)
ax1, ax2, ax3 = fig.subplots(3, 1, sharex=True)
# ax1.plot(measx[::100])
ax1.plot(truex[::100])
ax1.plot(stagex[::100])
# ax2.plot(measy[::100])
ax2.plot(truey[::100])
ax2.plot(stagey[::100])

intvals = scipy.signal.resample(intvals, 1000)
intvals = np.clip(intvals, 0, None)
intvals *= 1000

ax3.plot(intvals)

ax1.set_ylabel(r'X (\textmu m)')
ax2.set_ylabel(r'Y (\textmu m)')
ax3.set_xlabel('Time (ms)')
ax3.set_ylabel('Intensity (counts/ms)')

plt.tight_layout()
# plt.savefig(filename)

# plt.show()
