"""Main library for computing CRBs"""
import numpy as np
from matplotlib import pyplot as plt
import sympy as sp
import dill
dill.settings['recurse'] = True


class PositionMethod:

    def __init__(self, filename, iscat=False, bg=False):
        self.x, self.x0, self.y, self.y0, self.amp, self.fwhm, self.a, self.sigma = \
            sp.symbols('r x0 y y0 amp fwhm a sigma')
        self.r = sp.sqrt((self.x - self.x0) ** 2 + (self.y - self.y0) ** 2)
        self.L, self.N, self.sigma_n, self.SBR = sp.symbols('L, N, sigma_N, SBR')
        self.pvector = None
        self.filename = filename
        self.iscat = iscat
        self.bg = bg

    def parameter(self, xpos, ypos):
        """calculate parameter vector for beam center at xpos, ypos"""

        p_i = self.shape.subs([(self.x0, xpos), (self.y0, ypos)])
        # SBR = 110
        # SBR = 12
        # SBR = 1.9
        # SBR = 0.49
        # SBR = 0.12
        # SBR = 5000
        if self.bg:
            p_i = (self.SBR / (self.SBR + 1)) * p_i + 1 / ((self.SBR + 1) * 4)
        return p_i

    def param_vector(self):
        """calculate vector of parameters for list of positions"""

        xpositions = self.xpositions
        ypositions = self.ypositions

        sumi = 0
        for i, pos in enumerate(xpositions):
            sumi += self.parameter(xpositions[i], ypositions[i])

        pvec = []
        for i, pos in enumerate(xpositions):
            pvec.append(self.parameter(xpositions[i], ypositions[i]) / sumi)

        # sbr = self.sbr
        # k = len(pvec)
        # pvec = [(sbr / (sbr + 1)) * param + 1 / ((sbr + 1) * k) for param in pvec]

        self.pvector = pvec

    def return_lambda(self):

        crb = self.calculate_diffs()

        crb_lambda = self.lambdify(crb)

        self.pickle_lambda(crb_lambda)

    def lambdify(self, crb):
        if self.iscat:
            crb_lambda = sp.lambdify([self.x, self.y, self.L, self.N, self.fwhm, self.amp, self.sigma_n], crb,
                                     ['numpy', 'sympy'])
        elif self.bg:
            crb_lambda = sp.lambdify([self.x, self.y, self.L, self.N, self.fwhm, self.amp, self.SBR], crb,
                                     ['numpy', 'sympy'])
        else:
            crb_lambda = sp.lambdify([self.x, self.y, self.L, self.N, self.fwhm, self.amp], crb, ['numpy', 'sympy'])
        return crb_lambda

    def pickle_lambda(self, crb_lambda):
        fileobject = open(self.filename, 'wb')
        dill.dump(crb_lambda, fileobject)
        fileobject.close()

    def calculate_diffs(self):
        pvec = self.pvector
        xdiff = [p.diff(self.x) for p in pvec]
        ydiff = [p.diff(self.y) for p in pvec]

        # setup Fisher information matrix
        sum1 = 0
        sum2 = 0
        sum3 = 0
        sum4 = 0
        for i, p in enumerate(self.pvector[:]):
            if self.iscat:
                prec = 1 / p ** 2
            else:
                prec = 1 / p
            sum1 += prec * (xdiff[i] ** 2 + ydiff[i] ** 2)
            sum2 += prec * xdiff[i] ** 2
            sum3 += prec * ydiff[i] ** 2
            sum4 += prec * ydiff[i] * xdiff[i]
        if self.iscat:
            crb = sp.sqrt(self.sigma_n ** 2 / (self.N - self.sigma_n) ** 2) * sp.sqrt(sum1 / (2 * sum2 * sum3 - sum4 ** 2))
        else:
            crb = (1 / sp.sqrt(self.N)) * sp.sqrt(sum1 / (2 * sum2 * sum3 - sum4 ** 2))
        return crb

    def plotshape(self):
        pass
        # f = sp.lambdify([r, y, amp, fwhm], gaussian, "numpy")
        # xval = np.linspace(0, 10)
        # yval = 2
        # plt.plot(f(xval, yval, 1, 1))
        # plt.show()

    def plotpositions(self):
        pass
        # plt.plot(xpositions, ypositions)
        # plt.axis('equal')
        # plt.show()

    @staticmethod
    def doughnut(amp, r, fwhm):

        return amp * 4 * np.e * np.log(2) * ((r / fwhm) ** 2) * sp.exp(-4 * np.log(2) * ((r / fwhm) ** 2))


