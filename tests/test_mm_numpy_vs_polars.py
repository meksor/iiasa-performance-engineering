import numpy as np
import polars as pl

def multiply_matrix_python(A, B):
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

def test_nvp_python_mm_polars(benchmark, profiled):
    A = pl.DataFrame(np.random.random((50, 50))) 
    B = pl.DataFrame(np.random.random((50, 50))) 

    with profiled():
        result = multiply_matrix_python(A, B)

    benchmark(multiply_matrix_python, A, B)

def test_nvp_python_mm_numpy(benchmark, profiled):
    A = np.random.random((50, 50))
    B = np.random.random((50, 50))

    with profiled():
        result = multiply_matrix_python(A, B)

    benchmark(multiply_matrix_python, A, B)
