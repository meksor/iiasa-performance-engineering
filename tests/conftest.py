import pytest
from contextlib import contextmanager
import cProfile
import pstats
from pathlib import Path
import polars as pl

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

for size in ["10", "20", "30", "100", "200", "300", "1000"]:
    for v in ["A", "B", "R"]:
        df = pl.read_csv(data / v/  f"{size}.csv")
        MATRICES[v+size] = df

