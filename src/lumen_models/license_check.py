"""Compliance gate: every catalog entry's license must be cleared.

This is the automated half of the project's licensing policy; the
human-readable rationale for each entry lives in docs/LICENSES.md,
kept in sync by hand with docs/licenses.yaml, which this module reads.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .catalog import ModelDescriptor


@dataclass(frozen=True, slots=True)
class LicenseEntry:
    """One row of the license ledger."""

    id: str
    component: str
    spdx: str
    compatible_with_apache_2_0: bool | None
    notes: str


class LicenseComplianceError(Exception):
    """Raised when a catalog entry references an uncleared license."""


def load_licenses(path: Path) -> dict[str, LicenseEntry]:
    """Loads the license ledger at `path` into a lookup by id."""
    raw: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8"))
    entries: dict[str, LicenseEntry] = {}
    for item in raw["licenses"]:
        entry = LicenseEntry(
            id=item["id"],
            component=item["component"],
            spdx=item["spdx"],
            compatible_with_apache_2_0=item["compatible_with_apache_2_0"],
            notes=item["notes"],
        )
        entries[entry.id] = entry
    return entries


def check_catalog_licenses(
    catalog: list[ModelDescriptor],
    licenses: dict[str, LicenseEntry],
) -> None:
    """Raises `LicenseComplianceError` if any entry in `catalog`
    references a license id missing from `licenses`, or one marked as
    not cleared for Apache-2.0 distribution.
    """
    problems: list[str] = []
    for model in catalog:
        entry = licenses.get(model.license_id)
        if entry is None:
            problems.append(
                f'model "{model.id}" references unknown license id "{model.license_id}"'
            )
        elif entry.compatible_with_apache_2_0 is not True:
            problems.append(
                f'model "{model.id}" references license "{entry.id}" '
                "which is not cleared for Apache-2.0 distribution"
            )
    if problems:
        raise LicenseComplianceError("; ".join(problems))
