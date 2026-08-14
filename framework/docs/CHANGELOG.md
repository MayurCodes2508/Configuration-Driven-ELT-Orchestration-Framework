<<<<<<< HEAD
# **Configuration-Driven ELT Orchestration Framework - PRODUCTION RELEASE CHANGELOG**

## **Overview**

This release introduces significant architectural improvements to the data framework, focusing on modularization, metadata management, and observability enhancements.
=======
# **MARKET ANALYTICS PLATFORM - PRODUCTION RELEASE CHANGELOG**

## **Overview**

This release introduces significant architectural improvements to the data platform, focusing on modularization, metadata management, and observability enhancements.
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21

---

## Quick summary (top-level)

<<<<<<< HEAD
- Major reorganization: many components were consolidated under a new `framework/` directory. Several previous top-level packages (e.g. `el_system`, `metadata_system`, `orchestrator`, `dbt_transformations`) were moved/renamed into `framework/…` or removed and restructured.
- CI overhaul: new and standardized GitHub Actions workflows added/modified (including a new dbt CI workflow).
- Orchestration refactor: the orchestration modules (`elt_system`, `metadata_system`, `orchestrator`) were refactored — loader/validator/metadata/runner/executor logic rewritten; new executor entrypoints added.
- dbt / observability: dbt models and tests were reorganized into an `observability` domain; new models, tests, and SLO/alerts logic added; runtime SLO threshold increased (15s → 120s).
- Execution & destinations: API execution logic centralized (root_url registry), GCS destination now includes job_run_id in path template, and job metrics shape changed (job_metrics JSON).
- Packaging & infra: new `framework/Dockerfile`, Terraform Cloud Run jobs updated, changed Docker image names and added job timeouts/retries.
- Many deleted files and many new files — this is a large refactor consolidating frameworks and standardizing behavior.
=======
- Major reorganization: many components were consolidated under a new `platform/` directory. Several previous top-level packages (e.g. `el_system`, `metadata_system`, `orchestrator`, `dbt_transformations`) were moved/renamed into `platform/…` or removed and restructured.
- CI overhaul: new and standardized GitHub Actions workflows added/modified (including a new dbt CI workflow).
- Orchestration refactor: the orchestration modules (`el_system`, `metadata_system`, `orchestrator`) were refactored — loader/validator/metadata/runner/executor logic rewritten; new executor entrypoints added.
- dbt / observability: dbt models and tests were reorganized into an `observability` domain; new models, tests, and SLO/alerts logic added; runtime SLO threshold increased (15s → 120s).
- Execution & destinations: API execution logic centralized (root_url registry), GCS destination now includes job_run_id in path template, and job metrics shape changed (job_metrics JSON).
- Packaging & infra: new `platform/Dockerfile`, Terraform Cloud Run jobs updated, changed Docker image names and added job timeouts/retries.
- Many deleted files and many new files — this is a large refactor consolidating platforms and standardizing behavior.
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21

---

## Notable CI / GitHub Actions changes

- New workflow added:
  - `.github/workflows/ci_dbt_transformations.yml` — CI for dbt transformations (GCP auth via Workload Identity, Python 3.12.3, dbt deps/build).
<<<<<<< HEAD
- Existing workflows (`ci_elt_system.yml`, `ci_metadata_system.yml`, `ci_orchestrator_run.yml`) standardized:
  - Added `defaults.run.working-directory: ./framework/`
  - Standardized permission blocks (id-token write, contents read) and GCP auth steps.
  - Reworked steps into Build / Test jobs, added `workflow_dispatch` triggers.
  - Standardized Python version to 3.12.3 and dependency installs using `framework/requirements.txt`.
=======
- Existing workflows (`ci_el_system.yml`, `ci_metadata_system.yml`, `ci_orchestrator_run.yml`) standardized:
  - Added `defaults.run.working-directory: ./platform/`
  - Standardized permission blocks (id-token write, contents read) and GCP auth steps.
  - Reworked steps into Build / Test jobs, added `workflow_dispatch` triggers.
  - Standardized Python version to 3.12.3 and dependency installs using `platform/requirements.txt`.
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21
  - Test job added to orchestrator workflow (ruff checks and formatting checks).
