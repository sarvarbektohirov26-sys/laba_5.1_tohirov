"""Точка входа: обработка числовых рядов через CLI."""
from __future__ import annotations

import argparse
import csv
import sys
from typing import List, Optional, Tuple

from num_series import (
    random_series, sine_series, trend_series, two_harmonics_series,
    summarize, find_extrema, count_extrema,
    simple_moving_average, centered_moving_average,
    exponential_moving_average,
    benchmark_moving_average,
    save_series_json, load_series_auto,
)


def build_series(kind: str, n: int, seed: int) -> List[float]:
    """Фабрика ряда."""
    if kind == "random":
        return random_series(n, low=-50, high=50, seed=seed)
    if kind == "sine":
        return sine_series(n, amplitude=10, frequency=2, noise=1.5, seed=seed)
    if kind == "trend":
        return trend_series(n, start=0, step=1.0, noise=0.5, seed=seed)
    if kind == "two_harmonics":
        return two_harmonics_series(n, noise=0.2, seed=seed)
    raise ValueError(f"Неизвестный тип ряда: {kind!r}")


def obtain_series(args: argparse.Namespace) -> Tuple[List[float], str]:
    """Возвращает (ряд, описание источника)."""
    if args.load:
        data = load_series_auto(args.load)
        return data, f"файл: {args.load}"
    data = build_series(args.kind, args.n, args.seed)
    return data, f"сгенерирован ({args.kind}, n={args.n}, seed={args.seed})"


def export_series_csv(path: str, data: List[float]) -> None:
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["i", "value"])
            for i, v in enumerate(data):
                w.writerow([i, v])
    except OSError as err:
        raise ValueError(f"Не удалось записать CSV {path}: {err}") from err


def print_series(title: str, values: List[float], fmt: str = "{:>10.3f}") -> None:
    print(f"\n{title} (n={len(values)}):")
    print(" " + " ".join(fmt.format(v) for v in values))


def print_header(source: str) -> None:
    print("=" * 60)
    print(f"Источник данных: {source}")
    print("-" * 60)


def print_stats(stats: dict) -> None:
    print(f"Среднее арифметическое : {stats['mean']:>10.4f}")
    print(f"Медиана                : {stats['median']:>10.4f}")
    print(f"Размах (max - min)     : {stats['spread']:>10.4f}")
    print(f"min / max              : {stats['min']:>10.4f} / {stats['max']:.4f}")


def print_footer() -> None:
    print("=" * 60)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Алгоритмическая обработка числовых рядов",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
   
    parser.add_argument(
        "--kind",
        choices=["random", "sine", "trend", "two_harmonics"],
        default="sine",
        help="тип генерируемого ряда",
    )
    parser.add_argument("--n", type=int, default=20, help="количество точек")
    parser.add_argument("--seed", type=int, default=42, help="зерно ГПСЧ")
    parser.add_argument(
        "--load", metavar="PATH",
        help="загрузить ряд из файла (.json/.txt/.csv)",
    )
   
    parser.add_argument("--save", metavar="PATH", help="сохранить ряд в JSON")
    parser.add_argument("--export", metavar="FILE", help="экспорт ряда в CSV (i, value)")
    # анализ
    parser.add_argument("--window", type=int, default=3, help="окно SMA по умолчанию")
    parser.add_argument("--alpha", type=float, default=0.3, help="alpha для EMA")
    parser.add_argument(
        "--window-values", type=int, nargs="+", default=[5, 25, 75],
        help="окна для сравнения сглаживания (вариант 11)",
    )
    parser.add_argument(
        "--benchmark", action="store_true",
        help="замерить время SMA: list vs deque",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    
    try:
        data, source = obtain_series(args)
    except ValueError as err:
        print(f"Ошибка получения ряда: {err}", file=sys.stderr)
        return 1


    if args.save:
        meta = {"source": source}
        if not args.load:
            meta.update({"kind": args.kind, "seed": args.seed})
        try:
            save_series_json(data, args.save, meta=meta)
            print(f"[сохранено] {args.save} ({len(data)} точек)")
        except ValueError as err:
            print(f"Ошибка сохранения: {err}", file=sys.stderr)
            return 1

    if args.export:
        try:
            export_series_csv(args.export, data)
            print(f"[экспортировано] {args.export} ({len(data)} точек)")
        except ValueError as err:
            print(f"Ошибка экспорта: {err}", file=sys.stderr)
            return 1

    
    try:
        stats = summarize(data)
        sma = simple_moving_average(data, args.window)
        ema = exponential_moving_average(data, args.alpha)
        cma = (
            centered_moving_average(data, args.window)
            if args.window % 2 == 1 else None
        )
    except ValueError as err:
        print(f"Ошибка анализа: {err}", file=sys.stderr)
        return 1

    print_header(source)
    print_stats(stats)
    print_series("Исходный ряд", data)
    print_series(f"SMA (window={args.window})", sma)
    print_series(f"EMA (alpha={args.alpha})", ema)
    if cma is not None:
        print_series(f"Центрированное MA (window={args.window})", cma)

    # 4. Вариант 11
    if args.kind == "two_harmonics":
        maxima, minima = find_extrema(data)
        print("-" * 60)
        print(
            f"Экстремумы: {len(maxima) + len(minima)} "
            f"(максимумов: {len(maxima)}, минимумов: {len(minima)})"
        )

        print("-" * 60)
        print("Сравнение сглаживания (SMA vs EMA):")
        for k in args.window_values:
            if k > len(data):
                print(f"  [WARN] k={k} > n={len(data)}: пропускаем SMA")
                continue
            if k >= len(data) // 2:
                print(f"  [WARN] k={k} велико: сильное сглаживание, форма теряется")

            sma_k = simple_moving_average(data, k)
            alpha_k = 2.0 / (k + 1)
            ema_k = exponential_moving_average(data, alpha_k)
            print(f"  k={k:>3}: α = 2/(k+1) = {alpha_k:.4f}, "
                  f"SMA len = {len(sma_k)}, EMA len = {len(ema_k)}")

    # 5. Бенчмарк
    if args.benchmark:
        print("-" * 60)
        print("Замер времени SMA (list vs deque, среднее за 1000 повторов):")
        try:
            timings = benchmark_moving_average(data, args.window, repeats=1000)
            print(f"  list : {timings['list']:.8f} c")
            print(f"  deque: {timings['deque']:.8f} c")
            print(f"  отношение(list/deque): {timings['list'] / timings['deque']:.2f}")
        except ValueError as err:
            print(f"  [benchmark] {err}", file=sys.stderr)

    print_footer()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())