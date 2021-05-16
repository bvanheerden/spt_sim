"""CRB of knight's tour method for different scanning lengths"""
import matplotlib
from static_crb.CRB import *
import rsmf

color_list = ['#4477AA', '#66CCEE', '#228833', '#CC6677', '#EE6677', '#AA3377', '#BBBBBB']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

latex = False
if latex:
    formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                     pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

    matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})
    figure = formatter.figure(width_ratio=0.7)
else:
    figure = plt.figure(figsize=[5, 3], dpi=150)

dill.settings['recurse'] = True
file_knight_100 = 'pickles/crb_lambda_knight_0.1'
file_knight_100_bg = 'pickles/crb_lambda_knight_0.1_bg'
file_knight_300 = 'pickles/crb_lambda_knight'
file_knight_300_bg = 'pickles/crb_lambda_knight_bg'
file_knight_500 = 'pickles/crb_lambda_knight_0.5'
file_knight_500_bg = 'pickles/crb_lambda_knight_0.5_bg'
file_knight_700 = 'pickles/crb_lambda_knight_0.7'
file_knight_700_bg = 'pickles/crb_lambda_knight_0.7_bg'
file_knight_900 = 'pickles/crb_lambda_knight_0.9'
file_knight_900_bg = 'pickles/crb_lambda_knight_0.9_bg'

compute_crb = False

if compute_crb:
    knight = Knight(file_knight_100, 100)
    knight = Knight(file_knight_100_bg, 100, bg=True)

spec = matplotlib.gridspec.GridSpec(ncols=2, nrows=1)
ax1 = figure.add_subplot(spec[0, 0])
ax2 = figure.add_subplot(spec[0, 1], sharey=ax1)

y = np.linspace(-500, 500, num=100)
# x, y, L, N, w, amp

fileobject_knight = open(file_knight_100, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb100 = crb_lambda_knight(0, y, 50, 100, 133, 1)
fileobject_knight_bg = open(file_knight_100_bg, 'rb')
crb_lambda_knight_bg = dill.load(fileobject_knight_bg)
crb100_bg = crb_lambda_knight_bg(0, y, 50, 100, 133, 1, 20)

fileobject_knight = open(file_knight_300, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb300 = crb_lambda_knight(0, y, 100, 100, 400, 1)
fileobject_knight_bg = open(file_knight_300_bg, 'rb')
crb_lambda_knight_bg = dill.load(fileobject_knight_bg)
crb300_bg = crb_lambda_knight_bg(0, y, 100, 100, 400, 1, 20)

fileobject_knight = open(file_knight_500, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb500 = crb_lambda_knight(0, y, 282, 100, 665, 1)
fileobject_knight_bg = open(file_knight_500_bg, 'rb')
crb_lambda_knight_bg = dill.load(fileobject_knight_bg)
crb500_bg = crb_lambda_knight_bg(0, y, 282, 100, 665, 1, 20)

fileobject_knight = open(file_knight_700, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb700 = crb_lambda_knight(0, y, 400, 100, 931, 1)
fileobject_knight_bg = open(file_knight_700_bg, 'rb')
crb_lambda_knight_bg = dill.load(fileobject_knight_bg)
crb700_bg = crb_lambda_knight_bg(0, y, 400, 100, 931, 1, 20)

fileobject_knight = open(file_knight_900, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb900 = crb_lambda_knight(0, y, 400, 100, 1200, 1)
fileobject_knight_bg = open(file_knight_900_bg, 'rb')
crb_lambda_knight_bg = dill.load(fileobject_knight_bg)
crb900_bg = crb_lambda_knight_bg(0, y, 400, 100, 1200, 1, 20)

plt.yscale('log')
ax1.plot(y, crb300, label='L=300nm', lw=2)
ax1.plot(y, crb500, label='L=500nm', lw=2)
ax1.plot(y, crb700, label='L=700nm', lw=2)
ax1.plot(y, crb900, label='L=900nm', lw=2)

ax2.plot(y, crb300_bg, label='L=300nm', lw=2)
ax2.plot(y, crb500_bg, label='L=500nm', lw=2)
ax2.plot(y, crb700_bg, label='L=700nm', lw=2)
ax2.plot(y, crb900_bg, label='L=900nm', lw=2)

ax1.legend(loc='lower right', framealpha=0.7)
ax2.legend(loc='lower right', framealpha=0.7)
ax1.set_xlabel('x (nm)')
ax2.set_xlabel('x (nm)')
ax1.set_ylabel('CRB (nm)')
plt.tight_layout()
plt.savefig('../out/knight_crb.pdf')
plt.show()

