"""Core components for the Mycelia AI platform.

This module documents the high-level services that the platform will rely
on. Concrete implementations can evolve from these sketches as the
project matures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class DataIngestionPipeline:
    """Coordinates the acquisition and normalization of external data sources."""

    sources: List[str] = field(default_factory=list)

    def register_source(self, source: str) -> None:
        """Register a new data source for ingestion."""

        if source not in self.sources:
            self.sources.append(source)


@dataclass
class KnowledgeGraph:
    """Represents the graph-based knowledge store that powers Mycelia AI."""

    nodes: Dict[str, Dict[str, str]] = field(default_factory=dict)

    def upsert_node(self, identifier: str, metadata: Dict[str, str]) -> None:
        """Insert or update an entity in the knowledge graph."""

        self.nodes[identifier] = metadata


@dataclass
class ComponentRegistry:
    """Holds references to system components and facilitates dependency wiring."""

    ingestion_pipeline: DataIngestionPipeline = field(default_factory=DataIngestionPipeline)
    knowledge_graph: KnowledgeGraph = field(default_factory=KnowledgeGraph)

    def describe(self) -> Dict[str, str]:
        """Return a concise description of registered components."""

        return {
            "ingestion_pipeline": f"{len(self.ingestion_pipeline.sources)} sources registered",
            "knowledge_graph": f"{len(self.knowledge_graph.nodes)} nodes tracked",
        }


__all__ = [
    "ComponentRegistry",
    "DataIngestionPipeline",
    "KnowledgeGraph",
]
