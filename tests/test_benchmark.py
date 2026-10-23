import pytest

from lumen_models.benchmark.runner import (
    BenchmarkResult,
    format_markdown_table,
    run_benchmark,
)


def test_run_benchmark_measures_iterations_and_latency() -> None:
    calls = {"count": 0}

    def inference() -> None:
        calls["count"] += 1

    result = run_benchmark("example", "unit-test-host", inference, iterations=5)

    assert calls["count"] == 5
    assert result.iterations == 5
    assert result.mean_latency_ms >= 0
    assert result.p95_latency_ms >= 0
    assert result.peak_memory_kb >= 0
    assert result.battery_drain_percent is None


def test_run_benchmark_rejects_zero_iterations() -> None:
    with pytest.raises(ValueError):
        run_benchmark("example", "unit-test-host", lambda: None, iterations=0)


def test_format_markdown_table_handles_no_results() -> None:
    table = format_markdown_table([])
    assert "no benchmarks run yet" in table


def test_format_markdown_table_renders_a_result() -> None:
    result = BenchmarkResult(
        model_id="example",
        device_label="unit-test-host",
        iterations=1,
        mean_latency_ms=1.23,
        p95_latency_ms=1.5,
        peak_memory_kb=10,
    )
    table = format_markdown_table([result])
    assert "example" in table
    assert "not measured" in table
