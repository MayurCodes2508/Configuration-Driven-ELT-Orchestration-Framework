# Warehouse Layer

## Overview

The Warehouse layer represents the planned analytics staging area after ingestion. In `prod_v1`, the current implementation stops at the GCS landing zone, while the dbt project is focused on pipeline metadata observability and reliability reporting.

## Intended workflow

1. Ingest raw Parquet files into GCS
2. Load or transform data into BigQuery
3. Model data across Bronze, Silver, and Gold layers
4. Enable analytics and reporting

## Current state

- `prod_v1` currently writes to a GCS data lake
- `dbt_transformations/` includes current models for pipeline metadata observability, SLO reporting and monitoring
- The architecture is ready for broader analytics, but full warehouse load logic for market analytics is still planned
