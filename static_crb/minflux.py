"""CRB for minflux for different scanning lengths"""
import matplotlib
from static_crb.CRB import *
import rsmf

latex = True

if latex:
    formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                     pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

    matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

dill.settings['recurse'] = True
file_minflux = 'pickles/crb_lambda_minflux'

compute_crb = False

if compute_crb:
    minflux = MinFlux(file_minflux)

fileobject_minflux = open(file_minflux, 'rb')
crb_lambda_minflux = dill.load(fileobject_minflux)

y = np.linspace(-500, 500, num=200)

figure = formatter.figure(width_ratio=0.7)
plt.yscale('log')
# x, y, L, N, w, amp

crb100 = crb_lambda_minflux(0, y, 50, 10000, 800, 1)
crb200 = crb_lambda_minflux(0, y, 100, 10000, 800, 1)
crb400 = crb_lambda_minflux(0, y, 300, 10000, 800, 1)
crb800 = crb_lambda_minflux(0, y, 500, 10000, 800, 1)
crb1600 = crb_lambda_minflux(0, y, 700, 10000, 800, 1)

plt.plot(y, crb100, label='L=50nm')
plt.plot(y, crb200, label='L=100nm')
plt.plot(y, crb400, label='L=300nm')
plt.plot(y, crb800, label='L=500nm')
plt.plot(y, crb1600, label='L=700nm')
plt.legend(loc='lower right', framealpha=0.7)
plt.xlabel('x (nm)')
plt.ylabel('CRB (nm)')
plt.tight_layout()
plt.savefig('../out/minflux_crb.pdf')
plt.show()

