"CRB of orbital method using iSCAT"
import matplotlib
from static_crb.CRB import *
import rsmf

color_list = ['#1d6996', '#73af48', '#edad08', '#e17c05', '#cc503e', '#94346e', '#6f4070']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

col_width = 246  # For journal draft (JCP) - single column
# col_width = 418  # I don't know anymore

formatter = rsmf.CustomFormatter(columnwidth=col_width * 0.01389, fontsizes=10,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

# matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})
matplotlib.rcParams.update({'font.size': 8})
matplotlib.rcParams.update({'font.family': 'serif'})

dill.settings['recurse'] = True
file_orbital = 'pickles/crb_lambda_orbital_iscat'
file_orbital_20 = 'pickles/crb_lambda_orbital_iscat_20'
file_orbital_40 = 'pickles/crb_lambda_orbital_iscat_40'
file_orbital_80 = 'pickles/crb_lambda_orbital_iscat_80'

compute_crb = False

if compute_crb:
    # orbital = Orbital(file_orbital, iscat=True)
    orbital = Orbital(file_orbital_20, iscat=True, numpoints=20)
    orbital = Orbital(file_orbital_40, iscat=True, numpoints=40)
    orbital = Orbital(file_orbital_80, iscat=True, numpoints=80)

y = np.linspace(-300, 300, num=100)

contrast = 0.01
n = 100
nscat = 1 * n
nsigma = np.sqrt(2 * nscat / contrast)

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)
fileobject_orbital_20 = open(file_orbital_20, 'rb')
crb_lambda_orbital_20 = dill.load(fileobject_orbital_20)
fileobject_orbital_40 = open(file_orbital_40, 'rb')
crb_lambda_orbital_40 = dill.load(fileobject_orbital_40)
fileobject_orbital_80 = open(file_orbital_80, 'rb')
crb_lambda_orbital_80 = dill.load(fileobject_orbital_80)

# x, y, L, N, w, amp
crb20 = crb_lambda_orbital_20(0, y, 500, nscat, 353, 1, nsigma)
crb40 = crb_lambda_orbital_40(0, y, 500, nscat, 353, 1, nsigma)
crb60 = crb_lambda_orbital(0, y, 500, nscat, 353, 1, nsigma)
crb80 = crb_lambda_orbital_80(0, y, 500, nscat, 353, 1, nsigma)

fig = formatter.figure(width_ratio=1.0, aspect_ratio=0.6)
ax1 = fig.add_subplot()

ax1.plot(y, crb20)
ax1.plot(y, crb40)
ax1.plot(y, crb60)
ax1.plot(y, crb80)

ax1.text(190, 85, '20 points', fontsize=10, color='C0')
ax1.text(190, 61, '40 points', fontsize=10, color='C1')
ax1.text(190, 50, '60 points', fontsize=10, color='C2')
ax1.text(190, 43, '80 points', fontsize=10, color='C3')

ax1.set_xlabel('Position (nm)')
ax1.set_ylabel('CRB (nm)')

for line in ax1.lines:
    line.set_lw(1.3)

plt.tight_layout()
plt.savefig('../out/orbital_crb_iscat_numpoints.pdf')
