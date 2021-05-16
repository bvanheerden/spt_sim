"CRB of orbital method for different scanning lengths using fluorescence"
import matplotlib
from static_crb.CRB import *
from scipy.stats import norm
from scipy.signal import convolve
import rsmf

color_list = ['#4477AA', '#66CCEE', '#228833', '#CC6677', '#EE6677', '#AA3377', '#BBBBBB']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

latex = False

if latex:
    formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                     pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

    matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})
    fig = formatter.figure(width_ratio=0.7)
else:
    fig = plt.figure()

dill.settings['recurse'] = True
file_orbital = 'pickles/crb_lambda_orbital'
file_orbital_bg = 'pickles/crb_lambda_orbital_bg'

compute_crb = False

if compute_crb:
    orbital = Orbital(file_orbital, bg=False)
    orbital = Orbital(file_orbital_bg, bg=True)

fileobject_orbital = open(file_orbital, 'rb')
fileobject_orbital_bg = open(file_orbital_bg, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)
crb_lambda_orbital_bg = dill.load(fileobject_orbital_bg)

y = np.linspace(-500, 500, num=100)

spec = matplotlib.gridspec.GridSpec(ncols=2, nrows=1)
ax1 = fig.add_subplot(spec[0, 0])
ax2 = fig.add_subplot(spec[0, 1], sharey=ax1)

plt.yscale('log')
# x, y, L, N, w, amp
crb100 = crb_lambda_orbital(0, y, 300, 100, 212, 1)
crb200 = crb_lambda_orbital(0, y, 500, 100, 353, 1)
# crb400 = crb_lambda_orbital(0, y, 300, 4000, 424, 1)
crb800 = crb_lambda_orbital(0, y, 700, 100, 494, 1)
crb1600 = crb_lambda_orbital(0, y, 900, 100, 636, 1)

crb100_bg = crb_lambda_orbital_bg(0, y, 300, 100, 212, 1, 20)
crb200_bg = crb_lambda_orbital_bg(0, y, 500, 100, 353, 1, 20)
# crb400 = crb_lambda_orbital(0, y, 300, 4000, 424, 1)
crb800_bg = crb_lambda_orbital_bg(0, y, 700, 100, 494, 1, 20)
crb1600_bg = crb_lambda_orbital_bg(0, y, 900, 100, 636, 1, 20)

ax1.plot(y, crb100, label='L=300nm')
ax1.plot(y, crb200, label='L=500nm')
# plt.plot(y, crb400, label='L=564')
ax1.plot(y, crb800, label='L=700nm')
ax1.plot(y, crb1600, label='L=900nm')

ax2.plot(y, crb100_bg, label='L=300nm')
ax2.plot(y, crb200_bg, label='L=500nm')
ax2.plot(y, crb800_bg, label='L=700nm')
ax2.plot(y, crb1600_bg, label='L=900nm')

ax1.legend(loc='lower right')
ax1.set_xlabel('x (nm)')
ax1.set_ylabel('CRB (nm)')
plt.tight_layout()
plt.savefig('../out/orbital_crb.pdf')
plt.show()


