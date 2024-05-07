import numpy as np
from sympy import Lambda

from sympy.abc import x as X_sym


class LagrangeInterpolator():
    name = 'LagrangeInterpolator'
    def __init__(self, X: np.array, Y: np.array):
        self.Y = Y
        self.X = X
        self.n = X.size

    def _interpolate(self):
        n = self.X.size
        res = 0
        for i in range(n):
            part = self.Y[i]

            big_mult = 1
            for j in range(n):
                if i == j:
                    continue
                big_mult *= (X_sym - self.X[j]) / (self.X[i] - self.X[j])
            part *= big_mult

            res += part
        return res

    def do_interpolate(self):
        return Lambda(X_sym, self._interpolate())
