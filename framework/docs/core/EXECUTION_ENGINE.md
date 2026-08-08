# Execution Engine

## Overview

The Execution Engine orchestrates pipeline jobs by loading configs, validating them, dispatching execution commands, and tracking run metadata.

## Responsibilities

- Load JSON job configuration
- Load and validate against the JSON schema
- Load environment credentials
- Create and execute the API command
- Create and run the destination persistence layer
- Track run metadata in PostgreSQL

## Implementation

The main runner is in `el_system/orchestrator/orchestrator.py`.

### Execution flow

1. The orchestrator loads a list of configured jobs from `el_system/configs/catalog`
2. It validates each job config using `el_system/schemas/root_schema.json`
3. It builds metadata records and job context
4. It executes the EL ingestion job using `el_system/orchestrator/runner.py`
5. It persists ingestion output to GCS via `el_system/job_executors/dests/gcs.py`

## Design

The orchestrator separates orchestration from execution logic. Execution commands are pluggable, enabling future support for additional data sources without changing the engine.

The repository also includes a metadata system in `metadata_system/orchestrator/orchestrator.py` that loads run metadata from PostgreSQL and writes it to BigQuery using `metadata_system/job_executors/dests/bq_dest.py`.

## Current status

The runner supports `ApiExecCommand` in `prod_v1` and writes ingestion metadata to PostgreSQL. It uses `dev.env` locally for secrets, while production is designed to use secret manager values in Terraform.
