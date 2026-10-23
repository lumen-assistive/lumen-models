"""Command-line entry point for lumen-models."""

from __future__ import annotations

import argparse
from pathlib import Path

from .benchmark.runner import format_markdown_table
from .catalog import CATALOG
from .license_check import check_catalog_licenses, load_licenses

_REPO_ROOT = Path(__file__).resolve().parents[2]
_LICENSES_PATH = _REPO_ROOT / "docs" / "licenses.yaml"


def _check_licenses() -> int:
    licenses = load_licenses(_LICENSES_PATH)
    check_catalog_licenses(CATALOG, licenses)
    print(f"All {len(CATALOG)} catalog entries have a cleared license.")
    return 0


def _render_empty_benchmarks() -> int:
    print(format_markdown_table([]))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="lumen-models")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser(
        "check-licenses",
        help="Verify every catalog entry's license is cleared.",
    )
    subparsers.add_parser(
        "render-benchmarks",
        help="Print the current (possibly empty) benchmark table.",
    )
    args = parser.parse_args(argv)

    if args.command == "check-licenses":
        return _check_licenses()
    if args.command == "render-benchmarks":
        return _render_empty_benchmarks()
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
