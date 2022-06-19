import matplotlib
from static_crb.CRB import *
from scipy.stats import norm
from scipy.signal import convolve
import rsmf

color_list = ['#4477AA', '#66CCEE', '#228833', '#CC6677', '#EE6677', '#AA3377', '#BBBBBB']
color_list = ['#007982','#008373','#0b8b53','#528e25','#898a00','#c47b00', '#ff5900']
color_list = ['#5f4690', '#349ca3', '#52a14c', '#e79406', '#b9474e', '#764276', '#666666']
color_list = ['#1d6996', '#73af48', '#edad08', '#e17c05', '#cc503e', '#94346e', '#6f4070']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)

# col_width = 345  # For dissertation I think
# col_width = 470  # For journal draft (Interface)
col_width = 510  # For journal draft (JCP)

formatter = rsmf.CustomFormatter(columnwidth=col_width * 0.01389, fontsizes=10,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})
matplotlib.rcParams.update({'font.family': 'serif'})

dill.settings['recurse'] = True
file_orbital = 'pickles/crb_lambda_orbital'
file_minflux = 'pickles/crb_lambda_minflux'
file_knight_100 = 'pickles/crb_lambda_knight_0.1'
file_knight_300 = 'pickles/crb_lambda_knight'
file_knight_500 = 'pickles/crb_lambda_knight_0.5'
file_knight_700 = 'pickles/crb_lambda_knight_0.7'
file_knight_900 = 'pickles/crb_lambda_knight_0.9'

file_orbital_bg = 'pickles/crb_lambda_orbital_bg'
file_minflux_bg = 'pickles/crb_lambda_minflux_bg'
file_knight_100_bg = 'pickles/crb_lambda_knight_0.1_bg'
file_knight_300_bg = 'pickles/crb_lambda_knight_bg'
file_knight_500_bg = 'pickles/crb_lambda_knight_0.5_bg'
file_knight_700_bg = 'pickles/crb_lambda_knight_0.7_bg'
file_knight_900_bg = 'pickles/crb_lambda_knight_0.9_bg'

# orbital = Orbital(file_orbital)
# print('orbital')

# minflux = MinFlux(file_minflux)
# print('minflux')

sbr = 10

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)
fileobject_orbital_bg = open(file_orbital_bg, 'rb')
crb_lambda_orbital_bg = dill.load(fileobject_orbital_bg)

fileobject_minflux = open(file_minflux, 'rb')
crb_lambda_minflux = dill.load(fileobject_minflux)
fileobject_minflux_bg = open(file_minflux_bg, 'rb')
crb_lambda_minflux_bg = dill.load(fileobject_minflux_bg)

y = np.linspace(-400, 400, num=100)
y1 = np.linspace(-400, 400, num=100)

# x, y, L, N, w, amp
crb100 = crb_lambda_orbital(0, y, 300, 100, 212, 1)
crb200 = crb_lambda_orbital(0, y, 500, 100, 353, 1)
crb800 = crb_lambda_orbital(0, y, 700, 100, 494, 1)
crb1600 = crb_lambda_orbital(0, y, 900, 100, 636, 1)

crb100_bg = crb_lambda_orbital_bg(0, y, 300, 100, 212, 1, sbr)
crb200_bg = crb_lambda_orbital_bg(0, y, 500, 100, 353, 1, sbr)
crb800_bg = crb_lambda_orbital_bg(0, y, 700, 100, 494, 1, sbr)
crb1600_bg = crb_lambda_orbital_bg(0, y, 900, 100, 636, 1, sbr)

