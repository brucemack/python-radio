import math

standard_vals = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
standard_mags = [1, 10, 100, 1000, 10000, 1000000]


def parallel_r(a, b):
    return 1.0 / (1.0 / a + 1.0 / b)


def get_standard_resistors():
    result = []
    for mag in standard_mags:
        for val in standard_vals:
            result.append(val * mag)
    return result


def get_standard_resistors_in_range(min, max):
    result = []
    for mag in standard_mags:
        for val in standard_vals:
            r = val * mag
            if r >= min & r <= max:
                result.append(val * mag)
    return result


def standardize_resistor(target_r):
    last_r = 0
    rs = get_standard_resistors()
    for r in rs:
        # Look for when we go past
        if r > target_r:
            error_0 = math.fabs(target_r - last_r)
            error_1 = math.fabs(target_r - r)
            if error_0 < error_1:
                return last_r
            else:
                return r
        last_r = r
    raise Exception("Range error")