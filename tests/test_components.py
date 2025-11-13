"""Basic smoke tests for the component sketches."""

from mycelia_ai import ComponentRegistry


def test_component_registry_describe() -> None:
    registry = ComponentRegistry()
    summary = registry.describe()

    assert "ingestion_pipeline" in summary
    assert "knowledge_graph" in summary
