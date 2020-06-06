import matplotlib
from static_crb.CRB import *

matplotlib.rcParams.update({'font.size': 14})

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

contrast = 0.005
n = 10000
nscat = 7 * n
nsigma = np.sqrt(2 * nscat / contrast)

y = np.linspace(-500, 500, num=100)
# plt.yscale('log')
# x, y, L, N, w, amp
# crb100 = crb_lambda_orbital(0, y, 300, 10000, 212, 1, 1000)
# crb200 = crb_lambda_orbital(0, y, 500, 100, 353, 1, 0.5)
crb400 = crb_lambda_orbital(1, y, 300, nscat, 424, 1, nsigma)
# crb800 = crb_lambda_orbital(0, y, 700, 10000, 494, 1, 3000)
# crb800 = crb_lambda_orbital(0, y, 300, 670000, 424, 1, 8165)
# crb1600 = crb_lambda_orbital(0, y, 900, 100, 636, 1, 0.5)

crb800 = crb_lambda_orbital_fluo(0, y, 300, n, 424, 1)

# plt.plot(y, crb100, label='L=300')
# plt.plot(y, crb200, label='L=500')
plt.plot(y, crb400, label='L=564')
plt.plot(y, crb800, label='L=700')
# plt.plot(y, crb1600, label='L=900')
# plt.legend(loc='lower right')
# plt.xlabel('x (nm)')
# plt.ylabel('CRB (nm)')
# plt.tight_layout()
# plt.savefig('../out/orbital_crb.png')
plt.show()

# N = np.arange(1000, 100000, 1000)
# crbN = crb_lambda_orbital(0, 0, 300, N, 424, 1, np.sqrt(2*N*0.002))
# plt.loglog(N, crbN)
# plt.show()



