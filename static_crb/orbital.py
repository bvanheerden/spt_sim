import matplotlib
from static_crb.CRB import *

matplotlib.rcParams.update({'font.size': 14})

dill.settings['recurse'] = True
file_orbital = 'crb_lambda_orbital'

orbital = Orbital(file_orbital)
print('orbital')
# return_lambda('orbital', file_orbital)

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)

y = np.linspace(-500, 500, num=100)
plt.yscale('log')
# x, y, L, N, w, amp
crb100 = crb_lambda_orbital(0, y, 300, 100, 212, 1)
crb200 = crb_lambda_orbital(0, y, 500, 100, 353, 1)
# crb400 = crb_lambda_orbital(0, y, 300, 100, 424, 1)
crb800 = crb_lambda_orbital(0, y, 700, 100, 494, 1)
crb1600 = crb_lambda_orbital(0, y, 900, 100, 636, 1)

plt.plot(y, crb100, label='L=300')
plt.plot(y, crb200, label='L=500')
# plt.plot(y, crb400, label='L=564')
plt.plot(y, crb800, label='L=700')
plt.plot(y, crb1600, label='L=900')
plt.legend(loc='lower right')
plt.xlabel('x (nm)')
plt.ylabel('CRB (nm)')
plt.tight_layout()
# plt.savefig('../out/orbital_crb.png')
plt.show()

