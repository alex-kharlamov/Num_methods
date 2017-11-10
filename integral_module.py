import numpy as np
import types
from math import *


def count_integral(y, x=None, a=None, b=None, n=None):
    if n:
        assert n >= 1 and int(n) == n

    def count_with_grid(y, x):
        cumsum = (y[:-1] + y[1:]) / 2
        grid_dif = np.diff(x)
        return np.dot(cumsum, grid_dif)

    if type(y) != types.FunctionType and type(y) != types.BuiltinFunctionType:
        assert type(y) == type(np.array([])) and type(x) == type(np.array([]))
        return count_with_grid(y, x)
    else:
        x_array = np.arange(a, b, (b - a) / n)
        y_array = np.array([y(elem) for elem in x_array])
        return count_with_grid(y_array, x_array)