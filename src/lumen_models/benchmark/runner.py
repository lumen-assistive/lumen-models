"""On-device benchmark harness.

Measures wall-clock latency and this process's peak memory for a
caller-supplied inference callable. Battery drain requires on-device
instrumentation (Android Battery Historian, iOS Instruments) that is
not available in this environment; `battery_drain_percent` stays
`None` unless a caller supplies a real measurement obtained from such
a tool.
"""

from __future__ import annotations

import statistics
import time
import tracemalloc
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    """One benchmark run's measurements for a single model."""

    model_id: str
    device_label: str
    iterations: int
    mean_latency_ms: float
    p95_latency_ms: float
    peak_memory_kb: int
    battery_drain_percent: float | None = None


def run_benchmark(
    model_id: str,
    device_label: str,
    inference: Callable[[], None],
    iterations: int = 20,
) -> BenchmarkResult:
    """Times `inference` over `iterations` calls and reports latency and
    this process's peak memory use.
    """
    if iterations < 1:
        raise ValueError("iterations must be at least 1")

    latencies_ms: list[float] = []
    tracemalloc.start()
    try:
        for _ in range(iterations):
            start = time.perf_counter()
            inference()
            latencies_ms.append((time.perf_counter() - start) * 1000)
        _, peak_bytes = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    latencies_ms.sort()
    p95_index = max(0, round(0.95 * (len(latencies_ms) - 1)))
    return BenchmarkResult(
        model_id=model_id,
        device_label=device_label,
        iterations=iterations,
        mean_latency_ms=statistics.fmean(latencies_ms),
        p95_latency_ms=latencies_ms[p95_index],
        peak_memory_kb=peak_bytes // 1024,
        battery_drain_percent=None,
    )


def format_markdown_table(results: list[BenchmarkResult]) -> str:
    """Renders `results` as a Markdown table, or a placeholder row when
    empty.
    """
    header = (
        "| Model | Device | Iterations | Mean latency (ms) | "
        "p95 latency (ms) | Peak memory (KB) | Battery drain (%) |"
    )
    separator = "|---|---|---|---|---|---|---|"
    if not results:
        return f"{header}\n{separator}\n| _no benchmarks run yet_ | | | | | | |"

    rows = [header, separator]
    for result in results:
        battery = (
            f"{result.battery_drain_percent:.1f}"
            if result.battery_drain_percent is not None
            else "not measured"
        )
        rows.append(
            f"| {result.model_id} | {result.device_label} | "
            f"{result.iterations} | {result.mean_latency_ms:.2f} | "
            f"{result.p95_latency_ms:.2f} | {result.peak_memory_kb} | "
            f"{battery} |"
        )
    return "\n".join(rows)
