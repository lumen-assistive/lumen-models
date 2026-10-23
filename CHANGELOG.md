# Changelog

All notable changes to this project are documented in this file. The
format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org).

## [Unreleased]

### Added

- `docs/LICENSES.md` and `docs/licenses.yaml`: the model and dataset
  license ledger, researched and verified against each project's
  official current source. Flags three real conflicts (Ultralytics
  YOLO AGPL-3.0, ARASAAC's non-commercial clause, the Piper engine's
  relicensing from MIT to GPL-3.0) with a documented resolution for
  each, and leaves per-voice Piper licensing and the espeak-ng
  phonemization dependency explicitly unresolved pending a specific
  voice choice.
- `lumen_models.catalog`: the `ModelDescriptor`/`ModelTask` schema
  mirroring `lumen_sdk`'s contract. Empty catalog.
- `lumen_models.license_check`: automated compliance gate validating
  every catalog entry's license against the ledger.
- `lumen_models.convert`: `ModelConverter` interface and reference
  `CopyConverter` implementation.
- `lumen_models.benchmark`: `run_benchmark` harness and Markdown table
  formatter; `docs/benchmarks.md` currently empty pending a real model.
- `lumen-models` CLI with `check-licenses` and `render-benchmarks`
  commands.

### Known limitations

- No model has been converted, quantized, or benchmarked yet.
- No per-framework converter (TFLite, ONNX, GGUF) is implemented yet.
- The specific Italian (and any English) Piper voice to bundle has not
  been chosen; its license must be verified per-voice before use.