class MinFlux(PositionMethod):

    def __init__(self, filename, iscat=False, bg=False):
        super().__init__(filename, iscat, bg)
        self.shape = self.doughnut(self.amp, self.r, self.fwhm)
        # self.shape = self.amp * sp.exp(-4 * np.log(2) * ((self.r / self.fwhm) ** 2))
        self.get_pvector()
        self.return_lambda()

    def get_pvector(self):
        i = np.array([2.75, 3.75, 4.75])
        alpha = - (2 * np.pi / 3) * (i + 0.25)
        xpositions = self.L / 2 * np.cos(alpha)
        ypositions = self.L / 2 * np.sin(alpha)

        self.xpositions = np.insert(xpositions, 0, 0)
        self.ypositions = np.insert(ypositions, 0, 0)

        self.param_vector()

    def lambdify(self, crb):
        if self.bg:
            crb_lambda = sp.lambdify([self.x, self.y, self.L, self.N, self.fwhm, self.amp, self.SBR], crb, ['numpy', 'sympy'])
        else:
            crb_lambda = sp.lambdify([self.x, self.y, self.L, self.N, self.fwhm, self.amp], crb, ['numpy', 'sympy'])
        return crb_lambda


class Orbital(PositionMethod):

    def __init__(self, filename, iscat=False, bg=False):
        super().__init__(filename, iscat, bg)
        self.shape = self.amp * sp.exp(-4 * np.log(2) * ((self.r / self.fwhm) ** 2))
        self.get_pvector()
        self.return_lambda()

    def get_pvector(self):
        alpha = np.linspace(0, 360, 60, endpoint=False)
        print(alpha)
        alpha = np.deg2rad(alpha)
        self.xpositions = self.L / 2 * np.cos(alpha)
        self.ypositions = self.L / 2 * np.sin(alpha)

        self.param_vector()


class Knight(PositionMethod):

    def __init__(self, filename, spacing, iscat=False):
        super().__init__(filename, iscat)
        self.shape = self.amp * sp.exp(-4 * np.log(2) * ((self.r / self.fwhm) ** 2))
        # self.shape = self.doughnut(self.amp, self.r, self.fwhm)
        self.spacing = spacing
        self.get_pvector()
        self.return_lambda()

    def get_pvector(self):
        len_half = self.spacing * 2.5
        xrow = np.linspace(-len_half, len_half, 6)
        yrow = np.linspace(-len_half, len_half, 6)
        xpositions, ypositions = np.meshgrid(xrow, yrow)
        self.xpositions = xpositions.flatten()
        self.ypositions = ypositions.flatten()

        self.param_vector()


class Camera(PositionMethod):

    def __init__(self, filename):
        super().__init__(filename)
        self.shape = 0.25 * (sp.erf((self.x + self.a/2 - self.x0) / (sp.sqrt(2) * self.sigma)) -
                         sp.erf((self.x - self.a/2 - self.x0) / (sp.sqrt(2) * self.sigma))) * \
                 (sp.erf((self.y + self.a/2 - self.y0) / (sp.sqrt(2) * self.sigma)) -
                  sp.erf((self.y - self.a/2 - self.y0) / (sp.sqrt(2) * self.sigma)))
        self.get_pvector()
        self.return_lambda()

    def get_pvector(self):
        xrow = np.linspace(-450, 450, 3)
        yrow = np.linspace(-450, 450, 3)
        xpositions, ypositions = np.meshgrid(xrow, yrow)
        self.xpositions = xpositions.flatten()
        self.ypositions = ypositions.flatten()

        self.param_vector()


