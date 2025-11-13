# Mycelia AI Architecture Overview

```mermaid
graph TD
    A[Data Sources] -->|Ingest| B[Data Ingestion Pipeline]
    B -->|Normalize| C[Processing Services]
    C -->|Enrich| D[Knowledge Graph]
    D -->|Expose Insights| E[Applications & APIs]
```

## Component Responsibilities
- **Data Sources**: External datasets, APIs, or message streams that feed the platform.
- **Data Ingestion Pipeline**: Manages connectors, scheduling, and normalization tasks.
- **Processing Services**: Apply enrichment, validation, and feature extraction logic.
- **Knowledge Graph**: Centralized, queryable store for relationships and entities.
- **Applications & APIs**: Deliver insights to end users and downstream systems.
