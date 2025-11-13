"""Top-level package for the Mycelia AI project.

This package exposes the main building blocks that orchestrate the
application life-cycle. Modules inside the package can be extended to
cover ingestion, orchestration, persistence, and delivery concerns.
"""

from .components import ComponentRegistry, DataIngestionPipeline, KnowledgeGraph

__all__ = [
    "ComponentRegistry",
    "DataIngestionPipeline",
    "KnowledgeGraph",
]
