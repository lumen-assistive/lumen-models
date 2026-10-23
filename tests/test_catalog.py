from lumen_models.catalog import CATALOG, ModelDescriptor, ModelTask


def test_model_descriptor_fields() -> None:
    descriptor = ModelDescriptor(
        id="example",
        task=ModelTask.OCR,
        quantization="int8",
        size_bytes=1024,
        license_id="example-license",
        version="1.0.0",
    )
    assert descriptor.id == "example"
    assert descriptor.task is ModelTask.OCR
    assert descriptor.quantization == "int8"
    assert descriptor.size_bytes == 1024
    assert descriptor.license_id == "example-license"
    assert descriptor.version == "1.0.0"


def test_catalog_is_empty_until_a_model_is_converted() -> None:
    assert CATALOG == []
