import random


def almost_equal(a, b, decimals=3):
    return round(a, decimals) == round(b, decimals)


def frange(start, stop, step=0.01):
    while start <= stop:
        yield start
        start += step


def fuzz_factor():
    sign = -1 if random.randint(0, 1) else 1
    return 1 + (sign * random.random() * 0.1)  # returns values in [0.9, 1.1]
