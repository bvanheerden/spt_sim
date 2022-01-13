"""Compare iSCAT and fluorescence for different samples as afunction of number of photons"""
import matplotlib
from static_crb.CRB import *
import rsmf
import dill

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
    # col_width = 345  # For dissertation I think
    col_width = 470  # For journal draft
    # col_width = 483.7  # For SPIE paper I think
    formatter = rsmf.CustomFormatter(columnwidth=col_width * 0.01389, fontsizes=10,
                                     pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

    matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})
    matplotlib.rcParams.update({'font.family': 'serif'})

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

if latex:
    fig = formatter.figure(width_ratio=1.0, aspect_ratio=0.6)
else:
    fig = plt.figure(figsize=[7, 5])

# adjusted = True
for adjusted in [False, True]:

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
        contrast_4 = 0.903  # HIV-QD
    else:
        nfact1 = 3.1  # LHCII
        nfact11 = 13.5  # LHCII-micelle
        nfact2 = 2.1  # PB
        nfact3 = 5.3  # EGFP
        nfact4 = 88547  # HIV-QD

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

    endpower = 7  # x-axis ends at 10^7
    n = np.logspace(-0.7, endpower, num=20)

    if adjusted:
        numplotpoints = 2500
    else:
        numplotpoints = 200
    n1 = np.logspace(np.log10(asymp1_plot), endpower, num=numplotpoints)
    n1_kt = np.logspace(np.log10(asymp1_plot), endpower, num=numplotpoints)
    n11 = np.logspace(np.log10(asymp11_plot), endpower, num=numplotpoints)
    n11_kt = np.logspace(np.log10(asymp11_plot), endpower, num=numplotpoints)
    n2 = np.logspace(np.log10(asymp2_plot), endpower, num=numplotpoints)
    n2_kt = np.logspace(np.log10(asymp2_plot), endpower, num=numplotpoints)
    n3 = np.logspace(np.log10(asymp3_plot), endpower, num=numplotpoints)
    n3_kt = np.logspace(np.log10(asymp3_plot), endpower, num=numplotpoints)
    n4 = np.logspace(-0.7, endpower, num=100)

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

    if adjusted:
        ax1 = fig.add_subplot(122, sharey=plt.gca())
    else:
        ax1 = fig.add_subplot(121)

    ax1.set_yscale('log')
    gfp, = ax1.loglog(n3, crborb_iscat_3, label='GFP (iSCAT)', color='C4')
    lhcii, = ax1.loglog(n1, crborb_iscat_1, label='LHCII (iSCAT)', color='C1')
    mic, = ax1.loglog(n11, crborb_iscat_11, label='LHCII-micelle (iSCAT)', color='C2')
    pb, = ax1.loglog(n2, crborb_iscat_2, label='PB (iSCAT)', color='C3')
    fluo, = ax1.loglog(n, crborb_1, label='Fluorescence', color='C0')
    hiv, = ax1.loglog(n4, crborb_iscat_4, label='HIV-QD (iSCAT)', color='C5')

    # ax1.vlines(asymp1_plot, 10, 800, color='C1', linestyles='--', lw=1.0)
    # ax1.vlines(asymp11_plot, 10, 800, color='C2', linestyles='--', lw=1.0)
    # ax1.vlines(asymp2_plot, 10, 800, color='C3', linestyles='--', lw=1.0)
    # ax1.vlines(asymp3_plot, 10, 800, color='C4', linestyles='--', lw=1.0)

    # plt.ylim(None, 100)
    if adjusted:
        pass
        # legend1 = plt.legend([pb, gfp, hiv], ['PB (iSCAT)', 'GFP (iSCAT)', 'HIV-QD (iSCAT)'], ncol=1, loc='lower left',
        #                      framealpha=0)
        # plt.legend([fluo, lhcii, mic], ['Fluorescence', 'LHCII (iSCAT)', 'LHCII-micelle (iSCAT)'], ncol=1, loc='upper right',
        #            framealpha=0)
        # plt.gca().add_artist(legend1)
        # plt.legend(loc='upper right', framealpha=0.0, ncol=1)
    else:
        fig.legend(bbox_to_anchor=(0.10, 0.12), loc='lower left', framealpha=0.0, ncol=1)

    if not adjusted:
        ax1.set_ylabel('CRB (nm)')
    ax1.set_xlabel('Number of fluorescence photons')
    ax1.xaxis.tick_top()
    ax1.xaxis.set_label_position('top')
    ax1.spines['top'].set_color('C0')
    ax1.xaxis.label.set_color('C0')
    ax1.tick_params(axis='x', colors='C0')
    # ax1.text(100, 0.01, "LHCII")
    # ax1.text(100, 0.01, "LHCII-micelle")
    # ax1.text(100, 0.01, "PB")
    # ax1.text(100, 0.1, "GFP")
    # ax1.text(10, 0.0001, "HIV-QD")
    if adjusted:
        ax1.text(2e2, 0.9e-5, r'(iSCAT photons $\times 10^4$)', color='C5', rotation=-28.5)
        ax1.text(2e-1, 3e3, 'b', fontweight='bold', fontsize=12)
        ax1.tick_params(axis='y', labelleft=False, labelright=False)
    else:
        ax1.text(2e3, 0.9e-4, r'(iSCAT photons $\times 10^4$)', color='C5', rotation=-28.5)
        ax1.text(1e-1, 3e3, 'a', fontweight='bold', fontsize=12)

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
        # multip_func_4 = lambda x: 88547 * x * 1000  # HIV-QD
        # div_func_4 = lambda x: x / (88547 * 1000) # LHCII
    else:
        multip_func_av = lambda x: 6 * x  # LHCII
        div_func_av = lambda x: x / 6   # LHCII
        multip_func_1 = lambda x: 3.1 * x  # LHCII
        div_func_1 = lambda x: x / 3.1   # LHCII
        multip_func_11 = lambda x: 13.5 * x  # LHCII-micelle
        div_func_11 = lambda x: x / 13.5   # LHCII
        multip_func_2 = lambda x: 2.1 * x  # PB
        div_func_2 = lambda x: x / 2.1   # LHCII
        multip_func_3 = lambda x: 5.3 * x  # EGFP
        div_func_3 = lambda x: x / 5.3   # LHCII
    # multip_func_4 = lambda x: 88547 * x  # HIV-QD
    # div_func_4 = lambda x: x / 88547  # LHCII

    secax1 = ax1.secondary_xaxis('bottom', functions=(multip_func_av, div_func_av))
    # secax2.set_xlabel('Number of iSCAT photons (HIV-QD)')

    secax1.set_xlabel('Average number of iSCAT photons')

    for ax in fig.get_axes():
        for line in ax.lines:
            line.set_lw(1.5)

    if adjusted:
        pass

    if adjusted:
        ax1.set_ylim(4e-6, 1e3)
    else:
        ax1.set_ylim(None, 1e3)
    ax1.set_xlim(2e-1, 1e7)

plt.subplots_adjust(hspace=0.4)
plt.tight_layout()
plt.savefig('../out/comp_numphotons.pdf')
plt.show()