- Removed some path filters and old branch triggers (many workflows now trigger on `feature/**` or `workflow_dispatch` only).

---

## Code & repo structure (reorganization)

<<<<<<< HEAD
- A top-level `framework/` subtree was created and many files/directories were moved or recreated there:
  - `framework/elt_system/…`, `framework/metadata_system/…`, `framework/orchestrator/…`, `framework/dbt/…` (dbt under `metadata_system/dbt/`), plus `framework/Dockerfile`, `framework/.dockerignore`, `framework/.gcloudignore`.
- Old repo modules (e.g., separate `el_system/`, `orchestrator/`, `metadata_system/`, `dbt_transformations/`) were largely deleted or moved into `framework/`.
- Many docs were moved under `framework/docs/` (renamed from `docs/…`).

---

## Orchestration refactor (elt_system, metadata_system, orchestrator)

- New and reorganized orchestrator code:
  - New executor entrypoints: `framework/elt_system/orchestrator/executor.py`, `framework/elt_system/orchestrator/main.py`.
  - New loader/validator/metadata/runner modules for elt_system and metadata_system under `framework/.../orchestrator/`.
=======
- A top-level `platform/` subtree was created and many files/directories were moved or recreated there:
  - `platform/el_system/…`, `platform/metadata_system/…`, `platform/orchestrator/…`, `platform/dbt/…` (dbt under `metadata_system/dbt/`), plus `platform/Dockerfile`, `platform/.dockerignore`, `platform/.gcloudignore`.
- Old repo modules (e.g., separate `el_system/`, `orchestrator/`, `metadata_system/`, `dbt_transformations/`) were largely deleted or moved into `platform/`.
- Many docs were moved under `platform/docs/` (renamed from `docs/…`).

---

## Orchestration refactor (el_system, metadata_system, orchestrator)

- New and reorganized orchestrator code:
  - New executor entrypoints: `platform/el_system/orchestrator/executor.py`, `platform/el_system/orchestrator/main.py`.
  - New loader/validator/metadata/runner modules for el_system and metadata_system under `platform/.../orchestrator/`.
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21
  - `Executor` classes now generate UUID-based job_run_id and produce structured METADATA_DUMP JSON objects returned to callers.
  - Logging standardized using loguru with separate stdout/stderr filters; critical logs to stderr.
  - Error handling improved: more specific logging, exception-to-description mapping via `exceptions` modules.
- Job catalog and config loader:
  - Load paths are environment-aware (`ENV` defaulting to LOCAL/DEV/PROD).
<<<<<<< HEAD
  - Schema files (root schemas) updated and consolidated under `framework/*/schemas/`.
=======
  - Schema files (root schemas) updated and consolidated under `platform/*/schemas/`.
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21
- Runner changes:
  - Runner constructors and method signatures changed (accepting loader and job_run_id in places).
  - Run flow: run_exec_cmd() → run_dest_target() always used; job metrics are returned in a structured object (job_metrics).
- Metadata:
  - Metadata derivation is dynamic: `job_type` inferred from presence of `dest`; `sub_jobtype` from `exec_type`.
  - build_job_metadata now includes job_name, job_metrics, and standardized fields.

---

## Execution commands & registries

- API execution:
  - `ApiExecCommand` now receives a root URL from a `root_url_registry` (no `base_url` in job JSONs).
  - `root_url_registry = {"coingecko": "https://api.coingecko.com/api/v3"}`
  - Url building, error handling, and exception descriptions improved.
- DB exec & dbt:
  - `DBExecCommand` updated to return `job_metrics` instead of the raw rows integer directly.
<<<<<<< HEAD
  - New `dbtExecCommand` implemented under `framework/metadata_system/job_executors/exec_cmds/`:
=======
  - New `dbtExecCommand` implemented under `platform/metadata_system/job_executors/exec_cmds/`:
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21
    - Runs dbt commands via subprocess, parses `target/run_results.json`, and returns an artifact mapping (nodes → status/metrics).
  - Exec registries updated to include `"dbtExecCmd"` and wire dbt runner logic.
