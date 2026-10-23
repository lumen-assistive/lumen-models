# Contributing to lumen-models

This repository is the licensing and tooling gatekeeper for every model
Lumen bundles. See the organization-wide
[CONTRIBUTING.md](https://github.com/lumen-assistive/.github/blob/main/CONTRIBUTING.md)
for the general workflow. This file only covers what is specific to
this repository.

## Setup

```
python -m venv .venv
.venv/Scripts/activate  # or source .venv/bin/activate on Linux/macOS
pip install -e .[dev]
git config core.hooksPath .githooks
```

## Before sending a pull request

```
ruff check .
ruff format --check .
mypy .
pytest --cov
```

All four must pass; CI runs the same commands on every push and pull
request.

## Adding a new model to the catalog

1. Research the model's current, official license. Do not rely on
   memory or on what another project's README says about it — check
   the model's own license file or terms page.
2. Add or update an entry in `docs/licenses.yaml` with a dated note
   citing what you checked, and set `compatible_with_apache_2_0`
   truthfully (`true`, `false`, or `null` if it genuinely depends on an
   unmade choice, such as which specific voice or checkpoint size).
3. Add the same information in prose to `docs/LICENSES.md`.
4. Only once the license is marked `true`, add the model to
   `src/lumen_models/catalog.py`. `lumen-models check-licenses` and
   `tests/test_license_check.py` will fail the build otherwise.
5. If the model's license conflicts with Apache-2.0 distribution,
   do not add it to the catalog. Document the conflict in
   `docs/LICENSES.md` under "Flagged conflicts" and propose a
   compatible alternative instead.

## Adding a converter or benchmark target

Converters live under `src/lumen_models/convert/`, implementing the
`ModelConverter` interface. Prefer adding a converter only when a
specific plugin module actually needs it, to avoid installing a heavy
ML framework dependency speculatively.
