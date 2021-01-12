import matplotlib
from static_crb.CRB import *
import rsmf

formatter = rsmf.CustomFormatter(columnwidth=418.25368 * 0.01389, fontsizes=12,
                                 pgf_preamble=r'\usepackage{lmodern} \usepackage[utf8x]{inputenc}')

matplotlib.rcParams.update({'font.size': formatter.fontsizes.footnotesize})

dill.settings['recurse'] = True
file_minflux = 'pickles/crb_lambda_minflux'

# minflux = MinFlux(file_minflux)
# print('minflux')
# return_lambda('minflux', file_minflux)

fileobject_minflux = open(file_minflux, 'rb')
crb_lambda_minflux = dill.load(fileobject_minflux)

# fish = crb_lambda_minflux(0, 1, 300, 1000, 800, 1, 100)
# print(fish)
# fisher_inv = np.linalg.inv(fish)
# print(fisher_inv)
# print(np.mean(np.diag(fisher_inv)[1:]))
# fish = crb_lambda_minflux(0, 1, 300, 1000, 800, 1, 10)
# print(fish)
# fisher_inv = np.linalg.inv(fish)
# print(fisher_inv)
# print(np.mean(np.diag(fisher_inv)[1:]))

y = np.linspace(-500, 500, num=200)

figure = formatter.figure(width_ratio=0.7)
plt.yscale('log')
# x, y, L, N, w, amp

# crb400 = np.zeros(200)
# for i, val in enumerate(y):
#     inv = np.linalg.inv(crb_lambda_minflux(val, 0, 300, 10000, 800, 1, 2000))
#     crb = np.sqrt(np.abs(np.mean(np.diag(inv)[1:])))
#     crb400[i] = crb
#
# crb200 = np.zeros(200)
# for i, val in enumerate(y):
#     inv = np.linalg.inv(crb_lambda_minflux(0, val, 100, 10000, 800, 1, 20))
#     crb = np.sqrt(np.abs(np.mean(np.diag(inv)[1:])))
#     crb200[i] = crb
#
# crb100 = np.zeros(200)
# for i, val in enumerate(y):
#     inv = np.linalg.inv(crb_lambda_minflux(0, val, 50, 10000, 800, 1, 20))
#     crb = np.sqrt(np.abs(np.mean(np.diag(inv)[1:])))
#     crb100[i] = crb

# crb100 = crb_lambda_minflux(0, y, 50, 10000, 800, 1, 10)
# crb200 = crb_lambda_minflux(0, y, 100, 10000, 800, 1, 0.5)
# crb400 = crb_lambda_minflux(y, 0, 300, 10000, 300, 1, 3160)
# crb800 = crb_lambda_minflux(0, y, 500, 10000, 800, 1, 0.5)
# crb1600 = crb_lambda_minflux(0, y, 700, 10000, 800, 1, 0.5)
crb100 = crb_lambda_minflux(0, y, 50, 10000, 800, 1)
crb200 = crb_lambda_minflux(0, y, 100, 10000, 800, 1)
crb400 = crb_lambda_minflux(0, y, 300, 10000, 800, 1)
crb800 = crb_lambda_minflux(0, y, 500, 10000, 800, 1)
crb1600 = crb_lambda_minflux(0, y, 700, 10000, 800, 1)

plt.plot(y, crb100, label='L=50nm')
plt.plot(y, crb200, label='L=100nm')
plt.plot(y, crb400, label='L=300nm')
plt.plot(y, crb800, label='L=500nm')
plt.plot(y, crb1600, label='L=700nm')
plt.legend(loc='lower right', framealpha=0.7)
plt.xlabel('x (nm)')
plt.ylabel('CRB (nm)')
plt.tight_layout()
plt.savefig('../out/minflux_crb.pdf')
plt.show()

