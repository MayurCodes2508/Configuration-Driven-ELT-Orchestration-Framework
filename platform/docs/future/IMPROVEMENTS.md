# Pipeline Schema Documentation

---

## Table: `pipeline_runs`

### Description for `pipeline_runs`

Stores metadata for each pipeline execution.
Each record represents a single pipeline run, capturing its lifecycle, trigger source, and overall outcome.

### Columns: 8

| Column | Type | Constraints | Description |
| --- | --- | --- | --- |
| `pipeline_run_id` | UUID | PK | Unique identifier for a pipeline run. Recommended to use UUID for global uniqueness. |
| `pipeline_name` | TXT | NULLABLE | Name of the pipeline being executed. |
| `status` | TXT | | Current state of the pipeline run. |
| `start_time` | TS | NULLABLE | Timestamp when the pipeline execution started. |
| `end_time` | TS | NULLABLE | Timestamp when the pipeline execution completed. Remains `NULL` while the pipeline is still running. |
| `created_at` | TS | NULLABLE | Timestamp when the record was inserted into the database. Used for auditing and tracking. |
| `triggered_by` | TXT | NULLABLE | Indicates how the pipeline was triggered. |
| `error_message` | TXT | NULLABLE | Short, human-readable summary of the failure reason. Only populated if the pipeline fails. Derived from the first failed job in the pipeline. |
| `job_counts` | JSB | NULLABLE | JSON object containing total jobs executed, successful jobs, and failed jobs counts. |

### Allowed Values for `pipeline_runs`

**`status`**

- `RUNNING`
- `SUCCESS`
- `FAILED`

**`pipeline_name`** *(examples)*

- `market-analytics-pipeline`
- `platform-observability-pipeline`

**`triggered_by`** *(typical values)*

- `scheduler`
- `manual`
- `api`

---

## Table: `job_runs`

### Description for `job_runs`

Stores metadata for each job (step) executed within a pipeline run.
Each record represents a single step in a pipeline, including execution details, classification, and performance metrics.

### Columns: 13

| Column | Type | Constraints | Description |
| --- | --- | --- | --- |
| `job_run_id` | STR | PK | Unique identifier for a job run. Recommended to use UUID. |
| `pipeline_run_id` | STR | FK → `pipeline_runs.pipeline_run_id` | Links the job to its parent pipeline execution. |
| `job_name` | STR | | Business-level name of the job. |
| `system` | STR | | System or engine used to execute the job. |
| `job_type` | STR | | High-level category of the job. |
| `sub_jobtype` | STR | | Specific execution type within the job. Represents how the job runs. |
| `status` | STR | | Execution status of the job. |
| `start_time` | TS | | Timestamp when job execution started. |
| `end_time` | TS | Null | Timestamp when job execution finished. `NULL` while job is still running. |
| `created_at` | TS | | Timestamp when the job run record was created. |
| `error_message` | STR | Null | Short, structured error message if the job fails. |
| `job_metrics` | JSB | { } | metrics fetched by the job. Only applicable. |
| `extra_metadata` | JSB | | Flexible field to store system-specific metadata. |

### Allowed Values for `job_runs`

**`status`**

- `RUNNING`
- `SUCCESS`
- `FAILED`

**`job_name`** *(examples)*

- `prod_coingecko_market_price_ingestion`
- `prod_market_price_dbt_transform`

**`system`** *(examples)*

- `el`
- `dbt`
- `metadata`

**`job_type`** *(examples)*

- `ingestion`
- `transformation`
- `quality`

**`sub_jobtype`** *(examples)*

- `api`
- `file`
- `build`
- `test`
- `postgres_to_bq`

**`error_message`** *(examples)*

- `API rate limit exceeded`
- `dbt model customers failed`

### `extra_metadata` Examples

For EL jobs:

```json
{ "api_calls": 5, "latency_ms": 2300 }
```

For dbt jobs:

```json
{ "models_run": 12, "tests_failed": 1 }
```

---

## Relationships

```text
pipeline_runs (1) ──── (many) job_runs
```

One `pipeline_run` → many `job_runs`, linked via `pipeline_run_id`.
