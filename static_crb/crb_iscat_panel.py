"CRB of orbital method using iSCAT"
import matplotlib
from static_crb.CRB import *
import rsmf

color_list = ['#1d6996', '#73af48', '#edad08', '#e17c05', '#cc503e', '#94346e', '#6f4070']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

# col_width = 345  # For dissertation I think
col_width = 470  # For journal draft
# col_width = 483.7  # For SPIE paper I think

formatter = rsmf.CustomFormatter(columnwidth=col_width * 0.01389, fontsizes=10,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})
matplotlib.rcParams.update({'font.family': 'serif'})

dill.settings['recurse'] = True
file_orbital = 'pickles/crb_lambda_orbital_iscat'
file_orbital_fluo = 'pickles/crb_lambda_orbital'

file_minflux = 'pickles/crb_lambda_minflux_iscat'
file_minflux_fluo = 'pickles/crb_lambda_minflux'

file_knight_100 = 'pickles/crb_lambda_knight_0.1_iscat'
file_knight_300 = 'pickles/crb_lambda_knight_iscat'
file_knight_500 = 'pickles/crb_lambda_knight_0.5_iscat'
file_knight_700 = 'pickles/crb_lambda_knight_0.7_iscat'
file_knight_900 = 'pickles/crb_lambda_knight_0.9_iscat'

compute_crb = False

if compute_crb:
    minflux = MinFlux(file_minflux, iscat=True)
    orbital = Orbital(file_orbital, iscat=True)
    knight = Knight(file_knight_100, 100, iscat=True)
    knight = Knight(file_knight_300, 300, iscat=True)
    knight = Knight(file_knight_500, 500, iscat=True)
    knight = Knight(file_knight_700, 700, iscat=True)
    knight = Knight(file_knight_900, 900, iscat=True)

y = np.linspace(-300, 300, num=100)

contrast = 0.01
contrast5 = 0.05
n = 100
nscat = 1 * n
nsigma = np.sqrt(2 * nscat / contrast)
nsigma5 = np.sqrt(2 * nscat / contrast5)

fileobject_minflux = open(file_minflux, 'rb')
crb_lambda_minflux = dill.load(fileobject_minflux)

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)
fileobject_orbital_fluo = open(file_orbital_fluo, 'rb')
crb_lambda_orbital_fluo = dill.load(fileobject_orbital_fluo)

