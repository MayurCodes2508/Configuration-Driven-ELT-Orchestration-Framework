# Market Analytics Platform — README (prov v2)

Version: prov v2  
Last updated: 2026-08-06

---

## What this repo is now

This repository contains the Market Analytics Platform — a consolidated, production-oriented, config-driven data platform for extracting, transforming, and observing cryptocurrency market data. The project has been reorganized and standardized into a single top-level `platform/` subtree that houses ingestion, metadata pipelines, orchestration, dbt transformations, CI, and infra code.

High-level goals:

- Config-driven job declarations validated against JSON schemas.
- Modular execution engine for API, DB, and dbt-based tasks.
- Unified orchestration and runner patterns that emit structured metadata dumps.
- Observability-first dbt models and tests for SLOs and alerting.
- Standardized CI and containerized runtime for reproducible builds.

---

## Major changes since prod_v1

- Repo structure consolidated under `platform/` (e.g., `platform/el_system/`, `platform/metadata_system/`, `platform/orchestrator/`, `platform/metadata_system/dbt/`).
- New or refactored orchestrator/executor stack with improved logging, error handling, and standardized METADATA_DUMP JSON outputs.
- API exec logic centralized via a runtime `root_url_registry` (no more `base_url` in job JSONs).
- dbt observability moved and extended under `platform/metadata_system/dbt/` with:
  - New staging, reporting, and alerts models.
  - 20+ new data quality tests.
  - Runtime SLO threshold increased from 15s → 120s.
- Destinations updated:
  - GCS destination path templates now include `job_run_id`.
  - GCS & BQ dest classes accept richer job_metrics (JSON).
- CI modernized and standardized:
  - New workflow: `.github/workflows/ci_dbt_transformations.yml`
  - Workflows use `defaults.run.working-directory: ./platform/`
  - GCP auth standardized and Python version pinned to 3.12.x in CI.
- Terraform & Cloud Run:
  - Cloud Run job definitions updated (`timeout`, `max_retries`), and Docker images standardized to `platform-job`.
  - Environment variables and secret references adjusted for the consolidated layout.
- Packaging:
  - New `platform/Dockerfile`
  - Consolidated `platform/requirements.txt` and `platform/dev-requirements.txt`

---

## Repo layout (important paths)

- platform/
  - el_system/ (execution engine, api exec, gcs dest)
  - metadata_system/ (metadata ingestion, dbt integration)
    - dbt/ (dbt_project.yml, models, tests, packages.yml)
  - orchestrator/ (top-level orchestrator tooling)
  - docs/ (moved architecture & CT documentation)
  - Dockerfile, requirements.txt, dev-requirements.txt
- .github/workflows/ (standardized CI workflows)
- platform/terraform/ (Cloud Run jobs, buckets, scheduler, IAM)

Refer to `platform/docs/CHANGELOG.md` for a full release summary of this refactor.

---

## Key concepts & runtime behaviour

- Jobs are defined as JSON files that must include:
  - `metadata` (source, dataset, entity)
  - `exec` (exec_type and exec-specific params)
  - Optional `dest` (if the job is an ingestion)
- Runtime metadata derivation:
  - `job_type` is inferred at runtime (presence of `dest` → ingestion; otherwise extraction/transformation).
  - `sub_jobtype` is derived from the exec type (e.g., `ApiExecCmd` → `Api`).
  - The orchestrator generates a `job_run_id` (UUID) for each run and includes it in job metadata and destination paths.
- API executions use a `root_url_registry` to centralize base URLs (so configs do not embed `base_url`).
- dbt executions return structured artifacts parsed from `target/run_results.json` and are exposed as `job_metrics`.

---

## Running locally (recommended strategies)

Environment variables commonly needed:

- ENV (LOCAL | DEV | PROD)
- DBT_TARGET (dev | prod)
- COINGECKO_API_KEY (for Coingecko-based jobs)
- NEON_DB_URL (or other DB connection secrets)
- GOOGLE_APPLICATION_CREDENTIALS (for GCP operations)

### Using Docker (recommended — reproduces production image)

- From repo root, build the platform image:
  - docker build -t platform-job:latest -f platform/Dockerfile .
