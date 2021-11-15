""" Comparison of orbital, minflux, knights tour CRB as a function of position"""

import dill
import matplotlib
from static_crb.CRB import *
import rsmf

# color_list = ['#4477AA', '#66CCEE', '#228833', '#CC6677', '#EE6677', '#AA3377', '#BBBBBB']
color_list = ['#1d6996', '#73af48', '#edad08', '#e17c05', '#cc503e', '#94346e', '#6f4070']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

latex = False

if latex:
    formatter = rsmf.CustomFormatter(columnwidth=345 * 0.01389, fontsizes=10,
                                     pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

    matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

else:
    matplotlib.rcParams.update({'font.size': 13})

dill.settings['recurse'] = True
file_minflux = 'pickles/crb_lambda_minflux'
file_orbital = 'pickles/crb_lambda_orbital'
file_knight = 'pickles/crb_lambda_knight'
file_minflux_bg = 'pickles/crb_lambda_minflux_bg'
file_orbital_bg = 'pickles/crb_lambda_orbital_bg'
file_knight_bg = 'pickles/crb_lambda_knight_bg'

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
fileobject_minflux_bg = open(file_minflux_bg, 'rb')
crb_lambda_minflux_bg = dill.load(fileobject_minflux_bg)

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)
fileobject_orbital_bg = open(file_orbital_bg, 'rb')
crb_lambda_orbital_bg = dill.load(fileobject_orbital_bg)

fileobject_knight = open(file_knight, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
fileobject_knight_bg = open(file_knight_bg, 'rb')
crb_lambda_knight_bg = dill.load(fileobject_knight_bg)

x = np.linspace(-200, 200, num=200)
y = np.linspace(-400, 400, num=200)
xv, yv = np.meshgrid(x, y)
r = x

crbknight = crb_lambda_knight(0, y, 50, 100, 400, 1,)
crbmf_large = crb_lambda_minflux(0, y, 566, 100, 800, 1)
crbmf = crb_lambda_minflux(0, y, 50, 100, 800, 1)
crborb = crb_lambda_orbital(0, y, 566, 100, 400, 1)

crbknight_bg = crb_lambda_knight_bg(0, y, 50, 100, 400, 1, 20)
crbmf_large_bg = crb_lambda_minflux_bg(0, y, 566, 100, 800, 1, 20)
crbmf_bg = crb_lambda_minflux_bg(0, y, 50, 100, 800, 1, 20)
crborb_bg = crb_lambda_orbital_bg(0, y, 566, 100, 400, 1, 20)

if latex:
    figure = formatter.figure(width_ratio=0.7)
else:
    figure = plt.figure(figsize=[8, 3], dpi=150)

spec = matplotlib.gridspec.GridSpec(ncols=2, nrows=1)
ax1 = figure.add_subplot(spec[0, 0])
ax2 = figure.add_subplot(spec[0, 1], sharey=ax1)

ax1.set_yscale('log')
ax1.plot(y, crborb, label='Orbital', lw=2)
ax1.plot(y, crbknight, label="Knight's Tour", lw=2, color='C2')
ax1.plot(y, crbmf, label='MINFLUX', lw=2, color='C1')
# ax1.plot(y, crbmf_large, label='MINFLUX L=566nm')

ax2.plot(y, crborb_bg, label='Orbital L=566nm')
ax2.plot(y, crbknight_bg, label="Knight's Tour L=1500nm")
ax2.plot(y, crbmf_bg, label='MINFLUX L=50nm')
# ax2.plot(y, crbmf_large_bg, label='MINFLUX L=566nm')

ax1.legend(loc='lower left', framealpha=0.7, handlelength=1.0)
ax1.set_xlabel('Distance (nm)')
ax2.set_xlabel('Distance (nm)')
ax1.set_ylabel('CRB (nm)')
ax1.set_title('SBR = $\infty$')
ax2.set_title('SBR = 20')

plt.xlim(-500, 500)
plt.ylim(0.9, None)

plt.tight_layout()
plt.savefig('../out/comp_mf_large.pdf')
plt.show()
