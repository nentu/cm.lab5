from math import comb, factorial as fac

import numpy as np
from sympy.abc import x as X_sym, t
from sympy import Lambda, sympify, latex


class UniformNutonInterpolator:
    name = 'UniformNuton'
    def __init__(self, X: np.array, Y: np.array):
        self.Y = Y
        self.X = X
        self.n = X.size
        self.h = X[1] - X[0]

    def f(self, x_0):
        return self.Y[np.where(self.X == x_0)][0]

    def d_k_y_i(self, k, i=0):
        res = 0
        for j in range(k + 1):
            coef = comb(k, j) * (1 if j % 2 == 0 else -1)
            res += self.Y[k + i - j] * coef
        # return symbols(f'\Delta^{k}y_{i}')

        return res

    def _get_t(self):
        return (X_sym - self.X[0]) / self.h

    def _interpolate(self):
        res = 0
        t = self._get_t()
        for i in range(self.n):
            part = 1
            for j in range(i):
                part *= (t - j)
            part /= fac(i)

            part *= self.d_k_y_i(i)

            res += part

        return res

    def do_interpolate(self):
        return Lambda(X_sym, self._interpolate())
