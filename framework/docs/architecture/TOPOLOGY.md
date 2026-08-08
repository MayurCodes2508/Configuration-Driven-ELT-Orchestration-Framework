# Architecture Topology

## System topology

The platform is structured as a modular pipeline from configuration to storage and observability:

- Job configuration in JSON
- Schema validation layer
- Execution engine and command dispatch
- Destination persistence to GCS
- Run metadata capture in PostgreSQL
- Metadata ingestion to BigQuery
- Downstream dbt artifacts and analytics layer

## Pipeline stages

### 1. Configuration

Jobs are defined in `el_system/configs/job/coingecko_sources/*.json` and describe:

- source metadata
- API endpoint settings
- pagination and page size
- authentication details
- destination storage settings

### 2. Validation

- Job configs are validated against `el_system/schemas/root_schema.json` before execution.

### 3. Execution

The `Runner` loads the validated config and dispatches `ApiExecCommand` to fetch market data.

### 4. Destination

Extraction results are converted to Parquet and written to GCS using the configured path template.

### 5. Metadata ingestion

Run metadata is loaded from PostgreSQL into BigQuery using `metadata_system/orchestrator/orchestrator.py`.

### 6. Observability and reporting

A dbt project consumes the loaded run metadata and builds pipeline observability, SLO reporting and monitoring artifacts.

## Deployment topology

- Dev and prod environments are separated with distinct configs and storage
- Production uses Cloud Run jobs for EL ingestion, dbt execution, pipeline orchestration, and metadata ingestion
- Production is scheduled hourly via Cloud Scheduler for ingestion execution
- Secrets are managed in Google Secret Manager
- Infrastructure is defined in Terraform modules under `terraform/`

### Implementation details

- Run metadata is loaded from PostgreSQL into BigQuery by `metadata_system/orchestrator/orchestrator.py`
- The EL ingestion engine is implemented in `el_system/orchestrator/orchestrator.py`
