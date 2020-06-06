import matplotlib
from static_crb.CRB import *

matplotlib.rcParams.update({'font.size': 14})

dill.settings['recurse'] = True
file_minflux = 'pickles/crb_lambda_minflux'
file_orbital = 'pickles/crb_lambda_orbital'
file_orbital_iscat = 'pickles/crb_lambda_orbital_iscat'
file_knight = 'pickles/crb_lambda_knight'
file_knight_iscat = 'pickles/crb_lambda_knight_iscat'
file_camera = 'pickles/crb_lambda_camera'

# minflux = MinFlux(file_minflux)
# print('minflux')
# orbital = Orbital(file_orbital)
# print('orbital')
# orbital_iscat = Orbital(file_orbital_iscat, iscat=True)
# print('orbital_iscat')
# knight = Knight(file_knight, 300)
# knight_iscat = Knight(file_knight_iscat, 300, iscat=True)
# print('knight')
# camera = Camera(file_camera)
# print('camera')

# fileobject_minflux = open(file_minflux, 'rb')
# crb_lambda_minflux = dill.load(fileobject_minflux)

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)

fileobject_orbital_iscat = open(file_orbital_iscat, 'rb')
crb_lambda_orbital_iscat = dill.load(fileobject_orbital_iscat)

fileobject_knight = open(file_knight, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)

fileobject_knight_iscat = open(file_knight_iscat, 'rb')
crb_lambda_knight_iscat = dill.load(fileobject_knight_iscat)

# fileobject_camera = open(file_camera, 'rb')
# crb_lambda_camera = dill.load(fileobject_camera)

contrast = 4.47e-6  # LHCII
contrast = 0.0011  # PB
contrast = 6.39e-7  # EGFP
contrast = 2.97e-4  # HIV-QD
# contrast2 = 0.003
n = np.logspace(0.1, 9, num=20)
nscat = 106 * n  # LHCII
nscat = 118 * n  # PB
nscat = 0.497 * n  # EGFP
nscat = 79.8 * n  # HIV-QD
nsigma = np.sqrt(2 * nscat / contrast)
# nsigma2 = np.sqrt(2 * n / contrast2)

crborb = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat = crb_lambda_orbital_iscat(0, 1, 566, nscat, 400, 1, nsigma)
# crborb_iscat2 = crb_lambda_orbital_iscat(0, 1, 566, n, 400, 1, nsigma2)

crbknight = crb_lambda_knight(0, 1, 566, n, 400, 1)
crbknight_iscat = crb_lambda_knight_iscat(0, 1, 566, nscat, 400, 1, nsigma)
# fit = 100 / np.sqrt(n)

plt.figure(figsize=[7.0, 5.5])
plt.yscale('log')
plt.loglog(n, crborb, label='Orbital (Fluorescence)')
plt.loglog(n, crborb_iscat, label='Orbital (iScat)')
plt.loglog(n, crbknight, label='Knight (Fluorescence)')
plt.loglog(n, crbknight_iscat, label='Knight (iSCAT)')
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
