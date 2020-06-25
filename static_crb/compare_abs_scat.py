import matplotlib
from static_crb.CRB import *
from matplotlib import ticker

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

contrast_1 = 4.47e-6  # LHCII
contrast_2 = 0.0011  # PB
contrast_3 = 6.39e-7  # EGFP
contrast_4 = 2.97e-4  # HIV-QD
nscat_1 = 106   # LHCII
nscat_2 = 118   # PB
nscat_3 = 0.497   # EGFP
nscat_4 = 79.8   # HIV-QD

contrast = np.linspace(1e-8, 1e-2, num=20)
nfactor = np.linspace(0.1, 120, num=200)
contrast = np.logspace(-6.5, -2, num=20)
nfactor = np.logspace(-0.5, 2.1, num=20)
contrast = np.logspace(-6, -2, num=20)
nfactor = np.linspace(70, 130, num=20)
n = 1e8
nscat = nfactor * n
contrastv, nscatv = np.meshgrid(contrast, nscat)

nsigma = np.sqrt(2 * nscatv / contrastv)

crborb_1 = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat_1 = crb_lambda_orbital_iscat(0, 1, 566, nscatv, 400, 1, nsigma)

print(crborb_1)
crb_diff = crborb_iscat_1 - crborb_1
crb_diff = np.clip(crb_diff, -100, 1)

fig, ax = plt.subplots()
crbcont = ax.contourf(contrastv, nscatv, crb_diff, 100)
ax.set_xscale('log')
# ax.set_yscale('log')

fig.colorbar(crbcont)

ax.plot(4.47e-6, 106e8, 'ro')
ax.plot(0.0011, 118e8, 'ro')
# ax.plot(6.39e-7, 0.497e8, 'ro')
ax.plot(2.97e-4, 79.8e8, 'ro')

# plt.savefig('../out/comp_fluor_iscat.png')
plt.show()
