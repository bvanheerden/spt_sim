# Simple test script that does 1 simulation run
from matplotlib import pyplot as plt
import numpy as np
from sim_module import TrackingSim

freq = 12.5
freq = 8.3333333
ffreq = 3.125
ffreq = 8.3333333
# freq = 3.125

samples = ['lhcii', 'lhcii-mic', 'pb', 'gfp', 'hiv-qd']

adjusted = True

if adjusted:
    intfactors = [0.91, 4.0, 1.3, 2.0, 88548]
    contrasts = [4.75e-5, 2.09e-4, 4.00e-3, 6.36e-6, 0.90]
else:
    intfactors = [3.1, 13.5, 2.1, 5.3, 88548]
    contrasts = [1.61e-4, 7.07e-4, 6.53e-3, 1.71e-5, 0.90]

sample = 4
rvals = [0.1, 0.05, 0.05, 0.5, 0.02]
intfactor = intfactors[sample]
contrast = contrasts[sample]
rin = rvals[sample]

# simulation_orb = TrackingSim(numpoints=100000, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
#                              feedback=ffreq, iscat=False, rin=0.5, bg=0, kalman=True)#.00125)
simulation_orb = TrackingSim(numpoints=100000, method='knight',freq=freq, amp=24.0, waist=0.4, tracking=True,
                             feedback=ffreq, iscat=False, rin=1.0, stage=True, kalman=True)
# simulation_orb = TrackingSim(numpoints=100000, method='minflux', freq=freq, amp=45.0, L=0.05, tracking=True,
#                              feedback=ffreq, rin=0.01, fwhm=0.36)
simulation_orb_iscat = TrackingSim(numpoints=100000, method='orbital', freq=freq, amp=5.0, waist=0.4,
                                   tracking=True, feedback=ffreq, iscat=True, debug=False, rin=rin,
                                   intfactor=intfactor, contrast=contrast, adjustment=1000, avint=0.0125)

# err, measx, truex, measy, truey, intvals = simulation_orb_iscat.main_tracking(2.5e-6)

# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(1e-5)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.0001)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.001)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.02)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.05)
err, measx, truex, measy, truey, intvals = simulation_orb_iscat.main_tracking(0.0001)
# err, measx, truex, measy, truey, intvals = simulation_orb_iscat.main_tracking(0.001)
# err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.1)

# binnedints = np.zeros(100)
# for i in range(100):
#         binnedints[i] = np.sum(intvals[1000 * i:1000 * (i + 1)])

print(len(measx))
print(np.mean(intvals))
print('average intensity:', np.sum(intvals) / 100, ' counts/ms')
print('Meas variance:', np.std(measx) ** 2)
print('Tracking err: ', err)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
ax1.plot(measx[::10])
ax1.plot(truex[::10])
ax2.plot(measy[::10])
ax2.plot(truey[::10])
ax3.plot(intvals[::10])
plt.show()

# plt.plot(binnedints)
# plt.show()
