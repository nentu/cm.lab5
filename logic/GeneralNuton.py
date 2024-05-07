import numpy as np
from sympy.abc import x as X_sym
from sympy import Lambda



class NutonInterpolator:
    name = 'NutonInterpolator'
    def __init__(self, X: np.array, Y: np.array):
        self.Y = Y
        self.X = X
        self.n = X.size

    def f(self, x_0):
        return self.Y[np.where(self.X == x_0)][0]

    def dd(self, x_list):  # Divided differences
        if len(x_list) == 1:
            return self.f(x_list[0])

        return (self.dd(x_list[1:]) - self.dd(x_list[:-1])) / (x_list[-1] - x_list[0])

    def _interpolate(self):
        res = 0

        for k in range(self.n):
            part = 1
            for j in range(k):
                part *= X_sym - self.X[j]

            part *= self.dd(self.X[:k + 1])

            res += part

        return res

    def do_interpolate(self):
        return Lambda(X_sym, self._interpolate())

