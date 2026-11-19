"""Визуализация рядов и скользящих средних (для варианта 11)."""
from __future__ import annotations

from typing import Dict, List, Sequence

try:
    import matplotlib
    matplotlib.use("Agg")  # headless-режим: работает и без GUI
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


def plot_smoothing_comparison(
    data: Sequence[float],
    windows: List[int],
    sma_results: Dict[int, List[float]],
    ema_results: Dict[int, List[float]],
    output_path: str = "smoothing_comparison.png",
) -> None:
    """Строит 3 графика (по одному на каждое окно): исходный ряд + SMA + EMA."""
    if not HAS_MPL:
        raise RuntimeError(
            "Для построения графиков установите matplotlib: pip install matplotlib"
        )

    fig, axes = plt.subplots(len(windows), 1, figsize=(12, 4 * len(windows)))
    if len(windows) == 1:
        axes = [axes]

    n = len(data)
    x_full = list(range(n))

    for ax, k in zip(axes, windows):
        sma = sma_results[k]
        ema = ema_results[k]
        # SMA/EMA короче исходного ряда: у SMA длина n - k + 1,
        # у EMA — n (совпадает). Чтобы наложить на графике корректно,
        # SMA сдвигаем вправо на k-1 (индекс последнего элемента окна).
        x_sma = list(range(k - 1, n))
        x_ema = list(range(n))

        ax.plot(x_full, data, color="lightgray", linewidth=0.8, label="Исходный ряд")
        ax.plot(x_sma, sma, color="blue", linewidth=1.5, label=f"SMA (k={k})")
        ax.plot(x_ema, ema, color="red", linewidth=1.5, label=f"EMA (k={k})")
        ax.set_title(f"Сглаживание при k = {k}")
        ax.set_xlabel("Индекс i")
        ax.set_ylabel("Значение")
        ax.legend(loc="upper right")
        ax.grid(True, alpha=0.3)

    fig.suptitle("Сравнение сглаживающих свойств SMA и EMA (Вариант 11)", fontsize=14)
    fig.tight_layout()
    fig.savefig(output_path, dpi=120)
    plt.close(fig)
    print(f"[график сохранён] {output_path}")