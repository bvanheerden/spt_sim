"CRB of orbital method using iSCAT"
import matplotlib
from static_crb.CRB import *
import rsmf

color_list = ['#1d6996', '#73af48', '#edad08', '#e17c05', '#cc503e', '#94346e', '#6f4070']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

dill.settings['recurse'] = True
file_minflux = 'pickles/crb_lambda_minflux_iscat'
file_minflux_fluo = 'pickles/crb_lambda_minflux'

compute_crb = False

if compute_crb:
    minflux = MinFlux(file_minflux, iscat=True)
    # minflux = MinFlux(file_minflux_fluo, bg=True)

fileobject_minflux = open(file_minflux, 'rb')
crb_lambda_minflux = dill.load(fileobject_minflux)
fileobject_minflux_fluo = open(file_minflux_fluo, 'rb')
crb_lambda_minflux_fluo = dill.load(fileobject_minflux_fluo)

contrast = 0.01
n = 100
nscat = 1 * n
nsigma = np.sqrt(2 * nscat / contrast)

y = np.linspace(-300, 300, num=100)

nscat_arr = nscat * np.exp(-4 * np.log(2) * ((y / 424) ** 2))
n_arr = n * np.exp(-4 * np.log(2) * ((y / 424) ** 2))

# plt.yscale('log')
# x, y, L, N, w, amp
crb50 = crb_lambda_minflux(0, y, 50, nscat, 800, 1, nsigma)
crb100 = crb_lambda_minflux(0, y, 100, nscat, 800, 1, nsigma)
crb300 = crb_lambda_minflux(1, y, 300, nscat, 800, 1, nsigma)
crb500 = crb_lambda_minflux(0, y, 500, nscat, 800, 1, nsigma)
crb700 = crb_lambda_minflux(0, y, 700, nscat, 800, 1, nsigma)

# crb800 = crb_lambda_orbital_fluo(0, y, 300, n, 424, 1)
# crb800 = [crb_lambda_orbital_fluo(0, yval, 300, n_arr[i], 424, 1) for i, yval in enumerate(y)]

figure = formatter.figure(width_ratio=0.7)
plt.plot(y, crb50, label='L=50nm')
plt.plot(y, crb100, label='L=100nm')
plt.plot(y, crb300, label='L=300nm')
plt.plot(y, crb500, label='L=500nm')
plt.plot(y, crb700, label='L=700nm')
plt.legend(loc='lower right', framealpha=0.5)
plt.xlabel('x (nm)')
plt.ylabel('CRB (nm)')
plt.tight_layout()
plt.savefig('../out/minflux_crb_iscat.pdf')
plt.show()

# N = np.arange(1000, 100000, 1000)
# crbN = crb_lambda_orbital(0, 0, 300, N, 424, 1, np.sqrt(2*N*0.002))
# plt.loglog(N, crbN)
# plt.show()



