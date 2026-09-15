# Prod_v3 Release Changelog

## Overview

**Prod_v3** is a major refactor of the Configuration-Driven ELT Orchestration Framework. The release consolidates the project structure from `platform/` to `framework/`, simplifies the job orchestration model, introduces a new FastAPI-based orchestration server.

## Major Changes

### **Folder Reorganization: `platform/` → `framework/`**

- All source code, configuration, and infrastructure code moved from `platform/` to `framework/`
- Updated documentation paths: `docs/`, `terraform/`, and Python modules now live under `framework/`
- Impact: All import paths change (e.g., `el_system` → `elt_system`, `platform/` references → `framework/`)

### **Job Orchestration Refactor**

- **Renamed**: `el_system` → `elt_system` (to better reflect Extract-Load-Transform)
- **New Orchestration Flow**:
  - Jobs now follow a **layer-based** structure (`ingestion` → `storage`) instead of `exec` → `dest`
  - Configuration keys renamed: `exec` → `ingestion`, `dest` → `storage`
  - Execution types: `ApiExecCmd` → `API`, destination types: `GCS` → `GCS`
- **Job Execution Model**: Simplified to ingestion + storage layers with unified job_metrics output
- **Database Integration**: Direct PostgreSQL (Neon) writes for run tracking with UUID-based job/pipeline run IDs

### **New FastAPI Server (`framework/server.py`)**

- Added HTTP endpoints for pipeline lifecycle events:
  - `POST /pipeline_start_metadata` — log pipeline start
  - `POST /pipeline_end_metadata` — log pipeline end
  - `POST /status` — health check
- Receives pipeline and job metadata from Cloud Workflows
- Writes metadata to Neon PostgreSQL database

### **Google Cloud Workflows Automation**

- Replaced Cloud Run Job-triggered orchestration with **Google Cloud Workflows**
- New workflow files: `framework/terraform/dev_workflow.yml` and `framework/terraform/prod_workflow.yml`
- Workflows orchestrate:
  - Parallel secret retrieval (API keys, DB URLs) from Secret Manager
  - Pipeline start metadata logging (via FastAPI)
  - Job execution (calling Cloud Run Jobs)
  - Error handling and pipeline end metadata logging
- Decouples pipeline orchestration from individual job execution

### **Cloud Run Infrastructure Updates**

- Cloud Run Jobs changed from `dev-el-system-run`, `dev-metadata-system-run`, `dev-pipeline-run` to generic `dev-execution-job` and `prod-execution-job`
- Cloud Run Services added: `dev-execution-service` and `prod-execution-service` (for FastAPI orchestration server)
- Image naming unified: all images now reference `framework:testing` (dev) and `framework:latest` (prod)
- Job timeouts: `300s` (was `600s`), retries: `2`

### **Configuration Changes**

- **New Root Schema**: `framework/elt_system/schemas/root_schema.json`
  - `exec` → `layer.ingestion`
  - `dest` → `layer.storage`
  - Each layer has its own schema (ingestion/storage schemas)
- **Path Templates**: Changed to use `{jobRunID}` and `{ingestionDT}` / `{ingestionTS}` placeholders instead of `job_run_id`, `ingestion_dt`, `ingestion_ts`
- **Job Configs**: Simplified structure in `framework/elt_system/configs/job/` (dev/prod versions for market_price.json)

### **Python Module Refactoring**

#### ELT System (`framework/elt_system/`)

- **Ingestions** (was Exec Commands):
  - `Api` class (was `ApiExecCommand`) in `job_executors/ingestions/api.py`
  - `ingestionType` registry (was `ExecCmdType`)
- **Storages** (was Destinations):
  - `Gcs` class (was `GCS`) in `job_executors/storages/gcs.py`
  - Updated constructor: `storage_cfg`, `jobRunID` (instead of `job_run_id`)
  - `storageType` registry (was `DestType`)
