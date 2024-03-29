"""Compare iSCAT and fluorescence for different samples as afunction of number of photons"""
import matplotlib
from static_crb.CRB import *
import rsmf
import seaborn as sns

# color_list = ['#5f4690', '#349ca3', '#52a14c', '#e79406', '#b9474e', '#764276', '#666666']
# color_list = ['#5f4690', '#2f92a0', '#309350', '#edad08', '#d35f2b', '#963d7b', '#666666']
color_list = ['#5f4690', '#1d6996', '#38a6a5', '#0f8554', '#73af48', '#edad08', '#e17c05', '#cc503e', '#94346e',
              '#6f4070', '#994e95', '#666666']
color_list = ['#1d6996', '#73af48', '#edad08', '#e17c05', '#cc503e', '#94346e', '#6f4070']
# color_list = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33']
# plt.rcParams['axes.prop_cycle'] = plt.cycler(color=sns.color_palette())
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

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
    contrast_1 = 4.75e-5  # LHCII
    contrast_11 = 2.09e-4  # LHCII-micelle
    contrast_2 = 0.0004  # PB
    contrast_3 = 6.36e-6  # EGFP
    contrast_4 = 0.057  # HIV-QD
    n1 = np.logspace(1.8, 9, num=50)
    n1_kt = np.logspace(1.67, 9, num=50)
    n11 = np.logspace(1, 9, num=50)
    n11_kt = np.logspace(1, 9, num=50)
    n2 = np.logspace(1, 9, num=20)
    n2_kt = np.logspace(1, 9, num=50)
    n3 = np.logspace(2.3, 9, num=50)
    n3_kt = np.logspace(2.21, 9, num=50)
else:
    contrast_1 = 1.61e-4  # LHCII
    contrast_11 = 7.07e-4  # LHCII-micelle
    contrast_2 = 0.00663  # PB
    contrast_3 = 1.71e-5  # EGFP
    contrast_4 = 0.903  # HIV-QD
    n1 = np.logspace(3.6, 9, num=50)
    n1_kt = np.logspace(2.86, 9, num=50)
    n11 = np.logspace(2.3, 9, num=50)
    n11_kt = np.logspace(1.89, 9, num=50)
    n2 = np.logspace(2.2, 9, num=50)
    n2_kt = np.logspace(1.87, 9, num=50)
    n3 = np.logspace(4.4, 9, num=50)
    n3_kt = np.logspace(3.7, 9, num=50)
n4 = np.logspace(0, 9, num=50)

if adjusted:
    nscat_1 = 0.91 * n1 * 1000  # LHCII
    nscat_1_kt = 0.91 * n1_kt * 1000  # LHCII
    nscat_11 = 3.99 * n11 * 1000  # LHCII-micelle
    nscat_11_kt = 3.99 * n11_kt * 1000  # LHCII-micelle
    nscat_2 = 1.27 * n2 * 1000  # PB
    nscat_2_kt = 1.27 * n2_kt * 1000  # PB
    nscat_3 = 1.98 * n3 * 1000  # EGFP
    nscat_3_kt = 1.98 * n3_kt * 1000  # EGFP
else:
    nscat_1 = 3.1 * n1  # LHCII
    nscat_1_kt = 3.1 * n1_kt  # LHCII
    nscat_11 = 13.5 * n11  # LHCII-micelle
    nscat_11_kt = 13.5 * n11_kt  # LHCII-micelle
    nscat_2 = 2.1 * n2  # PB
    nscat_2_kt = 2.1 * n2_kt  # PB
    nscat_3 = 5.3 * n3  # EGFP
    nscat_3_kt = 5.3 * n3_kt  # EGFP
nscat_4 = 88547 * n4  # HIV-QD

nsigma_1 = np.sqrt(2 * nscat_1 / contrast_1)
nsigma_1_kt = np.sqrt(2 * nscat_1_kt / contrast_1)
nsigma_11 = np.sqrt(2 * nscat_11 / contrast_11)
nsigma_11_kt = np.sqrt(2 * nscat_11_kt / contrast_11)
nsigma_2 = np.sqrt(2 * nscat_2 / contrast_2)
nsigma_2_kt = np.sqrt(2 * nscat_2_kt / contrast_2)
nsigma_3 = np.sqrt(2 * nscat_3 / contrast_3)
nsigma_3_kt = np.sqrt(2 * nscat_3_kt / contrast_3)
nsigma_4 = np.sqrt(2 * nscat_4 / contrast_4)

crborb_1 = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat_1 = crb_lambda_orbital_iscat(0, 1, 566, nscat_1, 400, 1, nsigma_1)
crbknight_1 = crb_lambda_knight(0, 1, 566, n, 400, 1)
crbknight_iscat_1 = crb_lambda_knight_iscat(0, 1, 566, nscat_1_kt, 400, 1, nsigma_1_kt)

crborb_11 = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat_11 = crb_lambda_orbital_iscat(0, 1, 566, nscat_11, 400, 1, nsigma_11)
crbknight_11 = crb_lambda_knight(0, 1, 566, n, 400, 1)
crbknight_iscat_11 = crb_lambda_knight_iscat(0, 1, 566, nscat_11_kt, 400, 1, nsigma_11_kt)

crborb_2 = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat_2 = crb_lambda_orbital_iscat(0, 1, 566, nscat_2, 400, 1, nsigma_2)
crbknight_2 = crb_lambda_knight(0, 1, 566, n, 400, 1)
crbknight_iscat_2 = crb_lambda_knight_iscat(0, 1, 566, nscat_2_kt, 400, 1, nsigma_2_kt)

