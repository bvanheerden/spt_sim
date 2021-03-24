""" Comparison of orbital, minflux, knights tour CRB as a function of position"""

import dill
import matplotlib
from static_crb.CRB import *
import rsmf

latex = True

if latex:
    formatter = rsmf.CustomFormatter(columnwidth=345 * 0.01389, fontsizes=10,
                                     pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

    matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

else:
    matplotlib.rcParams.update({'font.size': 11})

dill.settings['recurse'] = True
file_minflux = 'pickles/crb_lambda_minflux'
file_orbital = 'pickles/crb_lambda_orbital'
file_knight = 'pickles/crb_lambda_knight'
file_camera = 'pickles/crb_lambda_camera'

compute_crb = False

if compute_crb:
    minflux = MinFlux(file_minflux)
    print('minflux')
    orbital = Orbital(file_orbital)
    print('orbital')
    knight = Knight(file_knight, 300)
    print('knight')

fileobject_minflux = open(file_minflux, 'rb')
crb_lambda_minflux = dill.load(fileobject_minflux)

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)

fileobject_knight = open(file_knight, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)

x = np.linspace(-200, 200, num=200)
y = np.linspace(-400, 400, num=200)
xv, yv = np.meshgrid(x, y)
r = x

crbknight = crb_lambda_knight(0, y, 50, 100, 400, 1,)
crbmf_large = crb_lambda_minflux(0, y, 566, 100, 800, 1)
crbmf = crb_lambda_minflux(0, y, 50, 100, 800, 1)
crborb = crb_lambda_orbital(0, y, 566, 100, 400, 1)

if latex:
    figure = formatter.figure(width_ratio=0.7)
else:
    plt.figure(figsize=[4, 3], dpi=150)

plt.yscale('log')
plt.plot(y, crborb, label='Orbital L=566nm')
plt.plot(y, crbknight, label="Knight's Tour L=1500nm")
plt.plot(y, crbmf, label='MINFLUX L=50nm')
plt.plot(y, crbmf_large, label='MINFLUX L=566nm')
plt.legend(loc='lower left', framealpha=0.7, handlelength=1.0)
plt.xlabel('Distance (nm)')
plt.ylabel('CRB (nm)')

plt.xlim(-500, 500)
plt.ylim(0.9, None)

plt.tight_layout()
plt.savefig('../out/comp_mf_large.pdf')
plt.show()
