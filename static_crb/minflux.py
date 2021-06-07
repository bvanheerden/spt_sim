"""CRB for minflux for different scanning lengths"""
import matplotlib
from static_crb.CRB import *
import rsmf

color_list = ['#4477AA', '#66CCEE', '#228833', '#CC6677', '#EE6677', '#AA3377', '#BBBBBB']
color_list = ['#0077bb', '#33bbee', '#009988', '#ee7733', '#cc3311', '#ee3377', '#bbbbbb']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

latex = False

if latex:
    formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                     pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

    matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})
    figure = formatter.figure(width_ratio=0.5)
else:
    figure = plt.figure(figsize=[8, 4], dpi=150)

dill.settings['recurse'] = True
file_minflux = 'pickles/crb_lambda_minflux'
file_minflux_bg = 'pickles/crb_lambda_minflux_bg'

compute_crb = True

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

crb50 = crb_lambda_minflux(0, y, 50, 100, 800, 1)
crb100 = crb_lambda_minflux(0, y, 100, 100, 800, 1)
crb300 = crb_lambda_minflux(0, y, 300, 100, 800, 1)
crb500 = crb_lambda_minflux(0, y, 500, 100, 800, 1)
crb700 = crb_lambda_minflux(0, y, 700, 100, 800, 1)

crb50_bg = crb_lambda_minflux_bg(0, y, 50, 100, 800, 1, 20)
crb100_bg = crb_lambda_minflux_bg(0, y, 100, 100, 800, 1, 20)
crb300_bg = crb_lambda_minflux_bg(0, y, 300, 100, 800, 1, 20)
crb500_bg = crb_lambda_minflux_bg(0, y, 500, 100, 800, 1, 20)
crb700_bg = crb_lambda_minflux_bg(0, y, 700, 100, 800, 1, 20)

# crb100 = crb_lambda_minflux(0, y, 5, 100, 360, 1, 110)
# crb200 = crb_lambda_minflux(0, y, 10, 100, 360, 1, 110)
# crb400 = crb_lambda_minflux(0, y, 20, 100, 360, 1, 110)
# crb800 = crb_lambda_minflux(0, y, 100, 100, 360, 1, 110)
# crb1600 = crb_lambda_minflux(0, y, 200, 100, 360, 1, 110)

ax1.plot(y, crb50, label='L=50nm')
ax1.plot(y, crb100, label='L=100nm')
ax1.plot(y, crb300, label='L=300nm')
ax1.plot(y, crb500, label='L=500nm')
ax1.plot(y, crb700, label='L=700nm')

ax2.plot(y, crb50_bg, label='L=50nm')
ax2.plot(y, crb100_bg, label='L=100nm')
ax2.plot(y, crb300_bg, label='L=300nm')
ax2.plot(y, crb500_bg, label='L=500nm')
ax2.plot(y, crb700_bg, label='L=700nm')

ax1.legend(loc='lower right', framealpha=0.7)
ax1.set_xlabel('x (nm)')
ax1.set_ylabel('CRB (nm)')
plt.tight_layout()
plt.savefig('../out/minflux_crb.pdf')
plt.show()