class OneDimPositionMethod:

    def __init__(self, filename, iscat=False):
        self.x, self.x0, self.amp, self.fwhm, self.a, self.sigma = sp.symbols('r x0 amp fwhm a sigma')
        self.L, self.N, self.sigma_n = sp.symbols('L, N, sigma_N')
        self.r = sp.sqrt((self.x - self.x0) ** 2)
        self.pvector = None
        self.filename = filename
        self.iscat = iscat

    def parameter(self, xpos):
        """calculate parameter vector for beam center at xpos, ypos"""

        p_i = self.shape.subs(self.x0, xpos)
        return p_i

    def param_vector(self):
        """calculate vector of parameters for list of positions"""

        xpositions = self.xpositions

        sumi = 0
        for i, pos in enumerate(xpositions):
            sumi += self.parameter(xpositions[i])

        pvec = []
        for i, pos in enumerate(xpositions):
            pvec.append(self.parameter(xpositions[i]) / sumi)

        self.pvector = pvec

    def return_lambda(self):

        crb = self.calculate_diffs()

        crb_lambda = self.lambdify(crb)

        self.pickle_lambda(crb_lambda)

    def lambdify(self, crb):
        if self.iscat:
            crb_lambda = sp.lambdify([self.x, self.L, self.N, self.fwhm, self.amp, self.sigma_n], crb, ['numpy', 'math'])
        else:
            crb_lambda = sp.lambdify([self.x, self.L, self.N, self.fwhm, self.amp], crb, ['numpy', 'math'])
        return crb_lambda

    def pickle_lambda(self, crb_lambda):
        fileobject = open(self.filename, 'wb')
        dill.dump(crb_lambda, fileobject)
        fileobject.close()

    def calculate_diffs(self):
        xdiff = [p.diff(self.x) for p in self.pvector]
        p = self.pvector[0]
        if self.iscat:
            crb = (self.sigma_n / (self.N - self.sigma_n)) * ((p * (1 - p)) / (sp.sqrt(1 - 2 * p + 2 * p ** 2) * sp.Abs(xdiff[0])))
        else:
            crb = (1 / sp.sqrt(self.N)) * (sp.sqrt(p * (1 - p)) / sp.Abs(xdiff[0]))
        return crb

    def plotshape(self, ampval, fwhmval, plotrange, L, ax=None):
        amp, r, fwhm = sp.symbols('amp, r, fwhm')
        f = sp.lambdify([amp, r, fwhm], self.shapes[self.shapename](amp, r, fwhm), 'numpy')
        xval = np.linspace(-plotrange, plotrange)
        if ax is not None:
            ax.plot(xval, f(ampval, xval - L / 2, fwhmval))
            ax.plot(xval, f(ampval, xval + L / 2, fwhmval))
        else:
            plt.plot(xval, f(ampval, xval - L / 2, fwhmval))
            plt.plot(xval, f(ampval, xval + L / 2, fwhmval))
            plt.show()

    def plotpositions(self):
        pass
        # plt.plot(xpositions, ypositions)
        # plt.axis('equal')
        # plt.show()

    @staticmethod
    def doughnut(amp, r, fwhm, *args):

        return amp * 4 * np.e * np.log(2) * ((r / fwhm) ** 2) * sp.exp(-4 * np.log(2) * ((r / fwhm) ** 2))

    @staticmethod
    def quad(amp, r, *args):

        return amp * r ** 2

    @staticmethod
    def cubic(amp, r, *args):

        return amp * sp.sqrt((r ** 6))

    @staticmethod
    def quartic(amp, r, *args):

        return amp * r ** 4

    @staticmethod
    def linear(amp, r, *args):

        return amp * sp.sqrt(r ** 2)

    @staticmethod
    def gaussian(amp, r, fwhm):
        return amp * sp.exp(-4 * np.log(2) * ((r / fwhm) ** 2))

    @staticmethod
    def piece1(r, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20,
              i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, i17, i18, i19, i20, *args):

        return sp.Piecewise((s1 * r + i1, (r >= 0) & (r < 9)), (s2 * r + i2, (r >= 9) & (r < 18)), (s3 * r + i3, (r >= 18) & (r < 27)),
                    (s4 * r + i4, (r >= 27) & (r < 36)), (s5 * r + i5, (r >= 36) & (r < 45)), (s6 * r + i6, (r >= 45) & (r < 54)),
                    (s7 * r + i7, (r >= 54) & (r < 63)), (s8 * r + i8, (r >= 63) & (r < 72)), (s9 * r + i9, (r >= 72) & (r < 81)),
                    (s10 * r + i10, (r >= 81) & (r < 90)), (s11 * r + i11, (r >= 90) & (r < 99)), (s12 * r + i12, (r >= 99) & (r < 108)),
                    (s13 * r + i13, (r >= 108) & (r < 117)), (s14 * r + i14, (r >= 117) & (r < 126)), (s15 * r + i15, (r >= 126) & (r < 135)),
                    (s16 * r + i16, (r >= 135) & (r < 144)), (s17 * r + i17, (r >= 144) & (r < 153)), (s18 * r + i18, (r >= 153) & (r < 162)),
                    (s19 * r + i19, (r >= 162) & (r < 171)), (s20 * r + i20, (r >= 171) & (r < 180)))

    def piece(self, r, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20,
              i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, i17, i18, i19, i20, *args):

        return sp.Piecewise((self.piece1(r, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17,
                                         s18, s19, s20, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14,
                                         i15, i16, i17, i18, i19, i20), (r >= 0) & (r < 180)),
                            (self.piece1(-r, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17,
                                         s18, s19, s20, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14,
                                         i15, i16, i17, i18, i19, i20), (r < 0) & (r > -180)))
                            # (self.piece1(-rout, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17,
                            #              s18, s19, s20, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14,
                            #              i15, i16, i17, i18, i19, i20), (r >= 0) & (r >= 180)),
                            # (self.piece1(rout, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17,
                            #              s18, s19, s20, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14,
                            #              i15, i16, i17, i18, i19, i20), (r < 0) & (r < -180)))

    @staticmethod
    def poly(r, a, b, c, d, e, f, g, h):
        return a * r ** 16 + b * r ** 14 + c * r ** 12 + d * r ** 10 + e * r ** 8 + f * r ** 6 + g * r ** 4 + h * r ** 2


