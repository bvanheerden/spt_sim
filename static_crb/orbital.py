import matplotlib
from static_crb.CRB import *

matplotlib.rcParams.update({'font.size': 14})

dill.settings['recurse'] = True
file_orbital = 'crb_lambda_orbital'

# orbital = Orbital(file_orbital)
# print('orbital')
# return_lambda('orbital', file_orbital)

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)

y = np.linspace(-300, 300, num=100)
# plt.yscale('log')
# x, y, L, N, w, amp
# crb100 = crb_lambda_orbital(0, y, 300, 10000, 212, 1, 1000)
# crb200 = crb_lambda_orbital(0, y, 500, 100, 353, 1, 0.5)
# crb400 = crb_lambda_orbital(0, y, 300, 100, 424, 1)
# crb800 = crb_lambda_orbital(0, y, 700, 100, 494, 1, 0.5)
# crb1600 = crb_lambda_orbital(0, y, 900, 100, 636, 1, 0.5)

# crb100 = np.zeros(100)
# for i, val in enumerate(y):
#     inv = np.linalg.inv(crb_lambda_orbital(val, 0, 300, 10000, 800, 1, 2000))
#     crb = np.sqrt(np.abs(np.mean(np.diag(inv)[1:])))
#     crb100[i] = crb
#
# crb200 = np.zeros(100)
# for i, val in enumerate(y):
#     inv = np.linalg.inv(crb_lambda_orbital(val, 0, 500, 10000, 800, 1, 2000))
#     crb = np.sqrt(np.abs(np.mean(np.diag(inv)[1:])))
#     crb200[i] = crb

# plt.plot(y, crb100, label='L=300')
# plt.plot(y, crb200, label='L=500')
# plt.plot(y, crb400, label='L=564')
# plt.plot(y, crb800, label='L=700')
# plt.plot(y, crb1600, label='L=900')
# plt.legend(loc='lower right')
# plt.xlabel('x (nm)')
# plt.ylabel('CRB (nm)')
# plt.tight_layout()
# plt.savefig('../out/orbital_crb.png')
# plt.show()

fish = crb_lambda_orbital(0, 0, 500, 100, 800, 1, 300)
print(fish)
inv = np.linalg.inv(fish)
print(inv)
crb = np.sqrt(np.abs(np.mean(np.diag(inv)[1:])))
print(crb)
fish = crb_lambda_orbital(0, 0, 500, 100, 800, 1, 20)
print(fish)
inv = np.linalg.inv(fish)
print(inv)
crb = np.sqrt(np.abs(np.mean(np.diag(inv)[1:])))
print(crb)

crb_n = np.zeros(50)
crb_n_sig = np.zeros(50)
nvals = np.logspace(2, 5)

for i, val in enumerate(nvals):
    sigma = np.sqrt(1000 * val)
    # print(sigma)
    inv = np.linalg.inv(crb_lambda_orbital(20, 0, 500, val, 800, 1, sigma))
    crb = np.sqrt(np.abs(np.mean(np.diag(inv)[:])))
    crb_n_sig[i] = crb
    inv = np.linalg.inv(crb_lambda_orbital(20, 0, 500, val, 800, 1, 100))
    crb = np.sqrt(np.abs(np.mean(np.diag(inv)[:])))
    crb_n[i] = crb

plt.figure()
plt.loglog(nvals, crb_n)
plt.loglog(nvals, crb_n_sig)
plt.show()
