

import numpy as np
import polars as pl

np.random.seed(1)

# 1e5 gives:
# Unable to allocate 74.5 GiB for an array with shape (100000, 100000) and data type float64
for size in np.array([10, 20, 30], dtype=int):
    df = pl.DataFrame(np.random.random((size, size))) 
    df.write_csv(f"{size}.csv")
