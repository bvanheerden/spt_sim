# Main simulation module. Instance of TrackingSim is created after which main_tracking can be called multiple times.
import numpy as np
from numpy.random import randn
import warnings
from filterpy.kalman import KalmanFilter
import scipy

from basic_sim import *


def scat_intensity(x, y, x0, y0, amp, waist):
    r = np.linalg.norm([x - x0, y - y0])
    retint = amp * np.exp(-4 * np.log(2) * ((r / waist) ** 2))
    return retint


class TrackingSim:

    def __init__(self, numpoints=10000, method='orbital', freq=50, amp=1.0, waist=0.532, L=1.0, fwhm=1.0, tracking=True,
                 feedback=50, iscat=False, stage=True, kalman=True, lqr=True, rin=0.1, weights=[1, 1, 1, 1]):

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
        self.stage = stage
        self.kalman = kalman
        self.lqr = lqr

        self.rin = rin

        self.rcont = weights[0]
        self.q1 = weights[1]
        self.q2 = weights[2]
        self.q3 = weights[3]

        self.x0 = 0
        self.y0 = 0
        self.first = 0  # quick fix for minflux problem with first measurement

    def particle_kf(self, x, dt, r=0.0, q=0.1):
        kf = KalmanFilter(dim_x=4, dim_z=1, dim_u=1)

        kf.F = np.array([[1., 0., 0., 0.],
                         [0., 1 - 2 * dt, dt, 0.],
                         [0., -dt, 1., 0.],
                         [dt, -dt, 0., 1.]])

        kf.H = np.array([[1., -1., 0, 0]])

        kf.B = np.array([[0., 2 * dt, dt, 0]]).T
        kf.R *= r
        kf.Q *= np.array([[q, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]])

        #     kf.x = np.array([[x, vx, y, vy]]).T
        kf.x = x
        return kf

    def get_lqr(self, r, dt, q1, q2, q3):

        F = np.array([[1 - 2 * dt, dt, 0.],
                     [-dt, 1., 0.],
                     [-dt, 0., 1.]])
        # F = np.array([[1 - 2 * dt, dt],
        #               [-1., 0.]])

        B = np.array([[2 * dt, dt, 0]]).T
        R = r
        # Q = np.array([[1, -1, 0, 0],
        #               [-1, 1, 0, 0],
        #               [0, 0, 1, 0],
        #               [0, 0, 0, 1]])
        Q = np.array([[q1, 0, 0],
                      [0, q2, 0],
                      [0, 0, q2]])

        # solve DARE
        X = np.matrix(scipy.linalg.solve_discrete_are(F, B, Q, R))

        # compute the LQR gain
        K = np.matrix(scipy.linalg.inv(B.T * X * B + R) * (B.T * X * F))
        return K

    def get_intensity(self, dt, fwhm, i, kt_positions, kt_steps, mf_positions, mf_steps, omega, posnum, r,
                      theta, xp, xs, yp, ys):
        if self.method == 'orbital':
            x0 = r * np.cos(theta)
            y0 = r * np.sin(theta)
            int_iter = intensity(xp, yp, xs + x0, ys + y0, self.amp, self.waist)

        elif self.method == 'knight':
            if i % kt_steps == 0:
                self.x0, self.y0 = kt_positions[posnum]
                if posnum == 39:
                    posnum = 0
                else:
                    posnum += 1
            int_iter = intensity(xp, yp, xs + self.x0, ys + self.y0, self.amp, self.waist)

        elif self.method == 'minflux':
            if i % mf_steps == 0:
                self.x0, self.y0 = mf_positions[posnum]
                if posnum == 3:
                    posnum = 0
                else:
                    posnum += 1
            int_iter = mf_intensity(xp, yp, xs + self.x0, ys + self.y0, fwhm, self.amp)
        if self.iscat:
            int_ms = 1180 * int_iter
            # int_ms = 800 * int_iter
            # int_ms = 1060 * int_iter
            # int_ms = 10 * int_iter
            int_s = np.int(int_ms * 1000)
            int_ms = np.random.poisson(int_s) / 1000
            # bg_ms = np.random.poisson(1072727)  # contrast 0.11% with average count rate 1.18 Mcps
            bg_ms = np.random.poisson(1072727000) / 1000  # contrast 0.11% with average count rate 1.18 Mcps
            # bg_ms = np.random.poisson(2666667)  # contrast 0.03% with average count rate 0.8 Mcps
            # bg_ms = np.random.poisson(2666667000) / 1000 # contrast 0.03% with average count rate 0.8 Mcps
            # bg_ms = np.random.poisson(235e6)  # contrast 0.00045% with average count rate 1.06 Mcps
            # bg_ms = np.random.poisson(235e9) / 1000  # contrast 0.00045% with average count rate 1.06 Mcps
            # bg_ms = np.random.poisson(1000000) / 1000  # contrast 1% with average count rate 10 kcps
            bg_meas = np.random.poisson(1072727000) / 1000
            contrast = (int_ms + bg_ms - bg_meas) / bg_meas
            return(contrast)
        else:
            int_ms = 10 * int_iter + 0  # SBR = 50
            ### big change 11/04!!! Trying to use correct iteration counts
            # int_ms = np.random.poisson(int_ms)
            int_iter_correct = int_ms * dt
            int_iter_correct = np.random.poisson(int_iter_correct)
            return(int_iter_correct)

    def get_meas_pos(self, L, cycle_steps, fwhm, i, int_fact, intvals, kt_positions, kt_steps, measx, measy,
                     mf_positions, mf_steps, omega, tvals):
        integral = np.sum(intvals[i - cycle_steps:i])
        if self.method == 'orbital':
            integral_sin = np.sum(intvals[i - cycle_steps:i] * np.sin(omega * tvals[i - cycle_steps:i]))
            integral_cos = np.sum(intvals[i - cycle_steps:i] * np.cos(omega * tvals[i - cycle_steps:i]))
            measx = int_fact * (integral_cos / integral)
            measy = int_fact * (integral_sin / integral)

        elif self.method == 'knight':
            if i != 0:
                kt_intensities = intvals[i - cycle_steps:i].reshape((40, kt_steps)).sum(axis=1)
                kt_intensities = kt_intensities / np.sum(kt_intensities)
                weighted_positions = \
                    [tuple(np.multiply(pos, kt_intensities[i])) for i, pos in enumerate(kt_positions)]
                sumpos = tuple(np.sum(weighted_positions, axis=0))
                measx, measy = sumpos
            else:
                measx, measy = 0, 0

        elif self.method == 'minflux':
            pos3_int = np.sum(intvals[i - mf_steps:i]) / integral
            pos2_int = np.sum(intvals[i - 2 * mf_steps:i - mf_steps]) / integral
            pos1_int = np.sum(intvals[i - 3 * mf_steps:i - 2 * mf_steps]) / integral
            pos0_int = np.sum(intvals[i - 4 * mf_steps:i - 3 * mf_steps]) / integral

            x0, y0 = mf_positions[0]
            x1, y1 = mf_positions[1]
            x2, y2 = mf_positions[2]
            x3, y3 = mf_positions[3]

            measx = np.dot([pos1_int, pos2_int, pos3_int], [x1, x2, x3])
            measy = np.dot([pos1_int, pos2_int, pos3_int], [y1, y2, y3])

            measx = measx * (-1) / (1 - ((L ** 2 * np.log(2)) / fwhm ** 2))
            measy = measy * (-1) / (1 - ((L ** 2 * np.log(2)) / fwhm ** 2))

            measx = measx * (1.27 + 3.8 * pos0_int)
            measy = measy * (1.27 + 3.8 * pos0_int)

            if self.first > 0:
                measx, measy = 0, 0
                self.first -= 1
        return measx, measy

    def main_tracking(self, D):
        warnings.filterwarnings("ignore", category=RuntimeWarning)  # Prevent warnings like division by zero
        x = np.array([[0, 0, 0, 0]]).T
        y = np.array([[0, 0, 0, 0]]).T
        trajectory = ParticleTrajectory2D(x0=x, y0=y, D=D, noise=[0.0, 0.0])

        dt = 0.001  # timestep in ms

        theta = 0
        t = 0
        freq = self.freq  # cycles / ms

        # initialize arrays
        tvals = np.zeros(self.numpoints)
        measx_vals = np.zeros(self.numpoints)
        truex_vals = np.zeros(self.numpoints)
        kalmx_vals = np.zeros(self.numpoints)
        stagex_vals = np.zeros(self.numpoints)

        measy_vals = np.zeros(self.numpoints)
        truey_vals = np.zeros(self.numpoints)
        kalmy_vals = np.zeros(self.numpoints)
        stagey_vals = np.zeros(self.numpoints)

        intvals = np.zeros(self.numpoints)

        # Orbital Method
        cycle_steps = np.int(1 / (freq * dt))
        # print('cycle_steps:', cycle_steps)
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
        # print('kt_steps:', kt_steps)
        posnum = 0

        # Minflux
        L = self.L
        fwhm = self.fwhm
        mf_positions = [(0, 0), (-0.25 * L, 0.43301 * L), (-0.25 * L, -0.43301 * L), (0.5 * L, 0)]
        mf_steps = np.int(cycle_steps / 4)
        # print('mf_steps:', mf_steps)

        feedback_steps = np.int(1 / (self.feedback * dt))
        # print('feedback steps:', feedback_steps)

        # kalman_freq = self.freq  # cycles / ms
        # kalman_steps = np.int(1 / (kalman_freq * dt))
        kalman_steps = feedback_steps
        kfx = self.particle_kf(x, kalman_steps * dt, r=self.rin, q=(2 * D * 100))
        kfy = self.particle_kf(y, kalman_steps * dt, r=self.rin, q=(2 * D * 100))

        K = self.get_lqr(self.rcont, dt, self.q1, self.q2, self.q3)
        # K = np.insert(K, 0, 0)
        print(K)

        measx = 0
        measy = 0
        prev_measx = 0
        prev_measy = 0
        xs = x[1]
        ys = y[1]
        ux = 0
        uy = 0

        # ---------------------------------------------------------------------------------------------------- #
        # Main simulation loop
        for i in range(self.numpoints):
            t += dt
            tvals[i] = t
            theta += dt * omega

            if not self.stage:
                ux = 0
                uy = 0

            # simulate system
            x, y = trajectory.step(dt, (ux, uy))

            yp = y[0]
            xp = x[0]
            if self.stage:
                ys = y[1]
                xs = x[1]

            # perform tracking (or not)
            if self.tracking:
                if i % feedback_steps == 0:
                    if self.stage:
                        if self.kalman:
                            # ux = K * (kfx.x[0, 0] - kfx.x[1, 0])
                            # uy = K * (kfy.x[0, 0] - kfy.x[1, 0])
                            ux = kfx.x[0, 0]
                            uy = kfy.x[0, 0]
                            # print(kfx.x[1:])
                            if self.lqr:
                                ux = -K @ (kfx.x[1:] - np.array([kfx.x[0], 0, 0], dtype=object))
                                uy = -K @ (kfy.x[1:] - np.array([kfy.x[0], 0, 0], dtype=object))
                                ux = ux[0, 0]
                                uy = uy[0, 0]
                        else:
                            ux = xs[0] + measx
                            uy = ys[0] + measy
                    else:
                        xs = xs + measx
                        ys = ys + measy
            else:
                xs = 0
                ys = 0

            # get measured intensity
            intvals[i] = self.get_intensity(dt, fwhm, i, kt_positions, kt_steps, mf_positions, mf_steps, omega, posnum,
                                            r, theta, xp, xs, yp, ys)

            # calculate measured position
            if i % cycle_steps == 0:
                measx, measy = self.get_meas_pos(L, cycle_steps, fwhm, i, int_fact, intvals, kt_positions, kt_steps,
                                                 measx, measy, mf_positions, mf_steps, omega, tvals)

            # check for invalid values
            if np.isnan(measx):
                measx = prev_measx
            if np.isnan(measy):
                measy = prev_measy

            prev_measx = measx
            prev_measy = measy
            truex_vals[i] = xp
            truey_vals[i] = yp

            if True:
                if i % kalman_steps == 0:
                    kfx.predict(u=ux)
                    kfx.update(measx)
                    kfy.predict(u=uy)
                    kfy.update(measy)

            measx_vals[i] = xs + measx
            measy_vals[i] = ys + measy
            stagex_vals[i] = xs
            stagey_vals[i] = ys

            if True:
                kalmx_vals[i] = kfx.x[0]
                kalmy_vals[i] = kfy.x[0]
            else:
                kalmx_vals[i] = xs[0] + measx
                kalmy_vals[i] = ys[0] + measy

        err = np.sum(np.sqrt((stagex_vals - truex_vals) ** 2 + (stagey_vals - truey_vals) ** 2)) / self.numpoints

        return err, measx_vals, truex_vals, kalmx_vals, stagex_vals, measy_vals, truey_vals, kalmy_vals, stagey_vals, intvals

