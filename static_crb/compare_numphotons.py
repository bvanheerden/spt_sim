"""Compare iSCAT and fluorescence for different samples as afunction of number of photons"""
import matplotlib
from static_crb.CRB import *
import rsmf

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

compute_crb = False

if compute_crb:
    # orbital = Orbital(file_orbital)
    # print('orbital')
    orbital_iscat = Orbital(file_orbital_iscat, iscat=True)
    print('orbital_iscat')
    # knight = Knight(file_knight, 300)
    # knight_iscat = Knight(file_knight_iscat, 300, iscat=True)
    # print('knight')

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)

fileobject_orbital_iscat = open(file_orbital_iscat, 'rb')
crb_lambda_orbital_iscat = dill.load(fileobject_orbital_iscat)

fileobject_knight = open(file_knight, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)

fileobject_knight_iscat = open(file_knight_iscat, 'rb')
crb_lambda_knight_iscat = dill.load(fileobject_knight_iscat)

adjusted = True


n = np.logspace(1, 9, num=20)
if adjusted:
    contrast_1 = 1.02e-5  # LHCII
    contrast_11 = 4.47e-5  # LHCII-micelle
    contrast_2 = 0.00042  # PB
    contrast_3 = 1.65e-6  # EGFP
    contrast_4 = 0.057  # HIV-QD
    n1 = np.logspace(2.5, 9, num=20)
    n11 = np.logspace(1, 9, num=20)
    n2 = np.logspace(2.2, 9, num=20)
    n3 = np.logspace(2.5, 9, num=20)
else:
    contrast_1 = 1.02e-5  # LHCII
    contrast_11 = 4.47e-5  # LHCII-micelle
    contrast_2 = 0.00042  # PB
    contrast_3 = 1.65e-6  # EGFP
    contrast_4 = 0.057  # HIV-QD
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

if latex:
    fig = formatter.figure(width_ratio=0.8, aspect_ratio=1)
else:
    fig = plt.figure(figsize=[7, 5])
spec = matplotlib.gridspec.GridSpec(ncols=2, nrows=3)
ax1 = fig.add_subplot(spec[0, 0])
ax2 = fig.add_subplot(spec[1, 0])
ax3 = fig.add_subplot(spec[1, 1])
ax4 = fig.add_subplot(spec[2, 0])
ax5 = fig.add_subplot(spec[2, 1])

ax1.set_yscale('log')
l1 = ax1.loglog(n, crborb_1, label='Orbitaal (Fluoressensie)')
l2 = ax1.loglog(n1, crborb_iscat_1, label='Orbitaal (iSCAT)')
l3 = ax1.loglog(n, crbknight_1, label='Ruitersprong (Fluoressensie)')
l4 = ax1.loglog(n1, crbknight_iscat_1, label='Ruitersprong (iSCAT)')

ax2.loglog(n, crborb_11)
ax2.loglog(n11, crborb_iscat_11)
ax2.loglog(n, crbknight_11)
ax2.loglog(n11, crbknight_iscat_11)

ax3.loglog(n, crborb_2)#, label='Orbital (Fluorescence)')
ax3.loglog(n2, crborb_iscat_2)#, label='Orbital (iScat)')
ax3.loglog(n, crbknight_2)#, label='Knight (Fluorescence)')
ax3.loglog(n2, crbknight_iscat_2)#, label='Knight (iSCAT)')
# ax2.loglog(n, fit)#, label='Knight (iSCAT)')

ax4.loglog(n, crborb_3)#, label='Orbital (Fluorescence)')
ax4.loglog(n3, crborb_iscat_3)#, label='Orbital (iScat)')
ax4.loglog(n, crbknight_3)#, label='Knight (Fluorescence)')
ax4.loglog(n3, crbknight_iscat_3)#, label='Knight (iSCAT)')

ax5.loglog(n, crborb_4)#, label='Orbital (Fluorescence)')
ax5.loglog(n4, crborb_iscat_4)#, label='Orbital (iScat)')
ax5.loglog(n, crbknight_4)#, label='Knight (Fluorescence)')
ax5.loglog(n4, crbknight_iscat_4)#, label='Knight (iSCAT)')

plt.ylim(None, 100)
fig.legend(bbox_to_anchor=(0.9, 0.85), loc='upper right')
ax1.set_ylabel('CRB (nm)')
ax2.set_ylabel('CRB (nm)')
ax4.set_ylabel('CRB (nm)')
ax4.set_xlabel('Number of photons (fluorescence)')
ax5.set_xlabel('Number of photons (fluorescence)')
ax1.set_title("LHCII")
ax2.set_title("LHCII-misel")
ax3.set_title("FB")
ax4.set_title("GFP")
ax5.set_title("MIV-QD")

if adjusted:
    ax1.text(1e6, 10, '$I_s = 5 I_f$', fontsize=16)
    # ax2.text(1e6, 10, '$I_s = 10 I_f$', fontsize=16)
    ax3.text(1e6, 10, '$I_s = 5000 I_f$', fontsize=16)

plt.subplots_adjust(hspace=0.4)
# plt.tight_layout()
if not adjusted:
    plt.savefig('../out/comp_numphotons.pdf')
else:
    plt.savefig('../out/comp_numphotons_adjusted.pdf')
plt.show()
