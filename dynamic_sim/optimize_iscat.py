# Simple test script that does 1 simulation run
from matplotlib import pyplot as plt
import numpy as np
from sim_module import TrackingSim
from scipy.optimize import brute
import os

freq = 12.5
ffreq = 3.125
# freq = 3.125

samples = ['lhcii', 'lhcii-mic', 'pb', 'gfp', 'hiv-qd']

adjusted = True

if adjusted:
    intfactors = [0.91, 4.0, 1.3, 2.0, 88548]
    contrasts = [4.75e-5, 2.09e-4, 4.00e-3, 6.36e-6, 0.90]
else:
    intfactors = [3.1, 13.5, 2.1, 5.3, 88548]
    contrasts = [1.61e-4, 7.07e-4, 6.53e-3, 1.71e-5, 0.90]

sample = 3
rvals = [0.008, 0.001, 0.0005, 0.1, 0.0005]
intfactor = intfactors[sample]
contrast = contrasts[sample]


def min_func(rin):
    rin = 10 ** rin
    simulation_orb_iscat = TrackingSim(numpoints=100000, method='orbital', freq=freq, amp=5.0, waist=0.4,
                                       tracking=True, feedback=ffreq, iscat=True, debug=False, rin=rin,
                                       intfactor=intfactor, contrast=contrast, adjustment=1000, avint=0.0124)
    errs = []
    for i in range(10):
        print(i)
        err, measx, truex, measy, truey, intvals = simulation_orb_iscat.main_tracking(0.00001)
        errs.append(err)

    print(rin)
    print(np.mean(errs))
    return np.mean(errs)


x0 = brute(min_func, [(-3, 1)], Ns=10, finish=None)
print(10 ** x0)
duration = 1  # seconds
freq = 440  # Hz
os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))




