"""Пакет алгоритмической обработки числовых рядов."""
from .generator import (
    random_series, sine_series, trend_series, two_harmonics_series,
)
from .stats import (
    mean, median, spread, summarize,
    find_extrema, count_extrema,
)
from .moving_average import (
    simple_moving_average, centered_moving_average,
    exponential_moving_average,
    simple_moving_average_deque, benchmark_moving_average,
)
from .deque_average import (
    simple_moving_average_deque as simple_moving_average_deque_v2,
    centered_moving_average_deque,
    exponential_moving_average_deque,
)
from .io_json import save_series_json, load_series_json
from .io_file import load_series_txt, load_series_csv, load_series_auto

__all__ = [
    # генерация
    "random_series", "sine_series", "trend_series", "two_harmonics_series",
    # статистика
    "mean", "median", "spread", "summarize",
    "find_extrema", "count_extrema",
    # скользящие средние
    "simple_moving_average", "centered_moving_average",
    "exponential_moving_average",
    "simple_moving_average_deque", "benchmark_moving_average",
    "simple_moving_average_deque_v2",
    "centered_moving_average_deque",
    "exponential_moving_average_deque",
    # I/O
    "save_series_json", "load_series_json",
    "load_series_txt", "load_series_csv", "load_series_auto",
]
__version__ = "1.2.0"