# Script that does 2 simulation runs to demonstrate good and bad tracking.
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from sim_module import TrackingSim
import rsmf

# plt.rc('text', usetex=True)

# col_width = 345  # For dissertation I think
# col_width = 470  # For journal draft (Interface)
col_width = 510  # For journal draft (JCP)

color_list = ['#1d6996', '#73af48', '#edad08', '#e17c05', '#cc503e', '#94346e', '#6f4070']
# color_list = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33']
# plt.rcParams['axes.prop_cycle'] = plt.cycler(color=sns.color_palette())
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

formatter = rsmf.CustomFormatter(columnwidth=col_width * 0.01389, fontsizes=10,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc} \usepackage{amsfonts} \usepackage{siunitx}')

# plt.rc('text.latex', preamble=r'\usepackage{upgreek}')
matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})
matplotlib.rcParams.update({'font.family': 'serif'})

freq = 8.333333333
ffreq = freq
simulate = False

if simulate:
    simulation_orb = TrackingSim(numpoints=500000, method='orbital', freq=freq, amp=5.0, waist=0.4, tracking=True,
                                 feedback=ffreq, iscat=False, rin=0.5, bg=0)

    # err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.0001)
    err, measx, truex, measy, truey, intvals = simulation_orb.main_tracking(0.02)

    binnedints = np.zeros(250)
    for i, val in enumerate(binnedints):
        binnedints[i] = np.sum(intvals[2000 * i:2000 * (i + 1)])

    print(np.mean(intvals))
    print('average intensity:', np.sum(intvals) / 100, ' counts/ms')
    print('Meas variance:', np.std(measx) ** 2)
    print(err)

    savearr = np.column_stack([measx[::200], truex[::200], measy[::200], truey[::200]])
    np.savetxt('trajectory_almost.txt', savearr)
    np.savetxt('intensity_almost.txt', binnedints)

    # traj_good = np.loadtxt('trajectory_good.txt')
    # binnedints_good = np.loadtxt('intensity_good.txt')
    # measx_good, truex_good, measy_good, truey_good = traj_good[:, 0], traj_good[:, 1], traj_good[:, 2], traj_good[:, 3]
    # traj_almost = np.loadtxt('trajectory_almost.txt')
    # binnedints_almost = np.loadtxt('intensity_almost.txt')
    # measx_almost, truex_almost, measy_almost, truey_almost = traj_almost[:, 0], traj_almost[:, 1], traj_almost[:, 2], \
    #                                                          traj_almost[:, 3]
    #
# else:

traj_good = np.loadtxt('trajectory_good.txt')
binnedints_good = np.loadtxt('intensity_good.txt')
measx_good, truex_good, measy_good, truey_good = traj_good[:, 0], traj_good[:, 1], traj_good[:, 2], traj_good[:, 3]
traj_almost = np.loadtxt('trajectory_almost.txt')
binnedints_almost = np.loadtxt('intensity_almost.txt')
measx_almost, truex_almost, measy_almost, truey_almost = traj_almost[:, 0], traj_almost[:, 1], traj_almost[:, 2], \
                                                         traj_almost[:, 3]

t = np.linspace(0, 500, 250)
t_ins = np.linspace(0, 500, 2500)  # t values for insert plot

fig = formatter.figure(width_ratio=0.9, aspect_ratio=0.6)
spec = matplotlib.gridspec.GridSpec(ncols=2, nrows=3)
ax1 = fig.add_subplot(spec[0, 0])
ax2 = fig.add_subplot(spec[1, 0], sharex=ax1)
ax3 = fig.add_subplot(spec[2, 0], sharex=ax1)
ax4 = fig.add_subplot(spec[0, 1])
ax5 = fig.add_subplot(spec[1, 1], sharex=ax4)
ax6 = fig.add_subplot(spec[2, 1], sharex=ax4)

ax1.plot(t, measx_good[::10], color='C0', label='Particle position')
ax1.plot(t, truex_good[::10], '--', color='C3', label='Stage position')
ax2.plot(t, measy_good[::10], color='C0')
ax2.plot(t, truey_good[::10], '--', color='C3')
ax3.plot(t, binnedints_good / 2)
ax3.set_ylim((0, None))
ax3.set_xlim((0, 500))

ax4.plot(t, measx_almost[::10])
ax4.plot(t, truex_almost[::10], '--', color='C3')
ax5.plot(t, measy_almost[::10])
ax5.plot(t, truey_almost[::10], '--', color='C3')
ax6.plot(t, binnedints_almost / 2)
ax6.set_ylim((0, None))
ax6.set_xlim((0, 500))

# axin = ax5.inset_axes([0.4, 0.55, 0.3, 0.4])
# axin.plot(t_ins[1400:1700], measy_almost[1400:1700])
# axin.plot(t_ins[1400:1700], truey_almost[1400:1700], '--', color='C3')
# axin.set_xticklabels([])
# axin.set_yticklabels([])
# ax5.indicate_inset_zoom(axin, edgecolor='black')

ax1.tick_params(axis='x', labelbottom=False)
ax2.tick_params(axis='x', labelbottom=False)
ax4.tick_params(axis='x', labelbottom=False)
ax5.tick_params(axis='x', labelbottom=False)

ax3.set_xlabel('Time (ms)')
ax6.set_xlabel('Time (ms)')
ax1.set_ylabel(r'$x$ position (\SI{}{\micro\meter})')
ax2.set_ylabel(r'$y$ position (\SI{}{\micro\meter})')
ax3.set_ylabel('Intensity (kcounts/s)')
# fig.legend()

# ax1.set_title(r'$D=0.1\mathrm{\mu}\mathrm{m}\cdot\mathrm{s}^{-1}')
ax1.set_title(r'$D=\SI{0.1}{\micro\meter\squared\per\second}')
ax4.set_title(r'$D=\SI{20}{\micro\meter\squared\per\second}')

fig.subplots_adjust(hspace=0.0)
plt.tight_layout()
plt.savefig('../out/traj_ex_combined.pdf')

# plt.show()

