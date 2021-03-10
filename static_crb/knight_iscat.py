"""CRB for knights tour with iSCAT localisation"""
import matplotlib
from static_crb.CRB import *

matplotlib.rcParams.update({'font.size': 14})

dill.settings['recurse'] = True
file_knight_100 = 'pickles/crb_lambda_knight_0.1_iscat'
file_knight_300 = 'pickles/crb_lambda_knight_iscat'
file_knight_500 = 'pickles/crb_lambda_knight_0.5_iscat'
file_knight_700 = 'pickles/crb_lambda_knight_0.7'
file_knight_700_iscat = 'pickles/crb_lambda_knight_0.7_iscat'
file_knight_900 = 'pickles/crb_lambda_knight_0.9_iscat'

# knight = Knight(file_knight_700, 700)
# knight_iscat = Knight(file_knight_700_iscat, 700, iscat=True)
# print('knight')

contrast = 0.005
n = 10000
nscat = 2 * n
nsigma = np.sqrt(2 * nscat / contrast)

y = np.linspace(-500, 500, num=100)
# x, y, L, N, w, amp

# fileobject_knight = open(file_knight_100, 'rb')
# crb_lambda_knight = dill.load(fileobject_knight)
# crb100 = crb_lambda_knight(0, y, 50, 10000, 133, 1, 3000)
#
# fileobject_knight = open(file_knight_300, 'rb')
# crb_lambda_knight = dill.load(fileobject_knight)
# crb300 = crb_lambda_knight(0, y, 100, 10000, 400, 1, 3000)
#
# fileobject_knight = open(file_knight_500, 'rb')
# crb_lambda_knight = dill.load(fileobject_knight)
# crb500 = crb_lambda_knight(0, y, 282, 10000, 665, 1, 3000)
#
fileobject_knight = open(file_knight_700, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb700 = crb_lambda_knight(0, y, 400, n, 931, 1)

fileobject_knight = open(file_knight_700_iscat, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)
crb700_iscat = crb_lambda_knight(0, y, 400, nscat, 931, 1, nsigma)

# fileobject_knight = open(file_knight_900, 'rb')
# crb_lambda_knight = dill.load(fileobject_knight)
# crb900 = crb_lambda_knight(0, y, 400, 10000, 1200, 1, 3000)

plt.figure()
plt.yscale('log')
# plt.plot(y, crb100, label='L=100')
# plt.plot(y, crb300, label='L=300')
# plt.plot(y, crb500, label='L=500')
plt.plot(y, crb700, label='fluo')
plt.plot(y, crb700_iscat, label='iscat')
# plt.plot(y, crb900, label='L=900')
plt.legend(loc='lower right')
plt.xlabel('x (nm)')
plt.ylabel('CRB (nm)')
plt.tight_layout()
# plt.savefig('../out/knight_crb.png')
plt.show()

