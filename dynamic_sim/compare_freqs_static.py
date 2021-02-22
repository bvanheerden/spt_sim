# Compares the "tracking" of a static particle for two different bandwidths
import numpy as np
from matplotlib import pyplot as plt
from sim_module import TrackingSim

b1 = 10
b2 = 50

simulation_orb_10 = TrackingSim(numpoints=10000, method='orbital', freq=b1, amp=5.0, waist=0.4, tracking=False)
err, measx, truex, measy, truey = simulation_orb_10.main_tracking(0)
sigma10 = np.std(measx)
print("sigma10 = ", sigma10)

simulation_orb_50 = TrackingSim(numpoints=10000, method='orbital', freq=b2, amp=5.0, waist=0.4, tracking=False)
err50, measx50, truex50, measy50, truey50 = simulation_orb_50.main_tracking(0)
sigma50 = np.std(measx50)
print("sigma50 = ", sigma50)
print("sigma50/sigma10 = ", sigma50 / sigma10)
print(np.sqrt(b2 / b1))

hist10, bins = np.histogram(measx, bins=20, density=True)
hist50, bins50 = np.histogram(measx50, bins=20, density=True)

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ax1.plot(measx50)
ax1.plot(measx)
ax2.plot(hist50, bins50[:-1])
ax2.plot(hist10, bins[:-1])
plt.show()
