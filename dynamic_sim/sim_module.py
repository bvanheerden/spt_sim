# Main simulation module. Instance of TrackingSim is created after which main_tracking can be called multiple times.
import numpy as np
from numpy.random import randn
import warnings
from filterpy.kalman import KalmanFilter
from basic_sim import *


class TrackingSim:
    """Main class of the module.

    After creating an instance, run main_tracking to simulate a trajectory.

    Arguments:

        numpoints -- number of simulation timesteps.
        method -- scanning method to use.
        freq -- scanning frequency in kHz.
        amp -- excitation intensity amplitude (a.u.)
        waist -- gaussian beam waist in um
        L -- tracking length in um
        tracking -- whether to apply feedback or not.
        feedback -- feedback frequency in kHz.
        stage -- whether to simulate stage dynamics or not.
        rin -- R value for Kalman filter.
        debug -- whether to print debug output.
        intfactor -- iSCAT vs fluorescence photon count factor.
        contrast -- average iSCAT contrast.
        """

    def __init__(self, numpoints=10000, method='orbital', freq=50, amp=1.0, waist=0.532, L=1.0, fwhm=1.0, tracking=True,
                 feedback=50, iscat=False, stage=True, kalman=True, rin=0.1, debug=True, intfactor=None, contrast=None):

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

        self.rin = rin

        self.debug = debug

        self.intfactor = intfactor
        self.contrast = contrast

        kt_positions = [(0, 5), (2, 6), (4, 5), (5, 3), (4, 1), (2, 0), (0, 1), (2, 2), (0, 3), (1, 5),
                        (3, 4), (5, 5), (6, 3), (5, 1), (3, 0), (1, 1), (3, 2), (1, 3), (2, 5), (4, 4),
                        (5, 2), (4, 0), (2, 1), (0, 0), (-1, 2), (0, 4), (2, 3), (3, 5), (5, 4), (4, 2),
                        (5, 0), (3, -1), (1, 0), (0, 2), (1, 4), (3, 3), (1, 2), (3, 1), (4, 3), (2, 4)]

        kt_positions = [np.subtract(pos, (2.5, 2.5)) for pos in kt_positions]
        kt_positions = [np.multiply(pos, 0.3) for pos in kt_positions]
        self.kt_positions = [tuple(pos) for pos in kt_positions]

    def particle_kf(self, x, dt, r=0.0, q=0.1):
        """Initialise Kalman filter using filterpy.

        Arguments:
            x -- initial state vector.
            dt -- timestep.
            r -- represents measurement noise.
            q -- represents process noise (brownian motion).
            """
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

    def meas_func(self, cycle_steps, i, int_fact, integralvals, intvals, kt_steps, measx, measy,
                  mf_positions, mf_steps, omega, tvals, x0, y0):
        """Return estimated position using some scanning method"""

        integral = np.sum(intvals[i - cycle_steps:i])
        integralvals[i] = integral

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
                    [tuple(np.multiply(pos, kt_intensities[i])) for i, pos in enumerate(self.kt_positions)]
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

            measx = measx * (-1) / (1 - ((self.L ** 2 * np.log(2)) / self.fwhm ** 2))
            measy = measy * (-1) / (1 - ((self.L ** 2 * np.log(2)) / self.fwhm ** 2))

            measx = measx * (1.27 + 3.8 * pos0_int)
            measy = measy * (1.27 + 3.8 * pos0_int)
        return measx, measy, x0, y0

    def main_tracking(self, D):
        warnings.filterwarnings("ignore", category=RuntimeWarning)  # Prevent warnings like division by zero
        x = np.array([[0, 0, 0, 0]]).T  # initial position and speed
        y = np.array([[0, 0, 0, 0]]).T
        trajectory = ParticleTrajectory2D(x0=x, y0=y, D=D)  # Initialise trajectory object from Cython library

        dt = 0.001  # timestep in ms
        cycle_steps = np.int(1 / (self.freq * dt))  # Number of time steps per feedback cycle
        if self.debug:
            print('cycle_steps:', cycle_steps)

        # Initialise loop variables
        t = 0
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
        integralvals = np.zeros(self.numpoints)

        # Orbital Method
        theta = 0
        omega = 2 * np.pi * self.freq
        r = self.waist / np.sqrt(2)  # Rotation radius
        int_fact = self.waist ** 2 / (2 * r)  # Factor used to compute position estimate
        
        # Knight's Tour
        kt_steps = np.int(cycle_steps / np.len(self.kt_positions))  # Number of time steps per KT scan point
        if self.debug:
            print('kt_steps:', kt_steps)
        posnum = 0  # Initialise current scan point

        # Minflux
        mf_positions = [(0, 0), (-0.25 * self.L, 0.43301 * self.L), (-0.25 * self.L, -0.43301 * self.L), (0.5 * self.L, 0)]
        mf_steps = np.int(cycle_steps / 4)
        if self.debug:
            print('mf_steps:', mf_steps)

        feedback_steps = np.int(1 / (self.feedback * dt))
        if self.debug:
            print('feedback steps:', feedback_steps)

        kalman_steps = feedback_steps
        kfx = self.particle_kf(x, kalman_steps * dt, r=self.rin, q=(2 * D * 100))
        kfy = self.particle_kf(y, kalman_steps * dt, r=self.rin, q=(2 * D * 100))

        measx = 0
        measy = 0
        prev_measx = 0
        prev_measy = 0
        xs = x[1]
        ys = y[1]
        ux = 0
        uy = 0

        # Main simulation loop
        for i in range(self.numpoints):
            t += dt
            tvals[i] = t

            if not self.stage:
                ux = 0
                uy = 0

            x, y = trajectory.step(dt, (ux, uy))

            yp = y[0]
            xp = x[0]
            # ys = y[1]
            # xs = x[1]
            if self.stage:
                ys = y[1]
                xs = x[1]

            if self.tracking:
                if i % feedback_steps == 0:
                    # xs = xs + measx
                    # ys = ys + measy
                    if self.stage:
                        if self.kalman:
                            ux = kfx.x[0, 0]
                            uy = kfy.x[0, 0]
                        else:
                            ux = xs[0] + measx
                            uy = ys[0] + measy
                    else:
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
                    x0, y0 = self.kt_positions[posnum]
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

                int_ms = self.intfactor * 2 * 10 * int_iter * dt

                int_ms = np.random.poisson(int_ms)

                bgval = (self.intfactor * 10 * dt) / self.contrast

                bg_ms = np.random.poisson(bgval*1000) / 1000
                bg_meas = np.random.poisson(bgval*1000) / 1000
                contrast = (int_ms + bg_ms - bg_meas) / bg_meas
                intvals[i] = contrast
            else:
                int_ms = 10 * int_iter + 0  # SBR = 10
                int_correct_iter = int_ms * dt
                int_correct_iter = np.random.poisson(int_correct_iter)
                intvals[i] = int_correct_iter

            if i % cycle_steps == 0:
                measx, measy, x0, y0 = self.meas_func(cycle_steps, i, int_fact, integralvals, intvals,
                                                      kt_steps, measx, measy, mf_positions, mf_steps,
                                                      omega, tvals, x0, y0)

            if np.isnan(measx):
                measx = prev_measx
            if np.isnan(measy):
                measy = prev_measy

            prev_measx = measx
            prev_measy = measy
            truex_vals[i] = xp
            # measx_vals[i] = xs
            truey_vals[i] = yp
            # measy_vals[i] = ys

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

        # err = np.sum(np.sqrt((measx_vals - truex_vals) ** 2 + (measy_vals - truey_vals) ** 2)) / self.numpoints
        err = np.sum(np.sqrt((stagex_vals - truex_vals) ** 2 + (stagey_vals - truey_vals) ** 2)) / self.numpoints
        # return err, measx_vals, truex_vals, measy_vals, truey_vals, integralvals
        return err, stagex_vals, truex_vals, stagey_vals, truey_vals, integralvals

