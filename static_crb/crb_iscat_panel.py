"CRB of orbital method using iSCAT"
import matplotlib
from static_crb.CRB import *
import rsmf

color_list = ['#1d6996', '#73af48', '#edad08', '#e17c05', '#cc503e', '#94346e', '#6f4070']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

formatter = rsmf.CustomFormatter(columnwidth=483.7 * 0.01389, fontsizes=10,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

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
n = 100
nscat = 1 * n
nsigma = np.sqrt(2 * nscat / contrast)

fileobject_minflux = open(file_minflux, 'rb')
crb_lambda_minflux = dill.load(fileobject_minflux)

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)
fileobject_orbital_fluo = open(file_orbital_fluo, 'rb')
crb_lambda_orbital_fluo = dill.load(fileobject_orbital_fluo)

fileobject_knight = open(file_knight_100, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb100_kt = crb_lambda_knight(0, y, 50, nscat, 133, 1, nsigma)

fileobject_knight = open(file_knight_300, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb300_kt = crb_lambda_knight(0, y, 100, nscat, 400, 1, nsigma)

fileobject_knight = open(file_knight_500, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb500_kt = crb_lambda_knight(0, y, 282, nscat, 665, 1, nsigma)

fileobject_knight = open(file_knight_700, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb700_kt = crb_lambda_knight(0, y, 400, nscat, 931, 1, nsigma)

fileobject_knight = open(file_knight_900, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb900_kt = crb_lambda_knight(0, y, 400, nscat, 1200, 1, nsigma)

nscat_arr = nscat * np.exp(-4 * np.log(2) * ((y / 424) ** 2))
n_arr = n * np.exp(-4 * np.log(2) * ((y / 424) ** 2))

# plt.yscale('log')
# x, y, L, N, w, amp
crb300 = crb_lambda_orbital(0, y, 300, nscat, 212, 1, nsigma)
crb500 = crb_lambda_orbital(0, y, 500, nscat, 353, 1, nsigma)
crb700 = crb_lambda_orbital(0, y, 700, nscat, 494, 1, nsigma)
crb900 = crb_lambda_orbital(0, y, 900, nscat, 636, 1, nsigma)

crb50_mf = crb_lambda_minflux(0, y, 50, nscat, 800, 1, nsigma)
crb100_mf = crb_lambda_minflux(0, y, 100, nscat, 800, 1, nsigma)
crb300_mf = crb_lambda_minflux(1, y, 300, nscat, 800, 1, nsigma)
crb500_mf = crb_lambda_minflux(0, y, 500, nscat, 800, 1, nsigma)
crb700_mf = crb_lambda_minflux(0, y, 700, nscat, 800, 1, nsigma)

fig = formatter.figure(width_ratio=0.8, aspect_ratio=0.4)
spec = matplotlib.gridspec.GridSpec(ncols=3, nrows=1)
ax1 = fig.add_subplot(spec[0, 0])
ax2 = fig.add_subplot(spec[0, 1], sharey=ax1)
ax3 = fig.add_subplot(spec[0, 2])

ax1.plot(y, crb300, label='L=300nm')
ax1.plot(y, crb500, label='L=500nm')
ax1.plot(y, crb700, label='L=700nm')
ax1.plot(y, crb900, label='L=900nm')

ax1.text(200, 30, '300', fontsize=10, color='C0')
ax1.text(200, 50, '500', fontsize=10, color='C1')
ax1.text(200, 70, '700', fontsize=10, color='C2')
ax1.text(200, 93, '900', fontsize=10, color='C3')

ax2.plot(y, crb300_kt, label='L=300nm')
ax2.plot(y, crb500_kt, label='L=500nm')
ax2.plot(y, crb700_kt, label='L=700nm')
ax2.plot(y, crb900_kt, label='L=900nm')

ax2.text(200, 33, '300', fontsize=10, color='C0')
ax2.text(200, 55, '500', fontsize=10, color='C1')
ax2.text(200, 76, '700', fontsize=10, color='C2')
ax2.text(200, 98, '900', fontsize=10, color='C3')

ax3.plot(y, crb50_mf, label='L=50')
ax3.plot(y, crb100_mf, label='L=100nm')
ax3.plot(y, crb300_mf, label='L=300nm')
ax3.plot(y, crb500_mf, label='L=500nm')
ax3.plot(y, crb700_mf, label='L=700nm')

ax3.text(40, 20, '50', fontsize=10, color='C0')
ax3.text(50, 50, '100', fontsize=10, color='C1')
ax3.text(70, 100, '300', fontsize=10, color='C2')
ax3.text(140, 180, '500', fontsize=10, color='C3')
ax3.text(230, 300, '700', fontsize=10, color='C4')

ax3.set_yscale('log')
ax3.set_ylim(10, None)

# plt.legend(loc='lower right', framealpha=0.5)
ax1.set_xlabel('x (nm)')
ax2.set_xlabel('x (nm)')
ax3.set_xlabel('x (nm)')
ax1.set_ylabel('CRB (nm)')

plt.tight_layout()
plt.savefig('../out/crb_iscat_panel.pdf')
