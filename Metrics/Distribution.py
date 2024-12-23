import numpy as np
from numba import prange
from numba import njit

@njit
def calc_skew(min_periods, nobs, x, xx, xxx, num_consecutive_same_value):
    if nobs >= min_periods:
        dnobs = float(nobs)
        a = x / dnobs
        b = xx / dnobs - a * a
        c = xxx / dnobs - a * a * a - 3 * a * b

        if nobs < 3:
            return np.nan
        elif num_consecutive_same_value >= nobs:
            return 0.0
        elif b <= 1e-14:
            return np.nan
        else:
            r = np.sqrt(b)
            return (np.sqrt(dnobs * (dnobs - 1.)) * c) / ((dnobs - 2) * r * r * r)
    else:
        return np.nan


@njit
def add_skew(val, nobs, x, xx, xxx, compensation_x, compensation_xx, compensation_xxx,
            num_consecutive_same_value, prev_value):
    if val == val:
        nobs += 1

        y = val - compensation_x
        t = x + y
        compensation_x = t - x - y
        x = t

        y = val * val - compensation_xx
        t = xx + y
        compensation_xx = t - xx - y
        xx = t

        y = val * val * val - compensation_xxx
        t = xxx + y
        compensation_xxx = t - xxx - y
        xxx = t

        if val == prev_value:
            num_consecutive_same_value += 1
        else:
            num_consecutive_same_value = 1
        prev_value = val

    return nobs, x, xx, xxx, compensation_x, compensation_xx, compensation_xxx, num_consecutive_same_value, prev_value


@njit
def remove_skew(val, nobs, x, xx, xxx, compensation_x, compensation_xx, compensation_xxx):
    if val == val:
        nobs -= 1

        y = -val - compensation_x
        t = x + y
        compensation_x = t - x - y
        x = t

        y = -val * val - compensation_xx
        t = xx + y
        compensation_xx = t - xx - y
        xx = t

        y = -val * val * val - compensation_xxx
        t = xxx + y
        compensation_xxx = t - xxx - y
        xxx = t

    return nobs, x, xx, xxx, compensation_x, compensation_xx, compensation_xxx


@njit
def rolling_skewness(array, length, min_length):
    N, M = array.shape
    output = np.empty((N, M), dtype=np.float64)
    output[:] = np.nan

    for col in prange(M):
        nobs, x, xx, xxx = 0, 0.0, 0.0, 0.0
        compensation_x, compensation_xx, compensation_xxx = 0.0, 0.0, 0.0
        prev_value = array[0, col]
        num_consecutive_same_value = 0

        for i in range(N):
            start = max(0, i - length + 1)
            end = i + 1

            if i == 0 or start >= i - 1:
                nobs, x, xx, xxx = 0, 0.0, 0.0, 0.0
                compensation_x, compensation_xx, compensation_xxx = 0.0, 0.0, 0.0
                prev_value = array[start, col]
                num_consecutive_same_value = 0
                for j in range(start, end):
                    nobs, x, xx, xxx, compensation_x, compensation_xx, compensation_xxx, num_consecutive_same_value, prev_value = \
                        add_skew(array[j, col], nobs, x, xx, xxx, compensation_x, compensation_xx, compensation_xxx, num_consecutive_same_value, prev_value)
            else:
                for j in range(max(0, i - length), start):
                    nobs, x, xx, xxx, compensation_x, compensation_xx, compensation_xxx = \
                        remove_skew(array[j, col], nobs, x, xx, xxx, compensation_x, compensation_xx, compensation_xxx)

                nobs, x, xx, xxx, compensation_x, compensation_xx, compensation_xxx, num_consecutive_same_value, prev_value = \
                    add_skew(array[i, col], nobs, x, xx, xxx, compensation_x, compensation_xx, compensation_xxx, num_consecutive_same_value, prev_value)

            output[i, col] = calc_skew(min_length, nobs, x, xx, xxx, num_consecutive_same_value)

    return output
    


@njit
def calc_kurt(min_periods, nobs, x, xx, xxx, xxxx, num_consecutive_same_value):
    if nobs >= min_periods:
        if nobs < 4:
            return np.nan
        elif num_consecutive_same_value >= nobs:
            return -3.0
        else:
            dnobs = float(nobs)
            A = x / dnobs
            R = A * A
            B = xx / dnobs - R
            R = R * A
            C = xxx / dnobs - R - 3 * A * B
            R = R * A
            D = xxxx / dnobs - R - 6 * B * A * A - 4 * C * A

            if B <= 1e-14:
                return np.nan
            else:
                K = (dnobs * dnobs - 1.) * D / (B * B) - 3 * ((dnobs - 1.) ** 2)
                return K / ((dnobs - 2.) * (dnobs - 3.))
    else:
        return np.nan