- Run an EL job locally (example):
  - docker run --rm -e COINGECKO_API_KEY="${COINGECKO_API_KEY}" -e DBT_TARGET=dev platform-job:latest el_system.orchestrator.executor --job_name dev_coingecko_market_price --file_path el_system/configs/job/coingecko_sources/dev/market_price.json
- Run a metadata/dbt job:
  - docker run --rm -e NEON_DB_URL="${NEON_DB_URL}" -e DBT_TARGET=dev platform-job:latest metadata_system.orchestrator.executor --job_name dev_neon_pipeline_runs --file_path metadata_system/configs/job/neon_sources/dev/pipeline_runs.json

### Native Python (dev convenience — change directory into platform/ first)

- cd platform
- Run an el_system executor:
  - python -m el_system.orchestrator.executor --job_name dev_coingecko_market_price --file_path el_system/configs/job/coingecko_sources/dev/market_price.json
- Run metadata executor:
  - python -m metadata_system.orchestrator.executor --job_name dev_neon_pipeline_runs --file_path metadata_system/configs/job/neon_sources/dev/pipeline_runs.json

### Running dbt (observability)

- cd platform/metadata_system/dbt
- dbt deps
- dbt build --target ${DBT_TARGET:-dev}
- dbt test --target ${DBT_TARGET:-dev} (or run specific exposures/tests as needed)

---

## Developer workflow

- Code & tests: develop under `platform/…`. Keep configs in `platform/*/configs/job/...` and catalog entries under `platform/*/configs/catalog/{dev,prod}/config.json`.
- Validate job JSONs against the provided schemas in `platform/*/schemas/`. Use `jsonschema_rs` or the included `Validator` classes.
- CI: push branches or open PRs; CI runs standardized workflows from `.github/workflows/`.
- Building images: use `platform/Dockerfile` to build reproducible images for local and cloud runs.

---

## Migration notes (when moving from prod_v1)

- Job JSON changes:
  - Remove these fields from job JSONs if present: `job_name`, `system`, `job_type`, `sub_jobtype`. The platform now derives them at runtime.
  - Ensure each job JSON contains `metadata`, `exec`, and (if ingestion) `dest`.
  - Remove `base_url` from API job JSONs — the execution registry provides root URLs.
- Destination path expectations:
  - GCS `path_template` now includes `job_run_id`. If you have external consumers depending on older paths, plan a migration or compatibility layer.
- dbt:
  - Tests and exposures moved under `platform/metadata_system/dbt/`. Update CI and local scripts to point to the new dbt project path and use `DBT_TARGET`.
- CI & runtime:
  - CI uses `platform/` as the working directory. Ensure workflow environment variables and secrets are configured in the repository (GCP Workload Identity, DBT_TARGET, NEON/DB secrets).
- Python & images:
  - Runtime is standardized on Python 3.12.x (CI and Dockerfiles). Rebuild images and pin runtime environments accordingly.

---

## Troubleshooting & tips

- Use the structured METADATA_DUMP logs (the orchestrator publishes JSON blobs with job_run_id, job_name, job_metrics, error_message) for debugging and for aggregating run telemetry.
- If a job fails during validation, check the schema in `platform/*/schemas/` and validate your job JSON with `Validator` classes and `jsonschema_rs`.
- For GCP issues, confirm `GOOGLE_APPLICATION_CREDENTIALS` and Workload Identity provider configuration are correct and that the CI service account has necessary IAM roles.

---

## Links & references

- Platform docs and changelog: `platform/docs/CHANGELOG.md`
- Orchestrator entrypoints:
  - EL: `platform/el_system/orchestrator/main.py`, `platform/el_system/orchestrator/executor.py`
  - Metadata: `platform/metadata_system/orchestrator/main.py`, `platform/metadata_system/orchestrator/executor.py`
- dbt project: `platform/metadata_system/dbt/`
- CI workflows: `.github/workflows/ci_dbt_transformations.yml`, `.github/workflows/ci_el_system.yml`, `.github/workflows/ci_metadata_system.yml`, `.github/workflows/ci_orchestrator_run.yml`
- Terraform: `platform/terraform/` (Cloud Run job updates & secrets)

---