- Destinations:
  - GCS: `GCS` class now accepts `job_run_id`, path_template updated to include job_run_id.
  - Dest registry changed to pass job_run_id to GCS factory.

---

## Schema & validation changes

- Root schema simplified: `job_name`, `system`, `job_type`, `sub_jobtype` are no longer required in job JSONs — metadata is derived at runtime.
- `api_exec_schema.json`:
  - `base_url` requirement removed (URL now provided by runtime registry).
  - `path` minLength tightened to 2.
  - `vs_currency` changed from enum to constant `"inr"`.
- `gcs_dest_schema.json`:
  - `bucket` and `format` minLength increased to 2.
  - `path_template` constant changed to include `job_run_id`.
- New dbt exec schema added (`dbt_exec_cmd_schema.json`) to validate dbt command forms.
- Validator classes updated to unify exception handling and use `jsonschema_rs`.

---

## dbt / Observability changes

<<<<<<< HEAD
- dbt project relocated to `framework/metadata_system/dbt/`; `dbt_project.yml` updated to tag models into `observability` (staging/reporting/alerts).
=======
- dbt project relocated to `platform/metadata_system/dbt/`; `dbt_project.yml` updated to tag models into `observability` (staging/reporting/alerts).
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21
- New observability models:
  - `stg_pipeline_runs.sql`, `stg_job_runs.sql` (staging)
  - `reporting/slo_successful_runs_*` — SLO tracking for success rate & runtime
  - `alerts/alert_daily_runs_consistency.sql` — daily runs consistency alert
<<<<<<< HEAD
- Tests: 20+ data tests and assertions added under `framework/metadata_system/dbt/tests/observability/` for SLOs, timestamps, naming, and alert logic.
=======
- Tests: 20+ data tests and assertions added under `platform/metadata_system/dbt/tests/observability/` for SLOs, timestamps, naming, and alert logic.
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21
- SLO runtime threshold changed from 15 seconds to 120 seconds.
- `profiles.yml` adjusted to use env var for `DBT_TARGET`.

---

## Exceptions & logging

<<<<<<< HEAD
- New centralized `exceptions/exceptions.py` modules added under `framework/elt_system` and `framework/metadata_system`. They map exception classes to human-friendly descriptions (EXCEPTION_DESCRIPTIONS).
=======
- New centralized `exceptions/exceptions.py` modules added under `platform/el_system` and `platform/metadata_system`. They map exception classes to human-friendly descriptions (EXCEPTION_DESCRIPTIONS).
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21
- Logging:
  - loguru configuration standardized across executor/ orchestrator entrypoints (stdout for INFO..TRACE, stderr for CRITICAL).
  - Logging messages reordered to be more consistent (initialization message then completion).

---

## Packaging, Docker & runtime

<<<<<<< HEAD
- New `framework/Dockerfile` (Python 3.12.3-slim) that installs `requirements.txt`, runs `dbt deps` for metadata/dbt subproject, and sets entrypoint to python -m.
- Docker image names in Terraform and CI updated to `framework` (replacing older job-specific images like el-job, metadata-job, dbt-job).
=======
- New `platform/Dockerfile` (Python 3.12.3-slim) that installs `requirements.txt`, runs `dbt deps` for metadata/dbt subproject, and sets entrypoint to python -m.
- Docker image names in Terraform and CI updated to `platform-job` (replacing older job-specific images like el-job, metadata-job, dbt-job).
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21
- Docker build steps added to orchestrator workflow for local-run/test reproducibility.

---

## Terraform / Cloud Run changes

- Cloud Run jobs updated to:
<<<<<<< HEAD
  - Use `framework` images;
  - Add `max_retries = 2` and `timeout = "600s"` to templates;
  - Add DBT envs (`DBT_TARGET`) to Cloud Run args and set run args so Cloud Run invokes `metadata_system.orchestrator.main` or `elt_system.orchestrator.main`.
