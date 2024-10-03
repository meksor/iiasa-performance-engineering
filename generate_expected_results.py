from tests.conftest import MATRICES
import polars as pl
import numpy as np

for size in ["10", "20", "30"]:
    A = MATRICES["A"+size]
    B = MATRICES["B"+size]
    R = pl.from_numpy(np.dot(A, B))
    R.write_csv(f"{size}.csv")
