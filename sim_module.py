import numpy as np
from numpy.random import randn
import warnings

from basic_sim import *


class TrackingSim:

    def __init__(self, numpoints=10000, method='orbital', freq=50, amp=1.0, waist=0.532, L=1.0, fwhm=1.0, tracking=True,
                 feedback=50):

        self.numpoints = numpoints
        self.method = method
        self.freq = freq

        self.amp = amp
        self.waist = waist

        self.L = L
        self.fwhm = fwhm

        self.tracking = tracking
        self.feedback = feedback

    def main_tracking(self, D):
        warnings.filterwarnings("ignore", category=RuntimeWarning)  # Prevent warnings like division by zero
        x = np.array([[0, 0, 0, 0]]).T
        y = np.array([[0, 0, 0, 0]]).T
        trajectory = ParticleTrajectory2D(x0=x, y0=y, D=D, noise=[0.0, 0.0])

        dt = 0.01  # timestep in ms

        theta = 0
        t = 0
        freq = self.freq  # cycles / ms

        tvals = np.zeros(self.numpoints)
        measx_vals = np.zeros(self.numpoints)
        truex_vals = np.zeros(self.numpoints)
        measy_vals = np.zeros(self.numpoints)
        truey_vals = np.zeros(self.numpoints)
        intvals = np.zeros(self.numpoints)

        # Orbital Method
        intsteps = np.int(1 / (freq * dt))
        # print('intsteps:', intsteps)
        omega = 2 * np.pi * freq
        r = self.waist / np.sqrt(2)
        # print('r:', r)
        int_fact = self.waist ** 2 / (2 * r)

        feedback_steps = np.int(1 / (self.feedback * dt))
        # print('feedback steps:', feedback_steps)

        measx = 0
        measy = 0
        prev_measx = 0
        prev_measy = 0
        xs = x[1]
        ys = y[1]

        for i in range(self.numpoints):
            t += dt
            tvals[i] = t

            ux = 0
            uy = 0

            x, y = trajectory.step(dt, (ux, uy))

            yp = y[0]
            xp = x[0]
            # ys = y[1]
            # xs = x[1]

            if self.tracking:
                if i % feedback_steps == 0:
                    xs = xs + measx
                    ys = ys + measy
            else:
                xs = 0
                ys = 0

            if self.method == 'orbital':
                theta += dt * omega
                x0 = r * np.cos(theta)
                y0 = r * np.sin(theta)
                int_iter = intensity(xp, yp, xs + x0, ys + y0, self.amp, self.waist)

            int_ms = 50 * int_iter + 0  # SBR = 50
            int_ms = np.random.poisson(int_ms)
            intvals[i] = int_ms

            if i % intsteps == 0:
                integral = np.sum(intvals[i - intsteps:i])
                if self.method == 'orbital':
                    integral_sin = np.sum(intvals[i-intsteps:i] * np.sin(omega * tvals[i-intsteps:i]))
                    integral_cos = np.sum(intvals[i-intsteps:i] * np.cos(omega * tvals[i-intsteps:i]))
                    measx = int_fact * (integral_cos / integral)
                    measy = int_fact * (integral_sin / integral)

            if np.isnan(measx):
                measx = prev_measx
            if np.isnan(measy):
                measy = prev_measy

            prev_measx = measx
            prev_measy = measy
            truex_vals[i] = xp
            measx_vals[i] = xs
            truey_vals[i] = yp
            measy_vals[i] = ys

        err = np.sum(np.sqrt((measx_vals - truex_vals) ** 2 + (measy_vals - truey_vals) ** 2)) / self.numpoints
        return err, measx_vals, truex_vals, measy_vals, truey_vals
