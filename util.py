
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
