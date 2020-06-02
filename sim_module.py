# Main simulation module. Instance of TrackingSim is created after which main_tracking can be called multiple times.
import numpy as np
from numpy.random import randn
import warnings

from basic_sim import *


def scat_intensity(x, y, x0, y0, amp, waist):
    r = np.linalg.norm([x - x0, y - y0])
    retint = amp * np.exp(-4 * np.log(2) * ((r / waist) ** 2))
    return retint


class TrackingSim:

    def __init__(self, numpoints=10000, method='orbital', freq=50, amp=1.0, waist=0.532, L=1.0, fwhm=1.0, tracking=True,
                 feedback=50, iscat=False):

        self.numpoints = numpoints
        self.method = method
        self.freq = freq

        self.amp = amp
        self.waist = waist

        self.L = L
        self.fwhm = fwhm

        self.tracking = tracking
        self.feedback = feedback

        self.iscat = iscat

    def main_tracking(self, D):
        warnings.filterwarnings("ignore", category=RuntimeWarning)  # Prevent warnings like division by zero
        x = np.array([[0, 0, 0, 0]]).T
        y = np.array([[0, 0, 0, 0]]).T
        trajectory = ParticleTrajectory2D(x0=x, y0=y, D=D, noise=[0.0, 0.0])

        dt = 0.001  # timestep in ms

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
        cycle_steps = np.int(1 / (freq * dt))
        print('cycle_steps:', cycle_steps)
        omega = 2 * np.pi * freq
        r = self.waist / np.sqrt(2)
        # print('r:', r)
        int_fact = self.waist ** 2 / (2 * r)
        
        # Knight's Tour
        kt_positions = [(0, 5), (2, 6), (4, 5), (5, 3), (4, 1), (2, 0), (0, 1), (2, 2), (0, 3), (1, 5),
                        (3, 4), (5, 5), (6, 3), (5, 1), (3, 0), (1, 1), (3, 2), (1, 3), (2, 5), (4, 4),
                        (5, 2), (4, 0), (2, 1), (0, 0), (-1, 2), (0, 4), (2, 3), (3, 5), (5, 4), (4, 2),
                        (5, 0), (3, -1), (1, 0), (0, 2), (1, 4), (3, 3), (1, 2), (3, 1), (4, 3), (2, 4)]

        kt_positions = [np.subtract(pos, (2.5, 2.5)) for pos in kt_positions]
        kt_positions = [np.multiply(pos, 0.3) for pos in kt_positions]
        kt_positions = [tuple(pos) for pos in kt_positions]
        kt_steps = np.int(cycle_steps / 40)
        print('kt_steps:', kt_steps)
        posnum = 0

        # Minflux
        L = self.L
        fwhm = self.fwhm
        mf_positions = [(0, 0), (-0.25 * L, 0.43301 * L), (-0.25 * L, -0.43301 * L), (0.5 * L, 0)]
        mf_steps = np.int(cycle_steps / 4)
        print('mf_steps:', mf_steps)

        feedback_steps = np.int(1 / (self.feedback * dt))
        print('feedback steps:', feedback_steps)

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

            elif self.method == 'knight':
                if i % kt_steps == 0:
                    x0, y0 = kt_positions[posnum]
                    if posnum == 39:
                        posnum = 0
                    else:
                        posnum += 1
                int_iter = intensity(xp, yp, xs + x0, ys + y0, self.amp, self.waist)

            elif self.method == 'minflux':
                if i % mf_steps == 0:
                    x0, y0 = mf_positions[posnum]
                    if posnum == 3:
                        posnum = 0
                    else:
                        posnum += 1
                int_iter = mf_intensity(xp, yp, xs + x0, ys + y0, fwhm, self.amp)

            if self.iscat:
                int_ms = 1 * int_iter
                int_ms = np.random.poisson(int_ms)
                bg_ms = np.random.poisson(40)  # contrast 3% with average count rate 6 Mcps
                contrast = int_ms / bg_ms
                intvals[i] = contrast
            else:
                int_ms = 50 * int_iter + 0  # SBR = 50
                int_ms = np.random.poisson(int_ms)
                intvals[i] = int_ms

            if i % cycle_steps == 0:
                integral = np.sum(intvals[i - cycle_steps:i])
                if self.method == 'orbital':
                    integral_sin = np.sum(intvals[i-cycle_steps:i] * np.sin(omega * tvals[i-cycle_steps:i]))
                    integral_cos = np.sum(intvals[i-cycle_steps:i] * np.cos(omega * tvals[i-cycle_steps:i]))
                    measx = int_fact * (integral_cos / integral)
                    measy = int_fact * (integral_sin / integral)

                elif self.method == 'knight':
                    if i != 0:
                        kt_intensities = intvals[i-cycle_steps:i].reshape((40, kt_steps)).sum(axis=1)
                        kt_intensities = kt_intensities / np.sum(kt_intensities)
                        weighted_positions = \
                            [tuple(np.multiply(pos, kt_intensities[i])) for i, pos in enumerate(kt_positions)]
                        sumpos = tuple(np.sum(weighted_positions, axis=0))
                        measx, measy = sumpos
                    else:
                        measx, measy = 0, 0

                elif self.method == 'minflux':
                    pos3_int = np.sum(intvals[i-mf_steps:i]) / integral
                    pos2_int = np.sum(intvals[i-2*mf_steps:i-mf_steps]) / integral
                    pos1_int = np.sum(intvals[i-3*mf_steps:i-2*mf_steps]) / integral
                    pos0_int = np.sum(intvals[i-4*mf_steps:i-3*mf_steps]) / integral

                    x0, y0 = mf_positions[0]
                    x1, y1 = mf_positions[1]
                    x2, y2 = mf_positions[2]
                    x3, y3 = mf_positions[3]

                    measx = np.dot([pos1_int, pos2_int, pos3_int], [x1, x2, x3])
                    measy = np.dot([pos1_int, pos2_int, pos3_int], [y1, y2, y3])

                    measx = measx * (-1)/(1 - ((L ** 2 * np.log(2)) / fwhm ** 2))
                    measy = measy * (-1)/(1 - ((L ** 2 * np.log(2)) / fwhm ** 2))

                    measx = measx * (1.27 + 3.8 * pos0_int)
                    measy = measy * (1.27 + 3.8 * pos0_int)

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
        return err, measx_vals, truex_vals, measy_vals, truey_vals, intvals
