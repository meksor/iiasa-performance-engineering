from multiprocessing.pool import Pool
from multiprocessing.dummy import Pool as ThreadPool
import sys
import numpy as np

import pytest

@pytest.mark.xfail(strict=False)
def test_gil_enabled():
    if sys.version_info == (3, 13):
        assert sys._is_gil_enabled()
    else:
        assert True

def factorial(x):
    acc = 1
    for i in range(x):
        acc = acc * i
    return acc

factorial_inputs = np.random.randint(0, 1000, 1000) 


def test_factorial_st(benchmark):
    def bench():
        results = []
        for args in factorial_inputs:
            results.append(factorial(args))
    
    benchmark(bench)


def test_factorial_mt(benchmark):
    pool = ThreadPool(8)
    def bench():
        return pool.map(factorial, factorial_inputs)
    
    benchmark(bench)

def test_factorial_mp(benchmark):
    pool = Pool(8)
    def bench():
        return pool.map(factorial, factorial_inputs)
    
    benchmark(bench)


np.random.seed(0)
chunks = 8
buffer_size = 4410000 // chunks
buffers = [np.random.random(buffer_size) for x in range(chunks)]
gains = [np.sin(np.arange(0, np.pi * 2, np.pi * 2 / buffer_size)) for x in range(chunks)]

def apply_gain(x):
    buffer, gain = x

    if len(buffer) != len(gain):
        raise ValueError("Gain and input buffer must have the same length.")

    return [b*g for b,g in zip(buffer, gain)]

def test_apply_gain_st(benchmark):
    def bench():
        results = []
        for args in zip(buffers, gains):
            results.append(apply_gain(args))
    
    benchmark(bench)

def test_apply_gain_mt(benchmark):
    pool = ThreadPool(8)
    def bench():
        return pool.map(apply_gain, list(zip(buffers, gains)))
    
    benchmark(bench)

def test_apply_gain_mp(benchmark):
    pool = Pool(8)
    def bench():
        return pool.map(apply_gain, list(zip(buffers, gains)))
    
    benchmark(bench)

