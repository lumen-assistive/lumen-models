# Benchmarks

No model has been converted or benchmarked yet, so there is nothing to
report here. This file is generated, not hand-edited: once a real
model exists and has been run through `lumen-models` on actual target
hardware, regenerate this table with:

```
lumen-models render-benchmarks > docs/benchmarks.md
```

(wrapped with whatever header text a future version of that command
adds; see `src/lumen_models/benchmark/runner.py` for the exact table
format). Do not type numbers into this file by hand.

| Model | Device | Iterations | Mean latency (ms) | p95 latency (ms) | Peak memory (KB) | Battery drain (%) |
|---|---|---|---|---|---|---|
| _no benchmarks run yet_ | | | | | | |

Battery drain requires on-device instrumentation (Android Battery
Historian, iOS Instruments) that `lumen-models` does not automate;
it must be measured separately per model and supplied to the harness,
not estimated.
