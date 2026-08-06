# Run Tracking

## Overview

Run Tracking provides observability into pipeline executions by recording metadata for each job run.

## What is tracked

- `run_id`
- `pipeline_name`
- `job_name`
- `job_type`
- `status`
- `rows_processed`
- `error_message`
- `start_time`
- `end_time`
- `created_at`

## Execution lifecycle

1. Runner inserts a `RUNNING` record before execution
2. The job executes
3. The runner updates the record to `SUCCESS` or `FAILED`
4. Errors are stored for debugging
5. A separate metadata system can ingest the run history into BigQuery dataset `prod_metadata.raw_pipeline_runs` for downstream dbt reporting

## Benefits

- Enables monitoring of production health
- Supports troubleshooting of failures
- Provides execution history for audits
- Enables future SLA reporting

## Current status

The pipeline writes run metadata to PostgreSQL using `psycopg2` and expects database credentials to be provided by environment variables.
