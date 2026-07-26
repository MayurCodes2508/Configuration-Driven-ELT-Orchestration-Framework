# Project Overview

## What this platform does

The Market Analytics Platform ingests cryptocurrency market data from the CoinGecko API and stores it as Parquet files in Google Cloud Storage. The system is designed to support versioned production releases, with `prod_v1` as the current production deployment.

## Core capabilities

- Declarative JSON pipeline configuration
- Schema validation before execution
- API extraction via `ApiExecCommand`
- GCS Parquet ingestion layer
- Run metadata tracking in PostgreSQL
- Metadata ingestion pipeline to BigQuery table `instant-medium-491107-t6.prod_metadata.raw_pipeline_runs`
- dbt models for pipeline observability, SLO reporting
- Artifact Registry repository `market-analytics-platform-repository` and GitHub Actions Workload Identity pool `github-actions-pool`
- Environment separation for dev and prod
- Infrastructure defined in Terraform

## Current state

- Production release: `prod_v1`
- Production EL ingestion config: `el_system/configs/job/coingecko_sources/prod/market_price.json`
- Production destination bucket: `prod-market-analytics-platform-bucket`
- Production EL Cloud Run job: `prod-el-system-run`
- Production dbt Cloud Run job: `prod-dbt-transformations-run`
- Production pipeline orchestration Cloud Run job: `prod-pipeline-run`
- Production metadata ingestion Cloud Run job: `prod-metadata-system-run`
- Production scheduler: `prod-pipeline-run-scheduler`
- Production secrets: `prod-market-analytics-platform-coingecko-api-key-secret`, `prod-market-analytics-platform-neon-db-url-secret`

## Why this matters

The system is built to support a SaaS-like release model: dev and prod are isolated, jobs are versioned, and the production deployment path is explicit. `prod_v1` is the first full production delivery of this ingestion pipeline.

## How the pipeline is structured

- `el_system/configs/job/` holds environment-specific ingestion definitions
- `el_system/schemas/` defines the contract for valid configs
- `el_system/orchestrator/orchestrator.py` drives execution and observability
- `el_system/job_executors/exec_cmds/` contains source extraction logic
- `el_system/job_executors/dests/` contains storage logic
- `metadata_system/` loads pipeline run metadata into BigQuery
- `dbt_transformations/` builds observability and SLO reporting models
- `terraform/` contains infrastructure provisioning
