from pathlib import Path

import pytest

from lumen_models.catalog import CATALOG, ModelDescriptor, ModelTask
from lumen_models.license_check import (
    LicenseComplianceError,
    LicenseEntry,
    check_catalog_licenses,
    load_licenses,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_REAL_LICENSES_PATH = _REPO_ROOT / "docs" / "licenses.yaml"


def test_check_passes_for_a_cleared_license() -> None:
    model = ModelDescriptor(
        id="example",
        task=ModelTask.OCR,
        quantization="int8",
        size_bytes=1,
        license_id="cleared",
        version="1.0.0",
    )
    licenses = {
        "cleared": LicenseEntry(
            id="cleared",
            component="Example",
            spdx="Apache-2.0",
            compatible_with_apache_2_0=True,
            notes="",
        )
    }
    check_catalog_licenses([model], licenses)


def test_check_rejects_an_uncleared_license() -> None:
    model = ModelDescriptor(
        id="example",
        task=ModelTask.OBJECT_DETECTION,
        quantization="fp16",
        size_bytes=1,
        license_id="agpl",
        version="1.0.0",
    )
    licenses = {
        "agpl": LicenseEntry(
            id="agpl",
            component="Example AGPL component",
            spdx="AGPL-3.0-only",
            compatible_with_apache_2_0=False,
            notes="",
        )
    }
    with pytest.raises(LicenseComplianceError):
        check_catalog_licenses([model], licenses)


def test_check_rejects_an_unresolved_license() -> None:
    model = ModelDescriptor(
        id="example",
        task=ModelTask.TEXT_TO_SPEECH,
        quantization="none",
        size_bytes=1,
        license_id="unresolved",
        version="1.0.0",
    )
    licenses = {
        "unresolved": LicenseEntry(
            id="unresolved",
            component="Example unresolved component",
            spdx="varies",
            compatible_with_apache_2_0=None,
            notes="",
        )
    }
    with pytest.raises(LicenseComplianceError):
        check_catalog_licenses([model], licenses)


def test_check_rejects_an_unknown_license_id() -> None:
    model = ModelDescriptor(
        id="example",
        task=ModelTask.OCR,
        quantization="int8",
        size_bytes=1,
        license_id="unknown",
        version="1.0.0",
    )
    with pytest.raises(LicenseComplianceError):
        check_catalog_licenses([model], {})


def test_real_license_ledger_loads_and_has_no_uncleared_catalog_entries() -> None:
    licenses = load_licenses(_REAL_LICENSES_PATH)
    check_catalog_licenses(CATALOG, licenses)


def test_real_license_ledger_flags_known_conflicts_as_incompatible() -> None:
    licenses = load_licenses(_REAL_LICENSES_PATH)
    assert licenses["ultralytics-yolo-agpl-3.0"].compatible_with_apache_2_0 is False
    assert licenses["arasaac-cc-by-nc-sa"].compatible_with_apache_2_0 is False
    assert licenses["espeak-ng-gpl-3.0"].compatible_with_apache_2_0 is False


def test_real_license_ledger_leaves_per_voice_choice_unresolved() -> None:
    licenses = load_licenses(_REAL_LICENSES_PATH)
    assert licenses["piper-voice-per-voice"].compatible_with_apache_2_0 is None
