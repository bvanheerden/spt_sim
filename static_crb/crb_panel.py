import matplotlib
from static_crb.CRB import *
from scipy.stats import norm
from scipy.signal import convolve
import rsmf

formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=10,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

dill.settings['recurse'] = True
file_orbital = 'pickles/crb_lambda_orbital'
file_minflux = 'pickles/crb_lambda_minflux'
file_knight_100 = 'pickles/crb_lambda_knight_0.1'
file_knight_300 = 'pickles/crb_lambda_knight'
file_knight_500 = 'pickles/crb_lambda_knight_0.5'
file_knight_700 = 'pickles/crb_lambda_knight_0.7'
file_knight_900 = 'pickles/crb_lambda_knight_0.9'

# orbital = Orbital(file_orbital)
# print('orbital')

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)

fileobject_minflux = open(file_minflux, 'rb')
crb_lambda_minflux = dill.load(fileobject_minflux)

y = np.linspace(-400, 400, num=100)
y1 = np.linspace(-400, 400, num=100)

# fig = plt.figure(figsize=(8, 5))
fig = formatter.figure(width_ratio=1.0, aspect_ratio=0.7)
spec = matplotlib.gridspec.GridSpec(ncols=2, nrows=2)
ax1 = fig.add_subplot(spec[0, 0])
ax2 = fig.add_subplot(spec[1, 0])
ax3 = fig.add_subplot(spec[0, 1], sharey=ax1)
ax4 = fig.add_subplot(spec[1, 1], sharey=ax2)

ax1.set_yscale('log')
# x, y, L, N, w, amp
crb100 = crb_lambda_orbital(0, y, 300, 100, 212, 1)
crb200 = crb_lambda_orbital(0, y, 500, 100, 353, 1)
# crb400 = crb_lambda_orbital(0, y, 300, 4000, 424, 1)
crb800 = crb_lambda_orbital(0, y, 700, 100, 494, 1)
crb1600 = crb_lambda_orbital(0, y, 900, 100, 636, 1)

fileobject_knight = open(file_knight_100, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb100_kt = crb_lambda_knight(0, y, 50, 100, 133, 1)

fileobject_knight = open(file_knight_300, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb300_kt = crb_lambda_knight(0, y, 100, 100, 400, 1)

fileobject_knight = open(file_knight_500, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb500_kt = crb_lambda_knight(0, y, 282, 100, 665, 1)

fileobject_knight = open(file_knight_700, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb700_kt = crb_lambda_knight(0, y, 400, 100, 931, 1)

fileobject_knight = open(file_knight_900, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb900_kt = crb_lambda_knight(0, y, 400, 100, 1200, 1)

crb100_mf = crb_lambda_minflux(0, y, 50, 100, 800, 1)
crb200_mf = crb_lambda_minflux(0, y, 100, 100, 800, 1)
crb400_mf = crb_lambda_minflux(0, y, 300, 100, 800, 1)
crb800_mf = crb_lambda_minflux(0, y, 500, 100, 800, 1)
crb1600_mf = crb_lambda_minflux(0, y, 700, 100, 800, 1)

fileobject_knight = open(file_knight_300, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crbknight = crb_lambda_knight(0, y1, 50, 100, 400, 1,)

crbmf_large = crb_lambda_minflux(0, y1, 566, 100, 800, 1)
crbmf = crb_lambda_minflux(0, y1, 50, 100, 800, 1)
crborb = crb_lambda_orbital(0, y1, 566, 100, 400, 1)

ax1.plot(y, crb100, label='L=300nm')
ax1.plot(y, crb200, label='L=500nm')
# plt.plot(y, crb400, label='L=564')
ax1.plot(y, crb800, label='L=700nm')
ax1.plot(y, crb1600, label='L=900nm')
ax1.legend(loc='upper center', framealpha=0.5, ncol=2)
ax1.set_ylabel('CRB (nm)')
ax1.text(-520, 50, 'a', fontweight='bold', fontsize='12')

ax3.set_yscale('log')
ax3.plot(y, crb300_kt, label='L=300nm')
ax3.plot(y, crb500_kt, label='L=500nm')
ax3.plot(y, crb700_kt, label='L=700nm')
ax3.plot(y, crb900_kt, label='L=900nm')
ax3.legend(loc='lower right', framealpha=0.5, ncol=2)
ax3.text(-520, 50, 'b', fontweight='bold', fontsize='12')

ax2.set_yscale('log')
ax2.plot(y, crb100_mf, label='L=50nm')
ax2.plot(y, crb200_mf, label='L=100nm')
ax2.plot(y, crb400_mf, label='L=300nm')
ax2.plot(y, crb800_mf, label='L=500nm')
ax2.plot(y, crb1600_mf, label='L=700nm')
ax2.legend(loc='upper center', framealpha=0.5, ncol=2)
ax2.text(-520, 2000, 'c', fontweight='bold', fontsize='12')
ax2.set_xlabel('x (nm)')
ax2.set_ylabel('CRB (nm)')

ax4.set_yscale('log')
ax4.plot(y1, crbknight, label="KT L=1500nm")
ax4.plot(y1, crbmf, label='MINFLUX L=50nm')
ax4.plot(y1, crbmf_large, label='MINFLUX L=566nm')
ax4.plot(y1, crborb, label='Orbital L=566nm')
ax4.legend(loc='upper center', framealpha=0.5)
ax4.text(-520, 2000, 'd', fontweight='bold', fontsize='12')
ax4.set_xlabel('x (nm)')

plt.tight_layout()
plt.savefig('../out/crb_panel_art.pdf')
# plt.show()

N = np.linspace(95, 105)
dist = norm(loc=100, scale=0.5)

crb = crb_lambda_orbital(0, y[:, None], 300, N, 212, 1)


