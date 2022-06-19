import control
from matplotlib import pyplot as plt
from matplotlib import rc
import matplotlib
import numpy as np
import rsmf

# col_width = 345  # For dissertation I think
col_width = 470  # For journal draft
# col_width = 483.7  # For SPIE paper I think
# col_width = 418  # I don't know anymore

formatter = rsmf.CustomFormatter(columnwidth=col_width * 0.01389, fontsizes=10,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})
matplotlib.rcParams.update({'font.family': 'serif'})
# rc('text', usetex=False)
# matplotlib.rcParams.update({'font.size': 14})

# G = control.tf([2, 1], [1, 2, 1])
gain = 1
freq = 1 * 2 * np.pi  # (rad/ms)
damping_ratio = 0.15

e = freq ** 2
c = gain * e
d = damping_ratio * 2 * freq
print(c, d, e)

# G = control.tf([c], [1, d, e])
G = control.tf([40], [1, 2, 40])
state_space = control.ss(G)
print(state_space.A, state_space.B, state_space.C, state_space.D)

G = control.ss([[0, -3.9], [3.9, -2]], [[3.9], [2]], [[0, 1]], [[0]])
# G = control.ss([[-2, -8], [1, 0]], [[8], [0]], [[0, 1]], [[0]])

# mag, phase, omega = control.bode_plot(G, Hz=True, dB=True)
# print(mag)

# plt.plot(omega, mag)
# plt.show()
#
t, yout = control.step_response(G, np.linspace(0, 8, num=200))
# plt.figure(figsize=[9.0, 6.0])
fig = formatter.figure(width_ratio=0.6)
plt.plot(t, 100 * yout)
plt.ylabel('Percent of input (%)')
plt.xlabel('Time (ms)')
plt.tight_layout()
plt.savefig('../out/step_ringing_art.pdf')