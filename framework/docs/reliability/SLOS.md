# Service Level Objectives (SLOs)

## Overview

SLOs define the reliability targets for production ingestion in `prod_v1`.

## Current objectives

- **Job success rate**: target 95%+ for hourly production runs with target 99.00%+ over 30 days
- **Average Runtime**: target -60 secs for hourly production runs with target 99.00%+ over 30 days

## Observability

Run tracking stores:

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

The metadata pipeline loads this execution history into BigQuery, where dbt models calculate runtime SLOs conditions.

## Failure handling

- The runner marks a run as `RUNNING` before execution
- On error, the final run status is updated to `FAILED`
- Error messages are persisted for debugging

## Current status

The `prod_v1` release is built on structured run tracking and hourly scheduled execution. Future releases should add automated SLA reporting.

### Reliability Report Dashboard Link

[Reliability report dashboard](https://datastudio.google.com/reporting/33a12455-9652-47ab-8f47-7ac4319ddf25)
