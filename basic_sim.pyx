import numpy as np
# cimport numpy as np
from numpy.random import RandomState


def rk4(y, x, dx, f, u):
    """computes 4th order Runge-Kutta for dy/dx.
    y is the initial value for y
    x is the initial value for x
    dx is the difference in x (e.g. the time step)
    f is a callable function (y, x) that you supply to
      compute dy/dx for the specified values.
    """

    k1 = dx * f(y, x, u)
    k2 = dx * f(y + 0.5 * k1, x + 0.5 * dx, u)
    k3 = dx * f(y + 0.5 * k2, x + 0.5 * dx, u)
    k4 = dx * f(y + k3, x + dx, u)

    return y + (k1 + 2 * k2 + 2 * k3 + k4) / 6.


def fx(xfull, t, u):
    xdot = np.array([[0, 0, 0, 0],
                     [0, -2, 1, 0],
                     [0, -1, 0, 0],
                     [1, -1, 0, 0]]) @ xfull + np.array([[0, 2, 1, 0]]).T * u
    return xdot


class ParticleTrajectory2D(object):
    def __init__(self, x0, y0, D, noise=[0.0, 0.0]):
        self.x = x0
        self.y = y0
        self.t = 0
        self.noise = noise
        self.D = D
        self.randomise = RandomState()

    def step(self, dt, u):
        # print(randn())
        if True:
            self.x = rk4(self.x, self.t, dt, fx, u[0]) + np.array([[np.sqrt(2 * self.D * dt) * self.randomise.randn(), 0, 0, 0]]).T
            self.y = rk4(self.y, self.t, dt, fx, u[1]) + np.array([[np.sqrt(2 * self.D * dt) * self.randomise.randn(), 0, 0, 0]]).T
        else:
            self.x = rk4(self.x, self.t, dt, fx, u[0]) + np.array([[0, 0, 0, 0]]).T
            self.y = rk4(self.y, self.t, dt, fx, u[1]) + np.array([[0, 0, 0, 0]]).T
        self.t += dt
        return self.x, self.y


def intensity(double x, double y, double x0, double y0, double amp, double waist):
    cdef double r = np.linalg.norm([x - x0, y - y0])
    # cdef double r = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)
    cdef double retint
    retint = amp * np.exp(-4 * np.log(2) * ((r / waist) ** 2))
    return retint


def mf_intensity(double x, double y, double x0, double y0, double fwhm, double amp):
    cdef double r = np.linalg.norm([x - x0, y - y0])
    cdef double inten = amp * 4 * np.e * np.log(2) * ((r / fwhm) ** 2) * np.exp(-4 * np.log(2) * ((r / fwhm) ** 2))
    return inten
