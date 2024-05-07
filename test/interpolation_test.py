from unittest import TestCase

from logic.interpolator import *


class InterpolationTest(TestCase):
    epsilon = 1e-1

    def test_lagrange_interpolation(self):
        x = np.linspace(0.1, 0.5, 5)
        y = np.array([1.25, 2.38, 3.79, 5.44, 7.14])
        lagrange = LagrangeInterpolator(x, y)
        self.assertLess((lagrange.do_interpolate()(0.35) - 4.594), self.epsilon)

        Lp = np.vectorize(lagrange.do_interpolate())
        self.assertLess(np.max(np.abs(y - Lp(x))), self.epsilon)

        # x = np.linspace(1, 4, 4)
        # y = np.array([0, 3, 5, 7])
        # self.assertEqual(
        #     simplify(lagrange_interpolation(x, y)),
        #     simplify((X_sym ** 3) * 1 / 6 - 9 / 6 * X_sym ** 2 + 38 / 6 * X_sym - 5))

    def test_divided_differences(self):
        x = np.array([0.15, 0.2, 0.33, 0.47])
        y = np.array([1.25, 2.38, 3.79, 5.44])

        nuton = NutonInterpolator(x, y)

        for x_i, y_i in zip(x, y):
            self.assertEqual(nuton.dd([x_i]), y_i)

        tests = [
            ([0, 1], 22.6),
            ([2, 1], 10.846),
            ([3, 2], 11.786),
            ([0, 1, 2], -65.3),
            ([1, 2, 3], 3.481),
            ([0, 1, 2, 3], 214.914)
        ]

        for ids, res in tests:
            self.assertLess(nuton.dd(x[ids]) - res, self.epsilon * 10 ** 3,
                            f'Test {ids}: expected: {res}, actual:{nuton.dd(x[ids])}')

    def test_d_k_y_i(self):
        x = np.linspace(0.1, 0.5, 5)
        y = np.array([1.25, 2.38, 3.79, 5.44, 7.14])

        nuton = UniformNutonInterpolator(x, y)

        res = [
            [1.25, 1.13, 0.28, -0.04, -0.15],
            [2.38, 1.41, 0.24, -0.19],
            [3.79, 1.65, 0.05],
            [5.44, 1.7],
            [7.14]
        ]

        for k in range(x.size):
            for i in range(x.size - k):
                self.assertLess(nuton.d_k_y_i(k, i) - res[i][k], self.epsilon)

    def test_nuton_interpolator(self):
        x = np.array([0.15, 0.2, 0.33, 0.47])
        y = np.array([1.25, 2.38, 3.79, 5.44])

        nuton = NutonInterpolator(x, y)

        Np = np.vectorize(nuton.do_interpolate())
        self.assertLess(np.max(np.abs(y - Np(x))), self.epsilon)

        self.assertLess(nuton.do_interpolate()(0.22) - 2.707, self.epsilon * 10 ** 3)

    def test_unifom_nuton_interpolator(self):
        x = np.linspace(0.1, 0.5, 5)
        y = np.array([1.25, 2.38, 3.79, 5.44, 7.14])

        nuton = UniformNutonInterpolator(x, y)

        Np = np.vectorize(nuton.do_interpolate())
        self.assertLess(np.max(np.abs(y - Np(x))), self.epsilon)

        self.assertLess(nuton.do_interpolate()(0.15) - 1.78336, self.epsilon ** 2)
        self.assertLess(nuton.do_interpolate()(0.22) - 2.63368, self.epsilon ** 2)
        self.assertLess(nuton.do_interpolate()(0.47) - 6.64208, self.epsilon ** 2)

    def test_gauss(self):
        x = np.linspace(0.1, 0.5, 5)
        y = np.array([1.25, 2.38, 3.79, 5.44, 7.14])

        gauss = GaussInterpolator(x, y)

        Gp = np.vectorize(gauss.do_interpolate())
        self.assertLess(np.max(np.abs(y - Gp(x))), self.epsilon)

    def test_bessel(self):
        x = np.linspace(0.1, 0.5, 5)
        y = np.array([1.25, 2.38, 3.79, 5.44, 7.14])

        gauss = BesselInterpolator(x, y)

        Bp = np.vectorize(gauss.do_interpolate())

        print(y)
        print(Bp(x))
        self.assertLess(np.sum(np.abs(y - Bp(x))) / x.size, self.epsilon)
