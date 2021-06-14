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

if adjusted:
    nfact1 = 0.91 * 1000  # LHCII
    nfact11 = 3.99 * 1000  # LHCII-micelle
    nfact2 = 1.27 * 1000  # PB
    nfact3 = 1.98 * 1000  # EGFP
    nfact4 = 88547 * 1000  # HIV-QD

    contrast_1 = 4.75e-5  # LHCII
    contrast_11 = 2.09e-4  # LHCII-micelle
    contrast_2 = 4.00e-3  # PB
    contrast_3 = 6.36e-6  # EGFP
    contrast_4 = 0.057  # HIV-QD
else:
    nfact1 = 3.1 # LHCII
    nfact11 = 13.5 # LHCII-micelle
    nfact2 = 2.1 # PB
    nfact3 = 5.3 # EGFP
    nfact4 = 88547 # HIV-QD

    contrast_1 = 1.61e-4  # LHCII
    contrast_11 = 7.07e-4  # LHCII-micelle
    contrast_2 = 0.00663  # PB
    contrast_3 = 1.71e-5  # EGFP
    contrast_4 = 0.903  # HIV-QD

asymp1 = 2 / contrast_1
asymp1_plot = asymp1 / nfact1
asymp11 = 2 / contrast_11
asymp11_plot = asymp11 / nfact11
asymp2 = 2 / contrast_2
asymp2_plot = asymp2 / nfact2
asymp3 = 2 / contrast_3
asymp3_plot = asymp3 / nfact3
print(asymp1, np.log10(asymp1))

n = np.logspace(-0.7, 9, num=20)

if adjusted:
    numplotpoints = 2500
else:
    numplotpoints = 200
n1 = np.logspace(np.log10(asymp1_plot), 9, num=numplotpoints)
n1_kt = np.logspace(np.log10(asymp1_plot), 9, num=numplotpoints)
n11 = np.logspace(np.log10(asymp11_plot), 9, num=numplotpoints)
n11_kt = np.logspace(np.log10(asymp11_plot), 9, num=numplotpoints)
n2 = np.logspace(np.log10(asymp2_plot), 9, num=numplotpoints)
n2_kt = np.logspace(np.log10(asymp2_plot), 9, num=numplotpoints)
n3 = np.logspace(np.log10(asymp3_plot), 9, num=numplotpoints)
n3_kt = np.logspace(np.log10(asymp3_plot), 9, num=numplotpoints)
n4 = np.logspace(-0.7, 9, num=100)

nscat_1 = nfact1 * n1  # LHCII
nscat_1_kt = nfact1 * n1_kt  # LHCII
nscat_11 = nfact11 * n11  # LHCII-micelle
nscat_11_kt = nfact11 * n11_kt  # LHCII-micelle
nscat_2 = nfact2 * n2  # PB
nscat_2_kt = nfact2 * n2_kt  # PB
nscat_3 = nfact3 * n3  # EGFP
nscat_3_kt = nfact3 * n3_kt  # EGFP
nscat_4 = nfact4 * n4  # HIV-QD

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
ax1 = fig.add_subplot()

ax1.set_yscale('log')
l1 = ax1.loglog(n, crborb_1, label='Fluorescence')
l2 = ax1.loglog(n1, crborb_iscat_1, label='LHCII (iSCAT)')
ax1.loglog(n11, crborb_iscat_11, label='LHCII-micelle (iSCAT)')
ax1.loglog(n2, crborb_iscat_2, label='PB (iSCAT)')
ax1.loglog(n3, crborb_iscat_3, label='GFP (iSCAT)')
ax1.loglog(n4, crborb_iscat_4, label='HIV-QD (iSCAT)')

# ax1.vlines(asymp1_plot, 10, 800, color='C1', linestyles='--', lw=1.0)
# ax1.vlines(asymp11_plot, 10, 800, color='C2', linestyles='--', lw=1.0)
# ax1.vlines(asymp2_plot, 10, 800, color='C3', linestyles='--', lw=1.0)
# ax1.vlines(asymp3_plot, 10, 800, color='C4', linestyles='--', lw=1.0)

# plt.ylim(None, 100)
fig.legend(bbox_to_anchor=(0.13, 0.10), loc='lower left', framealpha=0.0, ncol=1)
ax1.set_ylabel('CRB (nm)')
ax1.set_xlabel('Number of photons (fluorescence)')
# ax1.text(100, 0.01, "LHCII")
# ax1.text(100, 0.01, "LHCII-micelle")
# ax1.text(100, 0.01, "PB")
# ax1.text(100, 0.1, "GFP")
# ax1.text(10, 0.0001, "HIV-QD")

if adjusted:
    multip_func_av = lambda x: 2 * x * 1000  # LHCII
    div_func_av = lambda x: x / (2 * 1000)  # LHCII
    multip_func_1 = lambda x: 0.91 * x * 1000  # LHCII
    div_func_1 = lambda x: x / (0.91 * 1000)  # LHCII
    multip_func_11 = lambda x: 3.99 * x * 1000  # LHCII-micelle
    div_func_11 = lambda x: x / (3.99 * 1000)  # LHCII
    multip_func_2 = lambda x: 1.27 * x * 1000  # PB
    div_func_2 = lambda x: x / (1.27 * 1000)  # LHCII
    multip_func_3 = lambda x: 1.98 * x * 1000  # EGFP
    div_func_3 = lambda x: x / (1.98 * 1000)  # LHCII
else:
    multip_func_av = lambda x: 6 * x  # LHCII
    div_func_av = lambda x: x / (6 * 1000)  # LHCII
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

secax1 = ax1.secondary_xaxis('top', functions=(multip_func_av, div_func_av))
secax2 = ax1.secondary_xaxis(1.13, functions=(multip_func_4, div_func_4))
# secax3 = ax1.secondary_xaxis(1.2, functions=(multip_func_2, div_func_2))
# secax4 = ax1.secondary_xaxis(1.3, functions=(multip_func_3, div_func_3))
# secax5 = ax1.secondary_xaxis(1.4, functions=(multip_func_4, div_func_4))
secax2.set_xlabel('Number of iSCAT photons (HIV-QD)')
secax1.set_xlabel('Average number of iSCAT photons (Other samples)')
# secax1.tick_params(axis='x', colors='C1')
# secax2.tick_params(axis='x', colors='C2')
# secax3.tick_params(axis='x', colors='C3')
# secax4.tick_params(axis='x', colors='C4')
# secax5.tick_params(axis='x', colors='C5')

for ax in fig.get_axes():
    for line in ax.lines:
        line.set_lw(1.5)
        
if adjusted:
    pass

ax1.set_ylim(None, 5e3)

plt.subplots_adjust(hspace=0.4)
plt.tight_layout()
if not adjusted:
    plt.savefig('../out/comp_numphotons.pdf')
else:
    plt.savefig('../out/comp_numphotons_adjusted.pdf')
plt.show()
