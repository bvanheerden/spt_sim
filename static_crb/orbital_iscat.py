import matplotlib
from static_crb.CRB import *
import rsmf

formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

dill.settings['recurse'] = True
file_orbital = 'pickles/crb_lambda_orbital_iscat'
file_orbital_fluo = 'pickles/crb_lambda_orbital'

# orbital = Orbital(file_orbital, iscat=True)
# orbital_fluo = Orbital(file_orbital_fluo, iscat=False)
# print('orbital')

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)
fileobject_orbital_fluo = open(file_orbital_fluo, 'rb')
crb_lambda_orbital_fluo = dill.load(fileobject_orbital_fluo)

contrast = 0.01
n = 100
nscat = 1 * n
nsigma = np.sqrt(2 * nscat / contrast)

y = np.linspace(-300, 300, num=100)

nscat_arr = nscat * np.exp(-4 * np.log(2) * ((y / 424) ** 2))
n_arr = n * np.exp(-4 * np.log(2) * ((y / 424) ** 2))

# plt.yscale('log')
# x, y, L, N, w, amp
crb100 = crb_lambda_orbital(0, y, 300, nscat, 212, 1, nsigma)
crb200 = crb_lambda_orbital(0, y, 500, nscat, 353, 1, nsigma)
# crb400 = crb_lambda_orbital(1, y, 300, nscat, 424, 1, nsigma)
crb800 = crb_lambda_orbital(0, y, 700, nscat, 494, 1, nsigma)
# crb800 = crb_lambda_orbital(0, y, 300, nscat, 424, 1, nsigma)
crb1600 = crb_lambda_orbital(0, y, 900, nscat, 636, 1, nsigma)

# crb800 = crb_lambda_orbital_fluo(0, y, 300, n, 424, 1)
# crb800 = [crb_lambda_orbital_fluo(0, yval, 300, n_arr[i], 424, 1) for i, yval in enumerate(y)]

figure = formatter.figure(width_ratio=0.7)
plt.plot(y, crb100, label='L=300nm')
plt.plot(y, crb200, label='L=500nm')
# plt.plot(y, crb400, label='L=564')
plt.plot(y, crb800, label='L=700nm')
plt.plot(y, crb1600, label='L=900nm')
plt.legend(loc='lower right', framealpha=0.5)
plt.xlabel('x (nm)')
plt.ylabel('CRB (nm)')
plt.tight_layout()
plt.savefig('../out/orbital_crb_iscat.pdf')
plt.show()

# N = np.arange(1000, 100000, 1000)
# crbN = crb_lambda_orbital(0, 0, 300, N, 424, 1, np.sqrt(2*N*0.002))
# plt.loglog(N, crbN)
# plt.show()



