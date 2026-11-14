"""Скользящие средние: SMA, центрированное MA, EMA."""
from typing import List, Sequence


def _check_window(window: int, n: int) -> None:
    """Общая проверка окна для SMA и центрированного MA."""
    if not isinstance(window, int) or isinstance(window, bool):
        raise ValueError(f"window должно быть целым (получено: {window!r})")
    if window < 1:
        raise ValueError(f"window должно быть >= 1 (получено: {window})")
    if window > n:
        raise ValueError(f"window ({window}) > длины ряда ({n})")


def simple_moving_average(data: Sequence[float], window: int) -> List[float]:
    """SMA через бегущую сумму (O(n) вместо O(n*w)).

    Идея: при сдвиге окна на 1 мы не суммируем всё заново,
    а вычитаем ушедший элемент и добавляем пришедший.
    """
    if not data:
        raise ValueError("Ряд пуст")
    _check_window(window, len(data))

    running = sum(data[:window])
    result = [running / window]
    for i in range(window, len(data)):
        running += data[i] - data[i - window]  
        result.append(running / window)
    return result


def centered_moving_average(data: Sequence[float], window: int) -> List[float]:
    """Центрированное MA: окно нечётное, результат выровнен по центру.

    Длина результата = n - window + 1.
    """
    if not data:
        raise ValueError("Ряд пуст")
    if window % 2 == 0:
        raise ValueError(f"window должно быть нечётным (получено: {window})")
    _check_window(window, len(data))

    half = window // 2
    return [
        sum(data[i - half:i + half + 1]) / window
        for i in range(half, len(data) - half)
    ]


def exponential_moving_average(data: Sequence[float], alpha: float) -> List[float]:
    """EMA: EMA[0]=x[0]; EMA[i]=alpha*x[i]+(1-alpha)*EMA[i-1], 0<alpha<=1."""
    if not data:
        raise ValueError("Ряд пуст")
    if not (0 < alpha <= 1):
        raise ValueError(f"alpha должно быть в (0, 1] (получено: {alpha})")

    result = [float(data[0])]
    for i in range(1, len(data)):
        result.append(alpha * data[i] + (1 - alpha) * result[-1])
    return result