=======
  - Use `platform-job` images;
  - Add `max_retries = 2` and `timeout = "600s"` to templates;
  - Add DBT envs (`DBT_TARGET`) to Cloud Run args and set run args so Cloud Run invokes `metadata_system.orchestrator.main` or `el_system.orchestrator.main`.
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21
- Secrets references changed in a few places (e.g., secret name used for NEON_DB_URL changed to a prod secret for some resource).

---

## Dependencies & requirements

<<<<<<< HEAD
- Consolidated framework-level requirements: `framework/requirements.txt` (large, pinned set) and `framework/dev-requirements.txt`.
=======
- Consolidated platform-level requirements: `platform/requirements.txt` (large, pinned set) and `platform/dev-requirements.txt`.
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21
- Standardized Python target across CI and Docker to 3.12.x.
- Many smaller requirement & dev files removed from old subprojects; `pip-compile` generated pinned lists included.

---

## .gitignore & repo housekeeping

- `.gitignore` updated:
<<<<<<< HEAD
  - Added `.pytest_cache/`, `tests/`, `state/`, and other framework-specific items.
  - Kept `!framework/` and `!.github/` to ensure framework and GitHub workflows tracked.
- Many transient and per-subproject .dockerignore/.gcloudignore/Dockerfile files removed because consolidation into `framework/`.
=======
  - Added `.pytest_cache/`, `tests/`, `state/`, and other platform-specific items.
  - Kept `!platform/` and `!.github/` to ensure platform and GitHub workflows tracked.
- Many transient and per-subproject .dockerignore/.gcloudignore/Dockerfile files removed because consolidation into `platform/`.
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21

---

## Deleted / removed items

<<<<<<< HEAD
- Large number of old subproject files deleted (old `el_system/`, `orchestrator/`, `metadata_system/`, `dbt_transformations/` top-level copies), replaced by consolidated versions under `framework/`.
- Many Dockerfiles, `.dockerignore`, requirements files for previous subprojects removed; their replacements live under `framework/`.
=======
- Large number of old subproject files deleted (old `el_system/`, `orchestrator/`, `metadata_system/`, `dbt_transformations/` top-level copies), replaced by consolidated versions under `platform/`.
- Many Dockerfiles, `.dockerignore`, requirements files for previous subprojects removed; their replacements live under `platform/`.
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21

---

## Files of interest (high-level)

<<<<<<< HEAD
- New/updated CI: `.github/workflows/ci_dbt_transformations.yml`, `.github/workflows/ci_elt_system.yml`, `.github/workflows/ci_metadata_system.yml`, `.github/workflows/ci_orchestrator_run.yml`
- High-level framework entry: `framework/Dockerfile`, `framework/requirements.txt`, `framework/dev-requirements.txt`
- Orchestration: `framework/elt_system/orchestrator/`, `framework/metadata_system/orchestrator/`, `framework/orchestrator/…`
- dbt: `framework/metadata_system/dbt/` (models, tests, `dbt_project.yml`, `profiles.yml`)
- Exceptions and shared utils: `framework/*/exceptions/exceptions.py`
- Terraform: `framework/terraform/*` (Cloud Run job images/timeouts adjusted)
- Many deleted top-level module files (moved into `framework/`)
=======
- New/updated CI: `.github/workflows/ci_dbt_transformations.yml`, `.github/workflows/ci_el_system.yml`, `.github/workflows/ci_metadata_system.yml`, `.github/workflows/ci_orchestrator_run.yml`
- High-level platform entry: `platform/Dockerfile`, `platform/requirements.txt`, `platform/dev-requirements.txt`
- Orchestration: `platform/el_system/orchestrator/`, `platform/metadata_system/orchestrator/`, `platform/orchestrator/…`
- dbt: `platform/metadata_system/dbt/` (models, tests, `dbt_project.yml`, `profiles.yml`)
- Exceptions and shared utils: `platform/*/exceptions/exceptions.py`
- Terraform: `platform/terraform/*` (Cloud Run job images/timeouts adjusted)
- Many deleted top-level module files (moved into `platform/`)
>>>>>>> 6b19c5310d2bf8d81aeacb21189f34cf3b73bd21
