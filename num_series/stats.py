"""Базовые статистики: среднее, медиана, размах."""
from typing import Dict, Sequence
from typing import List, Tuple

def _ensure_not_empty(data: Sequence[float]) -> None:
    """Проверка, что ряд не пуст. Вызывается первой строкой всех функций."""
    if not data:
        raise ValueError("Ряд пуст: расчёт статистики невозможен")


def mean(data: Sequence[float]) -> float:
    """Среднее арифметическое."""
    _ensure_not_empty(data)
    return sum(data) / len(data)


def median(data: Sequence[float]) -> float:
    """Медиана (устойчива к выбросам)."""
    _ensure_not_empty(data)
    s = sorted(data)
    k = len(s) // 2
    if len(s) % 2:  
        return float(s[k])
    return (s[k - 1] + s[k]) / 2.0  


def spread(data: Sequence[float]) -> float:
    """Размах ряда: max - min."""
    _ensure_not_empty(data)
    return float(max(data) - min(data))


def summarize(data: Sequence[float]) -> Dict[str, float]:
    """Сводный отчёт: count, mean, median, spread, min, max."""
    _ensure_not_empty(data)
    return {
        "count": len(data),
        "mean": mean(data),
        "median": median(data),
        "spread": spread(data),
        "min": float(min(data)),
        "max": float(max(data)),
    }

def find_extrema(data: Sequence[float]) -> Tuple[List[int], List[int]]:
    """Находит индексы локальных максимумов и минимумов.
    
    Локальный максимум в точке i: data[i-1] < data[i] > data[i+1].
    Локальный минимум в точке i: data[i-1] > data[i] < data[i+1].
    Крайние точки (0 и n-1) не считаются экстремумами —
    у них нет соседа с одной стороны.
    """
    if len(data) < 3:
        return [], []
    
    maxima: List[int] = []
    minima: List[int] = []
    for i in range(1, len(data) - 1):
        if data[i] > data[i - 1] and data[i] > data[i + 1]:
            maxima.append(i)
        elif data[i] < data[i - 1] and data[i] < data[i + 1]:
            minima.append(i)
    return maxima, minima


def count_extrema(data: Sequence[float]) -> int:
    """Общее число экстремумов (максимумы + минимумы)."""
    maxima, minima = find_extrema(data)
    return len(maxima) + len(minima)