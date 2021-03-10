"CRB of orbital method for different scanning lengths using fluorescence"
import matplotlib
from static_crb.CRB import *
from scipy.stats import norm
from scipy.signal import convolve
import rsmf

latex = True

if latex:
    formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                     pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

    matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

dill.settings['recurse'] = True
file_orbital = 'pickles/crb_lambda_orbital'

compute_crb = False

if compute_crb:
    orbital = Orbital(file_orbital)
    print('orbital')

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)

y = np.linspace(-500, 500, num=100)

fig = formatter.figure(width_ratio=0.7)

plt.yscale('log')
# x, y, L, N, w, amp
crb100 = crb_lambda_orbital(0, y, 300, 100, 212, 1)
crb200 = crb_lambda_orbital(0, y, 500, 100, 353, 1)
# crb400 = crb_lambda_orbital(0, y, 300, 4000, 424, 1)
crb800 = crb_lambda_orbital(0, y, 700, 100, 494, 1)
crb1600 = crb_lambda_orbital(0, y, 900, 100, 636, 1)

plt.plot(y, crb100, label='L=300nm')
plt.plot(y, crb200, label='L=500nm')
# plt.plot(y, crb400, label='L=564')
plt.plot(y, crb800, label='L=700nm')
plt.plot(y, crb1600, label='L=900nm')
plt.legend(loc='lower right')
plt.xlabel('x (nm)')
plt.ylabel('CRB (nm)')
plt.tight_layout()
plt.savefig('../out/orbital_crb.pdf')
plt.show()


