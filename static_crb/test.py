import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

intcounts = 450
contrast = 0.0042
print("CN = ", intcounts * contrast)

reflected = np.random.poisson(intcounts / contrast, 50000)
background = np.random.poisson(intcounts / contrast, 50000)
interference = np.random.poisson(intcounts, 50000)

meas_cont = (interference + reflected - background) / background
meas_cont = meas_cont[background != 0]

meas_int = meas_cont * background[background != 0]
std = np.std(meas_int)
print("Standard deviation: ", std)
print("Expected standard deviation: ", np.sqrt(2 * intcounts / contrast))

gauss = np.random.normal(intcounts, std, 50000)

stat, pval = stats.kstest(meas_int, 'norm', args=(intcounts, std), alternative='less')
print(stat, pval)

plt.hist(meas_int, bins=50)
plt.hist(gauss, bins=50)
plt.show()