crborb_3 = crb_lambda_orbital(0, 1, 566, n, 400, 1)
crborb_iscat_3 = crb_lambda_orbital_iscat(0, 1, 566, nscat_3, 400, 1, nsigma_3)
crbknight_3 = crb_lambda_knight(0, 1, 566, n, 400, 1)
crbknight_iscat_3 = crb_lambda_knight_iscat(0, 1, 566, nscat_3_kt, 400, 1, nsigma_3_kt)

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
l2 = ax1.loglog(n1, crborb_iscat_1, label='Orbital (iSCAT)')
l4 = ax1.loglog(n1_kt, crbknight_iscat_1, label="Knight's Tour (iSCAT)")
l3 = ax1.loglog(n, crbknight_1, label="Knight's Tour (Fluorescence)", color='C3')
l1 = ax1.loglog(n, crborb_1, label='Orbital (Fluorescence)')

ax2.loglog(n11, crborb_iscat_11)
ax2.loglog(n11_kt, crbknight_iscat_11)
ax2.loglog(n, crborb_11)
ax2.loglog(n, crbknight_11)

ax3.loglog(n2, crborb_iscat_2)#, label='Orbital (iScat)')
ax3.loglog(n2_kt, crbknight_iscat_2)#, label='Knight (iSCAT)')
ax3.loglog(n, crborb_2)#, label='Orbital (Fluorescence)')
ax3.loglog(n, crbknight_2)#, label='Knight (Fluorescence)')
# ax2.loglog(n, fit)#, label='Knight (iSCAT)')

ax4.loglog(n3, crborb_iscat_3)#, label='Orbital (iScat)')
ax4.loglog(n3_kt, crbknight_iscat_3)#, label='Knight (iSCAT)')
ax4.loglog(n, crborb_3)#, label='Orbital (Fluorescence)')
ax4.loglog(n, crbknight_3)#, label='Knight (Fluorescence)')

ax5.loglog(n4, crborb_iscat_4)#, label='Orbital (iScat)')
ax5.loglog(n4, crbknight_iscat_4)#, label='Knight (iSCAT)')
ax5.loglog(n, crborb_4)#, label='Orbital (Fluorescence)')
ax5.loglog(n, crbknight_4)#, label='Knight (Fluorescence)')

plt.ylim(None, 100)
fig.legend(bbox_to_anchor=(0.9, 0.85), loc='upper right')
ax1.set_ylabel('CRB (nm)')
ax2.set_ylabel('CRB (nm)')
ax4.set_ylabel('CRB (nm)')
ax4.set_xlabel('Number of photons (fluorescence)')
ax5.set_xlabel('Number of photons (fluorescence)')
ax1.text(100, 0.01, "LHCII")
ax2.text(100, 0.01, "LHCII-micelle")
ax3.text(100, 0.01, "PB")
ax4.text(100, 0.1, "GFP")
ax5.text(10, 0.0001, "HIV-QD")

multip_func_1 = lambda x, n: x * n
div_func_1 = lambda x, n: x / n
if adjusted:
    multip_func_1 = lambda x: 0.91 * x * 1000  # LHCII
    div_func_1 = lambda x: x / (0.91 * 1000)  # LHCII
    multip_func_11 = lambda x: 3.99 * x * 1000  # LHCII-micelle
    div_func_11 = lambda x: x / (3.99 * 1000)  # LHCII
    multip_func_2 = lambda x: 1.27 * x * 1000  # PB
    div_func_2 = lambda x: x / (1.27 * 1000)  # LHCII
    multip_func_3 = lambda x: 1.98 * x * 1000  # EGFP
    div_func_3 = lambda x: x / (1.98 * 1000)  # LHCII
else:
    multip_func_1 = lambda x: 3.1 * x  # LHCII
    div_func_1 = lambda x: x / (3.1 * 1000)  # LHCII
    multip_func_11 = lambda x: 13.5 * x  # LHCII-micelle
    div_func_11 = lambda x: x / (13.5 * 1000)  # LHCII
    multip_func_2 = lambda x: 2.1 * x  # PB
    div_func_2 = lambda x: x / (2.1 * 1000)  # LHCII
    multip_func_3 = lambda x: 5.3 * x  # EGFP
    div_func_3 = lambda x: x / (5.3 * 1000)  # LHCII
multip_func_4 = lambda x: 88547 * x  # HIV-QD
div_func_4 = lambda x: x / 88547  # LHCII

secax1 = ax1.secondary_xaxis('top', functions=(multip_func_1, div_func_1))
secax1.set_xlabel('Number of photons (iSCAT)')
secax2 = ax2.secondary_xaxis('top', functions=(multip_func_11, div_func_11))
# secax2.set_xlabel('Number of photons (iSCAT)')
secax3 = ax3.secondary_xaxis('top', functions=(multip_func_2, div_func_2))
secax3.set_xlabel('Number of photons (iSCAT)')
secax4 = ax4.secondary_xaxis('top', functions=(multip_func_3, div_func_3))
# secax4.set_xlabel('Number of photons (iSCAT)')
secax5 = ax5.secondary_xaxis('top', functions=(multip_func_4, div_func_4))
# secax5.set_xlabel('Number of photons (iSCAT)')

for ax in fig.get_axes():
    for line in ax.lines:
        line.set_lw(1.2)
        
if adjusted:
    pass
    # ax1.text(1e6, 10, '$I_s = 5 I_f$', fontsize=16)
    # ax2.text(1e6, 10, '$I_s = 10 I_f$', fontsize=16)
    # ax3.text(1e6, 10, '$I_s = 5000 I_f$', fontsize=16)

plt.subplots_adjust(hspace=0.4)
# plt.tight_layout()
if not adjusted:
    plt.savefig('../out/comp_numphotons.pdf')
else:
    plt.savefig('../out/comp_numphotons_adjusted.pdf')
plt.show()
