# Script that does 2 simulation runs to demonstrate good and bad tracking.
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from sim_module import TrackingSim
import rsmf

# col_width = 345  # For dissertation I think
col_width = 470  # For journal draft

formatter = rsmf.CustomFormatter(columnwidth=col_width * 0.01389, fontsizes=10,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})
matplotlib.rcParams.update({'font.family': 'serif'})

freq = 12.5
ffreq = 3.125
simulate = False

if simulate:
    simulation_orb = TrackingSim(numpoints=500000, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                                 feedback=ffreq, iscat=False, rin=0.04, bg=0)

    # err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.0001)
    err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.0052)

    binnedints = np.zeros(250)
    for i, val in enumerate(binnedints):
        binnedints[i] = np.sum(intvals[2000 * i:2000 * (i + 1)])

    print(np.mean(intvals))
    print('average intensity:', np.sum(intvals) / 100, ' counts/ms')
    print('Meas variance:', np.std(measx) ** 2)
    print(err)

    savearr = np.column_stack([measx[::200], truex[::200], measy[::200], truey[::200]])
    np.savetxt('trajectory.txt', savearr)
    np.savetxt('intensity.txt', binnedints)

else:
    traj = np.loadtxt('trajectory_good.txt')
    binnedints = np.loadtxt('intensity_good.txt')
    measx, truex, measy, truey = traj[:, 0], traj[:, 1], traj[:, 2], traj[:, 3]

t = np.linspace(0, 500, 250)

fig = formatter.figure(width_ratio=0.7, aspect_ratio=0.8)
spec = matplotlib.gridspec.GridSpec(ncols=1, nrows=3)
ax1 = fig.add_subplot(spec[0, 0])
ax2 = fig.add_subplot(spec[1, 0], sharex=ax1)
ax3 = fig.add_subplot(spec[2, 0], sharex=ax1)
ax1.plot(t, measx[::10])
ax1.plot(t, truex[::10])
ax2.plot(t, measy[::10])
ax2.plot(t, truey[::10])
ax3.plot(t, binnedints / 2)
ax3.set_ylim((0, None))

ax3.set_xlabel('Time (ms)')
ax1.set_ylabel(r'$x$ Position ($\mathrm{\mu}$m)')
ax2.set_ylabel(r'$y$ Position ($\mathrm{\mu}$m)')
ax3.set_ylabel('Intensity (kcounts/s)')

plt.savefig('../out/traj_ex_good.pdf')

# plt.show()

