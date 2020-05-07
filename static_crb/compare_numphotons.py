import matplotlib
from static_crb.CRB import *

matplotlib.rcParams.update({'font.size': 14})

dill.settings['recurse'] = True
file_minflux = 'pickles/crb_lambda_minflux'
file_orbital = 'pickles/crb_lambda_orbital'
file_orbital_iscat = 'pickles/crb_lambda_orbital_iscat'
file_knight = 'pickles/crb_lambda_knight'
file_camera = 'pickles/crb_lambda_camera'

# minflux = MinFlux(file_minflux)
# print('minflux')
# orbital = Orbital(file_orbital)
# print('orbital')
# orbital_iscat = Orbital(file_orbital_iscat, iscat=True)
# print('orbital_iscat')
# knight = Knight(file_knight)
# print('knight')
# camera = Camera(file_camera)
# print('camera')

# fileobject_minflux = open(file_minflux, 'rb')
# crb_lambda_minflux = dill.load(fileobject_minflux)

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)

fileobject_orbital_iscat = open(file_orbital_iscat, 'rb')
crb_lambda_orbital_iscat = dill.load(fileobject_orbital_iscat)

# fileobject_knight = open(file_knight, 'rb')
# crb_lambda_knight = dill.load(fileobject_knight)

# fileobject_camera = open(file_camera, 'rb')
# crb_lambda_camera = dill.load(fileobject_camera)

contrast = 0.03
n = np.logspace(2, 6, num=20)
nsigma = np.sqrt(2 * n / contrast)

crborb = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat = crb_lambda_orbital_iscat(0, 1, 566, n, 400, 1, nsigma)

plt.figure(figsize=[7.0, 5.5])
plt.yscale('log')
plt.loglog(n, crborb, label='Orbital (Fluorescence)')
plt.loglog(n, crborb_iscat, label='Orbital (iScat)')
# plt.ylim(None, 100)
plt.legend(loc='lower right')
plt.xlabel('Number of photons')
plt.ylabel('CRB (nm)')
# plt.savefig('../out/comp_fluor_iscat.png')
plt.show()
