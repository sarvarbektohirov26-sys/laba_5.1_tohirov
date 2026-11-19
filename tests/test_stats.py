import pytest
from num_series.stats import mean, median, spread, summarize


def test_mean():
    assert mean([1, 2, 3]) == 2.0


def test_median_odd_even():
    assert median([3, 1, 2]) == 2.0
    assert median([4, 1, 2, 3]) == 2.5


def test_spread():
    assert spread([1, 5, 2]) == 4.0


def test_empty():
    for f in (mean, median, spread, summarize):
        with pytest.raises(ValueError):
            f([])


def test_summarize_keys():
    s = summarize([1, 2, 3, 4])
    assert set(s) == {"count", "mean", "median", "spread", "min", "max"}