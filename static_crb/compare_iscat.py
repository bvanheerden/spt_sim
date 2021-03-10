"""compare iscat and fluorescence CRB as a function of position"""
import matplotlib
from static_crb.CRB import *

matplotlib.rcParams.update({'font.size': 14})

dill.settings['recurse'] = True
file_orbital = 'pickles/crb_lambda_orbital'
file_knight = 'pickles/crb_lambda_knight'
file_orbital_iscat = 'pickles/crb_lambda_orbital_iscat'
file_knight_iscat = 'pickles/crb_lambda_knight_iscat'

compute_crb = False

if compute_crb:
    orbital = Orbital(file_orbital)
    print('orbital')
    knight = Knight(file_knight, 300)
    print('knight')
    orbital_iscat = Orbital(file_orbital_iscat, iscat=True)
    print('orbital')
    knight_iscat = Knight(file_knight_iscat, 300, iscat=True)
    print('knight')

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)

fileobject_knight = open(file_knight, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)

fileobject_orbital_iscat = open(file_orbital_iscat, 'rb')
crb_lambda_orbital_iscat = dill.load(fileobject_orbital_iscat)

fileobject_knight_iscat = open(file_knight_iscat, 'rb')
crb_lambda_knight_iscat = dill.load(fileobject_knight_iscat)

x = np.linspace(-200, 200, num=100)
y = np.linspace(-400, 400, num=100)
xv, yv = np.meshgrid(x, y)
r = x
# plt.yscale('log')
# # x, y, L, N, w, amp
#
# crbknight = crb_lambda_knight(0, y, 50, 100, 400, 1,)
# crbmf = crb_lambda_minflux(0, y, 50, 100, 800, 1)
# crborb = crb_lambda_orbital(0, y, 566, 100, 400, 1)
#
# plt.plot(y, crbknight, label="Knight's Tour")
# plt.plot(y, crbmf, label='MINFLUX')
# plt.plot(y, crborb, label='Orbital')
# plt.legend(loc='lower right')
# plt.xlabel('x (nm)')
# plt.ylabel('CRB (nm)')
# plt.savefig('../out/comp_mf_small.png')
# plt.show()

contrast = 0.005
n = 10000
nscat = 1 * n

nsigma = np.sqrt(2 * nscat / contrast)
crbknight = crb_lambda_knight(0, y, 50, n, 400, 1)
crbknight_iscat = crb_lambda_knight_iscat(0, y, 50, nscat, 400, 1, nsigma)
# crbmf_large = crb_lambda_minflux(0, y, 566, 100, 800, 1)
# crbmf = crb_lambda_minflux(0, y, 50, 100, 800, 1)
crborb = crb_lambda_orbital(0, y, 566, n, 400, 1)
crborb_iscat = crb_lambda_orbital_iscat(0, y, 566, nscat, 400, 1, nsigma)

plt.figure(figsize=[7.0, 5.5])
# plt.yscale('log')
plt.plot(y, crbknight, label="Knight's Tour")
plt.plot(y, crbknight_iscat, label="Knight's Tour (iscat)")
# plt.plot(y, crbmf, label='MINFLUX L=50')
# plt.plot(y, crbmf_large, label='MINFLUX L=566')
plt.plot(y, crborb, label='Orbital')
plt.plot(y, crborb_iscat, label='Orbital (iscat)')
# plt.ylim(None, 100)
plt.legend(loc='lower right')
plt.xlabel('x (nm)')
plt.ylabel('CRB (nm)')
# plt.savefig('../out/comp_mf_large.png')
plt.show()
