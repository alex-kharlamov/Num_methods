import numpy as np

from diff_solver_module import runge_kutta
from integral_module import integral_count
from interpolation_module import SplineInterpolator
from interpolation_module import tabulate_fun, tabulate_int


def getXY(beta, x0, y0, T, spline_z, spline_p_int, spline_s):
    def f(t, x, y):
        tmp1 = spline_z.grad(np.array([t]))
        tmp2 = spline_p_int.predict(np.array([y]))

        return tmp1 * tmp2

    def g(t, x, y):
        return functionFBeta(beta, t, x, spline_s)

    tempx, tempy = runge_kutta(T, 100, x0, y0, f, g)

    t_grid = np.linspace(0, T, num=100)

    sol_x = SplineInterpolator()
    sol_x.fit(t_grid, tempx)
    sol_y = SplineInterpolator()
    sol_y.fit(t_grid, tempy)

    return sol_x, sol_y


def functionFBeta(beta, t, x, spline_s):
    tmp = spline_s.predict(t)
    return beta * (tmp - x)


def C1(x, y, x0, y0, T, spline_p):
    t_grid = np.linspace(0, T, 100)
    y_grid = np.vectorize(y.predict)(t_grid)
    dx_grid = np.vectorize(x.grad)(t_grid)
    int_grid = []
    f = lambda w: w * np.vectorize(spline_p.predict)(w)
    for _y in y_grid:
        w_grid = np.linspace(_y, 1, 100)
        int_grid.append(integral_count(w_grid, f(w_grid)))

    agg = integral_count(t_grid, dx_grid * np.array(int_grid))
    ans = 1 - agg / (x.predict(T) - x0)
    return ans[0]


def C2(x, S, T):
    ans = abs(x.predict(T) - S.predict(T)) / S.predict(T)
    return ans[0]


def solve(x0, y0, T, A, B, pw, S, Z, beta_from, beta_n, mode=True, beta_to=None):
    px, py = tabulate_fun(pw, T)
    sx, sy = tabulate_fun(S, T)
    zx, zy = tabulate_fun(Z, T)
    p_int_x, p_int_y = tabulate_int(px, py)

    spline_p = SplineInterpolator()
    spline_p.fit(px, py)
    spline_s = SplineInterpolator()
    spline_s.fit(sx, sy)
    spline_z = SplineInterpolator()
    spline_z.fit(zx, zy)
    spline_p_int = SplineInterpolator()
    spline_p_int.fit(p_int_x, p_int_y)

    if mode:
        beta_search = np.linspace(beta_from, beta_to, beta_n)
    else:
        beta_search = np.array([beta_from])

    fun_val = []
    for beta in beta_search:
        sol_x, sol_y = getXY(beta, x0, y0, T, spline_z, spline_p_int, spline_s)
        fun_val.append(A * C1(sol_x, sol_y, x0, y0, T, spline_p) + B * C2(sol_x, spline_s, T))

    fun_val = np.array(fun_val)
    fun_val = np.nan_to_num(fun_val)
    beta_opt = beta_search[np.argmin(np.array(fun_val))]
    sol_x, sol_y = getXY(beta_opt, x0, y0, T, spline_z, spline_p_int, spline_s)

    c1_opt = C1(sol_x, sol_y, x0, y0, T, spline_p)
    c2_opt = C2(sol_x, spline_s, T)
    return beta_opt, sol_x, sol_y, c1_opt, c2_opt