- **New Orchestrator** (`framework/elt_system/orchestrator/`):
  - `main.py` — new entry point with direct DB writes (no metadata dumps)
  - `loader.py` — simplified to `JobConfigLoader` only (no job catalog)
  - `runner.py` — orchestrates ingestion + storage layers
  - `validator.py`, `metadata.py` — refactored logic

#### Authentication

- Imports updated: `framework/elt_system/job_executors/auth/`
- Registries simplified

#### Exception Handling

- Centralized `framework/elt_system/exceptions/exceptions.py`
- Exception descriptions mapped consistently

### **Dependencies & Docker**

- **Dockerfile**: New `framework/Dockerfile` (Python 3.12.3-slim)
  - CMD: `python -u -m server` (runs FastAPI)
  - Cleaner than before; runs dbt deps at build time
- **Requirements**: Consolidated `framework/requirements.txt` and `framework/dev-requirements.txt`
- **Dependency Changes**:
  - Removed: `dbt-core`, `dbt-bigquery`, `google-cloud-run`, `google-cloud-logging` (no longer needed in job execution)
  - Added: `fastapi`, `uvicorn` (for orchestration server)
  - Kept: `pandas`, `psycopg2`, `google-cloud-storage`, `loguru`

### **Infrastructure (Terraform)**

- **New Resources**:
  - `google_cloud_run_v2_service`: `dev_execution_service`, `prod_execution_service` (FastAPI orchestration)
  - `google_workflows_workflow`: `dev_orchestrator_workflow`, `prod_orchestrator_workflow`
  - `google_secret_manager_secret`: Unified secret names (dev/prod API keys, DB URLs)
- **Removed Resources**: Old Cloud Run Job definitions (el_system, metadata_system, pipeline_run)
- **Artifact Registry**: Updated naming: `configuration-driven-elt-orchestration-framework-repository`
- **GCS Buckets**: Added `raw-configuration-driven-elt-orchestration-framework-bucket` for prod storage; lifecycle and soft-delete policies applied
- **Scheduler**: Updated to trigger Cloud Workflows instead of Cloud Run Jobs

## Behavioral Changes

- **Job Execution Flow**:
  - Old: `orchestrator.main` → load job catalog → run jobs via Cloud Run
  - New: Cloud Workflows → `FastAPI /pipeline_start_metadata` → run jobs → `FastAPI /pipeline_end_metadata`
- **Metadata Tracking**:
  - Old: JSON metadata dumps in logs
  - New: Direct PostgreSQL writes with structured schema (pipeline_runs, job_runs tables)
- **Error Handling**: Moved from executor logs to database error_message field
- **Execution Parallelism**: Workflows now handle parallel secret fetching and job execution via built-in workflow steps

## Database / Metadata Changes

- **Table Schema Refactors**:
  - `public.job_runs`: now tracks job run execution on layer basis for improved observability

## Breaking Changes

1. **Import Paths**: All `el_system` → `elt_system`, all `platform/` → `framework/`
2. **Job Configuration Schema**: Old `exec`/`dest` structure is incompatible; must migrate to new `layer.ingestion`/`layer.storage`
3. **Job Execution Entry Point**: Old orchestrator scripts no longer work; jobs must be invoked via Cloud Workflows
4. **Container Image Names**: Updated to `framework:testing` and `framework:latest`
5. **Environment Variables**: Job invocation now via Workflows with environment variable passing (not secret references in Job definition)
6. **Orchestration Server**: Old monolithic orchestrator replaced with lightweight FastAPI endpoints

## Final Release Notes

**Prod_v3** represents a significant architectural shift toward **workflow-driven orchestration**, replacing job-centric execution with a declarative workflow model. The move from `platform/` to `framework/` also better reflects the project's nature as a reusable orchestration framework rather than a platform.

**Key Benefits**:

- Cleaner separation of concerns (orchestration server separate from job execution)
- Declarative workflow definitions in YAML (easier to audit and modify)
- Simplified job execution model (standardized ingestion → storage flow)
- Better observability through direct database logging
- Unified image and infrastructure naming
