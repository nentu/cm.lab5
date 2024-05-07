from math import factorial as fac

import numpy as np
from sympy.abc import x as X_sym, t
from sympy import symbols, Lambda, latex, sympify

from logic.UniformNuton import UniformNutonInterpolator


class GaussInterpolator(UniformNutonInterpolator):
    a = None
    name = 'GaussInterpolator'

    def __init__(self, X: np.array, Y: np.array, a: float = None):
        super().__init__(X, Y)
        if a is None:
            a = X[self.n // 2 + 1]

        roll_n = self.n // 2 + 1
        self.X = np.roll(self.X, roll_n)
        self.Y = np.roll(self.Y, roll_n)
        self.a = a

    def _get_t(self):
        return (X_sym - self.a) / self.h


    # def d_k_y_i(self, i, k=0):
    #     return symbols('\Delta^{'+str(k)+'}y_{'+str(i)+'}')


    def _greater_interpolate(self):
        res = 0
        t = self._get_t()
        for i in range(self.n):
            part = 1
            for j in range(1, i + 1):
                part *= (t + ((-1) ** (j + 1)) * (j // 2))
            part *= self.d_k_y_i(i, -1 * (i // 2))

            part /= fac(i)

            res += part
            pass
        return res

    def _less_interpolate(self):
        res = 0
        t = self._get_t()
        for i in range(self.n):
            part = 1
            for j in range(1, i + 1):
                part *= (t + ((-1) ** j) * (j // 2))

            part *= self.d_k_y_i(i, -1 * ((i + 1) // 2))

            part /= fac(i)
            res += part
            pass

        return res

    def do_interpolate(self):
        return lambda x: (
            Lambda(X_sym, self._greater_interpolate())(x)) if x >= self.a \
            else Lambda(X_sym, self._less_interpolate())(x)


if __name__ == '__main__':
    x_list = np.array([310,
                       320,
                       330,
                       340,
                       350,
                       360])
    y_list = np.array([2.4914,
                       2.5052,
                       2.5185,
                       2.5315,
                       2.5441,
                       2.5563])
    gauss = GaussInterpolator(x_list, y_list)
    vec_f = np.vectorize(gauss.do_interpolate)

    print(x_list)
    print(y_list)
    print([gauss.do_interpolate()(x) for x in x_list])
    print(gauss.do_interpolate()(335))
