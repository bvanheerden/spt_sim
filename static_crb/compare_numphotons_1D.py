import matplotlib
from static_crb.CRB import *

matplotlib.rcParams.update({'font.size': 14})

dill.settings['recurse'] = True
file_orbital = 'pickles/crb_lambda_orbital_1D'
file_orbital_iscat = 'pickles/crb_lambda_orbital_iscat_1D'

orbital = MinFlux1D(file_orbital, 'gaussian')
# print('orbital')
orbital_iscat = MinFlux1D(file_orbital_iscat, 'gaussian', iscat=True)
# print('orbital_iscat')

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)

fileobject_orbital_iscat = open(file_orbital_iscat, 'rb')
crb_lambda_orbital_iscat = dill.load(fileobject_orbital_iscat)

contrast = 0.005
# contrast2 = 0.003
n = np.logspace(0.1, 9, num=20)
nscat = 200 * n
nsigma = np.sqrt(2 * nscat / contrast)
# nsigma2 = np.sqrt(2 * n / contrast2)

crborb = crb_lambda_orbital(1, 566, n, 400, 1)
crborb_iscat = crb_lambda_orbital_iscat(1, 566, nscat, 400, 1, nsigma)
# crborb_iscat2 = crb_lambda_orbital_iscat(0, 1, 566, n, 400, 1, nsigma2)

# fit = 100 / np.sqrt(n)

plt.figure(figsize=[7.0, 5.5])
plt.yscale('log')
plt.loglog(n, crborb, label='Orbital (Fluorescence)')
plt.loglog(n, crborb_iscat, label='Orbital (iScat)')
# plt.loglog(n, fit, '--')
# plt.loglog(n, crborb_iscat2, label='Orbital (iScat)')
# plt.axvline(670000)
# plt.axhline(0.5)
# plt.ylim(None, 100)
plt.legend(loc='upper right')
plt.xlabel('Number of photons (fluorescence)')
plt.ylabel('CRB (nm)')
plt.title("Phycobilisome")
# plt.savefig('../out/comp_fluor_iscat.png')
plt.show()
