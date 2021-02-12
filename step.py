import control
from matplotlib import pyplot as plt
from matplotlib import rc
import matplotlib
import numpy as np
import rsmf

# formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=10,
#                                  pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

# matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})
# rc('text', usetex=False)
matplotlib.rcParams.update({'font.size': 14})

G = control.tf([2, 1], [1, 2, 1])

t, yout = control.step_response(G, np.linspace(0, 8, num=200))
plt.figure(figsize=[6.0, 4.0], dpi=300)
# fig = formatter.figure(width_ratio=0.6)
plt.plot(t, 100 * yout, linewidth=2)
plt.ylabel('Percent of input (\%)')
plt.xlabel('Time (ms)')
plt.tight_layout()
plt.savefig('out/step_art.png')
plt.show()