@njit
def add_kurt(val, nobs, x, xx, xxx, xxxx, compensation_x, compensation_xx, compensation_xxx, compensation_xxxx,
            num_consecutive_same_value, prev_value):
    if val == val:
        nobs += 1

        y = val - compensation_x
        t = x + y
        compensation_x = t - x - y
        x = t

        y = val * val - compensation_xx
        t = xx + y
        compensation_xx = t - xx - y
        xx = t

        y = val * val * val - compensation_xxx
        t = xxx + y
        compensation_xxx = t - xxx - y
        xxx = t

        y = val * val * val * val - compensation_xxxx
        t = xxxx + y
        compensation_xxxx = t - xxxx - y
        xxxx = t

        if val == prev_value:
            num_consecutive_same_value += 1
        else:
            num_consecutive_same_value = 1
        prev_value = val

    return nobs, x, xx, xxx, xxxx, compensation_x, compensation_xx, compensation_xxx, compensation_xxxx, num_consecutive_same_value, prev_value


@njit
def remove_kurt(val, nobs, x, xx, xxx, xxxx, compensation_x, compensation_xx, compensation_xxx, compensation_xxxx):
    if val == val:
        nobs -= 1

        y = -val - compensation_x
        t = x + y
        compensation_x = t - x - y
        x = t

        y = -val * val - compensation_xx
        t = xx + y
        compensation_xx = t - xx - y
        xx = t

        y = -val * val * val - compensation_xxx
        t = xxx + y
        compensation_xxx = t - xxx - y
        xxx = t

        y = -val * val * val * val - compensation_xxxx
        t = xxxx + y
        compensation_xxxx = t - xxxx - y
        xxxx = t

    return nobs, x, xx, xxx, xxxx, compensation_x, compensation_xx, compensation_xxx, compensation_xxxx

@njit
def rolling_kurtosis(array, length, min_length):
    N, M = array.shape
    output = np.empty((N, M), dtype=np.float64)
    output[:] = np.nan

    for col in prange(M):
        nobs, x, xx, xxx, xxxx = 0, 0.0, 0.0, 0.0, 0.0
        compensation_x, compensation_xx, compensation_xxx, compensation_xxxx = 0.0, 0.0, 0.0, 0.0
        prev_value = array[0, col]
        num_consecutive_same_value = 0

        for i in range(N):
            start = max(0, i - length + 1)
            end = i + 1

            if i == 0 or start >= i - 1:
                nobs, x, xx, xxx, xxxx = 0, 0.0, 0.0, 0.0, 0.0
                compensation_x, compensation_xx, compensation_xxx, compensation_xxxx = 0.0, 0.0, 0.0, 0.0
                prev_value = array[start, col]
                num_consecutive_same_value = 0
                for j in range(start, end):
                    nobs, x, xx, xxx, xxxx, compensation_x, compensation_xx, compensation_xxx, compensation_xxxx, \
                    num_consecutive_same_value, prev_value = \
                        add_kurt(array[j, col], nobs, x, xx, xxx, xxxx, compensation_x, compensation_xx,
                                    compensation_xxx, compensation_xxxx, num_consecutive_same_value, prev_value)
            else:
                for j in range(max(0, i - length), start):
                    nobs, x, xx, xxx, xxxx, compensation_x, compensation_xx, compensation_xxx, compensation_xxxx = \
                        remove_kurt(array[j, col], nobs, x, xx, xxx, xxxx, compensation_x, compensation_xx,
                                    compensation_xxx, compensation_xxxx)

                nobs, x, xx, xxx, xxxx, compensation_x, compensation_xx, compensation_xxx, compensation_xxxx, \
                num_consecutive_same_value, prev_value = \
                    add_kurt(array[i, col], nobs, x, xx, xxx, xxxx, compensation_x, compensation_xx,
                                compensation_xxx, compensation_xxxx, num_consecutive_same_value, prev_value)

            output[i, col] = calc_kurt(min_length, nobs, x, xx, xxx, xxxx, num_consecutive_same_value)

    return output