from pprint import pprint

import numpy as np
from sympy import Lambda
from sympy.abc import x as X_sym

from logic.Bessel import BesselInterpolator
from logic.Gauss import GaussInterpolator
from logic.GeneralNuton import NutonInterpolator
from logic.Lagrange import LagrangeInterpolator
from logic.Stirling import StirlingInterpolator
from logic.UniformNuton import UniformNutonInterpolator

class_list = [
    LagrangeInterpolator,
    NutonInterpolator,
    UniformNutonInterpolator,
    GaussInterpolator,
    StirlingInterpolator,
    BesselInterpolator
]

names = [i(np.array([1, 2, 3]), np.array([1, 2, 3])).name for i in class_list]
def interpolate(x_list: np.array, y_list: np.array):

    return [c(x_list, y_list).do_interpolate() for c in class_list]


if __name__ == '__main__':
    x = np.linspace(0, 0.5, 2)
    y = np.array([0, 0])

    pprint(interpolate(x, y))
