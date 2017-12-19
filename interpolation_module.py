import numpy as np

from integral_module import integral_count


def tabulate_fun(fun, T):
    data = np.linspace(0, T, 100)
    y = []

    for elem in data:
        if 'w' in fun:
            w = elem
        else:
            t = elem
        ans = eval(fun)
        y.append(ans)
    return data, np.array(y)


def tabulate_int(x, y):
    ans = []
    for i in range(len(y)):
        ans.append(integral_count(y[i:], x[i:]))
    return x, np.array(y)


class SplineInterpolator():
    def __init__(self):
        self.first = 0
        self.latest = 0
        self.coefs = []
        self.X = 0

    def fit(self, X, Y):
        self.X = X
        self.first = Y[0]
        self.latest = Y[-1]
        n = len(X)
        a = Y
        b = np.zeros((n + 1))
        c = np.zeros((n + 1))
        d = np.zeros((n + 1))
        h = np.diff(X)
        denom = np.zeros((n + 1))
        alpha = np.zeros((n + 1))
        beta = np.zeros((n + 1))
        denom[0] = 1

        for i in range(1, n - 1):
            ans = 3 / h[i] * (a[i + 1] - a[i]) - 3 / h[i - 1] * (a[i] - a[i - 1])
            denom[i] = 2 * (X[i + 1] - X[i - 1]) - h[i - 1] * alpha[i - 1]
            alpha[i] = h[i] / denom[i]
            beta[i] = (ans - h[i - 1] * beta[i - 1]) / denom[i]

        for i in reversed(range(n - 1)):
            c[i] = beta[i] - alpha[i] * c[i + 1]
            b[i] = (a[i + 1] - a[i]) / h[i] - (h[i] * (c[i + 1] + 2 * c[i])) / 3
            d[i] = (c[i + 1] - c[i]) / (3 * h[i])

        for i in range(n - 1):
            self.coefs.append([a[i], b[i], c[i], d[i]])

    def predict(self, X):
        if type(X) != type(np.array([])):
            X = np.array([X])
        ans = np.zeros((len(X)))
        for pred_ind, elem in enumerate(X):
            cur_ind = np.searchsorted(self.X, elem, side='right') - 1
            if cur_ind == len(self.X) - 1:
                cur_ind -= 1
            a, b, c, d = self.coefs[cur_ind]
            x = self.X[cur_ind]
            ans[pred_ind] = a + b * (elem - x) + c * ((elem - x) ** 2) + d * ((elem - x) ** 3)
            if elem == self.X[0]:
                ans[pred_ind] = self.first
            if elem == self.X[-1]:
                ans[pred_ind] = self.latest
        if len(ans) == 0:
            return ans[0]
        return ans

    def grad(self, X):
        if type(X) != type(np.array([])):
            X = np.array([X])
        ans = np.zeros((len(X)))
        for pred_ind, elem in enumerate(X):
            cur_ind = np.searchsorted(self.X, elem, side='right') - 1
            if cur_ind == len(self.X) - 1:
                cur_ind -= 1
            a, b, c, d = self.coefs[cur_ind]
            x = self.X[cur_ind]
            ans[pred_ind] = b + 2 * c * (elem - x) + 3 * d * (elem - x) ** 2
            if elem == self.X[0]:
                ans[pred_ind] = self.first
            if elem == self.X[-1]:
                ans[pred_ind] = self.latest
        if len(ans) == 0:
            return ans[0]
        return ans
