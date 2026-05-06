from collections import Counter
from time import perf_counter
from typing import Callable, TypeVar


T = TypeVar("T")


class MetricsRegistry:
    def __init__(self) -> None:
        self.counters: Counter[str] = Counter()
        self.timings: dict[str, list[float]] = {}

    def increment(self, name: str, amount: int = 1) -> None:
        self.counters[name] += amount

    def observe(self, name: str, value: float) -> None:
        self.timings.setdefault(name, []).append(value)

    def snapshot(self) -> dict:
        return {
            "counters": dict(self.counters),
            "timings": {
                name: {
                    "count": len(values),
                    "avg": round(sum(values) / len(values), 4) if values else 0,
                    "max": round(max(values), 4) if values else 0,
                }
                for name, values in self.timings.items()
            },
        }


metrics = MetricsRegistry()


def timed(metric_name: str, fn: Callable[..., T], *args, **kwargs) -> T:
    start = perf_counter()
    try:
        return fn(*args, **kwargs)
    finally:
        metrics.observe(metric_name, perf_counter() - start)
