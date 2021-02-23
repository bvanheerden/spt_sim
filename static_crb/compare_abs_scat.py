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

sigma_scat = 25e-6
sigma_scat2 = 25e-8
sigma_qy = np.logspace(-5, -3, num=200)
contrast = 2 * np.sqrt(sigma_scat)
contrast2 = 2 * np.sqrt(sigma_scat2)
nfactor = contrast / sigma_qy
# contrast = 0.01
# contrast2 = 0.001
# nfactor = np.logspace(-0.5, 2.2, num=200)
# contrast = np.linspace(1e-5, 0.01, num=200)
# nfactor = 100
n = 1e4
nscat = nfactor * n

nsigma = np.sqrt(2 * nscat / contrast)
nsigma2 = np.sqrt(2 * nscat / contrast2)

crborb_1 = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat_1 = crb_lambda_orbital_iscat(0, 1, 566, nscat, 400, 1, nsigma)
crborb_iscat_1_2 = crb_lambda_orbital_iscat(0, 1, 566, nscat, 400, 1, nsigma2)

crb_diff = crborb_iscat_1 - crborb_1
crb_diff2 = crborb_iscat_1_2 - crborb_1

fig, ax = plt.subplots()

ax.plot(sigma_qy, crb_diff, label='$\sigma_s = 2.5 \\times 10^{-5}$ cm$^2$')
ax.plot(sigma_qy, crb_diff2, label='$\sigma_s = 2.5 \\times 10^{-7}$ cm$^2$')
# ax.set_ylim(-2, 10)
ax.set_xscale('log')
ax.set_yscale('symlog')
ax.set_xlabel('Absorption cross-section (cm$^2$)')
ax.set_ylabel('CRB difference (iScat - fluorescence)')
plt.legend()

plt.show()
