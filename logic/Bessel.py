from math import comb, factorial as fac

import numpy as np
from sympy.abc import x as X_sym, t
from sympy import Lambda, symbols

from logic.UniformNuton import UniformNutonInterpolator


class BesselInterpolator(UniformNutonInterpolator):
    name = 'BesselInterpolator'
    def __init__(self, X: np.array, Y: np.array):
        super().__init__(X, Y)

        roll_n = self.n // 2 + 1
        self.X = np.roll(self.X, roll_n)
        self.Y = np.roll(self.Y, roll_n)

        # assert self.n % 2 == 1

    # def d_k_y_i(self, i, k=0):
    #     return symbols(f'd^{i}y_{k}')

    def _interpolate(self):
        res = 0
        t = self._get_t()
        for i in range(self.n // 2):
            part1 = 1
            for j in range(2 * i):
                part1 *= (t + (-1) ** j * j // 2)

            part2 = (self.d_k_y_i(2 * i, -i) + self.d_k_y_i(2 * i, -i + 1)) / 2 / fac(2 * i)

            part3 = (t - 1 / 2) * self.d_k_y_i(2 * i + 1, -i) / fac(2 * i + 1)

            full_part = part1 * (part2 + part3)
            res += full_part

        return res

    def do_interpolate(self):
        return Lambda(X_sym, self._interpolate())


if __name__ == '__main__':
    X = np.array([20, 24, 28, 32])
    Y = np.array([2854, 3162, 3544, 3992])
    b = BesselInterpolator(X, Y)
    print(b.do_interpolate()(25))
