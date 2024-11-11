from .conftest import get_lists
import pytest

def get_middle_item(items: list):
    return items[len(items) // 2]

def sum_items(items: list[int]):
    sum_ = 0
    for item in items:
        sum_ += item
    return sum_

def partition(items: list[int], low: int, high: int):
    pivot = items[high]
    i = low - 1
    for j in range(low, high):
        if items[j] <= pivot:
            i = i + 1
            (items[i], items[j]) = (items[j], items[i])
    (items[i + 1], items[high]) = (items[high], items[i + 1])
    return i + 1

def quick_sort(
    items: list[int], 
    low: int | None = None, 
    high: int | None = None
):
    if low is None or high is None:
        low = 0
        high = len(items) - 1
    
    if low < high:
        pi = partition(items, low, high)
        quick_sort(items, low, pi - 1)
        quick_sort(items, pi + 1, high)




@pytest.mark.parametrize(
    "list_", get_lists(None),
)
def test_tc_get_middle_item(benchmark, list_):
    def bench():
        return get_middle_item(list_)
    result = benchmark(bench)

    assert result == list_[len(list_) // 2]

@pytest.mark.parametrize(
    "list_", get_lists(None),
)
def test_tc_sum_items(benchmark, list_):
    def bench():
        return sum_items(list_)
    result = benchmark(bench)

    assert result == sum(list_)

@pytest.mark.parametrize(
    "list_", get_lists(None),
)
def test_tc_sum_builtin(benchmark, list_):
    def bench():
        return sum(list_)
    result = benchmark(bench)

    assert result == sum(list_)

@pytest.mark.parametrize(
    "list_", get_lists(None),
)
def test_tc_quick_sort(benchmark, list_):
    # need to copy the list since qs sorts in place
    subject = list_.copy()
    def bench():
        return quick_sort(subject)
    benchmark(bench)

    assert subject == sorted(list_)

@pytest.mark.parametrize(
    "list_", get_lists(None),
)
def test_tc_sorted_builtin(benchmark, list_):
    def bench():
        return sorted(list_)
    result = benchmark(bench)

    assert result == sorted(list_)