fileobject_knight = open(file_knight_100, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb100_kt = crb_lambda_knight(0, y, 50, nscat, 133, 1, nsigma)
crb100_kt_5 = crb_lambda_knight(0, y, 50, nscat, 133, 1, nsigma5)

fileobject_knight = open(file_knight_300, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb300_kt = crb_lambda_knight(0, y, 100, nscat, 400, 1, nsigma)
crb300_kt_5 = crb_lambda_knight(0, y, 100, nscat, 400, 1, nsigma5)

fileobject_knight = open(file_knight_500, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb500_kt = crb_lambda_knight(0, y, 282, nscat, 665, 1, nsigma)
crb500_kt_5 = crb_lambda_knight(0, y, 282, nscat, 665, 1, nsigma5)

fileobject_knight = open(file_knight_700, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb700_kt = crb_lambda_knight(0, y, 400, nscat, 931, 1, nsigma)
crb700_kt_5 = crb_lambda_knight(0, y, 400, nscat, 931, 1, nsigma5)

fileobject_knight = open(file_knight_900, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb900_kt = crb_lambda_knight(0, y, 400, nscat, 1200, 1, nsigma)
crb900_kt_5 = crb_lambda_knight(0, y, 400, nscat, 1200, 1, nsigma5)

nscat_arr = nscat * np.exp(-4 * np.log(2) * ((y / 424) ** 2))
n_arr = n * np.exp(-4 * np.log(2) * ((y / 424) ** 2))

# plt.yscale('log')
# x, y, L, N, w, amp
crb300 = crb_lambda_orbital(0, y, 300, nscat, 212, 1, nsigma)
crb500 = crb_lambda_orbital(0, y, 500, nscat, 353, 1, nsigma)
crb700 = crb_lambda_orbital(0, y, 700, nscat, 494, 1, nsigma)
crb900 = crb_lambda_orbital(0, y, 900, nscat, 636, 1, nsigma)
crb300_5 = crb_lambda_orbital(0, y, 300, nscat, 212, 1, nsigma5)
crb500_5 = crb_lambda_orbital(0, y, 500, nscat, 353, 1, nsigma5)
crb700_5 = crb_lambda_orbital(0, y, 700, nscat, 494, 1, nsigma5)
crb900_5 = crb_lambda_orbital(0, y, 900, nscat, 636, 1, nsigma5)

mf_beam = 800
crb50_mf = crb_lambda_minflux(0, y, 50, nscat, mf_beam, 1, nsigma)
crb100_mf = crb_lambda_minflux(0, y, 100, nscat, mf_beam, 1, nsigma)
crb300_mf = crb_lambda_minflux(0, y, 300, nscat, mf_beam, 1, nsigma)
crb500_mf = crb_lambda_minflux(0, y, 500, nscat, mf_beam, 1, nsigma)
crb700_mf = crb_lambda_minflux(0, y, 700, nscat, mf_beam, 1, nsigma)
crb50_mf_5 = crb_lambda_minflux(0, y, 50, nscat, mf_beam, 1, nsigma5)
crb100_mf_5 = crb_lambda_minflux(0, y, 100, nscat, mf_beam, 1, nsigma5)
crb300_mf_5 = crb_lambda_minflux(0, y, 300, nscat, mf_beam, 1, nsigma5)
crb500_mf_5 = crb_lambda_minflux(0, y, 500, nscat, mf_beam, 1, nsigma5)
crb700_mf_5 = crb_lambda_minflux(0, y, 700, nscat, mf_beam, 1, nsigma5)

fig = formatter.figure(width_ratio=0.7, aspect_ratio=1.2)
spec = matplotlib.gridspec.GridSpec(ncols=2, nrows=3)
ax1 = fig.add_subplot(spec[0, 0])
ax2 = fig.add_subplot(spec[1, 0], sharex=ax1)
ax3 = fig.add_subplot(spec[2, 0], sharex=ax1)
ax4 = fig.add_subplot(spec[0, 1], sharey=ax1)
ax5 = fig.add_subplot(spec[1, 1], sharex=ax4, sharey=ax2)
ax6 = fig.add_subplot(spec[2, 1], sharex=ax4, sharey=ax3)

ax1.plot(y, crb300_5, label='L=300nm')
ax1.plot(y, crb500_5, label='L=500nm')
ax1.plot(y, crb700_5, label='L=700nm')
ax1.plot(y, crb900_5, label='L=900nm')

ax1.text(200, 15, '300', fontsize=10, color='C0')
ax1.text(200, 25, '500', fontsize=10, color='C1')
ax1.text(200, 37, '700', fontsize=10, color='C2')
ax1.text(200, 50, '900', fontsize=10, color='C3')

ax2.plot(y, crb300_kt_5, label='L=300nm')
ax2.plot(y, crb500_kt_5, label='L=500nm')
ax2.plot(y, crb700_kt_5, label='L=700nm')
ax2.plot(y, crb900_kt_5, label='L=900nm')

ax2.text(200, 17, '300', fontsize=10, color='C0')
ax2.text(200, 28, '500', fontsize=10, color='C1')
ax2.text(200, 40, '700', fontsize=10, color='C2')
ax2.text(200, 53, '900', fontsize=10, color='C3')

ax3.plot(y, crb50_mf_5, label='L=50')
ax3.plot(y, crb100_mf_5, label='L=100nm')
ax3.plot(y, crb300_mf_5, label='L=300nm')
ax3.plot(y, crb500_mf_5, label='L=500nm')
ax3.plot(y, crb700_mf_5, label='L=700nm')

ax3.text(40, 15, '50', fontsize=10, color='C0')
ax3.text(50, 30, '100', fontsize=10, color='C1')
ax3.text(70, 50, '300', fontsize=10, color='C2')
ax3.text(140, 100, '500', fontsize=10, color='C3')
ax3.text(230, 160, '700', fontsize=10, color='C4')

ax1.set_yscale('log')
ax2.set_yscale('log')
ax3.set_yscale('log')
ax3.set_ylim(None, 2000)

ax4.plot(y, crb300, label='L=300nm')
ax4.plot(y, crb500, label='L=500nm')
ax4.plot(y, crb700, label='L=700nm')
ax4.plot(y, crb900, label='L=900nm')

ax4.text(200, 23, '300', fontsize=10, color='C0')
ax4.text(200, 40, '500', fontsize=10, color='C1')
ax4.text(200, 55, '700', fontsize=10, color='C2')
ax4.text(200, 75, '900', fontsize=10, color='C3')

ax5.plot(y, crb300_kt, label='L=300nm')
ax5.plot(y, crb500_kt, label='L=500nm')
ax5.plot(y, crb700_kt, label='L=700nm')
ax5.plot(y, crb900_kt, label='L=900nm')

ax5.text(200, 25, '300', fontsize=10, color='C0')
ax5.text(200, 43, '500', fontsize=10, color='C1')
ax5.text(200, 62, '700', fontsize=10, color='C2')
ax5.text(200, 80, '900', fontsize=10, color='C3')

ax6.plot(y, crb50_mf, label='L=50')
ax6.plot(y, crb100_mf, label='L=100nm')
ax6.plot(y, crb300_mf, label='L=300nm')
ax6.plot(y, crb500_mf, label='L=500nm')
ax6.plot(y, crb700_mf, label='L=700nm')

ax6.text(40, 20, '50', fontsize=10, color='C0')
ax6.text(50, 50, '100', fontsize=10, color='C1')
ax6.text(70, 100, '300', fontsize=10, color='C2')
ax6.text(140, 180, '500', fontsize=10, color='C3')
ax6.text(230, 300, '700', fontsize=10, color='C4')

ax3.yaxis.set_minor_locator(matplotlib.ticker.LogLocator(10, 'auto'))
ax3.tick_params(which='minor', length=2, color='black')
ax6.yaxis.set_minor_locator(matplotlib.ticker.LogLocator(10, 'auto'))
ax6.tick_params(which='minor', length=2, color='black')

# plt.legend(loc='lower right', framealpha=0.5)
ax1.set_xlabel('Position (nm)')
ax2.set_xlabel('Position (nm)')
ax3.set_xlabel('Position (nm)')
ax1.set_ylabel('CRB (nm)')
ax3.set_ylabel('CRB (nm)')
ax3.set_ylabel('CRB (nm)')
ax6.set_xlabel('x (nm)')

ax1.text(-470, 100, 'a', fontweight='bold', fontsize='12')
ax4.text(-470, 100, 'b', fontweight='bold', fontsize='12')
ax2.text(-470, 100, 'c', fontweight='bold', fontsize='12')
ax5.text(-470, 100, 'd', fontweight='bold', fontsize='12')
ax3.text(-470, 1500, 'e', fontweight='bold', fontsize='12')
ax6.text(-470, 1500, 'f', fontweight='bold', fontsize='12')

for ax in fig.get_axes():
    for line in ax.lines:
        line.set_lw(1.3)

plt.tight_layout()
plt.savefig('../out/crb_iscat_panel.pdf')
