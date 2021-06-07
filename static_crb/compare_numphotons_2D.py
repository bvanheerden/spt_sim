"""2D plot of CRB as a function of absorption and scattering cross sections"""
import matplotlib
import numpy as np

from static_crb.CRB import *
from matplotlib import ticker
import matplotlib.colors as colors
import matplotlib.patheffects as PathEffects
import rsmf

# matplotlib.rcParams.update({'font.size': 14})
latex = True

if latex:
    formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                     pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

    matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

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

sigma_scat = np.logspace(-13, -2, num=100)
sigma_qy = np.logspace(-8, -4, num=100)

sigma_scatv, sigma_qyv = np.meshgrid(sigma_scat, sigma_qy)
contrastv = 2 * np.sqrt(sigma_scatv) / np.sqrt(0.004)

n = 1e6
nfactor = 2 * np.sqrt(sigma_scatv * 0.004) / sigma_qyv
nscat = nfactor * n
nsigma = np.sqrt(2 * nscat / contrastv)

crborb_1 = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat_1 = crb_lambda_orbital_iscat(0, 1, 566, nscat, 400, 1, nsigma)

print(crborb_1)
crb_diff = - np.log(crborb_iscat_1) + np.log(crborb_1)
crb_diff = np.log(crborb_1 / crborb_iscat_1)
mask = np.zeros_like(crb_diff, dtype=bool)
for row, val in enumerate(mask):
    for col, val in enumerate(val):
        if col < 0.4*row - 10:
            mask[row, col] = True

crb_diff = np.ma.array(crb_diff, mask=mask)

if latex:
    fig = formatter.figure(width_ratio=0.7)
else:
    fig = plt.figure(figsize=[7, 5])
ax = fig.add_subplot()
ax.set_facecolor('lightgray')
crbcont = ax.contourf(sigma_qyv, sigma_scatv, crb_diff, 100, cmap='RdBu', norm=colors.TwoSlopeNorm(vcenter=1))
ax.set_xscale('log')
ax.set_ylabel('Scattering cross-section')
ax.set_xlabel('Absorption cross-section')
ax.set_yscale('log')

colorbar1 = fig.colorbar(crbcont)
colorbar1.set_label(r'Logarithm of CRB ratio $\log(\sigma_{scat}/\sigma_{fluo})$')

# ax.axhline(3e-7)

point1 = (2.096e-7, 2.57605e-11)  # LHCII
point2 = (2.096e-7, 4.99173e-10)  # LHCII-micelle
point3 = (1.258e-5, 4.39747e-8)  # PB
point4 = (1.3e-8, 2.9e-13)  # GFP
point5 = (4.08e-8, 8.2e-4)  # HIV-QD
points = [point1, point2, point3, point4, point5]
labels = ['LHCII', 'LHCII-micelle', 'PB', 'GFP', 'HIV-QD']

for i, point in enumerate(points):
    ax.plot(point[0], point[1], 'o', color='white', markeredgecolor='black')
    if labels[i] == 'HIV-QD':
        ax.annotate(labels[i], point, (5, -20), textcoords='offset pixels', color='black')
    else:
        ax.annotate(labels[i], point, (5, 5), textcoords='offset pixels', color='black')

plt.tight_layout()
plt.savefig('../out/comp_fluor_iscat.pdf')
plt.show()
