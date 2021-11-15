# Simple test script that does 1 simulation run
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from sim_module import TrackingSim
matplotlib.rcParams['text.usetex'] = False

freq = 12.5
ffreq = 3.125
# freq = 3.125

samples = ['lhcii', 'lhcii-mic', 'pb', 'gfp', 'hiv-qd']

adjusted = False

if adjusted:
    intfactors = [0.91, 4.0, 1.3, 2.0, 88548]
    contrasts = [4.75e-5, 2.09e-4, 4.00e-3, 6.36e-6, 0.90]
else:
    intfactors = [3.1, 13.5, 2.1, 5.3, 88548]
    contrasts = [1.61e-4, 7.07e-4, 6.53e-3, 1.71e-5, 0.90]

sample = 2
rvals = [0.04, 0.05, 0.2, 0.04, 0.04]
intfactor = intfactors[sample]
contrast = contrasts[sample]
rin = rvals[sample]

simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                             feedback=ffreq, iscat=False, rin=0.04, bg=0)#.00125)
# simulation_orb = TrackingSim(numpoints=10000, method='knight', freq=freq, amp=24.0, waist=0.4, tracking=True,
#                              feedback=ffreq, iscat=False, rin=0.3, stage=True, kalman=True)
# simulation_orb = TrackingSim(numpoints=10000, method='minflux', freq=freq, amp=45.0, L=0.05, tracking=True,
#                              feedback=ffreq, rin=0.004, fwhm=0.36)
simulation_orb_iscat = TrackingSim(numpoints=100000, method='orbital', freq=freq, amp=5.0, waist=0.4,
                                   tracking=True, feedback=ffreq, iscat=True, debug=False, rin=rin,
                                   intfactor=intfactor, contrast=contrast, adjustment=1000, avint=0.0124)

# err, measx, truex, measy, truey, intvals = simulation_orb_iscat.main_tracking(2.5e-6)

# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(1e-5)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.0001)
# err, measx, truex, measy, truey, intvals = simulation_orb_iscat.main_tracking(0.0001)
err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.001)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.01)
# err, measx, truex, measy, truey, intvals = simulation_orb_iscat.main_tracking(0.0001)
# err, measx, truex, measy, truey, intvals = simulation_orb_iscat.main_tracking(0.1)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.1)

# binnedints = np.zeros(100)
# for i in range(100):
#         binnedints[i] = np.sum(intvals[1000 * i:1000 * (i + 1)])

print(np.mean(intvals))
print('average intensity:', np.sum(intvals) / 100, ' counts/ms')
print('Meas variance:', np.std(measx) ** 2)
print(err)

# plt.xkcd()
fig, ax1 = plt.subplots(1, 1, sharex=True)
fig.patch.set_visible(False)
ax1.patch.set_visible(False)
ax1.axis('off')
ax1.plot(measx[::20], color='#808080', lw='3')
ax1.plot(truex[::20], color='#ea6410', lw='2')
plt.show()

# plt.plot(binnedints)
# plt.show()