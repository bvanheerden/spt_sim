"""CRB for minflux for different scanning lengths"""
import matplotlib
from static_crb.CRB import *
import rsmf

latex = False

if latex:
    formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                     pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

    matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})
    figure = formatter.figure(width_ratio=0.5)
else:
    figure = plt.figure()

dill.settings['recurse'] = True
file_minflux = 'pickles/crb_lambda_minflux'
file_minflux_bg = 'pickles/crb_lambda_minflux_bg'

compute_crb = False

if compute_crb:
    minflux = MinFlux(file_minflux, bg=False)
    minflux = MinFlux(file_minflux_bg, bg=True)

fileobject_minflux = open(file_minflux, 'rb')
fileobject_minflux_bg = open(file_minflux_bg, 'rb')
crb_lambda_minflux = dill.load(fileobject_minflux)
crb_lambda_minflux_bg = dill.load(fileobject_minflux_bg)

y = np.linspace(-500, 500, num=200)

spec = matplotlib.gridspec.GridSpec(ncols=2, nrows=1)
ax1 = figure.add_subplot(spec[0, 0])
ax2 = figure.add_subplot(spec[0, 1], sharey=ax1)
ax1.set_yscale('log')
# x, y, L, N, w, amp

crb100 = crb_lambda_minflux(0, y, 50, 100, 800, 1)
crb200 = crb_lambda_minflux(0, y, 100, 100, 800, 1)
crb400 = crb_lambda_minflux(0, y, 300, 100, 800, 1)
crb800 = crb_lambda_minflux(0, y, 500, 100, 800, 1)
crb1600 = crb_lambda_minflux(0, y, 700, 100, 800, 1)

crb100_bg = crb_lambda_minflux_bg(0, y, 50, 100, 800, 1, 20)
crb200_bg = crb_lambda_minflux_bg(0, y, 100, 100, 800, 1, 20)
crb400_bg = crb_lambda_minflux_bg(0, y, 300, 100, 800, 1, 20)
crb800_bg = crb_lambda_minflux_bg(0, y, 500, 100, 800, 1, 20)
crb1600_bg = crb_lambda_minflux_bg(0, y, 700, 100, 800, 1, 20)

# crb100 = crb_lambda_minflux(0, y, 5, 100, 360, 1, 110)
# crb200 = crb_lambda_minflux(0, y, 10, 100, 360, 1, 110)
# crb400 = crb_lambda_minflux(0, y, 20, 100, 360, 1, 110)
# crb800 = crb_lambda_minflux(0, y, 100, 100, 360, 1, 110)
# crb1600 = crb_lambda_minflux(0, y, 200, 100, 360, 1, 110)

ax1.plot(y, crb100, label='L=50nm')
ax1.plot(y, crb200, label='L=100nm')
ax1.plot(y, crb400, label='L=300nm')
ax1.plot(y, crb800, label='L=500nm')
ax1.plot(y, crb1600, label='L=700nm')

ax2.plot(y, crb100_bg, label='L=50nm')
ax2.plot(y, crb200_bg, label='L=100nm')
ax2.plot(y, crb400_bg, label='L=300nm')
ax2.plot(y, crb800_bg, label='L=500nm')
ax2.plot(y, crb1600_bg, label='L=700nm')

ax1.legend(loc='lower right', framealpha=0.7)
ax1.set_xlabel('x (nm)')
ax1.set_ylabel('CRB (nm)')
plt.tight_layout()
plt.savefig('../out/minflux_crb.pdf')
plt.show()

