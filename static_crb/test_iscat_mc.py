import numpy as np
import scipy
from scipy import stats
from scipy.special import comb
import math
from matplotlib import pyplot as plt


def metropolis_hastings(target_density, p0, x0, size=5000):
    burnin_size = 0
    size += burnin_size
    xt = x0

    xt_candidate = xt
    accept_prob = 0

    samples = []
    accepted = 0
    for i in range(size):
        if i % 1000 == 0:
            # print(xt)
            # print(target_density(int(xt)))
            print(xt_candidate)
            # print(target_density(int(xt_candidate)))
            print(accept_prob)
        xt_candidate = np.random.normal(xt, 3000)
        accept_prob = (target_density(np.int(xt_candidate), p0))/(target_density(np.int(xt), p0))
        if np.random.uniform(0, 1) < accept_prob:
            xt = xt_candidate
            accepted += 1
        samples.append(xt)
    samples = np.array(samples[burnin_size:])
    print(accepted)
    print('acceptance rate = ', accepted / (size))
    return samples


# set constant parameters
L = 300  # beam seperation nm
w = 500  # beam waist = 1.699*fwhm nm
fwhm = w / 1.699
fwhm = 300
N_hat = 10000  # expected counts
contrast = 0.002  # iscat contrast

sigma = np.sqrt(2 * N_hat / contrast)
print(sigma)

c = 0.001  # small number for Bernoulli distribution

# set position and get parameter
x = 0

p0 = np.exp(4 * np.log(2) * x * L / w ** 2) / (2 * np.cosh(4 * np.log(2) * x * L / w ** 2))
# print(p0)

Nvals = np.arange(5000, 15000, 100)
# Nvals = np.arange(0, 50000, 100)
# plt.plot(stats.binom.pmf(5000, Nvals, p0) * stats.norm.pdf(Nvals, N_hat, sigma))
# plt.show()


# define our PDF for n
class pdf_n(stats.rv_continuous):

    def _pdf(self, x, param):
        int_func = lambda N: stats.binom._pmf(x, N, param) * (stats.norm._pdf(((N - N_hat) / sigma)) / sigma)
        prob = np.sum([int_func(N) for N in range(20000)])
        # print(prob)
        return prob


ndist = pdf_n(a=0)
print(ndist.pdf(5000, 0.6))
# print(scipy.integrate.quad(lambda x: ndist.pdf(x, p0), 0, 20000))

iters = 100  # num of iterations in loop

# plot pdf
nvals = np.arange(0, 15000, 500, dtype=np.int)
sigmavals = []
pvals = []
for i in range(9):
    pdfvals = np.array([ndist.pdf(val, 0.1*(i+1)) for val in nvals])
    plt.plot(nvals, pdfvals)

    param, pcov = scipy.optimize.curve_fit(stats.norm.pdf, nvals, pdfvals, p0=[5000, 1000])
    fitted = stats.norm.pdf(nvals, param[0], param[1])
    plt.plot(nvals, fitted)
    sigmavals.append(param[1])
    pvals.append(0.1*(i+1))
    print(param)

plt.show()

plt.plot(pvals, sigmavals)
plt.show()

# get random value vectors
# nvals = metropolis_hastings(ndist.pdf, p0, 5050, 5000)
# np.save('samples.npy', nvals)
nvals = np.load('samples.npy')
# print(nvals)
# plt.hist(nvals, bins=50, range=(1000, 9000), density=True, histtype='step')
# plt.show()

nvals = np.int_(nvals[:iters])
deltavals = stats.bernoulli.rvs(0.5, size=iters)
delta_tildevals = stats.bernoulli.rvs(0.5, size=iters)
hess_sum = 0

# for i, n in enumerate(nvals):
#
#     if deltavals[i] == 0:
#         delta = - c
#     else:
#         delta = c
#     if delta_tildevals[i] == 0:
#         delta_tilde = - c
#     else:
#         delta_tilde = c
#
#     gplus = 0.5 * (np.log(ndist.pdf(n, p0 + delta + delta_tilde)) - np.log(ndist.pdf(n, p0 + delta - delta_tilde)))
#     gminus = 0.5 * (np.log(ndist.pdf(n, p0 - delta + delta_tilde)) - np.log(ndist.pdf(n, p0 - delta - delta_tilde)))
#     gplus = gplus / delta_tilde
#     gminus = gminus / delta_tilde
#
#     hess = 0.5 * (gplus - gminus) / delta
#     hess_sum += hess
#     # print(hess)
#     # print(gplus, gminus)
#
# fish = - hess_sum / iters  # fisher information is average hessian
# fish = fish * 21.353e-6 # convert to position space
# crb = 1 / np.sqrt(fish)
# print(crb)
