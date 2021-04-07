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
    """Compute derivative using ODE formula"""
    xdot = np.array([[0, 0, 0],
                     [0, -2, 1],
                     [0, -1, 0]]) @ xfull + np.array([[0, 2, 1]]).T * u
    return xdot


class ParticleTrajectory2D(object):
    """Tracjectory object. Used to get new system state in each iteration."""
    def __init__(self, x0, y0, D):
        self.x = x0
        self.y = y0
        self.t = 0
        self.D = D
        self.randomise = RandomState()

    def step(self, dt, u):
        """Return next state (integration step)"""
        diffx = np.sqrt(2 * self.D * dt) * self.randomise.randn()
        diffy = np.sqrt(2 * self.D * dt) * self.randomise.randn()

        self.x = rk4(self.x, self.t, dt, fx, u[0]) + np.array([[diffx, 0, 0]]).T
        self.y = rk4(self.y, self.t, dt, fx, u[1]) + np.array([[diffy, 0, 0]]).T
        self.t += dt
        return self.x, self.y


def intensity(double x, double y, double x0, double y0, double amp, double waist):
    """Calculate illumination intensity at particle postion x, y with laser position x0, y0"""
    cdef double r = np.linalg.norm([x - x0, y - y0])
    cdef double retint
    retint = amp * np.exp(-4 * np.log(2) * ((r / waist) ** 2))
    return retint


def mf_intensity(double x, double y, double x0, double y0, double fwhm, double amp):
    """Same as function intensity, but for a doughnut beam"""
    cdef double r = np.linalg.norm([x - x0, y - y0])
    cdef double inten = amp * 4 * np.e * np.log(2) * ((r / fwhm) ** 2) * np.exp(-4 * np.log(2) * ((r / fwhm) ** 2))
    return inten
