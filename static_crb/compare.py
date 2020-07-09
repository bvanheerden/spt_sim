import matplotlib
from static_crb.CRB import *

matplotlib.rcParams.update({'font.size': 14})

dill.settings['recurse'] = True
file_minflux = 'pickles/crb_lambda_minflux'
file_orbital = 'pickles/crb_lambda_orbital'
file_knight = 'pickles/crb_lambda_knight'
file_camera = 'pickles/crb_lambda_camera'

# minflux = MinFlux(file_minflux)
# print('minflux')
# orbital = Orbital(file_orbital)
# print('orbital')
# knight = Knight(file_knight)
# print('knight')
# camera = Camera(file_camera)
# print('camera')
# return_lambda('orbital', file_orbital)
# return_lambda('minflux', file_minflux)
# return_lambda('knight', file_knight)
# return_lambda('camera', file_camera)

fileobject_minflux = open(file_minflux, 'rb')
crb_lambda_minflux = dill.load(fileobject_minflux)

fileobject_orbital = open(file_orbital, 'rb')
crb_lambda_orbital = dill.load(fileobject_orbital)

fileobject_knight = open(file_knight, 'rb')
crb_lambda_knight = dill.load(fileobject_knight)

# fileobject_camera = open(file_camera, 'rb')
# crb_lambda_camera = dill.load(fileobject_camera)

x = np.linspace(-200, 200, num=200)
y = np.linspace(-400, 400, num=200)
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

crbknight = crb_lambda_knight(0, y, 50, 100, 400, 1,)
crbmf_large = crb_lambda_minflux(0, y, 566, 100, 800, 1)
crbmf = crb_lambda_minflux(0, y, 50, 100, 800, 1)
crborb = crb_lambda_orbital(0, y, 566, 100, 400, 1)

plt.figure(figsize=[7.0, 5.5])
plt.yscale('log')
plt.plot(y, crbknight, label="Knight's Tour")
plt.plot(y, crbmf, label='MINFLUX L=50')
plt.plot(y, crbmf_large, label='MINFLUX L=566')
plt.plot(y, crborb, label='Orbital')
# plt.ylim(None, 100)
plt.legend(loc='lower right')
plt.xlabel('x (nm)')
plt.ylabel('CRB (nm)')
plt.savefig('../out/comp_mf_large.png')
plt.show()
