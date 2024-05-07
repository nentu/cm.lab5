from math import factorial as fac

import numpy as np
from sympy.abc import x as X_sym
from sympy import symbols, Lambda

from logic.Gauss import GaussInterpolator

class StirlingInterpolator(GaussInterpolator):
    a = None
    name = 'StirlingInterpolator'
    def __init__(self, X: np.array, Y: np.array, a: float = None):
        super().__init__(X, Y)
        # assert self.n % 2 == 1

    #
    # def d_k_y_i(self, i, k=0):
    #     return symbols(f'd^{i}y_{k}')

    def _interpolate(self):
        return (super()._greater_interpolate() + super()._less_interpolate()) / 2

    def do_interpolate(self):
        return Lambda(X_sym, self._interpolate())


if __name__ == '__main__':
    x_list = np.linspace(0.1, 0.5, 5)
    y_list = np.array([1.25, 2.38, 3.79, 5.44, 7.14])
    gauss = GaussInterpolator(x_list, y_list)
    vec_f = np.vectorize(gauss.do_interpolate)

    print(x_list)
    print(y_list)
    print([gauss.do_interpolate()(x) for x in x_list])
