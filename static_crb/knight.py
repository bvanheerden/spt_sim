"""CRB of knight's tour method for different scanning lengths"""
import matplotlib
from static_crb.CRB import *
import rsmf

latex = True

if latex:
    formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                     pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

    matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

dill.settings['recurse'] = True
file_knight_100 = 'pickles/crb_lambda_knight_0.1'
file_knight_300 = 'pickles/crb_lambda_knight'
file_knight_500 = 'pickles/crb_lambda_knight_0.5'
file_knight_700 = 'pickles/crb_lambda_knight_0.7'
file_knight_900 = 'pickles/crb_lambda_knight_0.9'

compute_crb = False

if compute_crb:
    knight = Knight(file_knight_900, 900)

y = np.linspace(-500, 500, num=100)
# x, y, L, N, w, amp

fileobject_knight = open(file_knight_100, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb100 = crb_lambda_knight(0, y, 50, 100, 133, 1)

fileobject_knight = open(file_knight_300, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb300 = crb_lambda_knight(0, y, 100, 100, 400, 1)

fileobject_knight = open(file_knight_500, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb500 = crb_lambda_knight(0, y, 282, 100, 665, 1)

fileobject_knight = open(file_knight_700, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb700 = crb_lambda_knight(0, y, 400, 100, 931, 1)

fileobject_knight = open(file_knight_900, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb900 = crb_lambda_knight(0, y, 400, 100, 1200, 1)

figure = formatter.figure(width_ratio=0.7)
plt.yscale('log')
plt.plot(y, crb300, label='L=300nm')
plt.plot(y, crb500, label='L=500nm')
plt.plot(y, crb700, label='L=700nm')
plt.plot(y, crb900, label='L=900nm')
plt.legend(loc='lower right', framealpha=0.7)
plt.xlabel('x (nm)')
plt.ylabel('CRB (nm)')
plt.tight_layout()
plt.savefig('../out/knight_crb.pdf')
plt.show()