class MinFlux1D(OneDimPositionMethod):

    def __init__(self, filename, shapename, iscat=False):
        super().__init__(filename, iscat)
        self.shapename = shapename
        self.shapes = {'doughnut': self.doughnut, 'quadratic': self.quad, 'linear': self.linear,
                       'gaussian': self.gaussian, 'cubic': self.cubic, 'quartic': self.quartic, 'piecewise': self.piece}
        self.shape = self.shapes[shapename](self.amp, self.r, self.fwhm)
        self.get_pvector()
        self.return_lambda()

    def get_pvector(self):
        self.xpositions = np.array([- self.L / 2, self.L / 2])

        self.param_vector()


class MinFlux1DPiecewise(OneDimPositionMethod):

    def __init__(self, filename, shapename):
        super().__init__(filename)
        self.shapename = shapename
        self.shapes = {'doughnut': self.doughnut, 'quadratic': self.quad, 'linear': self.linear,
                       'gaussian': self.gaussian, 'cubic': self.cubic, 'quartic': self.quartic, 'piecewise': self.piece}
        r, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20 = \
            sp.symbols('r, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20')
        i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, i17, i18, i19, i20 = \
            sp.symbols('i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, i17, i18, i19, i20')
        self.shape = self.piece(self.r, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15,
                                    s16, s17, s18, s19, s20, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10,
                                    i11, i12, i13, i14, i15, i16, i17, i18, i19, i20)
        self.get_pvector()
        self.return_lambda()

    def get_pvector(self):
        self.xpositions = np.array([- self.L / 2, self.L / 2])

        self.param_vector()

    def lambdify(self, crb):
        r, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20 = \
            sp.symbols('r, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20')
        i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, i17, i18, i19, i20 = \
            sp.symbols('i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, i17, i18, i19, i20')
        crb_lambda = sp.lambdify([self.L, self.N, self.x, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18,
                                  s19, s20, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, i17,
                                  i18, i19, i20], crb, ['numpy', 'math'])
        return crb_lambda

    def plotshape(self, s, i, fwhmval, plotrange, L, ax=None):
        r, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20 = \
            sp.symbols('r, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20')
        i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, i17, i18, i19, i20 = \
            sp.symbols('i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, i17, i18, i19, i20')

        f = sp.lambdify([r, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20,
                         i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, i17, i18, i19, i20],
                        self.shapes[self.shapename](r, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15,
                                                    s16, s17, s18, s19, s20, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10,
                                                    i11, i12, i13, i14, i15, i16, i17, i18, i19, i20), 'numpy')
        xval = np.linspace(-plotrange, plotrange, num=200)
        if ax is not None:
            ax.plot(xval, f(xval, s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9], s[10], s[11], s[12],
                            s[13], s[14], s[15], s[16], s[17], s[18], s[19], i[0], i[1], i[2], i[3], i[4], i[5], i[6],
                            i[7], i[8], i[9], i[10], i[11], i[12], i[13], i[14], i[15], i[16], i[17], i[18], i[19]))
            # ax.plot(xval, f(xval + L / 2, s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9], s[10], s[11],
            # s[12], s[13], s[14], s[15], s[16], s[17], s[18], s[19]))
        # else:
        #     plt.plot(xval, f(xval, s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9], s[10], s[11], s[12],
        #     s[13], s[14], s[15], s[16], s[17], s[18], s[19]))
        #     plt.plot(xval, f(xval + L / 2, s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9], s[10], s[11],
        #     s[12], s[13], s[14], s[15], s[16], s[17], s[18], s[19]))
            # plt.show()


