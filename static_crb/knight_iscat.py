"""CRB of knight's tour method for different scanning lengths"""
import matplotlib
from static_crb.CRB import *
import rsmf

color_list = ['#1d6996', '#73af48', '#edad08', '#e17c05', '#cc503e', '#94346e', '#6f4070']
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
file_knight_100 = 'pickles/crb_lambda_knight_0.1_iscat'
file_knight_300 = 'pickles/crb_lambda_knight_iscat'
file_knight_500 = 'pickles/crb_lambda_knight_0.5_iscat'
file_knight_700 = 'pickles/crb_lambda_knight_0.7_iscat'
file_knight_900 = 'pickles/crb_lambda_knight_0.9_iscat'

compute_crb = False

if compute_crb:
    knight = Knight(file_knight_100, 100, iscat=True)
    print('1')
    knight = Knight(file_knight_300, 300, iscat=True)
    print('2')
    knight = Knight(file_knight_500, 500, iscat=True)
    print('3')
    knight = Knight(file_knight_700, 700, iscat=True)
    print('4')
    knight = Knight(file_knight_900, 900, iscat=True)
    print('5')

contrast = 0.01
n = 100
nscat = 1 * n
nsigma = np.sqrt(2 * nscat / contrast)

y = np.linspace(-500, 500, num=100)
# x, y, L, N, w, amp

fileobject_knight = open(file_knight_100, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb100 = crb_lambda_knight(0, y, 50, nscat, 133, 1, nsigma)

fileobject_knight = open(file_knight_300, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb300 = crb_lambda_knight(0, y, 100, nscat, 400, 1, nsigma)

fileobject_knight = open(file_knight_500, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb500 = crb_lambda_knight(0, y, 282, nscat, 665, 1, nsigma)

fileobject_knight = open(file_knight_700, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb700 = crb_lambda_knight(0, y, 400, nscat, 931, 1, nsigma)

fileobject_knight = open(file_knight_900, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb900 = crb_lambda_knight(0, y, 400, nscat, 1200, 1, nsigma)

plt.yscale('log')
plt.plot(y, crb300, label='L=300nm', lw=2)
plt.plot(y, crb500, label='L=500nm', lw=2)
plt.plot(y, crb700, label='L=700nm', lw=2)
plt.plot(y, crb900, label='L=900nm', lw=2)

plt.legend(loc='lower right', framealpha=0.7)
plt.legend(loc='lower right', framealpha=0.7)
plt.xlabel('x (nm)')
plt.xlabel('x (nm)')
plt.ylabel('CRB (nm)')
plt.tight_layout()
plt.savefig('../out/knight_crb_iscat.pdf')
plt.show()

