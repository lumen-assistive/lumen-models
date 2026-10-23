from pathlib import Path

from lumen_models.convert.base import CopyConverter


def test_copy_converter_preserves_bytes_and_computes_checksum(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.bin"
    source.write_bytes(b"lumen")
    destination = tmp_path / "destination.bin"

    manifest = CopyConverter().convert(source, destination)

    assert destination.read_bytes() == b"lumen"
    assert manifest.source_path == str(source)
    assert manifest.output_path == str(destination)
    assert manifest.output_size_bytes == 5
    assert len(manifest.output_sha256) == 64
