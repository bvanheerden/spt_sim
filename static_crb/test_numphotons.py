"""Compare iSCAT and fluorescence for different samples as afunction of number of photons"""
import matplotlib
from static_crb.CRB import *
import rsmf

latex = False

if latex:
    formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                     pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

    matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

dill.settings['recurse'] = True
file_orbital = 'pickles/crb_lambda_orbital'
file_orbital_iscat = 'pickles/crb_lambda_orbital_iscat'

compute_crb = True

if compute_crb:
    # orbital = Orbital(file_orbital)
    # print('orbital')
    orbital_iscat = Orbital(file_orbital_iscat, iscat=True)
    print('orbital_iscat')

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)

fileobject_orbital_iscat = open(file_orbital_iscat, 'rb')
crb_lambda_orbital_iscat = dill.load(fileobject_orbital_iscat)

contrast = 0.05

n = np.logspace(1, 9, num=20)
n_iscat = 1000 * n
n_scat = n_iscat * contrast / 4
n_scat = n_iscat
nsigma = np.sqrt(2 * n_iscat / contrast)

crborb = crb_lambda_orbital(0, 0, 566, n, 400, 1)
crborb_scat = crb_lambda_orbital(0, 0, 566, n_scat, 400, 1)
crborb_iscat = crb_lambda_orbital_iscat(0, 0, 566, n_iscat, 400, 1, nsigma)

print(crborb_scat / crborb_iscat)

if latex:
    fig = formatter.figure(width_ratio=0.8, aspect_ratio=1)
else:
    fig = plt.figure(figsize=[7, 5])
ax4 = fig.add_subplot()

ax4.loglog(n, crborb, label='Fluorescence')
ax4.loglog(n, crborb_scat, label='pure scattering')
ax4.loglog(n, 7.746 * crborb_iscat, label='iScat')

plt.ylim(None, 100)
fig.legend(bbox_to_anchor=(0.9, 0.85), loc='upper right')
ax4.set_ylabel('CRB (nm)')
ax4.set_xlabel('Aantal fotone (fluoressensie)')
ax4.set_title("GFP")

plt.tight_layout()
plt.show()
