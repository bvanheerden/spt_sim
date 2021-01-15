import matplotlib
from static_crb.CRB import *
import rsmf

# formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
#                                  pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': 11})

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

contrast_1 = 1.02e-5  # LHCII
contrast_11 = 4.47e-5  # LHCII-micelle
contrast_2 = 0.00042  # PB
contrast_3 = 1.65e-6  # EGFP
contrast_4 = 0.057  # HIV-QD

adjusted = False

n = np.logspace(1, 9, num=20)
if adjusted:
    n1 = np.logspace(2.5, 9, num=20)
    n11 = np.logspace(1, 9, num=20)
    n2 = np.logspace(2.2, 9, num=20)
    n3 = np.logspace(2.5, 9, num=20)
else:
    n1 = np.logspace(3, 9, num=20)
    n11 = np.logspace(1.9, 9, num=20)
    n2 = np.logspace(2.2, 9, num=20)
    n3 = np.logspace(4, 9, num=20)
n4 = np.logspace(2.3, 9, num=20)
n4 = np.logspace(0, 9, num=20)
if adjusted:
    nscat_1 = 260 * n1 * 5  # LHCII
    nscat_11 = 1145 * n11 * 5  # LHCII-micelle
    nscat_2 = 45 * n2 * 1  # PB
    nscat_3 = 1.45 * n3 * 5000  # EGFP
else:
    nscat_1 = 260 * n1  # LHCII
    nscat_11 = 1145 * n11  # LHCII-micelle
    nscat_2 = 45 * n2  # PB
    nscat_3 = 1.45 * n3  # EGFP
    nscat_3 = 128 * n3  # EGFP
nscat_4 = 1500000 * n4  # HIV-QD
nsigma_1 = np.sqrt(2 * nscat_1 / contrast_1)
nsigma_11 = np.sqrt(2 * nscat_11 / contrast_11)
nsigma_2 = np.sqrt(2 * nscat_2 / contrast_2)
nsigma_3 = np.sqrt(2 * nscat_3 / contrast_3)
nsigma_4 = np.sqrt(2 * nscat_4 / contrast_4)

crborb_1 = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat_1 = crb_lambda_orbital_iscat(0, 1, 566, nscat_1, 400, 1, nsigma_1)
crbknight_1 = crb_lambda_knight(0, 1, 566, n, 400, 1)
crbknight_iscat_1 = crb_lambda_knight_iscat(0, 1, 566, nscat_1, 400, 1, nsigma_1)

crborb_11 = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat_11 = crb_lambda_orbital_iscat(0, 1, 566, nscat_11, 400, 1, nsigma_11)
crbknight_11 = crb_lambda_knight(0, 1, 566, n, 400, 1)
crbknight_iscat_11 = crb_lambda_knight_iscat(0, 1, 566, nscat_11, 400, 1, nsigma_11)

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

fit = 100 / np.sqrt(n)

# plt.figure(figsize=[7.0, 5.5])

# fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, sharex='col', figsize=(7, 18))
fig = plt.figure(figsize=(4, 4), dpi=150)
# fig = formatter.figure(width_ratio=0.8, aspect_ratio=1)
spec = matplotlib.gridspec.GridSpec(ncols=1, nrows=1)
ax1 = fig.add_subplot(spec[0, 0])
# ax2 = fig.add_subplot(spec[1, 0])
# ax3 = fig.add_subplot(spec[1, 1])
# ax4 = fig.add_subplot(spec[2, 0])
# ax5 = fig.add_subplot(spec[2, 1])

ax1.set_yscale('log')
l1 = ax1.loglog(n, crborb_1, label='Fluorescence')
l2 = ax1.loglog(n1, crborb_iscat_1, label='LHCII')
# l3 = ax1.loglog(n, crbknight_1, label='Ruitersprong (Fluoressensie)')
# l4 = ax1.loglog(n1, crbknight_iscat_1, label='Ruitersprong (iSCAT)')

# ax1.loglog(n, crborb_11, label='LHCII-micelle')
ax1.loglog(n11, crborb_iscat_11, label='LHCII-micelle')
# ax2.loglog(n, crbknight_11)
# ax2.loglog(n11, crbknight_iscat_11)

# ax3.loglog(n, crborb_2)#, label='Orbital (Fluorescence)')
ax1.loglog(n2, crborb_iscat_2, label='PB')#, label='Orbital (iScat)')
# ax1.plot(np.zeros(1), np.zeros([1,3]), color='w', alpha=0, label=' ')#, label='Orbital (iScat)')
# ax3.loglog(n, crbknight_2)#, label='Knight (Fluorescence)')
# ax3.loglog(n2, crbknight_iscat_2)#, label='Knight (iSCAT)')
# ax2.loglog(n, fit)#, label='Knight (iSCAT)')

# ax4.loglog(n, crborb_3)#, label='Orbital (Fluorescence)')
ax1.loglog(n3, crborb_iscat_3, label='GFP')#, label='Orbital (iScat)')
# ax4.loglog(n, crbknight_3)#, label='Knight (Fluorescence)')
# ax4.loglog(n3, crbknight_iscat_3)#, label='Knight (iSCAT)')

# ax5.loglog(n, crborb_4)#, label='Orbital (Fluorescence)')
ax1.loglog(n4, crborb_iscat_4, label='HIV-QD')#, label='Orbital (iScat)')
# ax5.loglog(n, crbknight_4)#, label='Knight (Fluorescence)')
# ax5.loglog(n4, crbknight_iscat_4)#, label='Knight (iSCAT)')

# plt.loglog(n, fit, '--')
# plt.loglog(n, crborb_iscat2, label='Orbital (iScat)')
# plt.axvline(670000)
# plt.axhline(0.5)
# plt.ylim(None, 100)
fig.legend(loc='lower left', bbox_to_anchor=(0.19, 0.15), ncol=2, columnspacing=1, borderpad=0.1)
ax1.set_ylabel('CRB (nm)')
# ax2.set_ylabel('CRB (nm)')
# ax4.set_ylabel('CRB (nm)')
ax1.set_xlabel('Number of photons (Fluorescence)')
# ax4.set_xlabel('Aantal fotone (fluoressensie)')
# ax5.set_xlabel('Aantal fotone (fluoressensie)')
# ax1.set_title("LHCII")
# ax2.set_title("LHCII-misel")
# ax3.set_title("FB")
# ax4.set_title("GFP")
# ax5.set_title("MIV-QD")

ax1.set_ylim(1e-7, None)

if adjusted:
    ax1.text(1e6, 10, '$I_s = 5 I_f$', fontsize=16)
    # ax2.text(1e6, 10, '$I_s = 10 I_f$', fontsize=16)
    # ax3.text(1e6, 10, '$I_s = 5000 I_f$', fontsize=16)

# ax1.set_xlim((8e3, None))

# plt.subplots_adjust(right=0.6, left=0.12, top=0.95, hspace=0.3)
plt.subplots_adjust(hspace=0.4)
plt.tight_layout()
if not adjusted:
    plt.savefig('../out/poster/comp_numphotons.pdf')
else:
    plt.savefig('../out/poster/comp_numphotons_adjusted.png')
plt.show()
