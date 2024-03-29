# Main simulation module. Instance of TrackingSim is created after which main_tracking can be called multiple times.
import numpy as np
import scipy
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
                 feedback=50, iscat=False, stage=True, kalman=True, rin=0.1, debug=True, intfactor=None,
                 contrast=None, adjustment=1, bg=0, avint=0.01):

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
        self.bg = bg
        self.adjustment = adjustment
        self.avint = avint

        self.dt = 0.001  # timestep in ms
        self.cycle_steps = np.int(1 / (self.freq * self.dt))  # Number of time steps per feedback cycle

        self.omega = 2 * np.pi * self.freq  # Angular frequency for orbital method
        self.radius = self.waist / np.sqrt(2)  # Rotation radius
        self.int_fact = self.waist ** 2 / (2 * self.radius)  # Factor used to compute position estimate

        kt_positions = [(0, 5), (2, 6), (4, 5), (5, 3), (4, 1), (2, 0), (0, 1), (2, 2), (0, 3), (1, 5),
                        (3, 4), (5, 5), (6, 3), (5, 1), (3, 0), (1, 1), (3, 2), (1, 3), (2, 5), (4, 4),
                        (5, 2), (4, 0), (2, 1), (0, 0), (-1, 2), (0, 4), (2, 3), (3, 5), (5, 4), (4, 2),
                        (5, 0), (3, -1), (1, 0), (0, 2), (1, 4), (3, 3), (1, 2), (3, 1), (4, 3), (2, 4)]

        kt_positions = [np.subtract(pos, (2.5, 2.5)) for pos in kt_positions]
        kt_positions = [np.multiply(pos, 0.75 * self.waist) for pos in kt_positions]
        self.kt_positions = [tuple(pos) for pos in kt_positions]
        # Number of time steps per KT scan point:
        self.kt_steps = np.int(self.cycle_steps / (np.size(self.kt_positions) / 2))

        self.mf_positions = [(0, 0), (-0.25 * self.L, 0.43301 * self.L), (-0.25 * self.L, -0.43301 * self.L),
                             (0.5 * self.L, 0)]
        # Number of time steps per MF scan point:
        self.mf_steps = np.int(self.cycle_steps / 4)

        self.feedback_steps = np.int(1 / (self.feedback * self.dt))  # Number of steps per feedback cycle

        self.x0 = None
        self.y0 = None
        self.theta = 0  # Orbital method angle
        self.posnum = 0  # Current scan point for KT or MF
        self.tvals = np.zeros(self.numpoints)
        self.intvals = np.zeros(self.numpoints)
        self.avintvals = np.zeros(self.numpoints)
        self.integralvals = np.zeros(self.numpoints)
        self.bgvals = np.zeros(self.numpoints)

    def particle_kf(self, x, r=0.0, q=0.1):
        """Initialise Kalman filter using filterpy.

        Arguments:
            x -- initial state vector.
            r -- represents measurement noise.
            q -- represents process noise (brownian motion).
            """
        dt = self.feedback_steps * self.dt

        kf = KalmanFilter(dim_x=3, dim_z=1, dim_u=1)

        # kf.F = np.array([[1., 0., 0.],
        #                  [0., 1., dt],
        #                  [0., -8 * dt, 1 - 2 * dt]])
        # kf.F = np.array([[1., 0., 0.],
        #                  [0., 1 - 2 * dt, dt],
        #                  [0., -dt, 1.]])
        kf.F = np.array([[1., 0., 0.],
                         [0., 1 - 2 * dt, 4.0 * dt],
                         [0., -4.0 * dt, 1.]])

        kf.H = np.array([[1., -1., 0]])

        # kf.B = np.array([[0., 0., 8 * dt]]).T
        # kf.B = np.array([[0., 2 * dt, 1 * dt]]).T
        kf.B = np.array([[0., 2 * dt, 4.0 * dt]]).T
        kf.R *= r
        kf.Q *= np.array([[q, 0, 0],
                          [0, 0, 0],
                          [0, 0, 0]])

        kf.x = x
        kf.P = np.array([[0.0001, 0, 0],
                         [0, 0, 0],
                         [0, 0, 0]])
        return kf

    def meas_func(self, i):
        """Return estimated position using some scanning method"""

        cycle_steps = self.cycle_steps
        kt_steps = self.kt_steps
        omega = self.omega
        intvals = self.intvals
        bgvals = self.bgvals
        tvals = self.tvals
        integral = np.sum(intvals[i - cycle_steps:i])

        if self.method == 'orbital':
            integral_sin = np.sum(intvals[i - cycle_steps:i] * np.sin(omega * tvals[i - cycle_steps:i]))
            integral_cos = np.sum(intvals[i - cycle_steps:i] * np.cos(omega * tvals[i - cycle_steps:i]))
            measx = self.int_fact * (integral_cos / integral)
            measy = self.int_fact * (integral_sin / integral)

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
            pos3_int = np.sum(intvals[i - self.mf_steps:i]) / integral
            pos2_int = np.sum(intvals[i - 2 * self.mf_steps:i - self.mf_steps]) / integral
            pos1_int = np.sum(intvals[i - 3 * self.mf_steps:i - 2 * self.mf_steps]) / integral
            pos0_int = np.sum(intvals[i - 4 * self.mf_steps:i - 3 * self.mf_steps]) / integral

            x1, y1 = self.mf_positions[1]
            x2, y2 = self.mf_positions[2]
            x3, y3 = self.mf_positions[3]

            measx = np.dot([pos1_int, pos2_int, pos3_int], [x1, x2, x3])
            measy = np.dot([pos1_int, pos2_int, pos3_int], [y1, y2, y3])

            measx = measx * (-1) / (1 - ((self.L ** 2 * np.log(2)) / self.fwhm ** 2))
            measy = measy * (-1) / (1 - ((self.L ** 2 * np.log(2)) / self.fwhm ** 2))

            measx = measx * (1.27 + 3.8 * pos0_int)
            measy = measy * (1.27 + 3.8 * pos0_int)

        return measx, measy, integral

    def measure_pos(self, i, measx, measy, xp, xs, yp, ys):
        """Calculate measured intensity or contrast, and get measured position"""

        int_iter = self.calc_intensity(i, xp, xs, yp, ys)
        # TODO: remove the 10 here and add comments
        int_fluo = 10 * int_iter * self.dt

        if self.iscat:
            int_scat = int_fluo * self.intfactor * self.adjustment  # increased intensity for iscat
            int_scat = np.random.poisson(int_scat)

            bgval = (self.intfactor * self.adjustment * self.avint) / self.contrast
            bg_iter = np.random.poisson(bgval * 1000) / 1000
            bg_meas = np.random.poisson(bgval * 1000) / 1000  # background measured for calculating contrast

            contrast = (int_scat + bg_iter - bg_meas) / bg_meas
            self.intvals[i] = contrast
            self.avintvals[i] = int_fluo
            self.bgvals[i] = bg_meas
        else:
            bg = np.random.poisson(self.bg)
            int_fluo = np.random.poisson(int_fluo)
            self.intvals[i] = int_fluo + bg

        # Use intensity or contrast to get position estimate:
        if i % self.cycle_steps == 0:
            measx, measy, integral = self.meas_func(i)
            self.integralvals[i] = integral
        if np.isnan(measx):
            measx = 0
        if np.isnan(measy):
            measy = 0

        return measx, measy

    def calc_intensity(self, i, xp, xs, yp, ys):
        """Calculate current intensity at particle position"""

        if self.method == 'orbital':
            self.x0 = self.radius * np.cos(self.theta)
            self.y0 = self.radius * np.sin(self.theta)
            int_iter = intensity(xp, yp, xs + self.x0, ys + self.y0, self.amp, self.waist)

        elif self.method == 'knight':
            if i % self.kt_steps == 0:
                self.x0, self.y0 = self.kt_positions[self.posnum]
                if self.posnum == 39:
                    self.posnum = 0
                else:
                    self.posnum += 1
            int_iter = intensity(xp, yp, xs + self.x0, ys + self.y0, self.amp, self.waist)

        elif self.method == 'minflux':
            if i % self.mf_steps == 0:
                self.x0, self.y0 = self.mf_positions[self.posnum]
                if self.posnum == 3:
                    self.posnum = 0
                else:
                    self.posnum += 1
            int_iter = mf_intensity(xp, yp, xs + self.x0, ys + self.y0, self.fwhm, self.amp)
        return int_iter

    def main_tracking(self, D):

        warnings.filterwarnings("ignore", category=RuntimeWarning)  # Prevent warnings like division by zero
        if self.debug:
            print('cycle_steps:', self.cycle_steps)
            print('feedback steps:', self.feedback_steps)
            print('kt_steps:', self.kt_steps)
            print('mf_steps:', self.mf_steps)

        x = np.array([[0, 0, 0]]).T  # initial state
        y = np.array([[0, 0, 0]]).T
        trajectory = ParticleTrajectory2D(x0=x, y0=y, D=D)  # Initialise trajectory object from Cython library

        # Initialise loop variables
        t = 0
        self.tvals = np.zeros(self.numpoints)
        self.intvals = np.zeros(self.numpoints)
        self.integralvals = np.zeros(self.numpoints)

        measx_vals = np.zeros(self.numpoints)
        truex_vals = np.zeros(self.numpoints)
        kalmx_vals = np.zeros(self.numpoints)
        stagex_vals = np.zeros(self.numpoints)

        measy_vals = np.zeros(self.numpoints)
        truey_vals = np.zeros(self.numpoints)
        kalmy_vals = np.zeros(self.numpoints)
        stagey_vals = np.zeros(self.numpoints)

        kfx = self.particle_kf(x, r=self.rin, q=(2 * D))
        kfy = self.particle_kf(y, r=self.rin, q=(2 * D))

        self.theta = 0  # Orbital method angle
        self.posnum = 0  # Current scan point for KT or MF

        measx = 0  # Measred x position relative to stage
        measy = 0  # Measured y position relative to stage
        xs = x[1]  # Stage x position
        ys = y[1]  # Stage y position
        ux = 0  # Control x input
        uy = 0  # Control y input
        errsum_x = 0.
        errsum_y = 0.

        # Main simulation loop
        for i in range(self.numpoints):
            t += self.dt
            self.tvals[i] = t
            self.theta += self.dt * self.omega

            # Calculate new positions for stage and particle
            x, y = trajectory.step(self.dt, (ux, uy))
            yp = y[0]
            xp = x[0]
            if self.stage:
                ys = y[1]
                xs = x[1]

            # Apply feedback
            errsum_x += kfx.x[0, 0] - xs[0]
            errsum_y += kfy.x[0, 0] - ys[0]
            if self.tracking:
                if i % self.feedback_steps == 0:
                    if self.stage:
                        if self.kalman:
                            ux = kfx.x[0, 0]
                            uy = kfy.x[0, 0]
                            # ux = xs[0] + 0.005 * (kfx.x[0, 0] - xs[0]) + 0.000001 * errsum_x
                            # uy = ys[0] + 0.005 * (kfy.x[0, 0] - ys[0]) + 0.000001 * errsum_y
                        else:
                            ux = xs[0] + 0.3*measx
                            uy = ys[0] + 0.3*measy
                    else:
                        if self.kalman:
                            xs = kfx.x[0, 0]
                            ys = kfy.x[0, 0]
                        else:
                            xs = xs + measx
                            ys = ys + measy
            else:
                xs = 0
                ys = 0

            # Stage limit
            if xs > 20:
                xs = 20
            elif xs < -20:
                xs = -20
            if ys > 20:
                ys = 20
            elif ys < -20:
                ys = -20

            # Get measured postion
            measx, measy = self.measure_pos(i, measx, measy, xp, xs, yp, ys)

            # Update Kalman filter
            if i % self.feedback_steps == 0:
                kfx.predict(u=ux)
                kfx.update(measx)
                kfy.predict(u=uy)
                kfy.update(measy)

            truex_vals[i] = xp
            truey_vals[i] = yp
            measx_vals[i] = xs + measx
            measy_vals[i] = ys + measy
            stagex_vals[i] = xs
            stagey_vals[i] = ys
            kalmx_vals[i] = kfx.x[0]
            kalmy_vals[i] = kfy.x[0]
            # try:
            #     errsum_x += kfx.x[0, 0] - xs[0]
            #     errsum_y += kfy.x[0, 0] - ys[0]
            # except TypeError:
            #     errsum_x += kfx.x[0, 0] - xs
            #     errsum_y += kfy.x[0, 0] - ys
            #     print(xs)

        # err = np.sum(np.sqrt((measx_vals - truex_vals) ** 2 + (measy_vals - truey_vals) ** 2)) / self.numpoints
        err = np.sum(np.sqrt((stagex_vals - truex_vals) ** 2 + (stagey_vals - truey_vals) ** 2)) / self.numpoints
        # return err, measx_vals, truex_vals, measy_vals, truey_vals, intvals
        if self.debug:
            print("Average int expected: ", self.avint)
            print("Average int achieved: ", np.mean(self.avintvals))
        return err, stagex_vals, truex_vals, stagey_vals, truey_vals, self.intvals
        # return err, kalmx_vals, truex_vals, kalmy_vals, truey_vals, intvals