class MinFlux1DPoly(OneDimPositionMethod):

    def __init__(self, filename, shapename):
        super().__init__(filename)
        self.shapename = shapename
        self.shapes = {'doughnut': self.doughnut, 'quadratic': self.quad, 'linear': self.linear,
                       'gaussian': self.gaussian, 'cubic': self.cubic, 'quartic': self.quartic, 'poly': self.poly}
        self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h = sp.symbols('a, b, c, d, e, f, g, h')
        self.shape = self.poly(self.r, self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h)
        self.get_pvector()
        self.return_lambda()

    def get_pvector(self):
        self.xpositions = np.array([- self.L / 2, self.L / 2])

        self.param_vector()

    def lambdify(self, crb):
        crb_lambda = sp.lambdify([self.L, self.N, self.x, self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h], crb, ['numpy', 'math'])
        return crb_lambda

    def plotshape(self, a, b, c, d, e, f, g, h, plotrange, L, ax=None):

        r = sp.symbols('r')
        func = sp.lambdify([r, self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h],
                        self.shapes[self.shapename](r, self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h), ['numpy', 'math'])
        xval = np.linspace(-plotrange, plotrange, num=200)
        if ax is not None:
            ax.plot(xval, func(xval - L / 2, a, b, c, d, e, f, g, h))
            ax.plot(xval, func(xval + L / 2, a, b, c, d, e, f, g, h))
        else:
            plt.plot(xval, func(xval - L / 2, a, b, c, d, e, f, g, h))
            plt.plot(xval, func(xval + L / 2, a, b, c, d, e, f, g, h))
            plt.show()
