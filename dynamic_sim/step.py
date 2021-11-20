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

G = control.tf([2, 1], [1, 2, 1])

t, yout = control.step_response(G, np.linspace(0, 8, num=200))
# plt.figure(figsize=[9.0, 6.0])
fig = formatter.figure(width_ratio=0.6)
plt.plot(t, 100 * yout)
plt.ylabel('Percent of input (%)')
plt.xlabel('Time (ms)')
plt.tight_layout()
plt.savefig('../out/step_art.pdf')