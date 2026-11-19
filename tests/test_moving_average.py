import pytest
from num_series.moving_average import (
    simple_moving_average, centered_moving_average, exponential_moving_average,
)


def test_sma_simple():
    assert simple_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]


def test_sma_errors():
    with pytest.raises(ValueError):
        simple_moving_average([1, 2], 3)
    with pytest.raises(ValueError):
        simple_moving_average([], 1)


def test_cma():
    assert centered_moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]
    with pytest.raises(ValueError):
        centered_moving_average([1, 2, 3], 2)


def test_ema():
    res = exponential_moving_average([1, 2, 3], 0.5)
    assert res[0] == 1
    assert res[1] == pytest.approx(1.5)
    assert res[2] == pytest.approx(2.25)
    with pytest.raises(ValueError):
        exponential_moving_average([1, 2], 0)