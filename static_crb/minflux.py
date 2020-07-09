import matplotlib
from static_crb.CRB import *

matplotlib.rcParams.update({'font.size': 14})

dill.settings['recurse'] = True
file_minflux = 'pickles/crb_lambda_minflux'

# minflux = MinFlux(file_minflux)
# print('minflux')
# return_lambda('minflux', file_minflux)

fileobject_minflux = open(file_minflux, 'rb')
crb_lambda_minflux = dill.load(fileobject_minflux)

y = np.linspace(-500, 500, num=200)

plt.yscale('log')

crb100 = crb_lambda_minflux(0, y, 50, 100, 800, 1)
crb200 = crb_lambda_minflux(0, y, 100, 100, 800, 1)
crb400 = crb_lambda_minflux(0, y, 300, 100, 800, 1)
crb800 = crb_lambda_minflux(0, y, 500, 100, 800, 1)
crb1600 = crb_lambda_minflux(0, y, 700, 100, 800, 1)

plt.plot(y, crb100, label='L=50')
plt.plot(y, crb200, label='L=100')
plt.plot(y, crb400, label='L=300')
plt.plot(y, crb800, label='L=500')
plt.plot(y, crb1600, label='L=700')
plt.legend(loc='lower right')
plt.xlabel('x (nm)')
plt.ylabel('CRB (nm)')
plt.tight_layout()
plt.savefig('../out/minflux_crb.png')
plt.show()

