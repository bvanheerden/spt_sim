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

contrast_1 = 4.47e-6  # LHCII
contrast_2 = 0.0011  # PB
contrast_3 = 6.39e-7  # EGFP
contrast_4 = 2.97e-4  # HIV-QD

n = np.logspace(1, 9, num=20)
n1 = np.logspace(4, 9, num=20)
n2 = np.logspace(1.5, 9, num=20)
n3 = np.logspace(7, 9, num=20)
n4 = np.logspace(2.3, 9, num=20)
nscat_1 = 106 * n1  # LHCII
nscat_2 = 118 * n2  # PB
nscat_3 = 0.497 * n3  # EGFP
nscat_4 = 79.8 * n4  # HIV-QD
nsigma_1 = np.sqrt(2 * nscat_1 / contrast_1)
nsigma_2 = np.sqrt(2 * nscat_2 / contrast_2)
nsigma_3 = np.sqrt(2 * nscat_3 / contrast_3)
nsigma_4 = np.sqrt(2 * nscat_4 / contrast_4)

crborb_1 = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat_1 = crb_lambda_orbital_iscat(0, 1, 566, nscat_1, 400, 1, nsigma_1)
crbknight_1 = crb_lambda_knight(0, 1, 566, n, 400, 1)
crbknight_iscat_1 = crb_lambda_knight_iscat(0, 1, 566, nscat_1, 400, 1, nsigma_1)

crborb_2 = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat_2 = crb_lambda_orbital_iscat(0, 1, 566, nscat_2, 400, 1, nsigma_2)
crbknight_2 = crb_lambda_knight(0, 1, 566, n, 400, 1)
crbknight_iscat_2 = crb_lambda_knight_iscat(0, 1, 566, nscat_2, 400, 1, nsigma_2)

crborb_3 = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat_3 = crb_lambda_orbital_iscat(0, 1, 566, nscat_3, 400, 1, nsigma_3)
crbknight_3 = crb_lambda_knight(0, 1, 566, n, 400, 1)
crbknight_iscat_3 = crb_lambda_knight_iscat(0, 1, 566, nscat_3, 400, 1, nsigma_3)

crborb_4 = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat_4 = crb_lambda_orbital_iscat(0, 1, 566, nscat_4, 400, 1, nsigma_4)
crbknight_4 = crb_lambda_knight(0, 1, 566, n, 400, 1)
crbknight_iscat_4 = crb_lambda_knight_iscat(0, 1, 566, nscat_4, 400, 1, nsigma_4)

# fit = 100 / np.sqrt(n)

# plt.figure(figsize=[7.0, 5.5])

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', figsize=(13, 6))

ax1.set_yscale('log')
l1 = ax1.loglog(n, crborb_1, label='Orbital (Fluorescence)')
l2 = ax1.loglog(n1, crborb_iscat_1, label='Orbital (iScat)')
l3 = ax1.loglog(n, crbknight_1, label='Knight (Fluorescence)')
l4 = ax1.loglog(n1, crbknight_iscat_1, label='Knight (iSCAT)')

ax2.loglog(n, crborb_2)#, label='Orbital (Fluorescence)')
ax2.loglog(n2, crborb_iscat_2)#, label='Orbital (iScat)')
ax2.loglog(n, crbknight_2)#, label='Knight (Fluorescence)')
ax2.loglog(n2, crbknight_iscat_2)#, label='Knight (iSCAT)')

ax3.loglog(n, crborb_3)#, label='Orbital (Fluorescence)')
ax3.loglog(n3, crborb_iscat_3)#, label='Orbital (iScat)')
ax3.loglog(n, crbknight_3)#, label='Knight (Fluorescence)')
ax3.loglog(n3, crbknight_iscat_3)#, label='Knight (iSCAT)')

ax4.loglog(n, crborb_4)#, label='Orbital (Fluorescence)')
ax4.loglog(n4, crborb_iscat_4)#, label='Orbital (iScat)')
ax4.loglog(n, crbknight_4)#, label='Knight (Fluorescence)')
ax4.loglog(n4, crbknight_iscat_4)#, label='Knight (iSCAT)')

# plt.loglog(n, fit, '--')
# plt.loglog(n, crborb_iscat2, label='Orbital (iScat)')
# plt.axvline(670000)
# plt.axhline(0.5)
# plt.ylim(None, 100)
fig.legend(bbox_to_anchor=(1, 0), loc='lower right')
ax3.set_xlabel('Number of photons (fluorescence)')
ax1.set_ylabel('CRB (nm)')
ax4.set_xlabel('Number of photons (fluorescence)')
ax3.set_ylabel('CRB (nm)')
ax1.set_title("LHCII")
ax2.set_title("PB")
ax3.set_title("GFP")
ax4.set_title("HIV-QD")

# ax1.set_xlim((8e3, None))

plt.subplots_adjust(right=0.8, left=0.08)
# plt.savefig('../out/comp_fluor_iscat.png')
plt.show()
