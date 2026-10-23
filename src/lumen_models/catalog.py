"""Model pack catalog: descriptors for on-demand model packs.

Mirrors the shape of lumen_sdk's `ModelDescriptor` contract so entries
here can later be published, unchanged, as the model manifest that
lumen-server's `/api/v1/models` endpoint and lumen-core's
`ModelRegistry` both consume.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ModelTask(StrEnum):
    """The kind of inference a model pack performs."""

    OCR = "ocr"
    AUTOMATIC_SPEECH_RECOGNITION = "automatic_speech_recognition"
    SOUND_CLASSIFICATION = "sound_classification"
    TEXT_TO_SPEECH = "text_to_speech"
    OBJECT_DETECTION = "object_detection"
    SMALL_LANGUAGE_MODEL = "small_language_model"


@dataclass(frozen=True, slots=True)
class ModelDescriptor:
    """Describes a downloadable model pack without loading it."""

    id: str
    task: ModelTask
    quantization: str
    size_bytes: int
    license_id: str
    version: str


# No model has been converted, quantized, or benchmarked yet. Entries
# are added here only once a real on-device artifact exists and its
# license is recorded and cleared in docs/LICENSES.md and
# docs/licenses.yaml; see check_catalog_licenses in license_check.py,
# which CI runs against this list. See docs/benchmarks.md for the
# (currently empty) benchmark table.
CATALOG: list[ModelDescriptor] = []
