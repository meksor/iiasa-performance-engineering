import pytest
from contextlib import contextmanager
import cProfile
import pstats
from pathlib import Path
import polars as pl
import numpy as np
import sys

sys.setrecursionlimit(3000)
data = Path(__file__).parent / "data"

@pytest.fixture(scope="function")
def profiled(request):
    """Use this fixture for profiling tests:
    ```
    def test(profiled):
        # setup() ...
        with profiled():
            complex_procedure()
        # teardown() ...
    ```
    Profiler output will be written to '.profiles/{testname}.prof'
    """

    testname = request.node.name
    pr = cProfile.Profile()

    @contextmanager
    def profiled():
        pr.enable()
        yield
        pr.disable()

    yield profiled
    ps = pstats.Stats(pr)
    Path(".profiles").mkdir(parents=True, exist_ok=True)
    ps.dump_stats(f".profiles/{testname}.prof")

MATRICES = {}

for msize in ["10", "20", "30", "40", "50", "100", "200", "300", "1000"]:
    for v in ["A", "B", "R"]:
        df = pl.read_csv(data / v/  f"{msize}.csv")
        MATRICES[v+msize] = df.to_numpy()

LISTS = {}

np.random.seed(1)
for lsize in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]: # , 1100, 1200, 1300, 1400, 1500]:
    LISTS[lsize] = np.random.randint(0, 1000, lsize).tolist()

def get_lists(sizes: list[int] | None):
    if sizes is None:
        return LISTS.values()
    lists = []
    for k, v in LISTS.items():
        if k in sizes:
            lists.append(v.copy()) 