fileobject_knight = open(file_knight_100, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb100_kt = crb_lambda_knight(0, y, 50, 100, 133, 1)
fileobject_knight_bg = open(file_knight_100_bg, 'rb')
crb_lambda_knight_bg = dill.load(fileobject_knight_bg)
crb100_kt_bg = crb_lambda_knight_bg(0, y, 50, 100, 133, 1, sbr)

fileobject_knight = open(file_knight_300, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb300_kt = crb_lambda_knight(0, y, 100, 100, 400, 1)
fileobject_knight_bg = open(file_knight_300_bg, 'rb')
crb_lambda_knight_bg = dill.load(fileobject_knight_bg)
crb300_kt_bg = crb_lambda_knight_bg(0, y, 100, 100, 400, 1, sbr)

fileobject_knight = open(file_knight_500, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb500_kt = crb_lambda_knight(0, y, 282, 100, 665, 1)
fileobject_knight_bg = open(file_knight_500_bg, 'rb')
crb_lambda_knight_bg = dill.load(fileobject_knight_bg)
crb500_kt_bg = crb_lambda_knight_bg(0, y, 282, 100, 665, 1, sbr)

fileobject_knight = open(file_knight_700, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb700_kt = crb_lambda_knight(0, y, 400, 100, 931, 1)
fileobject_knight_bg = open(file_knight_700_bg, 'rb')
crb_lambda_knight_bg = dill.load(fileobject_knight_bg)
crb700_kt_bg = crb_lambda_knight_bg(0, y, 400, 100, 931, 1, sbr)

fileobject_knight = open(file_knight_900, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb900_kt = crb_lambda_knight(0, y, 400, 100, 1200, 1)
fileobject_knight_bg = open(file_knight_900_bg, 'rb')
crb_lambda_knight_bg = dill.load(fileobject_knight_bg)
crb900_kt_bg = crb_lambda_knight_bg(0, y, 400, 100, 1200, 1, sbr)

crb100_mf = crb_lambda_minflux(0, y, 50, 100, 800, 1)
crb200_mf = crb_lambda_minflux(0, y, 100, 100, 800, 1)
crb400_mf = crb_lambda_minflux(0, y, 300, 100, 800, 1)
crb800_mf = crb_lambda_minflux(0, y, 500, 100, 800, 1)
crb1600_mf = crb_lambda_minflux(0, y, 700, 100, 800, 1)
crb100_mf_bg = crb_lambda_minflux_bg(0, y, 50, 100, 800, 1, sbr)
crb200_mf_bg = crb_lambda_minflux_bg(0, y, 100, 100, 800, 1, sbr)
crb400_mf_bg = crb_lambda_minflux_bg(0, y, 300, 100, 800, 1, sbr)
crb800_mf_bg = crb_lambda_minflux_bg(0, y, 500, 100, 800, 1, sbr)
crb1600_mf_bg = crb_lambda_minflux_bg(0, y, 700, 100, 800, 1, sbr)

fileobject_knight = open(file_knight_300, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crbknight = crb_lambda_knight(0, y1, 50, 100, 400, 1,)
fileobject_knight_bg = open(file_knight_300_bg, 'rb')
crb_lambda_knight_bg = dill.load(fileobject_knight_bg)
crbknight_bg = crb_lambda_knight_bg(0, y1, 50, 100, 400, 1, sbr)

crbmf_large = crb_lambda_minflux(0, y1, 566, 100, 800, 1)
crbmf = crb_lambda_minflux(0, y1, 50, 100, 800, 1)
crborb = crb_lambda_orbital(0, y1, 566, 100, 400, 1)
crbmf_large_bg = crb_lambda_minflux_bg(0, y1, 566, 100, 800, 1, sbr)
crbmf_bg = crb_lambda_minflux_bg(0, y1, 50, 100, 800, 1, sbr)
crborb_bg = crb_lambda_orbital_bg(0, y1, 566, 100, 400, 1, sbr)

# fig = plt.figure(figsize=(8, 5))
fig = formatter.figure(width_ratio=0.65, aspect_ratio=1.6)
spec = matplotlib.gridspec.GridSpec(ncols=2, nrows=4)
ax1 = fig.add_subplot(spec[0, 0])
ax2 = fig.add_subplot(spec[1, 0], sharex=ax1)
ax3 = fig.add_subplot(spec[2, 0], sharex=ax1)
ax4 = fig.add_subplot(spec[3, 0], sharex=ax1)
ax5 = fig.add_subplot(spec[0, 1], sharey=ax1)
ax6 = fig.add_subplot(spec[1, 1], sharex=ax5, sharey=ax2)
ax7 = fig.add_subplot(spec[2, 1], sharex=ax5, sharey=ax3)
ax8 = fig.add_subplot(spec[3, 1], sharex=ax5, sharey=ax4)

loc = matplotlib.ticker.MultipleLocator(base=10)
formatter = plt.LogFormatter(labelOnlyBase=False, minor_thresholds=(2, 0.6))
formatter_mf = plt.LogFormatter(labelOnlyBase=True)

ax1.set_yscale('log')
ax1.plot(y, crb100, label='$L=300$ nm')
ax1.plot(y, crb200, label='$L=500$ nm')
# plt.plot(y, crb400, label='L=564')
ax1.plot(y, crb800, label='$L=700$ nm')
ax1.plot(y, crb1600, label='$L=900$ nm')
# ax1.legend(loc='upper center', framealpha=0.5, ncol=2, handlelength=1.0, labelspacing=0.3)
ax1.set_xlim(-500, 500)
ax1.set_ylim(6, 80)
# ax1.set_xlabel('Position (nm)')
ax1.set_ylabel('CRB (nm)')
ax1.yaxis.set_major_locator(loc)

ax1.text(130, 10, '300', fontsize=10, color='C0')
ax1.text(210, 16, '500', fontsize=10, color='C1')
ax1.text(280, 22, '700', fontsize=10, color='C2')
ax1.text(280, 43, '900', fontsize=10, color='C3')

ax2.set_yscale('log')
ax2.plot(y, crb300_kt, label='$L=300$ nm')
ax2.plot(y, crb500_kt, label='$L=500$ nm')
ax2.plot(y, crb700_kt, label='$L=700$ nm')
ax2.plot(y, crb900_kt, label='$L=900$ nm')
# ax3.legend(loc='lower right', framealpha=0.5, ncol=2, handlelength=1.0, labelspacing=0.3)
ax2.set_ylabel('CRB (nm)')
# ax2.set_xlabel('Position (nm)')
ax2.yaxis.set_major_locator(loc)
ax2.yaxis.set_major_formatter(formatter)

ax2.text(280, 18, '300', fontsize=10, color='C0')
ax2.text(280, 30, '500', fontsize=10, color='C1')
ax2.text(280, 42, '700', fontsize=10, color='C2')
ax2.text(280, 55, '900', fontsize=10, color='C3')

ax3.set_yscale('log')
ax3.plot(y, crb100_mf, label='$L=50$ nm')
ax3.plot(y, crb200_mf, label='$L=100$ nm')
ax3.plot(y, crb400_mf, label='$L=300$ nm')
ax3.plot(y, crb800_mf, label='$L=500$ nm')
ax3.plot(y, crb1600_mf, label='$L=700$ nm')
# ax2.legend(loc='upper center', framealpha=0.5, ncol=2, handlelength=1.0, labelspacing=0.3)
# ax3.set_xlabel('Position (nm)')
ax3.set_ylabel('CRB (nm)')

ax3.text(20, 1.7, '50', fontsize=10, color='C0')
ax3.text(35, 4, '100', fontsize=10, color='C1')
ax3.text(110, 7, '300', fontsize=10, color='C2')
ax3.text(180, 13, '500', fontsize=10, color='C3')
ax3.text(290, 20, '700', fontsize=10, color='C4')

ax4.set_yscale('log')
ax4.plot(y1, crbknight, label="KT: $L=1500$ nm")
ax4.plot(y1, crbmf, label='MINFLUX: $L=50$ nm')
ax4.plot(y1, crbmf_large, label='MINFLUX: $L=566$ nm')
ax4.plot(y1, crborb, label='Orbital: $L=566$ nm')
# ax4.legend(loc='upper center', framealpha=0.5, handlelength=1.0, labelspacing=0.3)
ax4.set_xlabel('Position (nm)')
ax4.set_ylabel('CRB (nm)')

ax4.text(120, 8, 'KT 1500', fontsize=10, color='C0')
ax4.text(40, 2, 'MF 50', fontsize=10, color='C1')
ax4.text(160, 70, 'MF 566', fontsize=10, color='C2')
ax4.text(-350, 9, 'Orb 566', fontsize=10, color='C3')

ax5.set_yscale('log')
ax5.plot(y, crb100_bg, label='$L=300$ nm')
ax5.plot(y, crb200_bg, label='$L=500$ nm')
# plt.plot(y, crb400, label='L=564')
ax5.plot(y, crb800_bg, label='$L=700$ nm')
ax5.plot(y, crb1600_bg, label='$L=900$ nm')
# ax1.legend(loc='upper center', framealpha=0.5, ncol=2, handlelength=1.0, labelspacing=0.3)
ax5.set_xlim(-500, 500)
ax5.set_ylim(6, 80)
# ax5.set_xlabel('Position (nm)')
# ax5.set_ylabel('CRB (nm)')
ax5.yaxis.set_major_locator(loc)
ax5.yaxis.set_major_formatter(formatter)

ax5.text(100, 9, '300', fontsize=10, color='C0')
ax5.text(170, 14, '500', fontsize=10, color='C1')
ax5.text(250, 24, '700', fontsize=10, color='C2')
ax5.text(280, 52, '900', fontsize=10, color='C3')

ax6.set_yscale('log')
ax6.plot(y, crb300_kt_bg, label='$L=300$ nm')
ax6.plot(y, crb500_kt_bg, label='$L=500$ nm')
ax6.plot(y, crb700_kt_bg, label='$L=700$ nm')
ax6.plot(y, crb900_kt_bg, label='$L=900$ nm')
# ax3.legend(loc='lower right', framealpha=0.5, ncol=2, handlelength=1.0, labelspacing=0.3)
# ax6.set_xlabel('Position (nm)')
# ax6.set_ylabel('CRB (nm)')
ax6.yaxis.set_major_locator(loc)
ax6.yaxis.set_major_formatter(formatter)

ax6.text(280, 17, '300', fontsize=10, color='C0')
ax6.text(280, 29, '500', fontsize=10, color='C1')
ax6.text(280, 41, '700', fontsize=10, color='C2')
ax6.text(280, 54, '900', fontsize=10, color='C3')

ax7.set_yscale('log')
ax7.plot(y, crb100_mf_bg, label='$L=50$ nm')
ax7.plot(y, crb200_mf_bg, label='$L=100$ nm')
ax7.plot(y, crb400_mf_bg, label='$L=300$ nm')
ax7.plot(y, crb800_mf_bg, label='$L=500$ nm')
ax7.plot(y, crb1600_mf_bg, label='$L=700$ nm')
# ax2.legend(loc='upper center', framealpha=0.5, ncol=2, handlelength=1.0, labelspacing=0.3)
# ax7.set_xlabel('Position (nm)')
# ax7.set_ylabel('CRB (nm)')

ax7.text(-120, 4, '50', fontsize=10, color='C0')
ax7.text(35, 4, '100', fontsize=10, color='C1')
ax7.text(110, 7, '300', fontsize=10, color='C2')
ax7.text(180, 13, '500', fontsize=10, color='C3')
ax7.text(290, 20, '700', fontsize=10, color='C4')

ax8.set_yscale('log')
ax8.plot(y1, crbknight_bg, label="KT: $L=1500$ nm")
ax8.plot(y1, crbmf_bg, label='MINFLUX: $L=50$ nm')
ax8.plot(y1, crbmf_large_bg, label='MINFLUX: $L=566$ nm')
ax8.plot(y1, crborb_bg, label='Orbital: $L=566$ nm')
# ax4.legend(loc='upper center', framealpha=0.5, handlelength=1.0, labelspacing=0.3)
ax8.set_xlabel('Position (nm)')
# ax8.set_ylabel('CRB (nm)')

ax8.text(130, 8, 'KT 1500', fontsize=10, color='C0')
ax8.text(-120, 3, 'MF 50', fontsize=10, color='C1')
ax8.text(170, 70, 'MF 566', fontsize=10, color='C2')
ax8.text(-370, 9, 'Orb 566', fontsize=10, color='C3')

ax3.yaxis.set_minor_locator(matplotlib.ticker.LogLocator(10, 'auto'))
ax3.tick_params(which='minor', length=2, color='black')
ax3.yaxis.set_major_formatter(formatter_mf)

ax7.yaxis.set_minor_locator(matplotlib.ticker.LogLocator(10, 'auto'))
ax7.tick_params(which='minor', length=2, color='black')

ax4.yaxis.set_minor_locator(matplotlib.ticker.LogLocator(10, 'auto'))
ax4.tick_params(which='minor', length=2, color='black')
ax4.yaxis.set_major_formatter(formatter_mf)

ax8.yaxis.set_minor_locator(matplotlib.ticker.LogLocator(10, 'auto'))
ax8.tick_params(which='minor', length=2, color='black')

ax1.set_xlim((-400, 400))
ax5.set_xlim((-400, 400))
ax3.set_ylim((None, 4000))

ax1.text(-570, 65, 'a', fontweight='bold', fontsize='12')
ax2.text(-570, 60, 'c', fontweight='bold', fontsize='12')
ax3.text(-570, 2000, 'e', fontweight='bold', fontsize='12')
ax4.text(-570, 2000, 'g', fontweight='bold', fontsize='12')
ax5.text(-540, 65, 'b', fontweight='bold', fontsize='12')
ax6.text(-540, 60, 'd', fontweight='bold', fontsize='12')
ax7.text(-540, 2000, 'f', fontweight='bold', fontsize='12')
ax8.text(-540, 2000, 'h', fontweight='bold', fontsize='12')

fig.text(0.4, 0.945, 'Orbital method', fontsize=12)
fig.text(0.35, 0.71, "Knight's Tour method", fontsize=12)
fig.text(0.45, 0.475, "MINFLUX", fontsize=12)

fig.text(0.22, 0.96, r'$\textrm{SBR}=\infty$', fontsize=10)
fig.text(0.71, 0.96, fr'$\textrm{{SBR}}={sbr}$', fontsize=10)

for ax in fig.get_axes():
    for line in ax.lines:
        line.set_lw(1.3)

plt.tight_layout()
plt.subplots_adjust(hspace=0.4, wspace=0.2, top=0.93)
plt.savefig('../out/crb_panel.pdf')
# plt.show()


