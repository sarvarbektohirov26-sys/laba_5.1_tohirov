import pytest
from num_series.generator import random_series, sine_series, trend_series


def test_random_length_and_reproducible():
    a = random_series(10, seed=1)
    b = random_series(10, seed=1)
    assert len(a) == 10
    assert a == b  # один seed → один ряд


def test_random_bad_low_high():
    with pytest.raises(ValueError):
        random_series(5, low=5, high=1)


@pytest.mark.parametrize("n", [0, -3])
def test_validate_n(n):
    with pytest.raises(ValueError):
        sine_series(n)


def test_trend_values():
    data = trend_series(5, start=0, step=1, noise=0)
    assert data == [0, 1, 2, 3, 4]