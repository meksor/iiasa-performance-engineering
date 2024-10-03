import pytest
from .conftest import MATRICES
import numpy as np
import numpy.typing as npt
import numpy.testing as nptest


def multiply_matrix_python(A: npt.NDArray, B: npt.NDArray):
    a_rows, a_cols = A.shape
    b_rows, b_cols = B.shape

    if a_rows != b_rows or a_cols != b_cols:
        return False
    result = np.zeros((a_rows, b_cols))
    for row in range(a_rows):
        for col in range(b_cols):
            for elt in range(a_rows):
                result[row, col] = result[row, col] + A[row, elt] * B[elt, col]
    return result


def test_python_too_fast(benchmark, profiled):
    with profiled():
        # turn off running the benchmark multiple times
        benchmark.pedantic(
            lambda: multiply_matrix_python(MATRICES["A10"], MATRICES["B10"]),
            iterations=1,
            rounds=1,
        )


@pytest.mark.parametrize(
    "A,B,R",
    [
        (MATRICES["A10"], MATRICES["B10"], MATRICES["R10"]),
        (MATRICES["A20"], MATRICES["B20"], MATRICES["R20"]),
        (MATRICES["A30"], MATRICES["B30"], MATRICES["R30"])
    ],
)
def test_python_mm(benchmark, profiled, A, B, R):
    with profiled():
        def bench():
            return multiply_matrix_python(A, B)
        result = benchmark(bench)

    nptest.assert_allclose(result, R)
