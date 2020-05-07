import matplotlib
from static_crb.CRB import *
from scipy.stats import norm
from scipy.signal import convolve

matplotlib.rcParams.update({'font.size': 14})

dill.settings['recurse'] = True
file_orbital = 'pickles/crb_lambda_orbital'

orbital = Orbital(file_orbital)
# print('orbital')

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)

y = np.linspace(-500, 500, num=100)
plt.yscale('log')
# x, y, L, N, w, amp
# crb100 = crb_lambda_orbital(0, y, 300, 100, 212, 1)
# crb200 = crb_lambda_orbital(0, y, 500, 100, 353, 1)
crb400 = crb_lambda_orbital(0, y, 300, 4000, 424, 1)
# crb800 = crb_lambda_orbital(0, y, 700, 100, 494, 1)
# crb1600 = crb_lambda_orbital(0, y, 900, 100, 636, 1)

# crb200 = crb_lambda_orbital(0, y, 500, 50, 353, 1)
# crb800 = crb_lambda_orbital(0, y, 700, 150, 494, 1)
# crb1600 = crb_lambda_orbital(0, y, 900, 100, 636, 1)

# plt.plot(y, crb100, label='L=300')
# plt.plot(y, crb200, label='L=500')
plt.plot(y, crb400, label='L=564')
# plt.plot(y, crb800, label='L=700')
# plt.plot(y, crb1600, label='L=900')
plt.legend(loc='lower right')
plt.xlabel('x (nm)')
plt.ylabel('CRB (nm)')
plt.tight_layout()
# plt.savefig('../out/orbital_crb.png')
plt.show()

N = np.linspace(95, 105)
dist = norm(loc=100, scale=0.5)

crb = crb_lambda_orbital(0, y[:, None], 300, N, 212, 1)

# plt.figure()
# # plt.plot(N, dist.pdf(N))
# convd = np.zeros((100, 50))
#
# for i, row in enumerate(crb):
#     convd[i] = convolve(dist.pdf(N), row, mode='same')
#
# plt.plot(convd[20, :])
# plt.plot(crb[20, :])
# plt.plot(dist.pdf(N))
# plt.show()


