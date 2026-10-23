"""Model conversion pipeline interfaces.

No per-framework converter (TFLite, ONNX, GGUF) is wired up yet; each
is added once a specific plugin module actually needs a concrete
model, rather than installing several heavyweight ML toolchains
speculatively ahead of need. `CopyConverter` below exercises and tests
the pipeline shape (manifest plus checksum) that every future
converter will follow.
"""

from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ConversionManifest:
    """Record of a single conversion run, written next to its output."""

    source_path: str
    output_path: str
    output_sha256: str
    output_size_bytes: int


class ModelConverter(ABC):
    """Converts a source model file into an on-device-ready artifact."""

    @abstractmethod
    def convert(self, source: Path, destination: Path) -> ConversionManifest:
        """Converts `source` into `destination` and returns a manifest."""


class CopyConverter(ModelConverter):
    """Reference converter: copies the source file unchanged.

    Used to exercise and test the conversion pipeline's manifest and
    checksum generation independently of any specific ML framework.
    """

    def convert(self, source: Path, destination: Path) -> ConversionManifest:
        data = source.read_bytes()
        destination.write_bytes(data)
        digest = hashlib.sha256(data).hexdigest()
        return ConversionManifest(
            source_path=str(source),
            output_path=str(destination),
            output_sha256=digest,
            output_size_bytes=len(data),
        )
